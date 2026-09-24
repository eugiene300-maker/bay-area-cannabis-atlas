"""Rewrite dist/ to extensionless page URLs (about.html -> about).

Cloudflare Pages redirects /page.html to /page, so canonical URLs, the sitemap
and internal links must use the extensionless form to avoid redirecting URLs.
Runs after build.py when data/config.json has "clean_urls": true.
"""
from pathlib import Path
import json, re

R = Path(__file__).resolve().parents[1]
D = R / 'dist'
C = json.loads((R / 'data/config.json').read_text())
if not C.get('clean_urls'):
    raise SystemExit(0)
URL = C['site_url'].rstrip('/')
pages = sorted(p.stem for p in D.glob('*.html'))
names = '|'.join(re.escape(n) for n in sorted(pages, key=len, reverse=True))
abs_re = re.compile(re.escape(URL) + r'/(' + names + r')\.html(?=[#?"\'<\s)]|$)')
rel_re = re.compile(r'(href=")(' + names + r')\.html(?=[#?"])')

def fix_abs(m):
    return URL + '/' + ('' if m.group(1) == 'index' else m.group(1))

def fix_rel(m):
    return m.group(1) + ('./' if m.group(2) == 'index' else m.group(2))

changed = 0
for f in D.rglob('*'):
    if f.suffix not in ('.html', '.xml', '.txt', '.json', '.csv', '.js'):
        continue
    s = f.read_text()
    t = abs_re.sub(fix_abs, s)
    if f.suffix == '.html':
        t = rel_re.sub(fix_rel, t)
        t = t.replace('href="./#', 'href="#') if f.name == 'index.html' else t
    if t != s:
        f.write_text(t)
        changed += 1
print(json.dumps({'clean_urls': 'applied', 'files_changed': changed}))
