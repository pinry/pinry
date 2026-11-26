import gzip
import os
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import mock
from django.test import SimpleTestCase, override_settings

from core.fetch import ImageFetchError, fetch_image, is_address_allowed


__all__ = ['AddressPolicyTests', 'FetchUrlCheckTests', 'FetchImageTests']

IMAGE = b'\x89PNG\r\n\x1a\n' + b'x' * 1000
PROXY_VARIABLES = (
    'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'NO_PROXY',
    'http_proxy', 'https_proxy', 'all_proxy', 'no_proxy',
)


def _addrinfo(*addresses):
    infos = []
    for address in addresses:
        family = socket.AF_INET6 if ':' in address else socket.AF_INET
        infos.append((family, socket.SOCK_STREAM, 6, '', (address, 80)))
    return infos


class AddressPolicyTests(SimpleTestCase):
    def test_blocks_internal_addresses(self):
        for address in (
            '127.0.0.1', '10.1.2.3', '172.16.0.1', '192.168.1.10',
            '169.254.169.254', '100.64.0.1', '100.100.100.200', '0.0.0.0',
            '224.0.0.1', '255.255.255.255', '::1', '::', 'fe80::1',
            'fe80::1%eth0', 'fc00::1', 'fd00:ec2::254', '::ffff:127.0.0.1',
            '::ffff:10.0.0.1', '2002:7f00:1::', '2002:a00:1::',
            '64:ff9b::7f00:1', '64:ff9b::a9fe:a9fe',
        ):
            self.assertFalse(is_address_allowed(address), address)

    def test_allows_public_addresses(self):
        for address in (
            '93.184.216.34', '8.8.8.8', '2606:4700:4700::1111',
            '2002:5db8:d822::', '64:ff9b::808:808',
        ):
            self.assertTrue(is_address_allowed(address), address)

    @override_settings(IMAGE_FETCH_ALLOWED_NETWORKS=['192.168.1.0/24', 'fd12::/16'])
    def test_allowed_networks(self):
        self.assertTrue(is_address_allowed('192.168.1.10'))
        self.assertTrue(is_address_allowed('::ffff:192.168.1.10'))
        self.assertTrue(is_address_allowed('fd12::5'))
        self.assertFalse(is_address_allowed('192.168.2.10'))
        self.assertFalse(is_address_allowed('10.0.0.1'))
        self.assertFalse(is_address_allowed('127.0.0.1'))
        self.assertTrue(is_address_allowed('8.8.8.8'))


class FetchUrlCheckTests(SimpleTestCase):
    """Refused before any connection is made."""

    def assertRefused(self, url):
        with mock.patch('requests.Session.send') as send:
            with self.assertRaises(ImageFetchError, msg=url):
                fetch_image(url)
            send.assert_not_called()

    def test_refuses_other_schemes(self):
        for url in (
            'file:///etc/passwd', 'ftp://example.com/a.png',
            'gopher://example.com/', 'dict://example.com:11211/',
            'javascript:alert(1)', '/relative/a.png', 'example.com/a.png',
        ):
            self.assertRefused(url)

    def test_refuses_internal_hosts(self):
        for url in (
            'http://127.0.0.1/a.png', 'http://localhost:8000/',
            'http://10.0.0.1/', 'http://192.168.1.1/', 'http://[::1]/',
            'http://[::ffff:127.0.0.1]/', 'http://169.254.169.254/',
            'http://0.0.0.0/', 'http://2130706433/', 'http://0x7f000001/',
            'http://0177.0.0.1/', 'http://127.1/',
            'https://127.0.0.1:443/', 'HTTP://127.0.0.1/',
            'http://user:pass@127.0.0.1/',
        ):
            self.assertRefused(url)

    def test_refuses_port_out_of_range(self):
        for url in (
            'http://example.com:70000/',
            'http://example.com:99999999999999999999/',
        ):
            self.assertRefused(url)

    def test_refuses_name_with_any_internal_address(self):
        with mock.patch(
            'core.fetch._resolve',
            return_value=_addrinfo('93.184.216.34', '10.0.0.1'),
        ):
            self.assertRefused('http://mixed.example.com/a.png')

    def test_refuses_unresolvable_name(self):
        with mock.patch(
            'core.fetch._resolve', side_effect=socket.gaierror('no name'),
        ):
            self.assertRefused('http://nonexistent.invalid/a.png')


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        port = self.server.server_address[1]
        path = self.path
        if path == '/image.png':
            self._send(200, IMAGE)
        elif path == '/no-length.png':
            self.send_response(200)
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(IMAGE)
        elif path == '/relative':
            self._redirect('/image.png')
        elif path == '/absolute':
            self._redirect('http://127.0.0.1:%d/image.png' % port)
        elif path == '/to-private':
            self._redirect('http://10.0.0.1/image.png')
        elif path == '/to-file':
            self._redirect('file:///etc/passwd')
        elif path.startswith('/chain/'):
            hops = int(path.split('/')[2])
            if hops == 0:
                self._redirect('/image.png')
            else:
                self._redirect('/chain/%d' % (hops - 1))
        elif path == '/scheme-relative':
            self._redirect('//10.0.0.1/image.png')
        elif path == '/to-ipv6-mapped':
            self._redirect('HTTP://[::ffff:a00:1]/image.png')
        elif path == '/gzip.png':
            body = gzip.compress(IMAGE)
            self.send_response(200)
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif path == '/gzip-bomb.png':
            body = gzip.compress(gzip.compress(b'\0' * (20 * 1024 * 1024)))
            self.send_response(200)
            self.send_header('Content-Encoding', 'gzip, gzip')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif path == '/single-gzip-bomb.png':
            body = gzip.compress(b'\0' * (20 * 1024 * 1024))
            self.send_response(200)
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif path == '/brotli.png':
            self.send_response(200)
            self.send_header('Content-Encoding', 'br')
            self.send_header('Content-Length', str(len(IMAGE)))
            self.end_headers()
            self.wfile.write(IMAGE)
        elif path == '/trickle-body':
            self.send_response(200)
            self.send_header('Content-Length', '100000')
            self.end_headers()
            self._trickle(b'x' * 100)
        elif path == '/trickle-body-no-length':
            self.send_response(200)
            self.end_headers()
            self._trickle(b'x' * 100)
        elif path == '/trickle-headers':
            self.wfile.write(b'HTTP/1.0 200 OK\r\n')
            self._trickle(b'X-Slow: ' + b'x' * 100)
        elif path == '/slow':
            time.sleep(2)
            self._send(200, IMAGE)
        elif path == '/headers':
            body = ('%s|%s|%s' % (
                self.headers.get('User-Agent'), self.headers.get('Referer'),
                self.headers.get('Accept-Encoding'),
            )).encode()
            self._send(200, body)
        else:
            self._send(404, b'not found')

    def _send(self, status, body):
        self.send_response(status)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _trickle(self, data):
        try:
            for byte in data:
                self.wfile.write(bytes([byte]))
                self.wfile.flush()
                time.sleep(0.1)
        except OSError:
            pass

    def _redirect(self, location):
        self.send_response(302)
        self.send_header('Location', location)
        self.send_header('Content-Length', '0')
        self.end_headers()


@override_settings(
    IMAGE_FETCH_ALLOWED_NETWORKS=['127.0.0.1/32'],
    IMAGE_FETCH_TIMEOUT=10,
)
class FetchImageTests(SimpleTestCase):
    """Fetch through a local server; 127.0.0.1 stands in for a public host."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # A proxy from the environment would take the local requests.
        cls.environ = mock.patch.dict(os.environ)
        cls.environ.start()
        for name in PROXY_VARIABLES:
            os.environ.pop(name, None)
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), _Handler)
        cls.server.daemon_threads = True
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()
        cls.base = 'http://127.0.0.1:%d' % cls.server.server_address[1]

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.environ.stop()
        super().tearDownClass()

    def test_fetches_image(self):
        self.assertEqual(fetch_image(self.base + '/image.png'), IMAGE)

    def test_sends_user_agent_and_referer(self):
        body = fetch_image(self.base + '/headers', 'http://example.com/page')
        user_agent, referer, encoding = body.decode().split('|')
        self.assertIn('Mozilla/5.0', user_agent)
        self.assertEqual(referer, 'http://example.com/page')
        self.assertEqual(encoding, 'identity')

    def test_non_200_body_is_returned(self):
        # Left to the image check, as before: it answers "invalid image".
        self.assertEqual(fetch_image(self.base + '/missing'), b'not found')

    def test_follows_redirects(self):
        for path in ('/relative', '/absolute', '/chain/9'):
            self.assertEqual(fetch_image(self.base + path), IMAGE, path)

    def test_too_many_redirects(self):
        with self.assertRaises(ImageFetchError):
            fetch_image(self.base + '/chain/10')

    def test_checks_every_redirect(self):
        for path in (
            '/to-private', '/to-file', '/scheme-relative', '/to-ipv6-mapped',
        ):
            with self.assertRaises(ImageFetchError, msg=path):
                fetch_image(self.base + path)

    @override_settings(IMAGE_FETCH_ALLOWED_NETWORKS=[])
    def test_checks_connected_address(self):
        # The name resolves to a public address when checked, but the
        # connection reaches a refused one (DNS rebinding).
        with mock.patch(
            'core.fetch._resolve', return_value=_addrinfo('93.184.216.34'),
        ):
            with self.assertRaises(ImageFetchError) as cm:
                fetch_image(self.base + '/image.png')
        self.assertIn('connected to 127.0.0.1', str(cm.exception))

    @override_settings(IMAGE_FETCH_ALLOWED_NETWORKS=[])
    def test_checks_connected_address_over_https(self):
        # Checked before the TLS handshake, so a plain server is enough.
        with mock.patch(
            'core.fetch._resolve', return_value=_addrinfo('93.184.216.34'),
        ):
            with self.assertRaises(ImageFetchError) as cm:
                fetch_image(self.base.replace('http:', 'https:') + '/x.png')
        self.assertIn('connected to 127.0.0.1', str(cm.exception))

    def test_decodes_gzip(self):
        self.assertEqual(fetch_image(self.base + '/gzip.png'), IMAGE)

    @override_settings(IMAGE_FETCH_MAX_BYTES=1024 * 1024)
    def test_refuses_compression_bombs(self):
        for path in ('/gzip-bomb.png', '/single-gzip-bomb.png'):
            with self.assertRaises(ImageFetchError, msg=path):
                fetch_image(self.base + path)

    def test_refuses_unsupported_encoding(self):
        with self.assertRaises(ImageFetchError):
            fetch_image(self.base + '/brotli.png')

    @override_settings(IMAGE_FETCH_TIMEOUT=1)
    def test_deadline_stops_trickling_server(self):
        for path in (
            '/trickle-body', '/trickle-body-no-length', '/trickle-headers',
        ):
            started = time.monotonic()
            with self.assertRaises(ImageFetchError, msg=path) as cm:
                fetch_image(self.base + path)
            self.assertLess(time.monotonic() - started, 3, path)
            self.assertIn('timed out', str(cm.exception), path)

    @override_settings(IMAGE_FETCH_MAX_BYTES=100)
    def test_refuses_large_response(self):
        for path in ('/image.png', '/no-length.png'):
            with self.assertRaises(ImageFetchError, msg=path):
                fetch_image(self.base + path)

    @override_settings(IMAGE_FETCH_MAX_BYTES=len(IMAGE))
    def test_allows_response_at_limit(self):
        self.assertEqual(fetch_image(self.base + '/no-length.png'), IMAGE)

    @override_settings(IMAGE_FETCH_TIMEOUT=0.5)
    def test_times_out(self):
        with self.assertRaises(ImageFetchError):
            fetch_image(self.base + '/slow')

    def test_connection_error(self):
        sock = socket.socket()
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
        sock.close()
        with self.assertRaises(ImageFetchError):
            fetch_image('http://127.0.0.1:%d/image.png' % port)
