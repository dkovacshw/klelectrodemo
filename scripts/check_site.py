"""Validate public HTML, local links/assets, canonical URLs, JSON-LD and sitemap."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, sys, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
PRODUCTION='--production' in sys.argv
if PRODUCTION:ROOT=ROOT/'.build/production'
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.tags=[];self.ids=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append((tag,a))
  if 'id' in a:self.ids.append(a['id'])

files=[ROOT/'index.html',*sorted(ROOT.glob('*/index.html'))]
files=[p for p in files if p.parent.name not in ('release','dist','.work')]
parsed={p.resolve():Page(p.read_text(encoding='utf-8-sig')) for p in files}
errors=[]; titles=set(); descriptions=set()
import re
for p,doc in parsed.items():
 text=p.read_text(encoding='utf-8-sig');label=str(p.relative_to(ROOT))
 def check(ok,message):
  if not ok:errors.append(f'{label}: {message}')
 check(sum(tag=='h1' for tag,a in doc.tags)==1,'expected one H1')
 check(len(doc.ids)==len(set(doc.ids)),'duplicate IDs')
 title=re.search(r'<title>(.*?)</title>',text).group(1)
 check(title not in titles,'duplicate title');titles.add(title)
 canonical='https://klelectro.hu/'+('' if p.parent==ROOT else p.parent.name+'/')
 check(any(t=='link' and a.get('rel')=='canonical' and a.get('href')==canonical for t,a in doc.tags),'canonical mismatch')
 check(any(t=='meta' and a.get('name')=='description' and a.get('content') for t,a in doc.tags),'missing description')
 robots=[a.get('content','') for t,a in doc.tags if t=='meta' and a.get('name')=='robots']
 check(len(robots)==1 and ('noindex' not in robots[0] if PRODUCTION else 'noindex' in robots[0]),'wrong indexing mode')
 description=next((a.get('content','') for t,a in doc.tags if t=='meta' and a.get('name')=='description'),'')
 check(description not in descriptions,'duplicate description');descriptions.add(description)
 previous=0
 for tag,a in doc.tags:
  if tag in ('h1','h2','h3','h4','h5','h6'):
   level=int(tag[1]);check(level<=previous+1,'skipped heading level');previous=level
 check(all(t=='Kép helye' for t in re.findall(r'<div class="picture-space[^\"]*"><span>(.*?)</span></div>',text)),'placeholder text must be exactly Kép helye')
 check(all('assets/brand/logo.webp' in a.get('src','') for tag,a in doc.tags if tag=='img'),'unexpected photo: logo is the only allowed image')
 for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S):
  data=json.loads(raw);check('@graph' in data,'missing schema graph')
 for tag,a in doc.tags:
  if tag=='img':check('alt' in a and 'width' in a and 'height' in a,'missing image attributes')
  refs=[a[x] for x in ('href','src') if x in a]
  if tag=='meta' and a.get('property')=='og:image': refs.append(a['content'])
  for ref in refs:
   u=urlsplit(ref)
   if u.scheme in ('mailto','tel','data') or (u.netloc and u.netloc!='klelectro.hu'):continue
   target=(ROOT/unquote(u.path).lstrip('/') if u.path.startswith('/') or u.netloc else p.parent/unquote(u.path)).resolve()
   if not u.path:target=p
   if target.is_dir():target=target/'index.html'
   check(target.exists(),f'broken reference {ref}')
   if u.fragment and target in parsed:check(u.fragment in parsed[target].ids,f'missing fragment {ref}')
urls={e.text for e in ET.parse(ROOT/'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
expected={'https://klelectro.hu/'+('' if p.parent==ROOT else p.parent.name+'/') for p in parsed}
if urls!=expected:errors.append('Sitemap does not match public pages')
print(f'Checked {len(files)} pages: metadata, links, fragments, assets, JSON-LD and sitemap.')
if errors: print('\n'.join(errors));raise SystemExit(1)
print('PASS')
