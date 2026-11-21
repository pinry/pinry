"""Read boards and pins from Pinterest's "Request your data" export.

The export is one HTML page with a section per kind of account data. Only
the Boards and Pins sections are read; the rest (email, login history,
messages and so on) is ignored. Each board and pin is a link followed by
``<br>Key: value`` lines in a fixed order, and values can themselves
contain ``<br>`` line breaks, so fields are found in that order rather
than by splitting on line breaks.
"""
import html
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import urlparse

from core.importers.importer import ImportBoard, ImportPin

NO_DATA = ("", "No data", "None")

BOARD_FIELDS = (
    "Created at", "Category", "Description", "Private", "Protected",
    "Collaborators",
)
PIN_FIELDS = (
    "Title", "Details", "Image", "Is Native", "Board Id", "Board Name",
    "Is Video", "Ip Address", "Username", "Alt Text", "Canonical Link",
    "Story Pin Media", "Video", "Created at", "Alive", "Is a repin",
    "Private",
)

_SECTION = re.compile(r"<h1[^>]*>([^<]*)</h1>")
_BOARD_HEAD = re.compile(
    r'<a href="(https://www\.pinterest\.com/[^"/]+/[^"/]+/)">([^<]*)</a>'
    r'\n<br>Created at: '
)
_PIN_HEAD = re.compile(
    r'<a href="https://www\.pinterest\.com/pin/(\d+)/">'
    r'https://www\.pinterest\.com/pin/\1/</a>\n<br>Title: '
)
_HREF = re.compile(r'<a href="([^"]*)"')
_IMAGE_ID = re.compile(r"[0-9a-f]{32}")
_TAG = re.compile(r"<[^>]+>")


class ExportFormatError(Exception):
    """The file isn't a Pinterest data export this reader understands."""


@dataclass
class ExportBoard:
    name: str
    url: str
    private: bool
    created: datetime = None


@dataclass
class ExportPin:
    id: str
    board_name: str
    image_id: str
    title: str = ""
    details: str = ""
    alt_text: str = ""
    link: str = ""
    private: bool = False
    created: datetime = None


def _spans(pattern, text):
    """Yield each match of ``pattern`` with where the next one starts."""
    heads = list(pattern.finditer(text))
    ends = [head.start() for head in heads[1:]] + [len(text)]
    for head, end in zip(heads, ends[:len(heads)], strict=True):
        yield head, end


def _sections(page):
    """Map each <h1> section title to its HTML."""
    sections = {}
    for head, end in _spans(_SECTION, page):
        sections.setdefault(head.group(1).strip(), page[head.end():end])
    return sections


def _fields(chunk, names):
    """Read ``names`` from ``chunk`` in order; the first has no prefix."""
    values = {}
    rest = chunk
    for name, following in zip(names, names[1:] + (None,), strict=True):
        if following is None:
            values[name] = rest
            break
        marker = "\n<br>%s: " % following
        pos = rest.find(marker)
        if pos < 0:
            raise ExportFormatError("Missing field %r" % following)
        values[name] = rest[:pos]
        rest = rest[pos + len(marker):]
    return values


def _text(value):
    """Turn an HTML field value into plain text, or "" for no data."""
    value = value.strip()
    if value.endswith(","):
        value = value[:-1]
    value = re.sub(r"\s*<br>\s*", "\n", value)
    value = html.unescape(_TAG.sub("", value)).replace("﻿", "")
    value = value.strip()
    return "" if value in NO_DATA else value


def _link(value):
    """The first http(s) link in a field value, or ""."""
    match = _HREF.search(value)
    if not match:
        return ""
    url = html.unescape(match.group(1)).strip()
    if urlparse(url).scheme.lower() not in ("http", "https"):
        return ""
    return url


def _flag(value):
    """True or False, or None when the value isn't either.

    Only the leading word counts: the last field of the last pin runs
    straight into whatever follows it in the page.
    """
    match = re.match(r"\s*(True|False)\b", value)
    return None if match is None else match.group(1) == "True"


def _private(value):
    # Anything that isn't clearly public is treated as private, so a
    # misread flag can't publish something that was private on Pinterest.
    return _flag(value) is not False


def _date(value):
    value = _text(value)
    try:
        parsed = datetime.strptime(value, "%Y/%m/%d %H:%M:%S")
    except ValueError:
        return None
    return parsed.replace(tzinfo=timezone.utc)


def _strip_end(chunk):
    # The last field of an entry runs into the separator before the next.
    return re.sub(r"(<br>)+\s*$", "", chunk.rstrip())


def _entries(section, head_pattern):
    for head, end in _spans(head_pattern, section):
        yield head, _strip_end(section[head.end():end])


def parse_boards(section):
    boards = []
    for head, chunk in _entries(section, _BOARD_HEAD):
        values = _fields(chunk, BOARD_FIELDS)
        boards.append(ExportBoard(
            name=_text(head.group(2)),
            url=html.unescape(head.group(1)),
            # Protected boards are ads-only boards; treat them as private.
            private=_private(values["Private"])
            or _flag(values["Protected"]) is True,
            created=_date(values["Created at"]),
        ))
    return boards


def parse_pins(section):
    pins = []
    for head, chunk in _entries(section, _PIN_HEAD):
        values = _fields(chunk, PIN_FIELDS)
        image_id = _text(values["Image"]).lower()
        pins.append(ExportPin(
            id=head.group(1),
            board_name=_text(values["Board Name"]),
            image_id=image_id if _IMAGE_ID.fullmatch(image_id) else "",
            title=_text(values["Title"]),
            details=_text(values["Details"]),
            alt_text=_text(values["Alt Text"]),
            link=_link(values["Canonical Link"]),
            private=_private(values["Private"]),
            created=_date(values["Created at"]),
        ))
    return pins


def parse_export(page):
    """Return ``(boards, pins)`` read from the export page's HTML."""
    sections = _sections(page)
    if "Boards" not in sections or "Pins" not in sections:
        raise ExportFormatError(
            "No Boards or Pins section found; is this a Pinterest data "
            "export?"
        )
    return parse_boards(sections["Boards"]), parse_pins(sections["Pins"])


def image_urls(image_id):
    """Candidate download URLs for an export image id, best first.

    Pinterest keeps the original under its own extension, which the export
    doesn't record, so try the common ones before the 736px-wide copy,
    which is always a JPEG.
    """
    path = "%s/%s/%s/%s" % (
        image_id[0:2], image_id[2:4], image_id[4:6], image_id,
    )
    urls = [
        "https://i.pinimg.com/originals/%s.%s" % (path, ext)
        for ext in ("jpg", "png", "gif", "webp")
    ]
    urls.append("https://i.pinimg.com/736x/%s.jpg" % path)
    return urls


def description(pin):
    """The title on the first line, then the details; alt text if neither."""
    parts = [pin.title]
    if pin.details and pin.details != pin.title:
        parts.append(pin.details)
    text = "\n\n".join(part for part in parts if part)
    return text or pin.alt_text


def import_items(boards, pins):
    """Turn parsed export data into importer items.

    Pins without an image id (blank records in the export) are left out.
    """
    return (
        [ImportBoard(name=board.name, private=board.private)
         for board in boards],
        [ImportPin(
            source_id="pinterest:%s" % pin.id,
            board_name=pin.board_name,
            image_urls=image_urls(pin.image_id),
            description=description(pin),
            link=pin.link,
            private=pin.private,
            created=pin.created,
        ) for pin in pins if pin.image_id],
    )
