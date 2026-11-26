#!/usr/bin/env python3
"""Render aileed's static pages. Use --base-url only when the domain is ready."""
from functools import lru_cache
from pathlib import Path
import argparse,json,re,html,hashlib
from urllib.parse import quote
from xml.sax.saxutils import escape
from visibility import observation_figure, report_preview, source_map, tone_figure
from guide import FAQ as why_faq, brand_guide
from editorial import POSTS, TOPICS, cover_art, journal, geo_article, mention_article, competitor_article
from cases import PROJECTS, case_index, case_article
from home import FAQ as home_faq, agency_home, home_hero
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--base-url',default='https://egi411.github.io/geo-audit/');args=ap.parse_args();BASE=args.base_url.rstrip('/')+'/'
FIRST_EDITION='2026-11-18'
UPDATED='2026-11-24'
REVISED_PAGES = dict.fromkeys(('', 'audit/', 'why-geo/', 'blog/', 'cases/', 'cases/fashion/', 'cases/winline/', *(post[0] for post in POSTS)), '2026-11-26')
@lru_cache(maxsize=None)
def asset(name):
 path = ROOT / 'assets' / name
 digest = hashlib.sha256(path.read_bytes()).hexdigest()[:12]
 return f'assets/{name}?v={digest}'
CONSULT_EMAIL = "egorkl2307@gmail.com"
CONSULT_SUBJECT = quote("Заявка на бесплатную консультацию")
CONSULT_BODY = quote("Здравствуйте! Хочу записаться на бесплатную консультацию.\n\nСайт: \nПродукт или услуга для продвижения: ")
CONSULT_LINK = f"mailto:{CONSULT_EMAIL}?subject={CONSULT_SUBJECT}&amp;body={CONSULT_BODY}"

def chapter(name, content, anchor=''):
 anchor = f' id="{anchor}"' if anchor else ''
 return f'<section class="edition {name}"><div class="wrap"{anchor}>{content}</div></section>'

def headline(question, answer):
 return f'<header class="edition-head"><h2>{question}</h2><p class="short-answer">{answer}</p></header>'

def faq_entries(items):
 return ''.join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><div class="faq-answer"><p>{a}</p></div></details>' for i,(q,a) in enumerate(items))

main = agency_home(home_hero(CONSULT_LINK), asset, CONSULT_LINK, faq_entries)
why = brand_guide(CONSULT_LINK, asset, faq_entries)


def audit_opening():
 return f'''<div class="audit-hero"><section class="audit-opening front-cover" id="audit-start">
 <div class="wrap cover-layout"><div class="cover-copy"><h1>GEO-аудит <span>бренда</span></h1>
 <p class="short-answer">Мы покажем, где нейросети называют ваш бренд, с&nbsp;кем сравнивают и&nbsp;куда ведут ссылки. По&nbsp;отчёту вы поймёте, какие темы и&nbsp;страницы требуют внимания.</p>
 <div class="front-actions"><a class="btn primary" href="{CONSULT_LINK}" data-open-brief>Обсудить аудит <span aria-hidden="true">↗</span></a>
 <a class="front-link" href="#observations">Смотреть образец <span aria-hidden="true">↓</span></a></div>
 </div>{report_preview()}</div>
 <nav class="wrap audit-cover-index" aria-label="Разделы отчёта"><span>В&nbsp;отчёте</span>
 <a href="#observations">Видимость <span aria-hidden="true">↓</span></a>
 <a href="#tone">Тональность <span aria-hidden="true">↓</span></a>
 <a href="#sample">Источники <span aria-hidden="true">↓</span></a></nav>
 </section></div>'''


def audit_model_ribbon():
 # Widths are the native SVG proportions. Wordmarks include their lettering.
 models = (
  ('ChatGPT', 'chatgpt.svg', 24), ('Claude', 'claude-lockup.svg', 124),
  ('Grok', 'grok-lockup.svg', 89), ('Gemini', 'gemini-text.svg', 98),
  ('Алиса', 'alice-mono.svg', 24), ('GigaChat', 'gigachat.svg', 24),
 )
 items = []
 for name, filename, width in models:
  lettering = f'<span aria-hidden="true">{name}</span>' if width == 24 else ''
  items.append(f'<li><img src="{{PRE}}{asset("brands/" + filename)}" alt="{name}" width="{width}" height="24" style="--mark-width:{width}">{lettering}</li>')
 logos = ''.join(items)
 return f'''<section class="model-ribbon" id="neural-networks" aria-labelledby="audit-models-title">
 <div class="wrap model-ribbon-heading"><h2 id="audit-models-title">Какие нейросети входят в&nbsp;аудит?</h2>
 <p>Сопоставляем ответы по&nbsp;одним и&nbsp;тем же вопросам. В&nbsp;отчёте видно, где вывод повторяется и&nbsp;где зависит от&nbsp;платформы.</p></div>
 <div class="model-ribbon-window" role="group" aria-labelledby="audit-models-title" tabindex="0">
 <ul role="list">{logos}</ul><ul aria-hidden="true">{logos}</ul></div></section>'''


def metric_sheet():
 metrics=[
  ('Упоминание', 'Текст ответа', '«<mark>Компания</mark> выполняет выезды по&nbsp;выходным».',
   'Мы фиксируем, увидел ли покупатель название в&nbsp;ответе. Одного упоминания недостаточно, чтобы считать его рекомендацией.'),
  ('Источник', 'Список источников', '<span class="evidence-ref"><i aria-hidden="true">↗</i> Сайт компании</span>',
   'Мы отмечаем домен в&nbsp;источниках, даже если в&nbsp;ответе нейросеть назвала другую компанию.'),
  ('Прямая ссылка', 'Текст ответа', '«Уточните <span class="evidence-link">условия выезда ↗</span> перед заказом».',
   'Мы проверяем, на&nbsp;какую страницу ведёт ссылка. Покупателю проще принять решение, если там сразу видны условия.'),
 ]
 rows = ''.join(f'''<div class="measurement-item"><dt>{name}</dt><dd>
 <div class="metric-specimen"><span>{context}</span><p>{example}</p></div><p>{detail}</p></dd></div>'''
                for name, context, example, detail in metrics)
 return chapter('measurement-notes', headline('Как читать показатели?', 'Мы различаем три ситуации, даже когда они встречаются в&nbsp;одном ответе. Вот что в&nbsp;каждой увидит покупатель.')+
 f'<figure class="measurement-figure"><figcaption>Учебный пример</figcaption><dl class="measurement-index">{rows}</dl></figure>'+
 '<details class="source-book"><summary>Как считается доля ответов?</summary><p>Число замеров с&nbsp;признаком делим на&nbsp;все попытки в&nbsp;выбранной группе. Отказы и&nbsp;ошибки отмечаем отдельно. Один ответ может учитываться в&nbsp;нескольких показателях.</p></details>', 'results')


def competitor_sheet():
 rows = (
  ('Выезд в&nbsp;выходные', 'Есть', 'Есть'),
  ('Срочный заказ', 'Нет', 'Есть'),
  ('Договор обслуживания', 'Есть', 'Нет'),
 )
 body = ''.join(f'<tr><th scope="row">{topic}</th><td><span data-status="{brand}">{brand}</span></td>'
                f'<td><span data-status="{rival}">{rival}</span></td></tr>' for topic, brand, rival in rows)
 return chapter('rival-sheet', headline('Где покупатели встречают конкурентов?', 'Мы сопоставляем компании, которых нейросеть называет по&nbsp;конкретным задачам клиента. Так видно, по&nbsp;каким темам покупатель пока встречает только других поставщиков.')+f'''
 <figure class="rival-board"><figcaption>Учебный пример · кого назвали в&nbsp;ответе</figcaption>
 <table class="rival-table"><thead><tr><th scope="col">Тема вопроса</th><th scope="col">Бренд</th><th scope="col">Конкурент</th></tr></thead>
 <tbody>{body}</tbody></table>
 <p>В&nbsp;этом примере стоит начать со&nbsp;срочных заказов, если компания их принимает.</p></figure>
 <details class="source-book"><summary>Что ещё входит в&nbsp;сравнение?</summary>
 <p>Мы сравниваем долю упоминаний, порядок появления брендов и&nbsp;страницы в&nbsp;источниках. Отдельно отмечаем ответы, где нейросеть прямо советует компанию, и&nbsp;смотрим, повторяется ли вывод.</p></details>''', 'competitors')


def audit_decisions():
 rows = [
  ('Выбрать тему для продвижения', 'Упомянули только конкурента', 'Проверить страницу услуги',
   'Если компания берёт срочные заказы, проверяем, можно ли узнать об&nbsp;этом из&nbsp;карточки услуги. По&nbsp;выводам аудита вы сможете выбрать тему для продвижения.'),
  ('Уточнить сведения о&nbsp;продукте', 'Указали старые условия', 'Сверить источник и&nbsp;условия',
   'Сопоставляем фразу из&nbsp;ответа с&nbsp;текущим предложением. Если причина в&nbsp;старой информации, в&nbsp;отчёте видно, где она опубликована.'),
 ]
 items = ''.join(f'''<article><h3>{title}</h3>
 <ol class="decision-route"><li><span>В&nbsp;ответе</span>{finding}</li>
 <li><span>Действие</span>{action}</li></ol><p>{description}</p></article>'''
                 for title, finding, action, description in rows)
 return chapter('audit-focus', headline('Какие решения можно принять?', 'Связываем наблюдение с&nbsp;конкретной задачей. Вот как из&nbsp;ответа ассистента получается то, что можно поручить команде.')+
 f'<div class="audit-lenses">{items}</div>', 'audit-value')


def deliverables():
 rows = [
  ('Маркетингу', 'Карта спроса', (('Тема', 'Срочный выезд'), ('Вопрос', 'Кто приедет сегодня?'), ('Кого назвали', 'Конкурент')), 'По&nbsp;каждой теме соберём вопросы, частоту упоминаний и&nbsp;имена конкурентов. Вы увидите, в&nbsp;каких задачах покупателя ваш бренд уже заметен.'),
  ('Продукту и&nbsp;PR', 'Подборка ответов', (('Цитата', '«Выезд по&nbsp;выходным»'), ('Факт', 'График работы'), ('Источник', 'Карточка услуги')), 'Передадим фразы, в&nbsp;которых нейросеть объясняет выбор. Команда сможет сверить характеристики и&nbsp;условия с&nbsp;текущим предложением.'),
  ('Редакции и&nbsp;разработке', 'Задачи по&nbsp;страницам', (('Страница', 'Карточка услуги'), ('Наблюдение', 'Графика нет'), ('Задача', 'Добавить часы выезда')), 'Свяжем каждый приоритет с&nbsp;адресом страницы и&nbsp;примером ответа. После правки команда сможет вернуться к&nbsp;тому же вопросу.'),
 ]
 items = []
 for team, title, fields, detail in rows:
  specimen = ''.join(f'<div><dt>{label}</dt><dd>{value}</dd></div>' for label, value in fields)
  items.append(f'''<article><p class="delivery-team">{team}</p><h3>{title}</h3>
  <dl class="delivery-specimen">{specimen}</dl><p>{detail}</p></article>''')
 return chapter('report-delivery', headline('Что вы получите после аудита?', 'Мы передадим выводы для руководителя и&nbsp;приложение с&nbsp;данными для проверки. По&nbsp;учебным фрагментам видно, что получит каждая команда.')+
 f'<div class="delivery-list">{''.join(items)}</div>', 'report')


def audit_closing():
 return chapter('brief-stage audit-next', headline('С&nbsp;чего начать GEO-аудит?', 'Пришлите ссылку на&nbsp;сайт и&nbsp;укажите продукт или услугу. На&nbsp;консультации обсудим, что вам важно узнать о&nbsp;бренде и&nbsp;конкурентах.')+f'''
 <div class="audit-mail"><div class="mail-preview" aria-hidden="true">
 <span>Готовое письмо</span><b>Заявка на&nbsp;консультацию</b>
 <span>Сайт</span><span>Продукт или услуга</span></div>
 <a class="btn primary" href="{CONSULT_LINK}" data-open-brief>Записаться на консультацию <span aria-hidden="true">↗</span></a></div>''', 'brief')


auditfaq = [
 ('Можно ли увидеть реальные ответы из&nbsp;моего аудита?', 'Да. Мы передаём тексты ответов, ссылки, даты, названия моделей и&nbsp;статусы замеров. Команда сможет сверить выводы с&nbsp;первичными данными.'),
 ('Что покажут вопросы без названия компании?', 'Мы покажем, в&nbsp;каких ситуациях нейросеть назвала вас без подсказки. Вопросы с&nbsp;названием разбираем отдельно. По&nbsp;ним видно, как нейросеть описывает уже известную покупателю компанию.'),
 ('Аудит покажет продажи из&nbsp;нейросетей?', 'Для оценки продаж нужны данные веб-аналитики и&nbsp;CRM. По&nbsp;аудиту мы покажем, где нейросети называют бренд и&nbsp;по&nbsp;каким ссылкам покупатель может перейти на&nbsp;сайт.'),
 ('Можно использовать результат со&nbsp;своей командой?', 'Да. Мы связываем наблюдения с&nbsp;ответами и&nbsp;страницами. Редакция или разработчики смогут взять задачи в&nbsp;работу.'),
]
audit_questions = chapter('question-column audit-questions', headline('Что уточнить перед заказом аудита?', 'К&nbsp;выводам прилагаем материалы, по&nbsp;которым их можно перепроверить.')+'''
 <div class="audit-faq-evidence"><h3>Как проверить вывод</h3>
 <ol><li>Найти вопрос покупателя</li><li>Прочитать полный ответ</li><li>Открыть страницу источника</li></ol>
 <a class="front-link" href="#sample">Посмотреть пример <span aria-hidden="true">↗</span></a></div>
 <div class="question-list">'''+faq_entries(auditfaq)+'</div>', 'faq')
audit = '<div class="audit-edition">' + ''.join((
 audit_opening(), audit_model_ribbon(), observation_figure(asset('audit-workspace.webp')), tone_figure(), source_map(),
 metric_sheet(), competitor_sheet(), audit_decisions(), deliverables(), audit_questions, audit_closing(),
)) + '</div>'


def reading_layout(sections, label, count_named=True):
 links=[]
 sequence=0
 def assign_anchor(match):
  nonlocal sequence
  attrs,heading=match.groups()
  current=re.search(r' id="([^"]+)"',attrs)
  if not current or count_named:
   sequence += 1
  anchor=current.group(1) if current else f'part-{sequence}'
  links.append(f'<a href="#{anchor}">{heading}</a>')
  if not current: attrs+=f' id="{anchor}"'
  return f'<section{attrs}><h2>{heading}</h2>'
 sections=re.sub(r'<section\b([^>]*)>\s*<h2>([^<]+)</h2>',assign_anchor,sections)
 nav=f'<nav class="reading-index" aria-label="{label}"><strong>{label}</strong>'+''.join(links)+'</nav>'
 return '<div class="reading-edition"><div class="wrap reading-layout">'+nav+'<div class="reading-body">'+sections+'</div></div></div>'

def common_header(pre,current):
 nav=[('', 'Главная'), ('audit/', 'Аудит'), ('cases/', 'Кейсы'), ('why-geo/', 'Зачем GEO'), ('blog/', 'Блог')]
 links=[]
 for route,label in nav:
  href = pre+route if route else pre or './'
  in_section = route in ('cases/', 'blog/') and current.startswith(route)
  if route == 'blog/' and current == 'what-is-geo/':
   in_section = True
  selected = ' aria-current="page"' if current == route else ' aria-current="location"' if in_section else ''
  links.append(f'<a href="{href}"{selected}>{label}</a>')
 return f'''<a class="skip" href="#main">К содержанию</a><header class="site-header"><div class="wrap nav">
 <a class="logo" href="{pre or "./"}" aria-label="aileed — главная"><img class="wordmark-logo" src="{pre}{asset('aileed-logo.svg')}" width="170" height="46" alt="aileed"></a>
 <nav class="nav-links" id="navigation" aria-label="Основная навигация">{''.join(links)}</nav>
 <a class="btn nav-cta" href="{CONSULT_LINK}" data-open-brief><span class="desktop-label">Бесплатная консультация</span><span class="mobile-label">Консультация</span><span aria-hidden="true">↗</span></a>
 <button class="menu-toggle" aria-controls="navigation" aria-expanded="false" aria-label="Открыть меню"><span class="menu-bars" aria-hidden="true"></span></button></div></header>'''
def notice(pre):return '<aside id="cookie-banner" class="cookie-banner a-cookie" aria-labelledby="cookie-title" hidden><div><h2 id="cookie-title">Какие cookie используются?</h2><p class="short-answer">Только необходимые настройки. Аналитика не подключена.</p></div><a href="'+pre+'privacy.html#cookies">Подробнее</a><button type="button" class="btn" data-cookie-accept>Понятно</button></aside>'
def footer(pre,published,current):
 case_links = [('cases/','Все кейсы')]
 if current != 'audit/':
  case_links += [('cases/fashion/','Модный бренд под NDA'),('cases/winline/','WINLINE')]
 groups=[
  ('Услуги', [('','GEO-продвижение'),('audit/','GEO-аудит')]),
  ('Кейсы', case_links),
  ('О GEO', [('why-geo/','Зачем бренду GEO'),('what-is-geo/','Что такое GEO'),('blog/','Блог')]),
  ('Документы', [('privacy.html','Конфиденциальность'),('consent.html','Обработка данных')])]
 columns=[]
 for group,links in groups:
  items=''.join(f'<a href="{pre + route if route else pre or "./"}">{label}</a>' for route,label in links)
  if group=='Документы':items+='<button type="button" data-cookie-settings>Настройки cookie</button>'
  columns.append(f'<nav class="footer-group" aria-label="{group}"><strong>{group}</strong>{items}</nav>')
 return f'''<footer class="site-footer"><div class="wrap"><div class="footer-map">
 <a class="logo" href="{pre or "./"}"><img src="{pre}{asset('aileed-logo.svg')}" width="170" height="46" alt="aileed"></a>
 {''.join(columns)}</div>
 <div class="owner-line"><span>ИП Клепцын Егор Дмитриевич</span><span>ИНН 615490188400</span><span>ОГРНИП 326619600258881</span><a href="mailto:egorkl2307@gmail.com">egorkl2307@gmail.com</a></div>
 <div class="footer-bottom">© 2026 aileed · Опубликовано <time itemprop="datePublished" datetime="{published}">{pretty(published)}</time></div></div></footer>'''
def pretty(d):
 y,m,day=d.split('-');return str(int(day))+' '+{'10':'октября','11':'ноября'}[m]+' '+y
# The consultation opens a prepared email in the visitor’s own mail app.
dialog = (ROOT/'content/brief.html').read_text().strip().replace('{CONSULT_LINK}', CONSULT_LINK)
SOCIAL_IMAGES={
 'audit/':'social-audit.png',
 'cases/':'social-cases.jpg',
 'cases/fashion/':'social-fashion.jpg',
 'cases/winline/':'social-winline.jpg',
 'why-geo/':'social-why.jpg',
 'blog/':'social-geo.png',
 'what-is-geo/':'social-definition.jpg',
 'blog/mention-or-recommendation/':'social-mention.jpg',
 'blog/why-ai-recommends-competitors/':'social-competitors.jpg',
 'privacy.html':'social-privacy.jpg',
 'consent.html':'social-consent.jpg',
}
def write(route,title,desc,body,published,article=False,faqs=None):
 file=ROOT/(route+'index.html' if not route.endswith('.html') else route);pre='../'*route.count('/')
 if route.endswith('.html'):pre=''
 url=BASE+route
 modified = REVISED_PAGES.get(route, UPDATED)
 org={'@type':'Organization','@id':BASE+'#org','name':'aileed','description':'Агентство GEO-продвижения и аудита видимости брендов в нейросетях.','legalName':'ИП КЛЕПЦЫН ЕГОР ДМИТРИЕВИЧ','taxID':'615490188400','email':'egorkl2307@gmail.com','identifier':{'@type':'PropertyValue','propertyID':'ОГРНИП','value':'326619600258881'},'url':BASE,'logo':BASE+asset('aileed-logo.svg')}
 page={'@type':'WebPage','@id':url+'#page','url':url,'name':title,'description':desc,'inLanguage':'ru-RU','author':{'@id':BASE+'#org'},'publisher':{'@id':BASE+'#org'},'datePublished':published,'dateModified':modified,'isPartOf':{'@id':BASE+'#website'}}
 graph=[org,{'@type':'WebSite','@id':BASE+'#website','name':'aileed','url':BASE,'inLanguage':'ru-RU','publisher':{'@id':org['@id']}},page]
 social=SOCIAL_IMAGES.get(route,'social.png')
 headline=html.unescape(re.sub('<[^>]+>','',re.search('<h1>(.*?)</h1>',body,re.S).group(1)))
 if article:
  graph.append({'@type':'Article','@id':url+'#article','headline':headline,'description':desc,'mainEntityOfPage':{'@id':url+'#page'},'author':{'@id':BASE+'#org'},'publisher':{'@id':BASE+'#org'},'datePublished':published,'dateModified':modified,'image':BASE+asset(social),'inLanguage':'ru-RU'});page['mainEntity']={'@id':url+'#article'}
 if route in ('', 'audit/'):
  service = {'@type':'Service','@id':url+'#service','name':'GEO-аудит бренда' if route else 'GEO-продвижение брендов','provider':{'@id':org['@id']},'areaServed':{'@type':'Country','name':'Россия'},'url':url,'description':desc}
  graph.append(service)
  page['mainEntity'] = {'@id':service['@id']}
 collection = {'blog/':[post[0] for post in POSTS], 'cases/':[f'cases/{key}/' for key in PROJECTS]}
 if route in collection:
  page['hasPart'] = [{'@type':'WebPage','@id':BASE+path+'#page'} for path in collection[route]]
 if faqs:
  questions = [{'@type': 'Question', 'name': html.unescape(question),
                'acceptedAnswer': {'@type': 'Answer', 'text': html.unescape(answer)}}
               for question, answer in faqs]
  graph.append({'@type': 'FAQPage', '@id': url + '#faq', 'isPartOf': {'@id': url + '#page'}, 'mainEntity': questions})
 if route:
  label=re.sub(r' \| aileed$','',title)
  crumbs=[{'@type':'ListItem','position':1,'name':'aileed','item':BASE}]
  if route.startswith('blog/') and route!='blog/':crumbs.append({'@type':'ListItem','position':2,'name':'Блог','item':BASE+'blog/'})
  if route.startswith('cases/') and route!='cases/':crumbs.append({'@type':'ListItem','position':2,'name':'Кейсы','item':BASE+'cases/'})
  crumbs.append({'@type':'ListItem','position':len(crumbs)+1,'name':label,'item':url})
  graph.append({'@type':'BreadcrumbList','itemListElement':crumbs})

 structured=''.join('<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org',**node},ensure_ascii=False)+'</script>' for node in graph)
 styles = ['paper.css', 'interior.css' if route else 'agency.css']
 scripts = ['site.js', 'privacy.js']
 if not route:
  scripts.append('visibility-goal.js')
 if route.startswith('cases/'):
  styles.append('cases.css')
  if route != 'cases/':
   scripts.append('case-navigation.js')
 if route == 'why-geo/':
  styles.append('why-geo.css')
 if route == 'audit/':
  styles.extend(('agency.css', 'audit.css'))
  scripts.append('audit-reveal.js')
 stylesheets = ''.join(f'<link rel="stylesheet" href="{pre}{asset(name)}">' for name in styles)
 image_meta = ''.join(f'<meta property="og:image:{key}" content="{value}">' for key, value in (
  ('width', 1200), ('height', 630), ('alt', html.escape(headline)),
 ))
 head='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><meta name="description" content="'+html.escape(desc)+'"><meta name="author" content="aileed"><meta name="datePublished" content="'+published+'"><meta name="dateModified" content="'+modified+'"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#101113"><link rel="canonical" href="'+url+'"><link rel="describedby" type="text/plain" href="'+BASE+'llms.txt"><meta property="og:title" content="'+html.escape(title)+'"><meta property="og:description" content="'+html.escape(desc)+'"><meta property="og:url" content="'+url+'"><meta property="og:site_name" content="aileed"><meta property="og:locale" content="ru_RU"><meta property="og:type" content="'+('article' if article else 'website')+'"><meta property="og:image" content="'+BASE+asset(social)+'">'+image_meta+'<meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/svg+xml" href="'+pre+asset('mark.svg')+'">'+stylesheets+structured+''.join('<script src="'+pre+asset(f)+'" defer></script>' for f in scripts)+'</head>'
 content=head+'<body class="paper-site" itemscope itemtype="https://schema.org/WebPage" itemid="'+url+'#page">'+common_header(pre,route)+notice(pre)+'<main id="main">'+body.replace('{PRE}',pre)+'</main>'+footer(pre,published,route)+dialog.replace('href="privacy.html"','href="'+pre+'privacy.html"').replace('href="consent.html"','href="'+pre+'consent.html"')+'<noscript><p class="cookie-noscript">Аналитика и рекламные cookie не используются.</p></noscript></body></html>'
 # Fragment-only primary destinations belong to the current page.
 content=content.replace('href="'+pre+'#','href="#')
 file.parent.mkdir(parents=True,exist_ok=True);file.write_text("\n".join(line.rstrip() for line in content.replace("><",">\n<").splitlines())+"\n")
PAGES=[]
def page(route,title,desc,body,date,article=False,faqs=None):write(route,title,desc,body,date,article,faqs);PAGES.append((route,date))
page('','GEO-продвижение брендов в нейросетях | aileed','Продвигаем бренды в нейросетях. Работаем над упоминаниями, цитированием и ссылками в ответах о ваших товарах и услугах. Кейсы и бесплатный разбор.',main,'2026-10-07',faqs=home_faq)
page('audit/','GEO-аудит бренда в нейросетях | aileed','Проверим, как ChatGPT, Алиса и другие нейросети описывают ваш бренд, кого называют рядом и куда ведут ссылки. Посмотрите образец GEO-аудита и состав отчёта.',audit,'2026-11-02',faqs=auditfaq)
page('why-geo/','Зачем бренду GEO-продвижение? | aileed','Зачем бренду GEO-продвижение. Сравните два ответа нейросети на один вопрос покупателя и узнайте, как оценить упоминания, ссылки, переходы и обращения.',why,FIRST_EDITION,faqs=why_faq)
page('cases/','Кейсы GEO-продвижения и аудита | aileed','Результаты продвижения модного бренда под NDA и GEO-аудита WINLINE. Переходы из нейросетей, упоминания и цитирование.',case_index(asset),UPDATED)
case_links = f'''<div class="reading-end wrap"><div class="story-next">
 <a class="btn primary" href="{CONSULT_LINK}" data-open-brief>Обсудить свой проект ↗</a>
 <a class="edition-link" href="{{PRE}}cases/">Все кейсы →</a></div></div>'''
for key, project in PROJECTS.items():
 page(f'cases/{key}/', project['title']+' | aileed', project['lead'],
      case_article(key, asset)+case_links, UPDATED, article=True)
page('blog/','Блог о GEO и видимости в нейросетях | aileed','Блог aileed для владельцев бизнеса и маркетологов: GEO, рекомендации нейросетей, доверие и выбор бренда.',journal(),FIRST_EDITION)
for (route,title,answer,image,date),text in zip(POSTS,[geo_article(),mention_article(),competitor_article()]):
 cover=cover_art(image)
 hero_title={'mention':'Упоминание или рекомендация?', 'choice':'Почему ИИ советует конкурентов?', 'prism':'Что такое GEO?'}[image]
 body=f'''<article class="a-article"><header class="studio-article-head"><div class="wrap article-lead">
 <div><p class="entry-meta">{TOPICS[image]}</p><h1>{hero_title}</h1><p class="short-answer">{answer}</p>
 </div>
 <div class="editorial-object">{cover}</div></div></header>'''+reading_layout(text, 'В этой статье', count_named=False)+'''<div class="reading-end wrap"><div class="a-article-cta">
 <a class="btn primary" href="{PRE}audit/#observations">Посмотреть образец аудита <span aria-hidden="true">↗</span></a><a class="text-link" href="{PRE}blog/">Все статьи <span aria-hidden="true">→</span></a></div></div></article>'''
 page(route,title+' | aileed',answer,body,date,True)
# Preserve necessary legal information and the previously agreed contact status.
for name,date in [('privacy.html','2026-10-07'),('consent.html','2026-11-02')]:
 source=json.loads((ROOT/'content/legal.json').read_text())[name]
 body=source['body']
 title=source['title'];desc=source['description']
 interior=body.strip().removeprefix('<article class="wrap document-page">').removesuffix('</article>')
 lead,separator,sections=interior.partition('<section')
 if not separator: raise ValueError('Missing document sections: '+name)
 doc='<article class="studio-document"><header class="document-lead"><div class="wrap">'+lead+'</div></header>'+reading_layout(separator+sections,'На этой странице')+'</article>'
 page(name,title,desc,doc,date)

# Keep old bookmarks useful while removing the retired page from discovery.
(ROOT/'contacts.html').write_text(f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow"><link rel="canonical" href="{BASE}privacy.html"><meta http-equiv="refresh" content="0; url=privacy.html#operator"><title>Реквизиты aileed</title></head><body><a href="privacy.html#operator">Реквизиты владельца сайта</a></body></html>\n')
(ROOT/'platforms/index.html').write_text(f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow"><link rel="canonical" href="{BASE}why-geo/"><meta http-equiv="refresh" content="0; url=../why-geo/"><title>Зачем бренду GEO? | aileed</title></head><body><a href="../why-geo/">Зачем бренду GEO?</a></body></html>\n')

(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+escape(BASE+r)+'</loc><lastmod>'+REVISED_PAGES.get(r, UPDATED)+'</lastmod></url>' for r,d in PAGES)+'</urlset>\n')
(ROOT/'llms.txt').write_text('# aileed\n\n> GEO-продвижение и аудит брендов в ответах нейросетей.\n\n## Услуги\n- [GEO-продвижение]('+BASE+'): присутствие бренда в выборе клиента внутри AI-ответов.\n- [GEO-аудит]('+BASE+'audit/): AI-видимость, конкуренты и образ бренда.\n\n## Материалы\n- [Кейсы]('+BASE+'cases/): истории двух проектов.\n- [Кейс модного бренда]('+BASE+'cases/fashion/): более 10 000 переходов из нейросетей за полгода.\n- [Кейс WINLINE]('+BASE+'cases/winline/): 15 000 замеров и задачи по 119 страницам.\n- [Зачем бренду GEO]('+BASE+'why-geo/): бизнес-смысл и применимость.\n- [Что такое GEO]('+BASE+'what-is-geo/): определение и отличия от SEO/AEO.\n- [Блог]('+BASE+'blog/): выбор бренда и рекомендации нейросетей.\n- [Упоминание или рекомендация]('+BASE+'blog/mention-or-recommendation/): разница для бизнеса.\n- [Почему ИИ рекомендует конкурентов]('+BASE+'blog/why-ai-recommends-competitors/): как понимать такой ответ.\n\n## Контакты и данные\n- [Реквизиты владельца]('+BASE+'privacy.html#operator): информация об ИП и адрес электронной почты.\n- [Конфиденциальность]('+BASE+'privacy.html)\n- [Обработка данных]('+BASE+'consent.html)\n\nРекомендации сторонних платформ и рост выручки не гарантируются.\n')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+BASE+'sitemap.xml\n')
print('Rendered',len(PAGES),'pages for',BASE)
