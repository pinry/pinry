# Import from Pinterest

`manage.py import_pinterest` copies your Pinterest boards and pins into
Pinry from Pinterest's own data export. It reads the export file and
downloads each pin's image from Pinterest's image server
(`i.pinimg.com`); it doesn't sign in to Pinterest or use its API.

## What gets imported

| Pinterest | Pinry |
| --- | --- |
| Board | Board with the same name, owned by the user you choose |
| Secret or protected board | Private board; its pins are private too |
| Pin image | The original image, or the 736-pixel copy if the original can't be found |
| Pin title and description | Description, title on the first line (alt text if both are empty) |
| Pin source link | Source |
| Date the pin was saved | Pin date; pins are created oldest first, so the newest are at the top of the feed |

Board sections aren't in the export, so their pins go into the parent
board. Video and story pins are imported as their cover image. Comments,
notes, followers and the rest of the account data in the export are
ignored.

A board with the same name that the user already has is reused. If the
Pinterest board was private, the Pinry board is made private; an existing
private board is never made public.

## 1. Get the export

On Pinterest, open **Settings > Privacy and data > Request your data**.
Pinterest emails a download link, usually within 48 hours. The download
is a single HTML file.

The file also holds personal account data (your email address, login
history and messages). Keep it somewhere private and delete it once the
import is done.

## 2. Copy it into the container

With the Docker setup in [Install with Docker](install-with-docker.md),
`./data` next to the compose file is `/data` inside the container, so copy
the file there:

```sh
cp ~/Downloads/pinterest_export.html ./data/
```

The pins need a Pinry user to own them. Create one first if needed
(`docker compose exec pinry python manage.py createsuperuser`).

## 3. Check what will happen

```sh
docker compose exec pinry python manage.py import_pinterest \
    /data/pinterest_export.html --user YOUR_USERNAME --dry-run
```

The dry run reads the file and prints how many boards would be created
and how many pins would be imported, public and private, without changing
anything or downloading images. Check the private count before going on:
anyone with a link can see public pins.

## 4. Import

```sh
docker compose exec pinry python manage.py import_pinterest \
    /data/pinterest_export.html --user YOUR_USERNAME
```

Options:

+ `--private`: import every board and pin as private, whatever it was on
  Pinterest. You can make boards and pins public later.
+ `--tag TAG`: add `TAG` to every imported pin, for example
  `--tag pinterest`. Give it more than once for several tags.
+ `--delay SECONDS`: pause before each image download (default 1). At the
  default, 5,000 pins take roughly one and a half to two hours.

Each pin is saved as soon as its image is downloaded. If the import stops
(or you stop it with Ctrl+C), run the same command again: pins imported
before are skipped. Pins whose image couldn't be downloaded are counted
at the end (`-v 2` lists them) and retried on the next run.

Running it again later with a newer export adds only the new pins.

## 5. Clean up

Delete the export file from `./data` when you're done:

```sh
rm ./data/pinterest_export.html
```
