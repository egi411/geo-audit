#!/usr/bin/env python3
"""Render aileed's static pages. Use --base-url only when the domain is ready."""
from pathlib import Path
import argparse,json,re,html,hashlib
from xml.sax.saxutils import escape
from visibility import observation_figure
from guide import brand_guide
from editorial import POSTS, TOPICS, cover_art, journal, geo_article, mention_article, competitor_article
from cases import PROJECTS, case_index, case_article
from home import FAQ as home_faq, agency_home
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--base-url',default='https://egi411.github.io/geo-audit/');args=ap.parse_args();BASE=args.base_url.rstrip('/')+'/'
FIRST_EDITION='2026-11-18'
UPDATED='2026-11-24'
def asset(name):
 p=ROOT/'assets'/name
 return 'assets/'+name+'?v='+hashlib.sha256(p.read_bytes()).hexdigest()[:12] if p.exists() else 'assets/'+name
CONSULT_EMAIL = "egorkl2307@gmail.com"
CONSULT_SUBJECT = "Заявка%20на%20бесплатную%20консультацию"
CONSULT_LINK = f"mailto:{CONSULT_EMAIL}?subject={CONSULT_SUBJECT}&amp;body=Здравствуйте!%20Хочу%20записаться%20на%20бесплатную%20консультацию."

def home_hero():
 return f'''<section class="home-hero market-hero"><div class="market-layout wrap" id="value">
 <div class="market-offer"><h1>Продвижение брендов в нейросетях</h1>
 <p class="short-answer">Помогаем покупателям находить вашу компанию в ответах нейросетей, когда они выбирают, у кого купить. На бесплатном разборе покажем, с чего начать продвижение вашего бренда.</p>
 <div class="actions"><a class="btn primary" href="{CONSULT_LINK}" data-open-brief>Бесплатный разбор ↗</a>
 <a class="text-link" href="{{PRE}}cases/">Наши кейсы →</a></div></div>
 <figure class="coverage-figure" id="business">
 <div class="coverage-dial"><div class="coverage-value"><strong>100<span>%</span></strong></div></div>
 <figcaption><strong>Наша цель по видимости бренда</strong>
 <p>Доля ответов, в которых нейросети называют ваш бренд по выбранным вопросам покупателей.</p></figcaption></figure>
 </div></section>'''


def chapter(name, content, anchor=''):
 anchor = f' id="{anchor}"' if anchor else ''
 return f'<section class="edition {name}"><div class="wrap"{anchor}>{content}</div></section>'

def headline(question, answer):
 return f'<header class="edition-head"><h2>{question}</h2><p class="short-answer">{answer}</p></header>'

def faq_entries(items):
 return ''.join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><div class="faq-answer"><p>{a}</p></div></details>' for i,(q,a) in enumerate(items))

def faq(items, heading='Что важно знать перед началом?', lead='Начните с продукта или услуги, по которым покупатель сравнивает вас с другими. Так будет понятно, какие ответы имеют значение для бизнеса.'):
 entries=faq_entries(items)
 intro = headline(heading,lead) if lead else f'<header class="edition-head"><h2>{heading}</h2></header>'
 return chapter('question-column',intro+'<div class="question-list">'+entries+'</div>','faq'),items

def closing(audit=False):
 question='С чего начать GEO-аудит?' if audit else 'С чего начать продвижение в ИИ?'
 return chapter('brief-stage',headline(question,'На бесплатной консультации покажем, какие вопросы о вашем продукте уже задают покупатели и где стоит начать продвижение.')+f'''
 <a class="action-pill" href="{CONSULT_LINK}" data-open-brief>Записаться на консультацию <span aria-hidden="true">↗</span></a>''','brief')

main = agency_home(home_hero(), asset, CONSULT_LINK, faq_entries)

# Detail pages.
why=brand_guide(CONSULT_LINK)
why_questions,whyfaq=faq([
 ('Когда имеет смысл вложиться в GEO?', 'Когда покупатели могут выбирать между несколькими компаниями и им важно разобраться в различиях до обращения. Если влияние нейросетей на выбор пока неизвестно, начните с разбора текущей видимости.'),
 ('Подойдёт ли GEO компании с известным именем?', 'Да. У известного бренда своя задача: проверить, как нейросети объясняют его предложение, какие ограничения упоминают и куда ведут за подробностями.'),
 ('Как понять, оправдан ли бюджет?', 'Согласуйте, какие темы важны для бизнеса, и зафиксируйте исходное положение. После публикаций сравните видимость по тем же вопросам. Для оценки коммерческого результата понадобятся данные о переходах, обращениях и сделках.')],
 'Перед решением о продвижении', '')
why+=why_questions+closing()
def audit_opening():
 return f'''<header class="audit-intro wrap"><h1>GEO-аудит бренда</h1>
 <div class="audit-offer"><p class="short-answer">Узнайте, что нейросети рассказывают покупателям о вашей компании и кого называют рядом с вами.</p>
 <p>В отчёте покажем, по каким вопросам виден ваш бренд, откуда нейросети берут сведения и какие страницы стоит обновить в первую очередь.</p>
 <div class="actions"><a class="btn primary" href="{CONSULT_LINK}" data-open-brief>Обсудить аудит ↗</a>
 <a class="text-link" href="#observations">Посмотреть образец отчёта ↓</a></div></div></header>'''


def metric_sheet():
 metrics=[
  ('text','Упоминание бренда','Название встречается в основном тексте.','Повтор названия в одном ответе засчитывается один раз. Название только в адресе или в подписи ссылки сюда не входит.'),
  ('sources','Сайт в источниках','Домен есть в списке источников ответа.','Несколько страниц одного сайта дают одно попадание за замер. Источник может остаться за пределами текста, который видит покупатель.'),
  ('url','URL в ответе','В тексте ответа есть прямая ссылка на страницу сайта.','Считается и ссылка под словом. В отчёте видно, куда попадёт покупатель по ссылке. Это может быть карточка продукта, обзор или главная страница.')]
 rows=''.join(f'<div><dt>{name}</dt><dd><strong>{definition}</strong><p>{detail}</p></dd></div>' for _,name,definition,detail in metrics)
 return chapter('measurement-notes',headline('Что считается попаданием в отчёт?','Для каждого ответа отдельно отмечаем название в тексте, сайт в списке источников и ссылку внутри ответа.')+f'<dl class="measurement-index">{rows}</dl>'+'''<details class="source-book"><summary>Как считается процент?</summary><p>Число замеров с признаком делим на все попытки в выбранной группе. Отказы и ошибки входят в знаменатель и отмечены отдельно. Один ответ может учитываться сразу в нескольких показателях.</p></details>''','results')

def answer_sample():
 samples=[
  ('name','Название','Для команды из пяти человек подойдёт <mark>Линия</mark>. В ней можно назначить ответственного за заявку.','Обзор сервисов поддержки · отраслевое издание','Есть','Нет','Нет','В тексте есть название сервиса. Чтобы открыть сайт, покупателю придётся найти его самому.'),
  ('source','Источник','Сравните, можно ли объединять обращения из почты и чата и назначать ответственного.','<mark>linea.example/help/inbox</mark> · документация сервиса','Нет','Есть','Нет','Нейросеть сослалась на инструкцию сервиса. Его название в ответе не прозвучало.'),
  ('link','Ссылка','У <mark>Линии</mark> есть общий ящик для команды. Откройте инструкцию на <mark>https://linea.example/help/inbox</mark>.','Список источников отсутствует в этом примере','Есть','Нет','Есть','Ссылка ведёт прямо к инструкции по настройке общего ящика.')]
 tabs=[];cards=[]
 for i,(key,label,line,refs,brand,src,url,conclusion) in enumerate(samples):
  tabs.append(f'<label><input type="radio" name="sample" value="{key}"'+(' checked' if i==0 else '')+f'><span>{label}</span></label>')
  flags=''.join(f'<div><dt>{name}</dt><dd class="flag-{"yes" if status=="Есть" else "no"}">{status}</dd></div>' for name,status in [('Имя в тексте',brand),('Сайт в источниках',src),('URL в ответе',url)])
  cards.append(f'''<div class="answer-variant" data-variant="{key}">
  <div class="sample-output"><span>Ответ нейросети</span><blockquote>{line}</blockquote>
  <p class="sample-source"><b>Источники</b> {refs}</p></div>
  <div class="sample-coding">
  <dl>{flags}</dl></div><p class="sample-result">{conclusion}</p></div>''')
 return f'''<section class="answer-lab wrap" id="sample">
 <header class="console-title"><div><h2>Что видно в одном ответе?</h2>
 <p class="short-answer">Три варианта ответа на один вопрос о сервисе «Линия». Выберите вкладку, чтобы увидеть, как ответ попадёт в отчёт.</p></div>
 <span class="demo-label">Учебный пример</span></header>
 <div id="sample-board" class="sample-board">
 <div class="sample-top"><div><span>Вопрос покупателя</span><b>Какой российский сервис соберёт почту и чат поддержки в одном окне?</b></div>
 <fieldset class="sample-choices"><legend>Вариант ответа</legend>{"".join(tabs)}</fieldset></div>
 <div class="sample-variants">{"".join(cards)}</div></div>
 <p class="sample-note">«Линия» в этом примере вымышлена.</p></section>'''

def competitor_sheet():
 rows=[
  ('Доля голоса','Какую часть всех появлений брендов из списка сравнения занимает ваша компания. Каждый бренд учитывается один раз за ответ.','Кто чаще других попадает в поле зрения покупателя.'),
  ('Первое место и топ-3','Как часто название встречается первым или среди первых трёх. Среднюю позицию считаем среди ответов, где бренд назван.','Кого клиент видит раньше. Порядок имён сам по себе не доказывает рекомендацию.'),
  ('Конкурент без вас','По каким вопросам другой бренд появляется, когда вашего нет. Для сайтов так же сравниваем конкретные URL и их порядок в источниках.','По каким темам покупатель видит только конкурента и его страницы.'),
  ('Повторяемость','В скольких повторах и на каких платформах воспроизводится наблюдение. Ответы на вопросы с названием бренда и без подсказки показываем раздельно.','Какие результаты подтвердились при повторной проверке.')]
 body=''.join(f'<tr><th scope="row">{key}</th><td>{rule}</td><td>{why}</td></tr>' for key,rule,why in rows)
 return chapter('rival-sheet',headline('В чём вас опережают конкуренты?','Вы увидите соперников по каждому вопросу и платформе. Даже при одинаковой частоте упоминаний порядок брендов и ссылки могут отличаться.')+
 '<table class="rival-table"><thead><tr><th>Показатель</th><th>Что входит в сравнение</th><th>Что это даёт бизнесу</th></tr></thead><tbody>'+body+'</tbody></table>','competitors')

def deliverables():
 rows=[
 ('Маркетингу','Карта спроса','По каждой теме вы получите вопрос покупателя, частоту упоминаний, имена конкурентов и ссылки на источники. Можно сразу увидеть темы, в которых ваш бренд пока не встречается.'),
 ('Продукту и PR','Что говорят о продукте','Фрагменты ответов с характеристиками продукта и причинами, по которым нейросеть предлагает его или исключает из выбора. Команда сможет сверить спорное утверждение с условиями, которые предлагает клиентам сейчас.'),
 ('Редакции и разработке','Приоритеты по страницам','Для конкретного URL собраны наблюдение, подтверждающий пример и задача по содержанию или доступности страницы. Команда может вернуться к тому же вопросу после изменений.')]
 return chapter('report-delivery',headline('Что команда получит на руки?','Вы получите отчёт для руководителя и рабочую таблицу для команды. У каждого вывода есть исходный ответ, у каждой задачи — страница, с которой можно начать.')+
 '<div class="delivery-list">'+''.join(f'<div><span>{team}</span><strong>{name}</strong><p>{desc}</p></div>' for team,name,desc in rows)+'</div>','report')

audit_focus = chapter('audit-focus', '''<header><h2>Что аудит даст вашему бизнесу</h2>
 <p>Отчёт показывает, по каким запросам покупатель встречает вашу компанию и что именно узнаёт о ней. Эти выводы помогают выбрать темы для продвижения и исправить ошибки в описании продукта.</p></header>
 <div class="audit-lenses"><article><h3>Положение среди конкурентов</h3><p>По каким темам вас видят рядом с другими компаниями? Где нейросети называют только конкурента? Отчёт показывает разницу по продуктам и отделяет поиск решения от вопросов об уже знакомом бренде.</p></article>
 <article><h3>Образ бренда</h3><p>Какие достоинства, недостатки и условия описывают нейросети? Сверяем эти утверждения с вашим предложением. Вы увидите, где сведения расходятся и к какому источнику отсылает ответ.</p></article></div>''', 'audit-value')
audit='<div class="audit-edition">'+audit_opening()+observation_figure(asset('audit-workspace.webp'))+audit_focus+answer_sample()+metric_sheet()+competitor_sheet()+deliverables()
x,auditfaq=faq([('Можно ли увидеть реальные ответы из моего аудита?','Да. В приложении доступны тексты, ссылки, даты, модели и статусы замеров. По ним команда может проверить выводы отчёта.'),('Что покажут вопросы без названия компании?','В каких ситуациях ИИ назвал бренд без подсказки. Вопросы с названием мы разбираем отдельно. По ним видно, как ИИ описывает уже известную покупателю компанию.'),('Аудит покажет продажи из ИИ?','Для выводов о продажах нужны данные аналитики и CRM. Аудит показывает содержание ответов, упоминания и ссылки в пределах исследованной выборки.'),('Можно использовать результат со своей командой?','Да. Таблица связывает наблюдения с вопросами и страницами. Редакция или разработчики могут взять задачи в работу.')], 'Вопросы о GEO-аудите', '')
audit+='<aside class="audit-projects wrap"><a href="{PRE}cases/">Посмотрите кейсы <span aria-hidden="true">→</span></a></aside>'
audit+=x+closing(True)+'</div>'

def reading_layout(sections,label):
 links=[]
 def assign_anchor(match):
  attrs,heading=match.groups()
  current=re.search(r' id="([^"]+)"',attrs)
  anchor=current.group(1) if current else 'part-'+str(len(links)+1)
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
  href = pre+(route or 'index.html')
  selected = ' aria-current="page"' if current==route else (' aria-current="location"' if route=='cases/' and current.startswith(route) else '')
  links.append(f'<a href="{href}"{selected}>{label}</a>')
 return f'''<a class="skip" href="#main">К содержанию</a><header class="site-header"><div class="wrap nav">
 <a class="logo" href="{pre}index.html" aria-label="aileed — главная"><img class="wordmark-logo" src="{pre}{asset('aileed-logo.svg')}" width="170" height="46" alt="aileed"></a>
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
  items=''.join(f'<a href="{pre}{route or "index.html"}">{label}</a>' for route,label in links)
  if group=='Документы':items+='<button type="button" data-cookie-settings>Настройки cookie</button>'
  columns.append(f'<nav class="footer-group" aria-label="{group}"><strong>{group}</strong>{items}</nav>')
 return f'''<footer class="site-footer"><div class="wrap"><div class="footer-map">
 <a class="logo" href="{pre}index.html"><img src="{pre}{asset('aileed-logo.svg')}" width="170" height="46" alt="aileed"></a>
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
 org={'@type':'Organization','@id':BASE+'#org','name':'aileed','legalName':'ИП КЛЕПЦЫН ЕГОР ДМИТРИЕВИЧ','taxID':'615490188400','email':'egorkl2307@gmail.com','identifier':{'@type':'PropertyValue','propertyID':'ОГРНИП','value':'326619600258881'},'url':BASE,'logo':BASE+asset('aileed-logo.svg')}
 page={'@type':'WebPage','@id':url+'#page','url':url,'name':title,'description':desc,'inLanguage':'ru-RU','author':{'@id':BASE+'#org'},'publisher':{'@id':BASE+'#org'},'datePublished':published,'dateModified':UPDATED,'isPartOf':{'@id':BASE+'#website'}}
 graph=[org,{'@type':'WebSite','@id':BASE+'#website','name':'aileed','url':BASE},page]
 social=SOCIAL_IMAGES.get(route,'social.png')
 if article:
  headline=re.sub('<[^>]+>','',re.search('<h1>(.*?)</h1>',body,re.S).group(1))
  graph.append({'@type':'Article','@id':url+'#article','headline':headline,'mainEntityOfPage':{'@id':url+'#page'},'author':{'@id':BASE+'#org'},'publisher':{'@id':BASE+'#org'},'datePublished':published,'dateModified':UPDATED,'image':BASE+asset(social),'inLanguage':'ru-RU'});page['mainEntity']={'@id':url+'#article'}
 if route in ['','audit/']:graph.append({'@type':'Service','name':('GEO-аудит' if route=='audit/' else 'GEO-продвижение'),'provider':{'@id':BASE+'#org'},'url':url,'description':desc})
 if faqs:graph.append({'@type':'FAQPage','@id':url+'#faq','isPartOf':{'@id':url+'#page'},'mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faqs]})
 if route:
  label=re.sub(r' \| aileed$','',title)
  crumbs=[{'@type':'ListItem','position':1,'name':'aileed','item':BASE}]
  if route.startswith('blog/') and route!='blog/':crumbs.append({'@type':'ListItem','position':2,'name':'Блог','item':BASE+'blog/'})
  if route.startswith('cases/') and route!='cases/':crumbs.append({'@type':'ListItem','position':2,'name':'Кейсы','item':BASE+'cases/'})
  crumbs.append({'@type':'ListItem','position':len(crumbs)+1,'name':label,'item':url})
  graph.append({'@type':'BreadcrumbList','itemListElement':crumbs})

 structured=''.join('<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org',**node},ensure_ascii=False)+'</script>' for node in graph)
 section_styles = '<link rel="stylesheet" href="'+pre+asset('interior.css' if route else 'agency.css')+'">'
 scripts = ['site.js','privacy.js','dashboard.js']
 if route == 'audit/':
  section_styles += '<link rel="stylesheet" href="'+pre+asset('audit.css')+'">'
  scripts.append('audit-reveal.js')
 head='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><meta name="description" content="'+html.escape(desc)+'"><meta name="author" content="aileed"><meta name="datePublished" content="'+published+'"><meta name="dateModified" content="'+UPDATED+'"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#101113"><link rel="canonical" href="'+url+'"><link rel="describedby" type="text/plain" href="'+BASE+'llms.txt"><meta property="og:title" content="'+html.escape(title)+'"><meta property="og:description" content="'+html.escape(desc)+'"><meta property="og:url" content="'+url+'"><meta property="og:site_name" content="aileed"><meta property="og:locale" content="ru_RU"><meta property="og:type" content="'+('article' if article else 'website')+'"><meta property="og:image" content="'+BASE+asset(social)+'"><meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/svg+xml" href="'+pre+asset('mark.svg')+'"><link rel="stylesheet" href="'+pre+asset('paper.css')+'">'+section_styles+structured+''.join('<script src="'+pre+asset(f)+'" defer></script>' for f in scripts)+'</head>'
 content=head+'<body class="paper-site" itemscope itemtype="https://schema.org/WebPage" itemid="'+url+'#page">'+common_header(pre,route)+notice(pre)+'<main id="main">'+body.replace('{PRE}',pre)+'</main>'+footer(pre,published,route)+dialog.replace('href="privacy.html"','href="'+pre+'privacy.html"').replace('href="consent.html"','href="'+pre+'consent.html"')+'<noscript><p class="cookie-noscript">Аналитика и рекламные cookie не используются.</p></noscript></body></html>'
 # Fragment-only primary destinations belong to the current page.
 content=content.replace('href="'+pre+'#','href="#')
 file.parent.mkdir(parents=True,exist_ok=True);file.write_text("\n".join(line.rstrip() for line in content.replace("><",">\n<").splitlines())+"\n")
PAGES=[]
def page(route,title,desc,body,date,article=False,faqs=None):write(route,title,desc,body,date,article,faqs);PAGES.append((route,date))
page('','Продвижение в нейросетях для бизнеса в России | aileed','GEO-продвижение для российских компаний. Помогаем покупателям находить ваши товары и услуги в нейросетях. Запишитесь на бесплатную консультацию.',main,'2026-10-07',faqs=home_faq)
page('audit/','Что измеряет GEO-аудит бренда в нейросетях? | aileed','GEO-аудит бренда в нейросетях. Упоминания, сайт в источниках, URL в ответах, доля голоса и место среди конкурентов. Посмотрите пример и состав отчёта.',audit,'2026-11-02',faqs=auditfaq)
page('why-geo/','Зачем бренду GEO-продвижение? | aileed','Когда покупатели ищут, сравнивают и выбирают бренды в нейросетях. Как оценить пользу GEO для бизнеса и выбрать первое направление продвижения.',why,FIRST_EDITION,faqs=whyfaq)
page('cases/','Что GEO дало бизнесу? Кейсы продвижения и аудита | aileed','Результаты продвижения модного бренда под NDA и GEO-аудита WINLINE. Переходы из нейросетей, упоминания и цитирование.',case_index(asset),UPDATED)
case_links = f'''<div class="reading-end wrap"><div class="story-next">
 <a class="btn primary" href="{CONSULT_LINK}" data-open-brief>Обсудить свой проект ↗</a>
 <a class="edition-link" href="{{PRE}}cases/">Все кейсы →</a></div></div>'''
for key, project in PROJECTS.items():
 page(f'cases/{key}/', project['title']+' | aileed', project['lead'],
      case_article(key, asset)+case_links, UPDATED, article=True)
page('blog/','Что важно знать о GEO и AI-видимости? Блог | aileed','Блог aileed для владельцев бизнеса и маркетологов: GEO, рекомендации нейросетей, доверие и выбор бренда.',journal(),FIRST_EDITION)
for (route,title,answer,image,date),text in zip(POSTS,[geo_article(),mention_article(),competitor_article()]):
 cover=cover_art(image)
 hero_title={'mention':'Упоминание или совет?', 'choice':'Почему ИИ назвал конкурента?', 'prism':'Что такое GEO?'}[image]
 body=f'''<article class="a-article"><header class="studio-article-head"><div class="wrap article-lead">
 <div><p class="entry-meta">{TOPICS[image]}</p><h1>{hero_title}</h1><p class="short-answer">{answer}</p>
 </div>
 <div class="editorial-object">{cover}</div></div></header>'''+reading_layout(text,'В этой статье')+'''<div class="reading-end wrap"><div class="a-article-cta">
 <a class="btn" href="{PRE}audit/">Об услуге GEO-аудита <span aria-hidden="true">↗</span></a><a class="text-link" href="{PRE}blog/">Весь блог <span aria-hidden="true">→</span></a></div></div></article>'''
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

(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+escape(BASE+r)+'</loc><lastmod>'+UPDATED+'</lastmod></url>' for r,d in PAGES)+'</urlset>\n')
(ROOT/'llms.txt').write_text('# aileed\n\n> GEO-продвижение и аудит брендов в ответах нейросетей.\n\n## Услуги\n- [GEO-продвижение]('+BASE+'): присутствие бренда в выборе клиента внутри AI-ответов.\n- [GEO-аудит]('+BASE+'audit/): AI-видимость, конкуренты и образ бренда.\n\n## Материалы\n- [Кейсы]('+BASE+'cases/): истории двух проектов.\n- [Кейс модного бренда]('+BASE+'cases/fashion/): более 10 000 переходов из нейросетей за полгода.\n- [Кейс WINLINE]('+BASE+'cases/winline/): 15 000 замеров и задачи по 119 страницам.\n- [Зачем бренду GEO]('+BASE+'why-geo/): бизнес-смысл и применимость.\n- [Что такое GEO]('+BASE+'what-is-geo/): определение и отличия от SEO/AEO.\n- [Блог]('+BASE+'blog/): выбор бренда и рекомендации нейросетей.\n- [Упоминание или рекомендация]('+BASE+'blog/mention-or-recommendation/): разница для бизнеса.\n- [Почему ИИ рекомендует конкурентов]('+BASE+'blog/why-ai-recommends-competitors/): как понимать такой ответ.\n\n## Контакты и данные\n- [Реквизиты владельца]('+BASE+'privacy.html#operator): информация об ИП и адрес электронной почты.\n- [Конфиденциальность]('+BASE+'privacy.html)\n- [Обработка данных]('+BASE+'consent.html)\n\nРекомендации сторонних платформ и рост выручки не гарантируются.\n')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+BASE+'sitemap.xml\n')
print('Rendered',len(PAGES),'pages for',BASE)
