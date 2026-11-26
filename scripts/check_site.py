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
stylesheets=set()
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
  title=re.search('<title>(.*?)</title>',s,re.S).group(1);assert title.strip() and title==page['name']
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
   chapters=re.findall(r'<section id="([^"]+)" class="story-(?:chapter|interlude)',s)
   assert chapters and all(f'href="#{anchor}"' in s for anchor in chapters),'case navigation'
   assert 'slide-reader' not in s,'duplicate case reader'
   headings=re.findall(r'<h[12]>(.*?)</h[12]>',s,re.S)
   assert headings and all('?' not in heading for heading in headings),'case should read as a story'
   assert next(node['headline'] for node in graph if node['@type']=='Article')==headings[0]
  if name=='index.html':
   assert not any(t=='video' for t,a in p.tags),'unrelated film in hero'
   assert 'aria-label="100 процентов"' in s and 'Цель продвижения' in s, 'visibility goal missing'
   assert all(anchor in ids for anchor in ('scope','demand','offers','projects','winline-study','faq','brief'))
   assert 'Что мы меняем в&nbsp;ответах нейросетей?' in s, 'promotion outcomes heading missing'
   assert [a.get('data-result') for t,a in p.tags if t=='article' and 'data-result' in a]==['mention','citation','link'], 'promotion outcomes missing'
   assert 'Когда мы можем помочь?' in s, 'promotion suitability missing'
   assert all(any(t=='a' and a.get('href')==path for t,a in p.tags) for path in ('cases/fashion/','cases/winline/')), 'case link missing'
   assert all(marker not in s for marker in ('market-examples', 'Пример запроса покупателя', 'scope-estimate', 'Как работать с вашей командой')), 'retired homepage content'
  if name!='cases/fashion/index.html':
   assert not re.search('дуба[йяеию]', s, re.I), 'Dubai belongs only to the fashion case'
  if name in ('index.html', 'audit/index.html', 'why-geo/index.html'):
   main=s.split('<main id="main">',1)[1].split('</main>',1)[0]
   headings=re.findall(r'<h2(?: [^>]*)?>(.*?)</h2>',main,re.S)
   assert headings and all(heading.strip().endswith('?') for heading in headings), 'section headings must be buyer questions'
  if name=='audit/index.html':
   assert all(s.count(f'data-measure="{key}"')==1 for key in ('name','source','link'))
   assert 'Учебный отчёт' in s and 'scoreboard' in s and 'tone-ring' in s
   audit_main = s.split('<main id="main">',1)[1].split('</main>',1)[0]
   assert not re.search(r'href="\.\./cases/', audit_main), 'case promotion in the audit'
   assert 'Линия' not in audit_main and 'WINLINE' not in s, 'sample must be anonymous'
   assert all(anchor in ids for anchor in ('audit-start', 'observations', 'tone', 'sample-board', 'results', 'competitors', 'audit-value', 'report', 'faq', 'brief')), 'audit sections missing'
   assert 'audit-opening front-cover' in audit_main and 'Учебный срез' in audit_main, 'audit cover or sample label missing'
   assert [a.get('value') for t, a in p.tags if t=='input' and a.get('name')=='preview-metric']==['name','source','link'], 'audit cover measures missing'
   roster = re.search(r'<section class="model-ribbon".*?<ul role="list">(.*?)</ul>', audit_main, re.S)
   assert roster and re.findall(r'alt="([^"]+)"', roster[1]) == ['ChatGPT','Claude','Grok','Gemini','Алиса','GigaChat'], 'unexpected audit models'
  if name.startswith(('blog/','what-is-geo/')):
   for t,a in p.tags:
    if t!='a': continue
    if urlsplit(a.get('href','')).netloc:
     assert 'nofollow' in a.get('rel','').split(),'outbound blog source must be nofollow'
    else:
     assert 'nofollow' not in a.get('rel','').split(),'internal editorial link must stay followable'
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
   if t=='link' and a.get('rel')=='stylesheet':
    stylesheets.add(target.resolve())
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
for sheet in sorted(stylesheets):
 for match in re.finditer(r"""url\(\s*(['"]?)(.*?)\1\s*\)""",sheet.read_text(),re.I):
  url=urlsplit(match[2])
  if url.scheme or url.netloc or not url.path:continue
  target=ROOT/url.path.lstrip('/') if url.path.startswith('/') else sheet.parent/url.path
  if not target.is_file():
   errors.append((sheet.name,url.path))
   print(sheet.relative_to(ROOT),'missing',url.path)
if errors:sys.exit(1)
print('All',len(files),'public pages passed.')
