import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import parse_qs, urlparse

from unittest import mock
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core import fetch as fetch_module
from core.fetch import BlockedAddressError, FetchError, fetch_url, is_public_address
from core.models import Image, Pin
from .helpers import TEST_IMAGE_PATH, create_user


with open(TEST_IMAGE_PATH, 'rb') as f:
    PNG_BYTES = f.read()


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, code, body=b"", headers=None, content_length=True):
        self.send_response(code)
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        if content_length:
            self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.server.requests.append((self.path, dict(self.headers)))
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        if parsed.path in ("/logo.png", "/page.html"):
            self._send(200, PNG_BYTES, {"Content-Type": "text/html"})
        elif parsed.path == "/big":
            self._send(200, b"x" * 5000)
        elif parsed.path == "/big-no-length":
            self._send(200, b"x" * 5000, content_length=False)
        elif parsed.path in ("/slow", "/slow-no-length"):
            # Trickles bytes, each well within the per-read timeout.
            self.send_response(200)
            if parsed.path == "/slow":
                self.send_header("Content-Length", "100")
            self.end_headers()
            try:
                for _ in range(100):
                    self.wfile.write(b"x")
                    self.wfile.flush()
                    time.sleep(0.1)
            except OSError:
                pass
        elif parsed.path == "/missing":
            self._send(404, b"not here")
        elif parsed.path == "/redirect":
            self._send(302, headers={"Location": query["to"][0]})
        elif parsed.path == "/chain":
            hops = int(query["n"][0])
            to = "/logo.png" if hops == 0 else "/chain?n=%d" % (hops - 1)
            self._send(302, headers={"Location": to})
        else:
            self._send(404)


class _Server(ThreadingMixIn, HTTPServer):
    daemon_threads = True


_real_getaddrinfo = socket.getaddrinfo

# Test hostnames and what they resolve to.
FAKE_DNS = {
    "public.test": ["127.0.0.1"],
    "internal.test": ["10.0.0.5"],
    "metadata.test": ["169.254.169.254"],
    "mixed.test": ["127.0.0.1", "10.0.0.5"],
}


def fake_getaddrinfo(host, port, *args, **kwargs):
    if host in FAKE_DNS:
        return [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, port))
            for ip in FAKE_DNS[host]
        ]
    return _real_getaddrinfo(host, port, *args, **kwargs)


def loopback_is_public(ip):
    # Lets tests treat the local test server as a public host.
    return ip == "127.0.0.1" or _real_is_public_address(ip)


_real_is_public_address = is_public_address


class FetchServerMixin(object):
    @classmethod
    def setUpClass(cls):
        super(FetchServerMixin, cls).setUpClass()
        cls.server = _Server(("127.0.0.1", 0), _Handler)
        cls.server.requests = []
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        super(FetchServerMixin, cls).tearDownClass()

    def setUp(self):
        super(FetchServerMixin, self).setUp()
        self.server.requests[:] = []
        patches = [
            mock.patch("socket.getaddrinfo", fake_getaddrinfo),
            mock.patch("core.fetch.is_public_address", loopback_is_public),
        ]
        for patch in patches:
            patch.start()
            self.addCleanup(patch.stop)

    def url(self, path, host="public.test"):
        return "http://%s:%d%s" % (host, self.port, path)


class IsPublicAddressTests(SimpleTestCase):
    def test_blocks_non_public_addresses(self):
        for ip in (
            "127.0.0.1", "10.1.2.3", "172.16.0.1", "192.168.1.1",
            "169.254.169.254", "100.64.0.1", "0.0.0.0", "224.0.0.1",
            "255.255.255.255", "240.0.0.1",
            "::1", "::", "fe80::1", "fc00::1", "ff02::1",
            "::ffff:127.0.0.1", "::ffff:169.254.169.254",
            "64:ff9b::a00:1", "2002:7f00:1::",
        ):
            self.assertFalse(is_public_address(ip), ip)

    def test_allows_public_addresses(self):
        for ip in ("8.8.8.8", "1.1.1.1", "2606:4700:4700::1111",
                   "64:ff9b::808:808"):
            self.assertTrue(is_public_address(ip), ip)


class FetchUrlTests(FetchServerMixin, SimpleTestCase):
    def test_fetches_public_url(self):
        self.assertEqual(fetch_url(self.url("/logo.png")), PNG_BYTES)

    def test_sends_referer_and_honest_user_agent(self):
        fetch_url(self.url("/logo.png"), referer="http://example.com/")
        _, headers = self.server.requests[0]
        self.assertEqual(headers["Referer"], "http://example.com/")
        self.assertEqual(headers["User-Agent"], fetch_module.USER_AGENT)

    def test_blocks_private_addresses(self):
        for host in ("internal.test", "metadata.test", "mixed.test",
                     "10.0.0.5", "169.254.169.254"):
            with self.assertRaises(BlockedAddressError, msg=host):
                fetch_url(self.url("/logo.png", host=host))

    def test_blocks_loopback_by_default(self):
        with mock.patch("core.fetch.is_public_address", _real_is_public_address):
            with self.assertRaises(BlockedAddressError):
                fetch_url(self.url("/logo.png", host="127.0.0.1"))
            with self.assertRaises(BlockedAddressError):
                fetch_url(self.url("/logo.png", host="localhost"))
        self.assertEqual(self.server.requests, [])

    @override_settings(ALLOW_PRIVATE_URL_FETCH=True)
    def test_opt_out_allows_private_addresses(self):
        with mock.patch("core.fetch.is_public_address", _real_is_public_address):
            data = fetch_url(self.url("/logo.png", host="127.0.0.1"))
        self.assertEqual(data, PNG_BYTES)

    def test_connects_to_the_checked_address(self):
        # A rebinding DNS server answers public first, private afterwards.
        answers = [["127.0.0.1"], ["10.0.0.5"]]
        lookups = []

        def rebinding_getaddrinfo(host, port, *args, **kwargs):
            if host == "rebind.test":
                lookups.append(host)
                ips = answers[min(len(lookups), len(answers)) - 1]
                return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, port))
                        for ip in ips]
            return fake_getaddrinfo(host, port, *args, **kwargs)

        with mock.patch("socket.getaddrinfo", rebinding_getaddrinfo):
            data = fetch_url(self.url("/logo.png", host="rebind.test"))
        self.assertEqual(data, PNG_BYTES)
        self.assertEqual(lookups, ["rebind.test"])
        path, headers = self.server.requests[0]
        self.assertEqual(headers["Host"], "rebind.test:%d" % self.port)

    def test_rejects_non_http_schemes(self):
        for url in ("file:///etc/passwd", "ftp://public.test/x.png",
                    "gopher://public.test/"):
            with self.assertRaises(FetchError, msg=url):
                fetch_url(url)

    def test_follows_redirects(self):
        self.assertEqual(fetch_url(self.url("/chain?n=2")), PNG_BYTES)

    def test_stops_after_three_redirects(self):
        self.assertEqual(fetch_url(self.url("/chain?n=2")), PNG_BYTES)
        with self.assertRaisesMessage(FetchError, "Too many redirects"):
            fetch_url(self.url("/chain?n=3"))

    def test_rechecks_redirect_target(self):
        for target in (self.url("/logo.png", host="internal.test"),
                       "http://169.254.169.254/latest/meta-data/"):
            with self.assertRaises(BlockedAddressError, msg=target):
                fetch_url(self.url("/redirect?to=" + target))
        paths = [path for path, _ in self.server.requests]
        self.assertNotIn("/logo.png", paths)

    def test_rejects_redirect_to_non_http_scheme(self):
        with self.assertRaises(FetchError):
            fetch_url(self.url("/redirect?to=file:///etc/passwd"))

    @override_settings(MAX_FETCH_BYTES=1000)
    def test_size_cap(self):
        for path in ("/big", "/big-no-length"):
            with self.assertRaisesMessage(FetchError, "too large"):
                fetch_url(self.url(path))

    @override_settings(MAX_FETCH_BYTES=5000)
    def test_size_cap_allows_exact_limit(self):
        self.assertEqual(len(fetch_url(self.url("/big-no-length"))), 5000)

    def test_total_timeout_stops_trickling_server(self):
        with mock.patch("core.fetch.TOTAL_TIMEOUT", 1):
            for path in ("/slow", "/slow-no-length"):
                started = time.monotonic()
                with self.assertRaisesMessage(FetchError, "too long"):
                    fetch_url(self.url(path))
                self.assertLess(time.monotonic() - started, 3, path)

    def test_total_timeout_covers_redirects(self):
        with mock.patch("core.fetch.TOTAL_TIMEOUT", 1):
            with self.assertRaisesMessage(FetchError, "too long"):
                fetch_url(self.url("/redirect?to=/slow"))

    def test_rejects_error_status(self):
        with self.assertRaises(FetchError):
            fetch_url(self.url("/missing"))

    def test_uses_timeout(self):
        with mock.patch("requests.Session.get",
                        side_effect=fetch_module.requests.Timeout) as mocked_get:
            with self.assertRaises(FetchError):
                fetch_url(self.url("/logo.png"))
        self.assertEqual(mocked_get.call_args[1]["timeout"], (5, 15))


class CreateForUrlTests(FetchServerMixin, TestCase):
    def tearDown(self):
        Image.objects.all().delete()
        super(CreateForUrlTests, self).tearDown()

    def test_extension_comes_from_detected_format(self):
        image = Image.objects.create_for_url(self.url("/page.html"))
        self.assertTrue(image.image.name.endswith("/page.png"), image.image.name)

    def test_base_name_ignores_query_and_fragment(self):
        image = Image.objects.create_for_url(self.url("/logo.png?x=a.html#b"))
        self.assertTrue(image.image.name.endswith("/logo.png"), image.image.name)

    def test_non_image_content_returns_none(self):
        with override_settings(MAX_FETCH_BYTES=10000):
            self.assertIsNone(Image.objects.create_for_url(self.url("/big")))
        self.assertEqual(Image.objects.count(), 0)


class PinFetchApiTests(FetchServerMixin, APITestCase):
    def setUp(self):
        super(PinFetchApiTests, self).setUp()
        self.user = create_user("default")
        self.client.login(username=self.user.username, password='password')

    def tearDown(self):
        Pin.objects.all().delete()
        Image.objects.all().delete()
        super(PinFetchApiTests, self).tearDown()

    def test_private_url_is_rejected_with_400(self):
        response = self.client.post(
            reverse("pin-list"),
            data={"url": self.url("/logo.png", host="internal.test")},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("not allowed", str(response.json()["url"]))
        self.assertEqual(Image.objects.count(), 0)
        self.assertEqual(self.server.requests, [])

    def test_public_url_creates_pin(self):
        response = self.client.post(
            reverse("pin-list"),
            data={"url": self.url("/page.html")},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         response.content)
        pin = Pin.objects.get()
        self.assertTrue(pin.image.image.name.endswith(".png"))
