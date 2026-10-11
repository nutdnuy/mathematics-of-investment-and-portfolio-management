#!/usr/bin/env python3
"""Export the authorized draft reader and keep legacy overview routes valid."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import shutil, runpy, json, hashlib
ROOT = Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT / 'scripts/build_overview.py'), run_name='__main__')
manifest = json.loads((ROOT / 'reader-manifest.json').read_text())
for name, digest in manifest['files'].items():
    path = ROOT / 'reader' / name
    assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest, name
shutil.copytree(ROOT / 'reader', ROOT / '_site', dirs_exist_ok=True)
class References(HTMLParser):
    def __init__(self):
        super().__init__(); self.urls = []; self.ids = set()
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src') and value: self.urls.append(value)
            if key == 'id': self.ids.add(value)
parsers = {}
for page in (ROOT / '_site').rglob('*.html'):
    parser = References(); parser.feed(page.read_text()); parsers[page.resolve()] = parser
errors = []
for page, parser in parsers.items():
    for url in parser.urls:
        parts = urlsplit(url)
        if parts.scheme or parts.netloc: continue
        dest = (page.parent / unquote(parts.path)).resolve() if parts.path else page
        if dest.is_dir(): dest /= 'index.html'
        if not dest.is_file(): errors.append(f'{page.name}: missing {url}')
        elif parts.fragment and dest in parsers and unquote(parts.fragment) not in parsers[dest].ids:
            errors.append(f'{page.name}: missing anchor {url}')
assert not errors, '\n'.join(errors[:30])
print(f'Validated {len(parsers)} HTML pages and {len(manifest["files"])} reader files')
