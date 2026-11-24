#!/usr/bin/env python3
"""Check generated public pages for broken local links and publishing metadata."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import html,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
files=[ROOT/'index.html',ROOT/'audit/index.html',ROOT/'why-geo/index.html',ROOT/'blog/index.html',ROOT/'what-is-geo/index.html',ROOT/'blog/mention-or-recommendation/index.html',ROOT/'blog/why-ai-recommends-competitors/index.html',ROOT/'cases/index.html',ROOT/'cases/fashion/index.html',ROOT/'cases/winline/index.html',ROOT/'privacy.html',ROOT/'consent.html']
errors=[]
for f in files:
 s=f.read_text();p=Page();p.feed(s);name=str(f.relative_to(ROOT))
 try:
  graph=[json.loads(raw) for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)]
  assert graph and all(node.get('@context')=='https://schema.org' for node in graph),'missing schema context'
  page=next(node for node in graph if node['@type']=='WebPage')
  faqs=[node for node in graph if node['@type']=='FAQPage']
  visible=re.findall(r'<summary>([^<]+)</summary>\s*<div class="faq-answer">\s*<p>([^<]+)</p>',s)
  questions=[(q['name'],q['acceptedAnswer']['text']) for faq in faqs for q in faq['mainEntity']]
  assert questions==visible,'FAQ markup differs from visible questions and answers'
  title=re.search('<title>(.*?)</title>',s,re.S).group(1);assert title==page['name'] and '?' in title
  assert next(a['content'] for t,a in p.tags if t=='meta' and a.get('property')=='og:title')==title
  assert next(a['href'] for t,a in p.tags if t=='link' and a.get('rel')=='canonical')==page['url']
  assert 'AiLeeds' not in s and 'AILEEDS' not in s
  visible_text=' '.join(html.unescape(re.sub('<[^>]+>', ' ', s)).split())
  assert not re.search(r'(?<!\d)(31|33)\s*(%|из 100|вопрос|промпт)',visible_text),'retired frequency figures'
  assert all(a.get('href','').startswith('mailto:egorkl2307@gmail.com?') for t,a in p.tags if 'data-open-brief' in a),'missing consultation destination'
  assert not any(t in ('input','textarea','select') and a.get('name') in ('brand','audience','task','service') for t,a in p.tags),'old brief fields'
  ids=[a['id'] for t,a in p.tags if 'id' in a];assert len(ids)==len(set(ids)),'duplicate ids'
  assert sum(t=='h1' for t,a in p.tags)==1
  if name in ('cases/fashion/index.html','cases/winline/index.html'):
   slide_count=10 if 'fashion' in name else 11
   transcript=re.search(r'<details class="slide-transcript">(.*?)</details>',s,re.S)
   assert transcript and transcript[1].count('<li>')==slide_count,'incomplete slide transcript'
   assert s.count('<figure class="deck-slide">')==slide_count,'incomplete slide reader'
   headings=re.findall(r'<h[12]>(.*?)</h[12]>',s,re.S)
   assert headings and all('?' not in heading for heading in headings),'case should read as a story'
   assert next(node['headline'] for node in graph if node['@type']=='Article')==headings[0]
  if name=='index.html':
   film=next(a for t,a in p.tags if t=='video' and 'data-line-src' in a)
   assert film.get('preload')=='none' and 'src' not in film
   for key in ('data-line-src','data-line-mobile'):
    assert (ROOT/urlsplit(film[key]).path).is_file(),'missing hero film'
   for t,a in p.tags:
    if t=='source':assert (ROOT/urlsplit(a['srcset']).path).is_file(),'missing responsive poster'
  for field in ['datePublished','dateModified']:
   assert next(a['content'] for t,a in p.tags if t=='meta' and a.get('name')==field)==page[field]
   if field=='datePublished':assert next(a['datetime'] for t,a in p.tags if t=='time' and a.get('itemprop')==field)==page[field]
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
assert 'url=privacy.html#operator' in (ROOT/'contacts.html').read_text()
legacy=(ROOT/'platforms/index.html').read_text()
assert 'noindex,follow' in legacy and 'url=../why-geo/' in legacy
for path in [*files,ROOT/'sitemap.xml',ROOT/'llms.txt']:
 assert 'platforms/' not in path.read_text(), f'Retired route linked in {path.name}'
if errors:sys.exit(1)
print('All',len(files),'public pages passed.')
