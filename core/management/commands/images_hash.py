from collections import defaultdict

from django.core.management import BaseCommand
from django.db import transaction
from django.db.models import Count

from core.models import Image, Pin
from django_images.utils import file_sha256, open_django_file


class Command(BaseCommand):
    help = (
        "Record the content hash of images stored without one, and report "
        "duplicate images. With --merge, fold duplicates whose pins all "
        "belong to the same user into one image (issue #8)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--merge', action='store_true',
            help="Merge duplicate images that belong to the same user.",
        )

    def handle(self, *args, merge=False, **options):
        self._hash_missing()
        groups = self._duplicate_groups()
        extra = sum(len(duplicates) for _, duplicates in groups)
        if not merge:
            self.stdout.write(
                "%d duplicate image(s) can be merged; run again with "
                "--merge to merge them." % extra
            )
            return
        for keep, duplicates in groups:
            with transaction.atomic():
                Pin.objects.filter(image__in=duplicates).update(image=keep)
                for image in duplicates:
                    # Deletes the duplicate's files and thumbnails too.
                    image.delete()
        self.stdout.write("Merged %d duplicate image(s)." % extra)

    def _hash_missing(self):
        hashed = missing = 0
        for image in Image.objects.filter(sha256='').iterator():
            try:
                with open_django_file(image.image) as f:
                    sha256 = file_sha256(f)
            except OSError:
                self.stderr.write(
                    "Image %d: can't read %s, skipped." % (
                        image.pk, image.image.name,
                    )
                )
                missing += 1
                continue
            # update(), not save(): saving an Image deletes its thumbnails.
            Image.objects.filter(pk=image.pk).update(sha256=sha256)
            hashed += 1
        self.stdout.write(
            "Hashed %d image(s), %d unreadable." % (hashed, missing)
        )

    def _duplicate_groups(self):
        """
        Return (image to keep, [duplicates]) for each set of images with the
        same content whose pins all belong to one user. Images shared by
        several users' pins, and uploads no pin uses yet, are left alone, so
        merging never moves one user's pin onto another user's image.
        """
        hashes = Image.objects.exclude(sha256='').values('sha256') \
            .annotate(n=Count('id')).filter(n__gt=1) \
            .values_list('sha256', flat=True)
        groups = []
        for sha256 in hashes:
            by_owner = defaultdict(list)
            for image in Image.objects.filter(sha256=sha256).order_by('pk'):
                owners = set(image.pin.values_list('submitter_id', flat=True))
                if len(owners) == 1:
                    by_owner[owners.pop()].append(image)
            for images in by_owner.values():
                if len(images) > 1:
                    groups.append((images[0], images[1:]))
        return groups
