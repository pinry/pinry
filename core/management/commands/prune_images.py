from datetime import timedelta

from django.core.management import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from core.models import Image, Pin


class Command(BaseCommand):
    help = (
        "Delete images that no pin uses, such as uploads whose new-pin "
        "dialog was closed without saving. Only lists them unless --delete "
        "is given."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--older-than", type=float, default=24, metavar="HOURS",
            help="Only images stored more than HOURS ago (default 24), so "
                 "an upload that is still being pinned is left alone.",
        )
        parser.add_argument(
            "--delete", action="store_true",
            help="Delete the images instead of listing them.",
        )

    def handle(self, *args, older_than, delete, **options):
        if older_than < 0:
            raise CommandError("--older-than can't be negative.")
        cutoff = timezone.now() - timedelta(hours=older_than)
        unused = list(
            Image.objects.filter(pin__isnull=True, created__lt=cutoff)
            .order_by("pk").values_list("pk", "image")
        )
        count = 0
        for pk, name in unused:
            if delete and not self._delete_if_unused(pk):
                continue
            count += 1
            if options["verbosity"] >= 2:
                verb = "Deleted" if delete else "Would delete"
                self.stdout.write("%s image %d (%s)" % (verb, pk, name))
        if delete:
            self.stdout.write("Deleted %d unused images." % count)
        else:
            self.stdout.write(
                "%d unused images would be deleted. Run with --delete to "
                "delete them." % count
            )

    @staticmethod
    def _delete_if_unused(pk):
        # Same lock as delete_pin_images, so a pin created from the image
        # in the meantime keeps it.
        with transaction.atomic():
            image = Image.objects.select_for_update().filter(pk=pk).first()
            if image is None or Pin.objects.filter(image_id=pk).exists():
                return False
            image.delete()
            return True
