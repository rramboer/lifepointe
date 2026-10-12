#!/usr/bin/env python3
"""Preview the built site on this computer, served the way GitHub Pages serves it.

    python3 preview.py            serve dist/ at http://localhost:8000
    python3 preview.py DIR        serve DIR instead (such as an unpacked pull-request build)
    python3 preview.py --port N   use another port

Like GitHub Pages, /about loads about.html (the site's links leave out .html), and an address
with no page gets 404.html with status 404. Folders are never listed. Only this computer can
connect. Python 3.9+ standard library only.
"""
import argparse
import http.server
import sys
from functools import partial
from pathlib import Path

if sys.version_info < (3, 9):
    sys.exit('preview.py needs Python 3.9 or newer')


class PagesHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        local = super().translate_path(path)
        page = Path(local + '.html')
        # /about -> about.html, but not /about/ (GitHub Pages has no page there either).
        if not local.endswith(('/', '\\')) and not Path(local).exists() and page.is_file():
            return str(page)
        return local

    def list_directory(self, path):
        self.send_error(404)
        return None

    def send_error(self, code, message=None, explain=None):
        not_found = Path(self.directory) / '404.html'
        if code != 404 or not not_found.is_file():
            super().send_error(code, message, explain)
            return
        body = not_found.read_bytes()
        self.send_response(404)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(body)


def main():
    parser = argparse.ArgumentParser(prog='preview.py', description='Preview the built Lifepointe website.')
    parser.add_argument('dir', nargs='?', default=str(Path(__file__).resolve().parent / 'dist'),
                        help='the built site (default: dist/)')
    parser.add_argument('--port', type=int, default=8000, help='port (default: 8000)')
    args = parser.parse_args()
    root = Path(args.dir).resolve()
    if not (root / 'index.html').is_file():
        sys.exit(f'{root} has no index.html; run python3 build.py first')
    handler = partial(PagesHandler, directory=str(root))
    with http.server.ThreadingHTTPServer(('127.0.0.1', args.port), handler) as server:
        print(f'Serving {root} at http://localhost:{args.port}/ (Ctrl+C stops it)', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
