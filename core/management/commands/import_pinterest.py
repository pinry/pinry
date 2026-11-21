from django.core.management import BaseCommand, CommandError

from core.importers.importer import PinImporter
from core.importers.pinterest_export import (
    ExportFormatError, import_items, parse_export,
)
from users.models import User


class Command(BaseCommand):
    help = (
        "Import boards and pins from a Pinterest data export (the HTML file "
        "from Settings > Privacy and data > Request your data). Images are "
        "downloaded from Pinterest's image server. Pins imported before are "
        "skipped, so an interrupted import can be run again."
    )

    def add_arguments(self, parser):
        parser.add_argument("export", help="Path to the export's HTML file.")
        parser.add_argument(
            "--user", required=True,
            help="Username of the Pinry user who will own the pins.",
        )
        parser.add_argument(
            "--dry-run", action="store_true",
            help="Count what would be imported without changing anything "
                 "or downloading images.",
        )
        parser.add_argument(
            "--private", action="store_true",
            help="Make every imported board and pin private, whatever its "
                 "privacy on Pinterest.",
        )
        parser.add_argument(
            "--tag", action="append", default=[], metavar="TAG",
            help="Add TAG to every imported pin. Can be given more than "
                 "once.",
        )
        parser.add_argument(
            "--delay", type=float, default=1.0, metavar="SECONDS",
            help="Pause before each image download (default 1).",
        )

    def handle(self, *args, export, user, dry_run, private, tag, delay,
               **options):
        if delay < 0:
            raise CommandError("--delay can't be negative.")
        try:
            owner = User.objects.get(username=user)
        except User.DoesNotExist:
            raise CommandError("No user named %r." % user) from None
        try:
            with open(export, encoding="utf-8") as f:
                page = f.read()
        except (OSError, UnicodeDecodeError) as e:
            raise CommandError("Can't read %s: %s" % (export, e)) from e
        try:
            boards, pins = import_items(*parse_export(page))
        except ExportFormatError as e:
            raise CommandError(str(e)) from e

        self.stdout.write(
            "Found %d boards and %d pins in the export."
            % (len(boards), len(pins))
        )
        importer = PinImporter(
            owner,
            force_private=private,
            tags=[t.strip() for t in tag if t.strip()],
            delay=delay,
            dry_run=dry_run,
            progress=self.stdout.write,
        )
        report = importer.run(boards, pins)

        verb = "would be" if dry_run else "were"
        self.stdout.write(
            "Boards: %d %s created, %d already existed."
            % (report.boards_created, verb, report.boards_existing)
        )
        if report.boards_made_private:
            self.stdout.write(
                "%d existing boards %s made private to match Pinterest."
                % (report.boards_made_private, verb)
            )
        self.stdout.write(
            "Pins: %d %s imported (%d public, %d private), %d were imported "
            "before."
            % (report.pins_imported, verb, report.pins_public,
               report.pins_private, report.pins_already_imported)
        )
        if report.failed:
            self.stdout.write(
                "%d pins failed; run the import again to retry them."
                % len(report.failed)
            )
            if options["verbosity"] >= 2:
                for source_id, reason in report.failed:
                    self.stdout.write("  %s: %s" % (source_id, reason))
        if dry_run:
            self.stdout.write("Dry run: nothing was changed.")
