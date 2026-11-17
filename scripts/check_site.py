#!/usr/bin/env python3
"""Check generated public pages for broken local links and publishing metadata."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
files=[ROOT/'index.html',ROOT/'audit/index.html',ROOT/'why-geo/index.html',ROOT/'platforms/index.html',ROOT/'blog/index.html',ROOT/'what-is-geo/index.html',ROOT/'blog/mention-or-recommendation/index.html',ROOT/'blog/why-ai-recommends-competitors/index.html',ROOT/'contacts.html',ROOT/'privacy.html',ROOT/'consent.html']
errors=[]
for f in files:
 s=f.read_text();p=Page();p.feed(s);name=str(f.relative_to(ROOT))
 try:
  data=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',s,re.S).group(1));graph=data['@graph'];page=next(x for x in graph if x['@type']=='WebPage')
  title=re.search('<title>(.*?)</title>',s,re.S).group(1);assert title==page['name'] and '?' in title
  assert next(a['content'] for t,a in p.tags if t=='meta' and a.get('property')=='og:title')==title
  assert next(a['href'] for t,a in p.tags if t=='link' and a.get('rel')=='canonical')==page['url']
  assert 'AiLeeds' not in s and 'AILEEDS' not in s
  ids=[a['id'] for t,a in p.tags if 'id' in a];assert len(ids)==len(set(ids)),'duplicate ids'
  assert sum(t=='h1' for t,a in p.tags)==1
  for field in ['datePublished','dateModified']:
   assert next(a['content'] for t,a in p.tags if t=='meta' and a.get('name')==field)==page[field]
   assert next(a['datetime'] for t,a in p.tags if t=='time' and a.get('itemprop')==field)==page[field]
  for t,a in p.tags:
   if t=='img':assert a.get('alt'),'missing alt'
   ref=a.get('src','') if t in ['img','script'] else a.get('href','') if t in ['a','link'] else ''
   if not ref or ref.startswith(('http:','https:','mailto:','tel:')):continue
   u=urlsplit(ref);target=f if not u.path else f.parent/u.path
   if target.is_dir():target=target/'index.html'
   assert target.exists(),ref
   if u.fragment:assert re.search(r'\bid="'+re.escape(u.fragment)+'"',target.read_text()),ref
  for a in [x for x in graph if x['@type']=='Article']:
   assert a.get('author') and a['datePublished']==page['datePublished']
  print(name,'OK')
 except Exception as e:errors.append((name,str(e)));print(name,'FAIL',e)
if errors:sys.exit(1)
print('All',len(files),'public pages passed.')
