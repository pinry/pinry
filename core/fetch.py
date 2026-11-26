"""Download the image behind a pin's URL without reaching internal hosts.

Pin creation fetches a user-supplied URL on the server. Unrestricted, that
lets any signed-in user make the server request loopback, private-network
or cloud metadata addresses (SSRF), probe them through the response, and
read any image they serve. Only public addresses are fetched unless the
administrator allows a network in IMAGE_FETCH_ALLOWED_NETWORKS.
"""
import http.client
import ipaddress
import socket
import threading
import time
import zlib
from urllib.parse import urljoin

import requests
import urllib3.exceptions
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from requests.adapters import HTTPAdapter
from urllib3.connection import HTTPConnection, HTTPSConnection
from urllib3.connectionpool import HTTPConnectionPool, HTTPSConnectionPool
from urllib3.util import parse_url

USER_AGENT = (
    'Mozilla/5.0 (Windows NT 5.1) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/48.0.2564.82 Safari/537.36'
)

MAX_REDIRECTS = 10
CONNECT_TIMEOUT = 5
CHUNK_SIZE = 16 * 1024

_NAT64 = ipaddress.ip_network('64:ff9b::/96')

# The deadline of the fetch running in this thread, for _PeerCheckMixin.
_current = threading.local()


class ImageFetchError(Exception):
    """The image could not be fetched; the message is for the server log."""


def _allowed_networks():
    networks = []
    for value in getattr(settings, 'IMAGE_FETCH_ALLOWED_NETWORKS', []):
        try:
            networks.append(ipaddress.ip_network(str(value), strict=False))
        except ValueError:
            raise ImproperlyConfigured(
                'IMAGE_FETCH_ALLOWED_NETWORKS contains an invalid '
                'network: %r' % (value,)
            )
    return networks


def _embedded_ipv4(ip):
    # These IPv6 forms carry an IPv4 address that the packet ends up at,
    # so judge them by that address.
    if ip.version != 6:
        return None
    if ip.ipv4_mapped is not None:
        return ip.ipv4_mapped
    if ip.sixtofour is not None:
        return ip.sixtofour
    if ip in _NAT64:
        return ipaddress.IPv4Address(int(ip) & 0xFFFFFFFF)
    return None


def _is_public(ip):
    # is_global alone differs between Python versions, so also list the
    # special-purpose ranges explicitly.
    if ip.is_private or ip.is_loopback or ip.is_link_local \
            or ip.is_multicast or ip.is_reserved or ip.is_unspecified:
        return False
    if ip.version == 6 and ip.is_site_local:
        return False
    return ip.is_global


def is_address_allowed(address):
    ip = ipaddress.ip_address(address.split('%', 1)[0])
    ip = _embedded_ipv4(ip) or ip
    for network in _allowed_networks():
        if ip.version == network.version and ip in network:
            return True
    return _is_public(ip)


class _Deadline:
    """Enforce the total time limit, even on a server that trickles bytes.

    Socket timeouts only bound a single read, so when time is up a timer
    shuts down every connection of the fetch, which ends any blocked read.
    """

    def __init__(self, seconds):
        self.end = time.monotonic() + seconds
        self.expired = False
        self._sockets = []
        self._lock = threading.Lock()
        self._timer = threading.Timer(seconds, self._expire)
        self._timer.daemon = True

    def __enter__(self):
        _current.deadline = self
        self._timer.start()
        return self

    def __exit__(self, *exc_info):
        self._timer.cancel()
        _current.deadline = None
        with self._lock:
            for sock in self._sockets:
                sock.close()
            self._sockets = []

    def watch(self, sock):
        # Keep a duplicate: shutting it down ends the shared connection,
        # and unlike the original (which TLS wrapping detaches) it stays
        # valid until __exit__.
        with self._lock:
            if self.expired:
                raise ImageFetchError('timed out')
            self._sockets.append(sock.dup())

    def _expire(self):
        with self._lock:
            self.expired = True
            for sock in self._sockets:
                try:
                    sock.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass

    def remaining(self):
        remaining = self.end - time.monotonic()
        if self.expired or remaining <= 0:
            raise ImageFetchError('timed out')
        return remaining


def _resolve(host, port):
    return socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)


def _check_url(url):
    """Return the normalized URL if its scheme and every address are allowed."""
    prepared = requests.PreparedRequest()
    prepared.prepare_url(url, None)
    parts = parse_url(prepared.url)
    scheme = (parts.scheme or '').lower()
    if scheme not in ('http', 'https'):
        raise ImageFetchError('scheme %r is not allowed' % scheme)
    host = (parts.host or '').strip('[]')
    if not host:
        raise ImageFetchError('URL has no host')
    port = parts.port
    if port is None:
        port = 443 if scheme == 'https' else 80
    if not 1 <= port <= 65535:
        raise ImageFetchError('port %d is out of range' % port)
    try:
        infos = _resolve(host, port)
    except (OSError, UnicodeError, OverflowError) as e:
        raise ImageFetchError('cannot resolve %r: %s' % (host, e))
    if not infos:
        raise ImageFetchError('cannot resolve %r' % host)
    for info in infos:
        address = info[4][0]
        if not is_address_allowed(address):
            raise ImageFetchError(
                '%r resolves to %s, which is not allowed' % (host, address)
            )
    return prepared.url


class _PeerCheckMixin:
    # The name may resolve differently when urllib3 connects than when
    # _check_url looked it up (DNS rebinding), so check the address that
    # was actually connected to before sending anything.
    def _new_conn(self):
        sock = super()._new_conn()
        try:
            address = sock.getpeername()[0]
            if not is_address_allowed(address):
                raise ImageFetchError(
                    'connected to %s, which is not allowed' % address
                )
            deadline = getattr(_current, 'deadline', None)
            if deadline is not None:
                deadline.watch(sock)
        except Exception:
            sock.close()
            raise
        return sock


class _GuardedHTTPConnection(_PeerCheckMixin, HTTPConnection):
    pass


class _GuardedHTTPSConnection(_PeerCheckMixin, HTTPSConnection):
    pass


class _GuardedHTTPConnectionPool(HTTPConnectionPool):
    ConnectionCls = _GuardedHTTPConnection


class _GuardedHTTPSConnectionPool(HTTPSConnectionPool):
    ConnectionCls = _GuardedHTTPSConnection


class _GuardedAdapter(HTTPAdapter):
    # Connections through a proxy from the environment are not covered:
    # the peer is the proxy, which resolves the name itself.
    def init_poolmanager(self, *args, **kwargs):
        super().init_poolmanager(*args, **kwargs)
        self.poolmanager.pool_classes_by_scheme = {
            'http': _GuardedHTTPConnectionPool,
            'https': _GuardedHTTPSConnectionPool,
        }


def _get(session, url, headers, deadline):
    # Follow redirects here instead of in requests so that every hop is
    # checked; redirects to CDNs or from http to https keep working.
    for _ in range(MAX_REDIRECTS + 1):
        deadline.remaining()
        url = _check_url(url)
        remaining = deadline.remaining()
        response = session.get(
            url,
            headers=headers,
            allow_redirects=False,
            stream=True,
            timeout=(min(CONNECT_TIMEOUT, remaining), remaining),
        )
        location = session.get_redirect_target(response)
        if location is None:
            return response
        response.close()
        url = urljoin(response.url, location)
    raise ImageFetchError('too many redirects')


def _decoder(response):
    # Decode at most one layer, with a bounded output size: urllib3 would
    # decode stacked encodings ("gzip, gzip") a whole chunk at a time,
    # which lets a tiny response expand to gigabytes before any check.
    encoding = response.headers.get('Content-Encoding', '').strip().lower()
    if encoding in ('', 'identity'):
        return None
    if encoding in ('gzip', 'x-gzip'):
        return zlib.decompressobj(16 + zlib.MAX_WBITS)
    if encoding == 'deflate':
        return zlib.decompressobj()
    raise ImageFetchError('unsupported Content-Encoding %r' % encoding)


def _read_body(response, max_bytes, deadline):
    def too_large():
        return ImageFetchError('response is larger than %d bytes' % max_bytes)

    decoder = _decoder(response)
    length = response.headers.get('Content-Length', '')
    if length.isdigit() and int(length) > max_bytes:
        raise too_large()
    body = bytearray()
    for chunk in response.raw.stream(CHUNK_SIZE, decode_content=False):
        if decoder is None:
            body += chunk
            if len(body) > max_bytes:
                raise too_large()
        while chunk and decoder is not None:
            # Output stops at one byte over the limit; that is enough to
            # tell the body is too large.
            body += decoder.decompress(chunk, max_bytes + 1 - len(body))
            if len(body) > max_bytes:
                raise too_large()
            chunk = decoder.unconsumed_tail
        deadline.remaining()
    if decoder is not None:
        body += decoder.flush()
        if len(body) > max_bytes:
            raise too_large()
    # A connection shut down by the deadline can look like the end of a
    # body sent without Content-Length.
    deadline.remaining()
    return bytes(body)


def fetch_image(url, referer=None):
    """Return the body at ``url``; raise ImageFetchError if not allowed."""
    headers = {
        'User-Agent': USER_AGENT,
        'Accept-Encoding': 'identity',
    }
    if referer is not None:
        headers['Referer'] = referer
    with _Deadline(settings.IMAGE_FETCH_TIMEOUT) as deadline, \
            requests.Session() as session:
        adapter = _GuardedAdapter()
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        try:
            response = _get(session, url, headers, deadline)
            with response:
                return _read_body(
                    response, settings.IMAGE_FETCH_MAX_BYTES, deadline,
                )
        except (
            requests.RequestException,
            urllib3.exceptions.HTTPError,
            http.client.HTTPException,
            zlib.error,
            OSError,
            ValueError,
        ) as e:
            if deadline.expired:
                raise ImageFetchError('timed out')
            raise ImageFetchError('request failed: %s' % e)
