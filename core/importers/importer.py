"""Create Pinry boards and pins from data exported by another service.

Readers (such as ``pinterest_export``) turn their source into ImportBoard
and ImportPin items; PinImporter writes them for one user. Each imported
pin records its ``source_id``, so running the same import again skips the
pins already imported and only retries the ones that failed.
"""
import time
from dataclasses import dataclass, field
from datetime import datetime

from django.db import transaction
from django.db.models import Q

from core.fetch import FetchError
from core.models import Board, Image, Pin

BOARD_NAME_LENGTH = Board._meta.get_field("name").max_length
LINK_LENGTH = Pin._meta.get_field("referer").max_length


@dataclass
class ImportBoard:
    name: str
    private: bool


@dataclass
class ImportPin:
    source_id: str
    board_name: str
    # Candidate image URLs, tried in order until one gives an image.
    image_urls: list
    description: str = ""
    link: str = ""
    private: bool = False
    created: datetime = None


@dataclass
class ImportReport:
    boards_created: int = 0
    boards_existing: int = 0
    boards_made_private: int = 0
    pins_imported: int = 0
    pins_public: int = 0
    pins_private: int = 0
    pins_already_imported: int = 0
    failed: list = field(default_factory=list)


def board_name(name):
    return name.strip()[:BOARD_NAME_LENGTH] or "Untitled"


class PinImporter(object):
    def __init__(self, user, force_private=False, tags=(), delay=1.0,
                 dry_run=False, progress=None, sleep=time.sleep):
        self.user = user
        self.force_private = force_private
        self.tags = list(tags)
        self.delay = delay
        self.dry_run = dry_run
        self.progress = progress or (lambda message: None)
        self.sleep = sleep
        self.report = ImportReport()
        self._boards = {}
        self._board_private = {}
        # Image URL -> Image, so a picture several pins share is
        # downloaded once per run.
        self._images = {}

    def run(self, boards, pins):
        boards = list(boards)
        known = {board_name(board.name) for board in boards}
        # A pin can name a board missing from the board list; create it
        # private, since nothing says it was public.
        for pin in pins:
            name = board_name(pin.board_name)
            if name not in known:
                known.add(name)
                boards.append(ImportBoard(name=name, private=True))
        for board in boards:
            self._add_board(board)

        done = set(
            Pin.objects.filter(
                submitter=self.user,
                source_id__in=[pin.source_id for pin in pins],
            ).values_list("source_id", flat=True)
        )
        # Oldest first: the feed lists pins by id, newest at the top.
        pins = sorted(pins, key=lambda pin: (
            pin.created is not None, pin.created or datetime.min,
        ))
        for index, pin in enumerate(pins, 1):
            if pin.source_id in done:
                self.report.pins_already_imported += 1
                continue
            self._add_pin(pin)
            if index % 100 == 0:
                self.progress("%d of %d pins processed" % (index, len(pins)))
        return self.report

    def _add_board(self, item):
        name = board_name(item.name)
        if name in self._board_private:
            return
        private = item.private or self.force_private
        board = Board.objects.filter(submitter=self.user, name=name).first()
        if board is None:
            self.report.boards_created += 1
            if not self.dry_run:
                board = Board.objects.create(
                    submitter=self.user, name=name, private=private,
                )
        else:
            self.report.boards_existing += 1
            # Never make an existing board public, but don't leave a
            # board public when it holds pins that were private.
            if private and not board.private:
                self.report.boards_made_private += 1
                if not self.dry_run:
                    board.private = True
                    board.save(update_fields=["private"])
            private = board.private
        self._boards[name] = board
        self._board_private[name] = private

    def _add_pin(self, item):
        name = board_name(item.board_name)
        private = (item.private or self.force_private
                   or self._board_private[name])
        if self.dry_run:
            self._count(private)
            return
        try:
            with transaction.atomic():
                image, url = self._image(item.image_urls)
                pin = Pin.objects.create(
                    submitter=self.user,
                    image=image,
                    url=url,
                    referer=self._link(item.link),
                    description=item.description or None,
                    private=private,
                    source_id=item.source_id,
                )
                if self.tags:
                    pin.tags.set(self.tags)
                self._boards[name].pins.add(pin)
                if item.created is not None:
                    # published is auto_now_add, so set it after creating.
                    Pin.objects.filter(pk=pin.pk).update(
                        published=item.created,
                    )
        except FetchError as e:
            self.report.failed.append((item.source_id, str(e)))
            return
        self._count(private)

    def _count(self, private):
        self.report.pins_imported += 1
        if private:
            self.report.pins_private += 1
        else:
            self.report.pins_public += 1

    @staticmethod
    def _link(link):
        if not link or len(link) > LINK_LENGTH:
            return None
        return link

    def _reusable(self):
        # The user's own images: in their pins, or uploaded and unused.
        return Image.objects.filter(
            Q(pin__submitter=self.user)
            | Q(pin__isnull=True, uploaded_by=self.user),
        ).distinct()

    def _image(self, urls):
        """Return ``(image, url)`` for the first URL that gives an image."""
        for url in urls:
            cached = self._images.get(url)
            if cached is not None and \
                    Image.objects.filter(pk=cached.pk).exists():
                return cached, url
        error = "No image found."
        for url in urls:
            if self.delay:
                self.sleep(self.delay)
            try:
                image = Image.objects.create_for_url(
                    url, uploaded_by=self.user, reusable=self._reusable(),
                )
            except FetchError as e:
                error = str(e)
                continue
            if image is not None:
                self._images[url] = image
                return image, url
            error = "The download isn't an image."
        raise FetchError(error)
