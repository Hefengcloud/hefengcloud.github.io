"""Validate imported content, story timings and built internal links."""
from pathlib import Path
import json
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
root=Path(__file__).resolve().parents[1]
c=json.loads((root/'assets/learning/catalog.json').read_text());m=json.loads((root/'assets/learning/manifest.json').read_text())
from content_tracks import track_for
assert all(x['track']==track_for(x) for x in c)
assert sum(x['track']=='pep' for x in c)==110
assert len({x['id'] for x in c})==len(c)
assert len(m)==sum(len(x['sources']) for x in c)+sum(x['status']=='ignored metadata' for x in m)
for x in c:
 assert (root/x['url'].lstrip('/')).is_file(),x['url']
 if x['kind']=='audio':assert x['duration']>0
 last=-1
 for s in x.get('segments',[]):
  assert 0<=s['start']<s['end']<=x['duration']+.1,(x['title'],s)
  assert s['start']>=last,(x['title'],s)
  last=s['start']
assert sum(x['category']=='stories' for x in c)==13
assert not list((root/'_posts').glob('*'))
assert not list((root/'_pages').glob('*.md'))
site=root/'_site'
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for name,value in attrs:
   if name in ('src','href') and value and value.startswith('/') and not value.startswith('//'):
    path=site/unquote(urlsplit(value).path.lstrip('/'))
    assert path.exists(),f'Missing internal link: {value}'
for p in site.rglob('*.html'):Links().feed(p.read_text())
for old in ['about','products','services','blogs']:assert not (site/old).exists(),old
print(f'PASS: {len(m)} source records, {len(c)} unique resources, 13 story timelines, internal links and retired routes.')
