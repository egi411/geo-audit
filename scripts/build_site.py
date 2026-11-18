#!/usr/bin/env python3
"""Render aileed's static pages. Use --base-url only when the domain is ready."""
from pathlib import Path
import argparse,json,re,html,hashlib
from xml.sax.saxutils import escape
from visibility import frequency_figure, observation_figure, overview
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--base-url',default='https://egi411.github.io/geo-audit/');args=ap.parse_args();BASE=args.base_url.rstrip('/')+'/';TODAY='2026-11-18'
def asset(name):
 p=ROOT/'assets'/name
 return 'assets/'+name+'?v='+hashlib.sha256(p.read_bytes()).hexdigest()[:12] if p.exists() else 'assets/'+name
def img(src,alt,cls='',eager=False):
 decorative=' aria-hidden="true"' if src.startswith('brands/') else ''
 return f'<img class="{cls}" src="{{PRE}}{asset(src)}" alt="{html.escape(alt)}"{decorative} width="1000" height="1000" '+('fetchpriority="high"' if eager else 'loading="lazy"')+' decoding="async" />'
def hero(h,a,p,profile,alt,primary,secondary=('Зачем бренду GEO','why-geo/')):
 product=asset('studio-'+profile+'.webp')
 if profile=='shortlist':
  art='<div class="shortlist-model" role="img" aria-label="Три карточки предложений. Карточка с отметкой выходит вперёд."><div class="shortlist-tray"><i class="offer-plate rear"></i><i class="offer-plate middle"></i><i class="offer-plate front"><span aria-hidden="true"></span><b aria-hidden="true">✓</b></i></div></div>'
 else:
  art=f'<div class="quote-objects studio-object"><img class="quote-body" data-profile="{profile}" src="{{PRE}}{product}" width="724" height="724" alt="{alt}" fetchpriority="high"><canvas class="quote-canvas" aria-hidden="true"></canvas></div>'
 stage_attr=' data-quote-stage' if profile!='shortlist' else ''
 return f'''<section class="studio-hero studio-{profile}"{stage_attr}>
   <div class="wrap studio-hero-layout"><div class="studio-intro">
   <h1>{h}</h1><p class="short-answer">{a}</p><p class="a-lead">{p}</p>
   <div class="actions"><a class="btn primary" href="{{PRE}}{primary[1]}">{primary[0]} <span aria-hidden="true">↗</span></a>
   <a class="text-link" href="{{PRE}}{secondary[1]}">{secondary[0]} <span aria-hidden="true">→</span></a></div></div>
   <div class="studio-showcase"><div class="studio-floor" aria-hidden="true"></div>
   {art}</div></div>
 </section>'''

def quote_stage():
 horizon=asset('optical-horizon.webp')
 horizon_small=asset('optical-horizon-small.webp')
 return f"""<section class="quote-stage" data-quote-stage>
   <picture class="quote-horizon" aria-hidden="true">
     <source media="(max-width: 650px)" srcset="{{PRE}}{horizon_small}">
     <img src="{{PRE}}{horizon}" width="1600" height="593" alt="Световая дуга за сценой" fetchpriority="high">
   </picture>
   <div class="quote-falloff" aria-hidden="true"></div>
   <div class="quote-objects" aria-hidden="true">
     <img data-profile="metal" class="quote-body quote-metal" src="{{PRE}}{asset('quote-metal.webp')}" width="640" height="766" alt="Кавычка из шлифованного металла">
     <img data-profile="glass" class="quote-body quote-glass" src="{{PRE}}{asset('quote-glass.webp')}" width="640" height="766" alt="Кавычка из дымчатого стекла">
     <canvas class="quote-canvas"></canvas>
   </div>
   <div class="quote-copy wrap">
     <h1>Как стать брендом, который <span>рекомендуют нейросети?</span></h1>
     <p class="short-answer">GEO-продвижение помогает вашему бренду попасть в список компаний, которые покупатель рассматривает по совету ChatGPT или Алисы.</p>
     <div class="actions"><a class="btn primary" href="{{PRE}}audit/">Проверить упоминания <span aria-hidden="true">↗</span></a>
     <a class="text-link" href="{{PRE}}why-geo/">Зачем бренду GEO <span aria-hidden="true">→</span></a></div>
   </div>

 </section>"""
def chapter(name, content, anchor=''):
 anchor = f' id="{anchor}"' if anchor else ''
 return f'<section class="edition {name}"><div class="wrap"{anchor}>{content}</div></section>'

def headline(question, answer):
 return f'<header class="edition-head"><h2>{question}</h2><p class="short-answer">{answer}</p></header>'

def arrow_link(route, label):
 return f'<a class="edition-link" href="{{PRE}}{route}">{label} <span aria-hidden="true">↗</span></a>'

def scene_image(name, alt, sizes):
 return f'''<img class="scene-image" src="{{PRE}}{asset(name+"-small.webp")}"
 srcset="{{PRE}}{asset(name+"-small.webp")} 720w, {{PRE}}{asset(name+".webp")} 1440w"
 sizes="{sizes}" width="1440" height="960" alt="{alt}" loading="lazy" decoding="async">'''

def faq(items):
 entries=''.join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i,(q,a) in enumerate(items))
 return chapter('question-column',headline('Что важно знать перед началом?','Начните с продукта или услуги, по которым покупатель сравнивает вас с другими. Так будет понятно, какие ответы имеют значение для бизнеса.')+'<div class="question-list">'+entries+'</div>','faq'),items

def closing(audit=False):
 question='С чего начать GEO-аудит?' if audit else 'С чего начать продвижение в ИИ?'
 return chapter('brief-stage',headline(question,'Опишите ваш продукт и тех, кто его выбирает. Бриф можно сохранить в TXT и обсудить с командой.')+'''
 <button class="action-pill" type="button" data-open-brief>Составить бриф <span aria-hidden="true">↗</span></button>''','brief')

def services(question, answer):
 options=[
  ('audit/','GEO-аудит','Узнайте, в каких ответах появляется ваш бренд, что о нём говорят и кого предлагают рядом.','report','Стеклянные листы отчёта о видимости бренда','Что входит в аудит'),
  ('why-geo/#investment','GEO-продвижение','Покупатель спрашивает про сроки, совместимость или условия. Дайте ему повод включить ваш продукт в список и посмотреть предложение.','answer-display','Объёмная реплика из стекла над экраном смартфона','Когда нужно продвижение')]
 items=[]
 for route,name,reason,image,alt,link in options:
  if image=='report':
   art=f'''<div class="dossier-art"><img src="{{PRE}}{asset("object-sources.webp")}" class="dossier-sheets" width="512" height="512" alt="{alt}" loading="lazy">
   <div class="dossier-fields" aria-hidden="true"><span>В отчёте</span><b>Упоминания</b><b>Источники</b><b>Ссылки</b></div></div>'''
  else:
   art=scene_image(image,alt,'(max-width: 700px) 96vw, (max-width: 1200px) 51vw, 660px')
  items.append(f'<a class="service-tile" href="{{PRE}}{route}"><div class="product-shot" data-scene>{art}</div><div class="service-description"><strong>{name}</strong><p>{reason}</p><span class="tile-action">{link} <span aria-hidden="true">↗</span></span></div></a>')
 return chapter('service-gallery',headline(question,answer)+'<div class="service-pair">'+''.join(items)+'</div>','offers')

def buyer_scenarios():
 examples=[
  ('b2b','Услуги для бизнеса','Кто спроектирует освещение для небольшого отеля?','Заказчику важно увидеть бюро с опытом в гостиницах. Так он решает, у кого запросить портфолио.','scene-hotel','Архитектурный макет отеля с подсветкой фасада и гостевых комнат'),
  ('retail','Товары','Какую кофемолку выбрать для эспрессо на маленькой кухне?','Покупатель ищет подходящую модель. Размер корпуса и качество помола для него важнее известности марки.','scene-grinder','Компактная металлическая кофемолка для эспрессо на кухонной столешнице'),
  ('saas','SaaS','Какой сервис записи подойдёт двум салонам с общей базой клиентов?','Владельцу нужны два расписания и одна клиентская база. Если в ответе есть только цена подписки, ему придётся искать информацию о филиалах отдельно.','scene-booking','Планшет с расписанием приёмов на стойке салона')]
 choices=[]; panels=[]
 for i,(key,label,prompt,comment,photo,alt) in enumerate(examples):
  choices.append(f'<label><input type="radio" name="buyer" value="{key}"'+(' checked' if i==0 else '')+f'><span>{label}</span></label>')
  art=scene_image(photo,alt,'(max-width: 700px) 100vw, (max-width: 1400px) 82vw, 1200px')
  panels.append(f'<figure class="buyer-example" data-buyer="{key}"><div class="buyer-photo" data-scene>{art}</div><figcaption><span class="prompt-label">Пример запроса</span><blockquote>{prompt}</blockquote><p>{comment}</p></figcaption></figure>')
 return chapter('buyer-stage',headline('Как покупатель выбирает бренд в ИИ?','Покупатель описывает задачу своими словами. Для отеля, магазина и онлайн-сервиса короткий список выглядит по-разному.')+'<div class="scenario-view" id="business"><fieldset class="buyer-controls"><legend>Сфера бизнеса</legend>'+''.join(choices)+'</fieldset><div class="buyer-examples">'+''.join(panels)+'</div></div>','value')

main=quote_stage()+buyer_scenarios()
main+=overview()
main+=services('Аудит или продвижение?','Аудит покажет, что покупатели видят сейчас. Продвижение помогает бренду появляться в ответах о тех товарах и услугах, которые он продаёт.')
commonfaq=[('Можно гарантировать рекомендацию нейросети?','Нет. Даже один покупатель может получить другой список, когда уточнит город, бюджет или требования к продукту.'),('GEO заменяет SEO?','Нет. SEO помогает покупателю найти вашу страницу через поиск. GEO помогает ему встретить ваш бренд, когда он просит нейросеть сравнить варианты.'),('Упоминание бренда уже означает продажу?','Покупатель может увидеть знакомое название и уйти к конкуренту. Продажу подтверждает сделка, а связь с рекомендацией помогают проверить переходы и обращения.'),('Можно начать с отдельного аудита?','Да. Вы получите отчёт и сможете передать его своей команде. Продвижение можно обсудить отдельно.')]
home_questions,mainfaq=faq(commonfaq)
# Detail pages.
why=hero('Зачем бренду <span>GEO?</span>','Чтобы покупатель учитывал вашу компанию, когда спрашивает у нейросети, к кому обратиться или что купить.','Если нейросеть назвала двух конкурентов, именно их предложения клиент может открыть первыми. Стоит узнать, попадаете ли вы в этот список и что о вас говорят.','shortlist','Стеклянная карточка выделена среди двух металлических альтернатив',('Посмотреть пример аудита','audit/#sample-board'),('Упоминания и цитирования','#visibility'))
why+=frequency_figure()
why+=chapter('investment-feature',f"""
 <div class="investment-spread" id="investment">{scene_image('scene-hotel','Модель гостиницы с подсвеченными окнами и фасадом','(max-width: 700px) 95vw, 80vw')}
 <div class="investment-copy"><h2>Когда GEO стоит вложений?</h2>
 <p class="short-answer">Когда вас сравнивают до первого звонка.</p>
 <p>Владелец отеля спрашивает, кому заказать освещение фасада. В ответе два бюро. Оба делают свет, но только у одного есть ссылка на готовую гостиницу. Именно этот проект заказчик может переслать архитектору.</p>
 <p>Если клиенты уже приходят с таким списком, начните с одного вопроса из переговоров. Посмотрите, кого назвали и чей проект привели в пример.</p>
 {arrow_link('audit/#sample-board','Разобрать пример ответа')}</div></div>""")
why+=closing()
def audit_opening():
 return """<header class="audit-opening wrap"><h1>Называет ли ИИ <span>ваш бренд?</span></h1>
 <p class="short-answer">GEO-аудит покажет, где вас упоминают, кому достаются ссылки и какие конкуренты появляются в ответах вместо вас.</p>
 <div class="actions"><a class="btn primary" href="#sample-board">Разобрать пример <span aria-hidden="true">↓</span></a>
 <a class="text-link" href="#results">Посмотреть метрики <span aria-hidden="true">↗</span></a></div></header>"""

def metric_sheet():
 metrics=[
  ('text','Упоминание бренда','Название встречается в основном тексте.','Повтор названия в одном ответе засчитывается один раз. Название только в адресе или в подписи ссылки сюда не входит.'),
  ('sources','Сайт в источниках','Домен есть в списке источников ответа.','Несколько страниц одного сайта дают одно попадание за замер. Источник может остаться за пределами текста, который видит покупатель.'),
  ('url','URL в ответе','Полный адрес сайта встроен в сам ответ.','Считается и ссылка под словом. В отчёте видно, куда попадёт покупатель по ссылке. Это может быть карточка продукта, обзор или главная страница.')]
 rows=''.join(f'<div><dt>{name}</dt><dd><strong>{definition}</strong><p>{detail}</p></dd></div>' for _,name,definition,detail in metrics)
 return chapter('measurement-notes',headline('Что считается попаданием в отчёт?','Для каждого ответа отдельно отмечаем название в тексте, сайт в списке источников и ссылку внутри ответа.')+f'<dl class="measurement-index">{rows}</dl>'+'''<details class="source-book"><summary>Как считается процент?</summary><p>Число замеров с признаком делим на все попытки в выбранной группе. Отказы и ошибки входят в знаменатель и отмечены отдельно. Один ответ может учитываться сразу в нескольких показателях.</p></details>''','results')

def answer_sample():
 samples=[
  ('name','Название','Для команды из пяти человек подойдёт <mark>Линия</mark>. В ней можно назначить ответственного за заявку.','Обзор сервисов поддержки · отраслевое издание','Есть','Нет','Нет','Покупатель узнал название. Адрес сайта ему придётся искать отдельно.'),
  ('source','Источник','Сравните, можно ли объединять обращения из почты и чата и назначать ответственного.','<mark>linea.example/help/inbox</mark> · документация сервиса','Нет','Есть','Нет','Страница продукта попала в источники. В тексте ответа покупатель увидел только критерии выбора.'),
  ('link','Ссылка','У <mark>Линии</mark> есть общий ящик для команды. Инструкция по настройке — <mark>https://linea.example/help/inbox</mark>.','Список источников отсутствует в этом примере','Есть','Нет','Есть','У покупателя есть путь к конкретной инструкции. Фактический переход проверяют отдельно в аналитике сайта.')]
 tabs=[];cards=[]
 for i,(key,label,line,refs,brand,src,url,conclusion) in enumerate(samples):
  tabs.append(f'<label><input type="radio" name="sample" value="{key}"'+(' checked' if i==0 else '')+f'><span>{label}</span></label>')
  flags=''.join(f'<div><dt>{name}</dt><dd class="flag-{"yes" if status=="Есть" else "no"}">{status}</dd></div>' for name,status in [('Имя в тексте',brand),('Сайт в источниках',src),('URL в ответе',url)])
  cards.append(f'''<div class="answer-variant" data-variant="{key}">
  <div class="sample-output"><span>Ответ нейросети</span><blockquote>{line}</blockquote>
  <p class="sample-source"><b>Источники</b> {refs}</p></div>
  <div class="sample-coding"><img class="indicator-poster" src="{{PRE}}{asset("indicator-"+key+".webp")}" width="600" height="400" alt="Индикатор присутствия бренда" aria-hidden="true">
  <dl>{flags}</dl></div><p class="sample-result">{conclusion}</p></div>''')
 return f'''<section class="answer-lab wrap" id="sample">
 <header class="console-title"><div><h2>Что видно в одном ответе?</h2>
 <p class="short-answer">Переключите пример и посмотрите, какие признаки попадут в отчёт.</p></div>
 <span class="demo-label">Учебный пример</span></header>
 <div id="sample-board" class="sample-board" data-indicator="{{PRE}}{asset("indicator-frames.webp")}">
 <div class="sample-top"><div><span>Вопрос покупателя</span><b>Какой сервис поддержки подойдёт небольшой команде?</b></div>
 <fieldset class="sample-choices"><legend>Вариант ответа</legend>{"".join(tabs)}</fieldset></div>
 <div class="sample-variants">{"".join(cards)}<div class="animated-indicator" aria-hidden="true"><canvas width="420" height="280"></canvas></div></div></div>
 <p class="sample-note">«Линия» в этом примере вымышлена.</p></section>'''

def competitor_sheet():
 rows=[
  ('Доля голоса','Какую часть всех появлений брендов из списка сравнения занимает ваша компания. Каждый бренд учитывается один раз за ответ.','Кто чаще других попадает в поле зрения покупателя.'),
  ('Первое место и топ-3','Как часто название встречается первым или среди первых трёх. Среднюю позицию считаем среди ответов, где бренд назван.','Кого клиент видит раньше. Порядок имён сам по себе не доказывает рекомендацию.'),
  ('Конкурент без вас','По каким вопросам другой бренд появляется, когда вашего нет. Для сайтов так же сравниваем конкретные URL и их порядок в источниках.','Какие темы отданы конкуренту и какая его страница попадает в источники.'),
  ('Повторяемость','В скольких повторах и на каких платформах воспроизводится наблюдение. Ответы на вопросы с названием бренда и без подсказки показываем раздельно.','Где результат устойчив в пределах выборки, а где вывод держится на одном ответе.')]
 body=''.join(f'<tr><th scope="row">{key}</th><td>{rule}</td><td>{why}</td></tr>' for key,rule,why in rows)
 return chapter('rival-sheet',headline('В чём вас опережают конкуренты?','Вы увидите соперников по каждому вопросу и платформе. Даже при одинаковой частоте упоминаний порядок брендов и ссылки могут отличаться.')+
 '<table class="rival-table"><thead><tr><th>Показатель</th><th>Что входит в сравнение</th><th>Что это даёт бизнесу</th></tr></thead><tbody>'+body+'</tbody></table>','competitors')

def deliverables():
 rows=[
 ('Маркетингу','Карта спроса','По каждой теме вы получите вопрос покупателя, частоту упоминаний, имена конкурентов и ссылки на источники. Можно сразу увидеть темы, в которых ваш бренд пока не встречается.'),
 ('Продукту и PR','Что говорят о продукте','Фрагменты ответов с характеристиками продукта, оговорками и оценками. Команда сможет сверить спорное утверждение с условиями, которые предлагает клиентам сейчас.'),
 ('Редакции и разработке','Приоритеты по страницам','Для конкретного URL собраны наблюдение, подтверждающий пример и задача по содержанию или доступности страницы. Команда может вернуться к тому же вопросу после изменений.')]
 return chapter('report-delivery',headline('Что команда получит на руки?','Отчёт с выводами, рабочую таблицу и приложение с ответами. Каждый вывод можно проследить до вопроса, модели, даты и источника.')+
 '<div class="delivery-list">'+''.join(f'<div><div class="report-glyph glyph-{i}" aria-hidden="true"><i></i><i></i><i></i></div><span>{team}</span><strong>{name}</strong><p>{desc}</p></div>' for i,(team,name,desc) in enumerate(rows))+'</div>','report')

audit='<div class="audit-stage">'+audit_opening()+answer_sample()+'</div>'+observation_figure()+metric_sheet()+competitor_sheet()+deliverables()
x,auditfaq=faq([('Можно ли увидеть реальные ответы из моего аудита?','Да. В приложении доступны тексты, ссылки, даты, модели и статусы замеров. По ним команда может проверить выводы отчёта.'),('Что покажут вопросы без названия компании?','В каких ситуациях ассистент сам назвал бренд. Вопросы с названием мы разбираем отдельно. По ним видно, как ИИ описывает уже известную покупателю компанию.'),('Аудит покажет продажи из ИИ?','Для выводов о продажах нужны данные аналитики и CRM. Аудит показывает содержание ответов, упоминания и ссылки в пределах исследованной выборки.'),('Можно использовать результат со своей командой?','Да. Таблица связывает наблюдения с вопросами и страницами. Задачи можно передать своей редакции, продуктовой команде или разработчикам.')])
audit+=x+closing(True)

# Editorial pages explain customer choices, not the agency's execution playbook.
posts=[('what-is-geo/','Что такое GEO и зачем оно бизнесу?','GEO помогает бренду и его сайту появляться в ответах нейросетей на вопросы покупателей.','studio-dialogue.webp','2026-11-04'),('blog/mention-or-recommendation/','Означает ли упоминание бренда рекомендацию?','Нет. Нейросеть может назвать компанию в справке о рынке. Для рекомендации нужен совет, кому и почему подойдёт её продукт.','quote-glass.webp',TODAY),('blog/why-ai-recommends-competitors/','Почему ИИ рекомендует конкурентов?','Покупатель может увидеть конкурента, даже когда ваш сайт выше в поиске. Имеет значение, какую задачу он описал и чем нейросеть объяснила свой совет.','studio-shortlist.webp',TODAY)]
cover_alt={
 'studio-dialogue.webp':'Реплики из дымчатого стекла и металла',
 'quote-glass.webp':'Объёмная кавычка из янтарного стекла',
 'studio-shortlist.webp':'Стеклянная карточка на переднем плане среди вариантов',
}
def story_shelf(items, heading, journal=False):
 artwork={
  'what-is-geo/':('prism','Свет преломляется на гранях прозрачной призмы'),
  'blog/mention-or-recommendation/':('mention','Пара металлических и стеклянных кавычек'),
  'blog/why-ai-recommends-competitors/':('choice','Медное ребро выделяет один из трёх объектов'),
 }
 rows=[]
 for route,title,answer,_,date in items:
  cover,alt=artwork[route]
  topics={'prism':'Основы GEO','mention':'Разбор ответа','choice':'Конкуренты'}
  meta=f'<div class="story-meta"><span>{topics[cover]}</span><time datetime="{date}">{date[8:]}.{date[5:7]}.{date[:4]}</time></div>' if journal else ''
  rows.append(f'''<article class="shelf-story"><a href="{{PRE}}{route}">
  <div class="shelf-art"><img src="{{PRE}}{asset("cover-"+cover+".webp")}" width="1024" height="504" alt="{alt}" loading="lazy"></div>
  <div class="shelf-words">{meta}<{heading}>{title}</{heading}><p class="short-answer">{answer}</p></div><span class="shelf-arrow" aria-hidden="true">↗</span></a></article>''')
 return '<div class="story-shelf">'+''.join(rows)+'</div>'

main+=chapter('journal-shelf',headline('Что почитать о выборе бренда в ИИ?','Разберитесь, чем совет отличается от простого упоминания и почему нейросеть может предложить конкурента.')+story_shelf(posts,'h3')+arrow_link('blog/','Весь блог'),'blog')+home_questions+closing()
blog='''<section class="journal-opening"><div class="wrap"><h1>Как работает <span>GEO?</span></h1>
 <p class="short-answer">В блоге разбираем, как нейросети называют компании, ссылаются на сайты и объясняют покупателю свой выбор.</p></div></section>'''+chapter('journal-shelf archive-edition',story_shelf(posts,'h2',journal=True))

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

def prose(h,a,paras):return '<section class="a-prose-section"><h2>'+h+'</h2><p class="short-answer">'+a+'</p>'+''.join('<p>'+p+'</p>' for p in paras)+'</section>'
geo=prose('Чем GEO отличается от SEO?','SEO помогает найти страницу в поиске. При GEO смотрят, кого нейросеть назвала в ответе и на какие сайты сослалась.',['В поиске покупатель сам открывает ссылки. В диалоге он может сначала попросить сравнить несколько поставщиков, а уже потом открыть один сайт.','GEO не отменяет SEO. Google указывает, что для AI Overviews и AI Mode сохраняют актуальность обычные требования к страницам и основы SEO. Специальная разметка не гарантирует присутствие в ответе. <a href="https://developers.google.com/search/docs/appearance/ai-features">Официальная документация Google</a>.'])
geo+=prose('А что означает AEO?','Обычно так называют направление, связанное с прямыми ответами на вопросы пользователя.',['В маркетинговых описаниях GEO и AEO могут пересекаться. При выборе услуги полезнее уточнить, какую задачу бизнеса она решает и какой результат вы получаете, чем ориентироваться только на аббревиатуру.'])
geo+=prose('Зачем это владельцу бизнеса?','Чтобы знать, встречает ли покупатель ваш бренд, когда просит совета у нейросети.',['Покупатель должен понять, что именно вы предлагаете. Если ассистент не называет бренд либо неверно описывает продукт, потенциальный покупатель может не рассмотреть предложение.','Это особенно значимо при сравнении подрядчиков, товаров или сервисов. Но само упоминание не равно обращению и не доказывает рост выручки.'])
geo+=prose('Можно ли купить гарантированную рекомендацию?','Нет. Агентство не управляет ответами сторонней нейросети.',['Ответы зависят от платформы, вопроса и контекста пользователя. Результаты отдельного исследования нельзя автоматически переносить на весь рынок или на всех пользователей.','Исходная научная работа <a href="https://arxiv.org/abs/2311.09735">GEO: Generative Engine Optimization</a> рассматривает видимость контента в генеративных ответах. Авторы измеряли видимость на запросах из своего исследования. По этим данным нельзя предсказать результат отдельной компании.'])
geo+=prose('С какой услуги начать знакомство с GEO?','Начните с аудита, если ещё не видели, что нейросети пишут о вас.',['<a href="{PRE}audit/">В отчёте аудита</a> видно, кто попадает в ответы на вопросы о вашем продукте.','О выборе между услугами читайте в материале <a href="{PRE}why-geo/">«Зачем бренду GEO-продвижение?»</a>.'])
mention=prose('В чём разница для покупателя?','Упоминание знакомит с названием, рекомендация предлагает рассмотреть его как подходящий выбор.',['Нейтральная справка о компании и предложение обратиться именно к ней выполняют разные роли. В первом случае пользователь узнаёт о существовании бренда. Во втором у него появляется причина присмотреться к продукту.','Уточните, какими словами нейросеть описала компанию. Это поможет понять, получил ли покупатель повод обратиться к вам.'])
mention+=prose('Как это выглядит в обычном ответе?','У одного названия могут быть разные роли в диалоге.',['Фраза «Компания работает в этой категории» знакомит с названием. Слова «Для вашей задачи можно рассмотреть эту компанию» добавляют бренд в список вариантов. В ответе «С учётом ваших условий этот вариант подходит» уже есть совет.','Это учебные примеры. Чтобы узнать, состоялась ли продажа, нужны данные о сделке.'])
mention+=prose('Всегда ли больше упоминаний лучше?','Нет, если они не связаны с нужной аудиторией или искажают предложение.',['Бренд может встречаться в нерелевантной категории, устаревшем описании или критическом контексте. Такое присутствие нельзя автоматически считать успехом продвижения.','Полезный вопрос для бизнеса: помогает ли это представление компании покупателю рассмотреть подходящий ему продукт?'])
mention+=prose('Что обсуждать при выборе GEO-услуги?','Связь результата с вашей коммерческой задачей.',['Важно различать видимость, характер рекомендации и обращения. Если речь идёт о росте продаж, одного красивого показателя присутствия недостаточно.','<a href="{PRE}audit/">GEO-аудит aileed</a> покажет, какие доводы получает ваш покупатель. Отчёт можно обсудить со своей командой.'])
competitor=prose('Это означает, что у конкурента продукт лучше?','Нет. По одному ответу нельзя судить о качестве всех продуктов на рынке.',['Ассистент отвечает в определённом контексте, а не выдаёт универсальный рейтинг всех компаний. Вопрос, уточнения пользователя и возможности платформы могут менять результат.','Посмотрите, какое требование покупателя нейросеть связала с конкурентом. Например, рекомендация местного подрядчика может объясняться городом, а не качеством услуги.'])
competitor+=prose('Почему сильное SEO не даёт одинаковую картину в ИИ?','Место страницы в поиске ничего не говорит о том, посоветует ли нейросеть компанию в ответе.',['Даже если сайт заметен в привычной выдаче, это не доказывает, что бренд будет назван в каждом AI-диалоге. И наоборот, отдельное упоминание не означает высокую поисковую позицию.','Google описывает AI-функции как отдельный пользовательский опыт внутри поиска, при этом сохраняет актуальность основ SEO. <a href="https://developers.google.com/search/docs/appearance/ai-features">Источник: Google Search Central</a>.'])
competitor+=prose('Относится ли этот запрос к вашим продажам?','На соответствие вашего предложения задаче покупателя.',['Если человек ищет подрядчика определённой специализации, ему важно понять, кто подходит под задачу. При выборе товара он ищет модели, которые подходят ему по условиям покупки. Не каждое попадание конкурента в ответ относится к вашей целевой аудитории.','Поэтому решение о GEO-продвижении стоит связывать с продуктами, рынком и сценарием выбора, а не со стремлением присутствовать в любом ответе.'])
competitor+=prose('Стоит сразу заказывать продвижение?','Сначала выясните, почему появление конкурента важно для ваших продаж.',['Если вы ещё не видели, как нейросети описывают вашу компанию, начните с <a href="{PRE}audit/">самостоятельного аудита</a>. Если задача уже ясна, оцените <a href="{PRE}why-geo/">пользу GEO для бренда</a>.','Обещания гарантированных мест, фиксированного роста выручки и одинаковых ответов для всех пользователей следует оценивать критически.'])
# Shared components.
geo+=prose('Как выглядит присутствие бренда в ответе?','У бренда есть как минимум три разных способа появиться перед покупателем.',['Ассистент может назвать компанию, включить её сайт в перечень источников или дать адрес страницы прямо в тексте. Публикация компании бывает источником для сравнения, в котором сам продукт вообще не назван. Поэтому эти признаки стоит смотреть отдельно. <a href="{PRE}audit/#sample">Разобрать пример ответа</a>.'])
mention+=prose('Как понять, что вас посоветовали?','Посмотрите на действие, которое ассистент предлагает покупателю.',['Фраза «У Линии есть общий ящик» описывает функцию вымышленного сервиса. А в предложении «Для вашего отдела подойдёт Линия, потому что можно распределять обращения» есть и совет, и довод в пользу продукта. В обоих случаях название встретилось один раз.','При оценке ответа сохраните вопрос пользователя и соседние предложения. Оговорка о тарифе или ограничении может полностью изменить смысл совета.'])
competitor+=prose('Как отличить разовый ответ от закономерности?','Смотрите на повторяемость по одной и той же теме в сопоставимых условиях.',['Если соперник появился однажды, это повод прочитать ответ. Если он появляется повторно у нескольких ассистентов по одному типу вопросов, сравните предложенный продукт, доводы и ссылки. Вопросы, где покупатель уже указал название компании, имеет смысл рассматривать отдельно. <a href="{PRE}audit/#competitors">Сравнение конкурентов в GEO-аудите</a>.'])
def common_header(pre,current):
 nav=[('','Продвижение'),('audit/','Аудит'),('why-geo/','Зачем GEO'),('blog/','Блог')]
 return '<a class="skip" href="#main">К содержанию</a><header class="site-header"><div class="wrap nav"><a class="logo" href="'+pre+'index.html" aria-label="aileed — главная"><img class="wordmark-logo" src="'+pre+asset('aileed-logo.svg')+'" width="170" height="46" alt="aileed"></a><nav class="nav-links" id="navigation" aria-label="Основная навигация">'+''.join('<a href="'+pre+(r or 'index.html')+'"'+(' aria-current="page"' if current==r else '')+'>'+t+'</a>' for r,t in nav)+'</nav><button class="btn nav-cta" type="button" aria-label="Составить бриф" data-open-brief><span class="desktop-label">Составить бриф</span><span class="mobile-label" aria-hidden="true">Бриф</span><span aria-hidden="true">↗</span></button><button class="menu-toggle" aria-controls="navigation" aria-expanded="false" aria-label="Открыть меню">Меню</button></div></header>'
def notice(pre):return '<aside id="cookie-banner" class="cookie-banner a-cookie wrap" aria-labelledby="cookie-title" hidden><div><h2 id="cookie-title">Какие cookie используются?</h2><p class="short-answer">Только необходимые настройки. Аналитика не подключена.</p></div><a href="'+pre+'privacy.html#cookies">Подробнее</a><button type="button" class="btn" data-cookie-accept>Понятно</button></aside>'
def footer(pre,published):
 links=[('what-is-geo/','Что такое GEO?'),('why-geo/','Зачем бренду GEO?'),('blog/','Блог'),('contacts.html','Контакты'),('privacy.html','Конфиденциальность'),('consent.html','Обработка данных')]
 return '<footer class="site-footer a-footer"><div class="wrap"><div class="footer-top"><a class="logo" href="'+pre+'index.html"><img class="wordmark-logo" src="'+pre+asset('aileed-logo.svg')+'" width="170" height="46" alt="aileed"></a><nav class="footer-links" aria-label="Ссылки в подвале">'+''.join('<a href="'+pre+r+'">'+t+'</a>' for r,t in links)+'<button type="button" data-cookie-settings>Настройки cookie</button></nav></div><div class="content-byline"><a href="'+pre+'contacts.html#editorial" rel="author">Материалы: редакция aileed</a><span>Опубликовано <time itemprop="datePublished" datetime="'+published+'">'+pretty(published)+'</time></span><span>Обновлено <time itemprop="dateModified" datetime="'+TODAY+'">'+pretty(TODAY)+'</time></span></div><div class="footer-bottom">© 2026 aileed</div></div></footer>'
def pretty(d):
 y,m,day=d.split('-');return str(int(day))+' '+{'10':'октября','11':'ноября'}[m]+' '+y
# Keep the established local-only brief form.
old= (ROOT/'index.html').read_text();dialog=re.search(r'<dialog\b.*?</dialog>',old,re.S).group(0).replace('AiLeeds','aileed')
SOCIAL_IMAGES={
 'audit/':'social-audit.png',
 'why-geo/':'social-why.jpg',
 'blog/':'social-geo.png',
 'what-is-geo/':'social-definition.jpg',
 'blog/mention-or-recommendation/':'social-mention.jpg',
 'blog/why-ai-recommends-competitors/':'social-competitors.jpg',
}
def write(route,title,desc,body,published,article=False,faqs=None):
 file=ROOT/(route+'index.html' if not route.endswith('.html') else route);pre='../'*route.count('/')
 if route.endswith('.html'):pre=''
 url=BASE+route
 org={'@type':'Organization','@id':BASE+'#org','name':'aileed','url':BASE,'logo':BASE+asset('aileed-logo.svg')}
 page={'@type':'WebPage','@id':url+'#page','url':url,'name':title,'description':desc,'inLanguage':'ru-RU','author':{'@id':BASE+'#org'},'publisher':{'@id':BASE+'#org'},'datePublished':published,'dateModified':TODAY,'isPartOf':{'@id':BASE+'#website'}}
 graph=[org,{'@type':'WebSite','@id':BASE+'#website','name':'aileed','url':BASE},page]
 social=SOCIAL_IMAGES.get(route,'social.png')
 if article:
  headline=re.sub('<[^>]+>','',re.search('<h1>(.*?)</h1>',body,re.S).group(1))
  graph.append({'@type':'Article','@id':url+'#article','headline':headline,'mainEntityOfPage':{'@id':url+'#page'},'author':{'@id':BASE+'#org'},'publisher':{'@id':BASE+'#org'},'datePublished':published,'dateModified':TODAY,'image':BASE+asset(social),'inLanguage':'ru-RU'});page['mainEntity']={'@id':url+'#article'}
 if route in ['','audit/']:graph.append({'@type':'Service','name':('GEO-аудит' if route=='audit/' else 'GEO-продвижение'),'provider':{'@id':BASE+'#org'},'url':url,'description':desc})
 if faqs:graph.append({'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faqs]})
 if route:
  label=re.sub(r' \| aileed$','',title)
  crumbs=[{'@type':'ListItem','position':1,'name':'aileed','item':BASE}]
  if route.startswith('blog/') and route!='blog/':crumbs.append({'@type':'ListItem','position':2,'name':'Блог','item':BASE+'blog/'})
  crumbs.append({'@type':'ListItem','position':len(crumbs)+1,'name':label,'item':url})
  graph.append({'@type':'BreadcrumbList','itemListElement':crumbs})

 head='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><meta name="description" content="'+html.escape(desc)+'"><meta name="author" content="Редакция aileed"><meta name="datePublished" content="'+published+'"><meta name="dateModified" content="'+TODAY+'"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#080909"><link rel="canonical" href="'+url+'"><link rel="describedby" type="text/plain" href="'+BASE+'llms.txt"><meta property="og:title" content="'+html.escape(title)+'"><meta property="og:description" content="'+html.escape(desc)+'"><meta property="og:url" content="'+url+'"><meta property="og:site_name" content="aileed"><meta property="og:locale" content="ru_RU"><meta property="og:type" content="'+('article' if article else 'website')+'"><meta property="og:image" content="'+BASE+asset(social)+'"><meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/svg+xml" href="'+pre+asset('mark.svg')+'"><link rel="stylesheet" href="'+pre+asset('site.css')+'"><link rel="stylesheet" href="'+pre+asset('studio.css')+'"><link rel="stylesheet" href="'+pre+asset('editions.css')+'"><script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False)+'</script>'+''.join('<script src="'+pre+asset(f)+'" defer></script>' for f in ['site.js','privacy.js','experience.js']+(['quote-stage.js'] if 'data-quote-stage' in body else [])+(['audit-indicator.js'] if 'data-indicator=' in body else []))+'</head>'
 content=head+'<body class="brand-refresh" itemscope itemtype="https://schema.org/WebPage" itemid="'+url+'#page">'+common_header(pre,route)+notice(pre)+'<main id="main">'+body.replace('{PRE}',pre)+'</main>'+footer(pre,published)+dialog.replace('href="privacy.html"','href="'+pre+'privacy.html"').replace('href="consent.html"','href="'+pre+'consent.html"')+'<noscript><p class="cookie-noscript">Аналитика и рекламные cookie не используются.</p></noscript></body></html>'
 # Fragment-only primary destinations belong to the current page.
 content=content.replace('href="'+pre+'#','href="#')
 file.parent.mkdir(parents=True,exist_ok=True);file.write_text("\n".join(line.rstrip() for line in content.replace("><",">\n<").splitlines())+"\n")
PAGES=[]
def page(route,title,desc,body,date,article=False,faqs=None):write(route,title,desc,body,date,article,faqs);PAGES.append((route,date))
page('','Как стать брендом, который рекомендуют нейросети? | aileed','GEO-продвижение бренда в ChatGPT, Алисе и других нейросетях. Помогаем бизнесу участвовать в выборе покупателя внутри AI-ответа. aileed.',main,'2026-10-07',faqs=mainfaq)
page('audit/','Что измеряет GEO-аудит бренда в нейросетях? | aileed','GEO-аудит бренда в нейросетях. Упоминания, сайт в источниках, URL в ответах, доля голоса и место среди конкурентов. Посмотрите пример и состав отчёта.',audit,'2026-11-02',faqs=auditfaq)
page('why-geo/','Зачем бренду GEO-продвижение? | aileed','Зачем бизнесу GEO-продвижение: видимость, доверие и участие в выборе клиента. Когда оно уместно для B2B, магазинов и сервисов.',why,TODAY)
page('blog/','Что важно знать о GEO и AI-видимости? Блог | aileed','Блог aileed для владельцев бизнеса и маркетологов: GEO, рекомендации нейросетей, доверие и выбор бренда.',blog,TODAY)
for (route,title,answer,image,date),text in zip(posts,[geo,mention,competitor]):
 cover=img(image,cover_alt[image],'article-object',True)
 hero_title='Вас назвали или посоветовали?' if route=='blog/mention-or-recommendation/' else title
 body=f'''<article class="a-article"><header class="studio-article-head"><div class="wrap article-lead">
 <div><h1>{hero_title}</h1><p class="short-answer">{answer}</p>
 <p class="a-article-author"><a href="{{PRE}}contacts.html#editorial" rel="author">Редакция aileed</a> · Обновлено <time datetime="{TODAY}">{pretty(TODAY)}</time></p></div>
 <div class="editorial-object" data-scene>{cover}</div></div></header>'''+reading_layout(text,'В этой статье')+'''<div class="wrap a-article-cta">
 <a class="btn" href="{PRE}audit/">Об услуге GEO-аудита <span aria-hidden="true">↗</span></a><a class="text-link" href="{PRE}blog/">Весь блог <span aria-hidden="true">→</span></a></div></article>'''
 page(route,title+' | aileed',answer,body,date,True)
# Preserve necessary legal information and the previously agreed contact status.
for name,date in [('contacts.html','2026-11-02'),('privacy.html','2026-10-07'),('consent.html','2026-11-02')]:
 source=json.loads((ROOT/'content/legal.json').read_text())[name]
 body=source['body'].replace('AiLeeds','aileed').replace('AILEEDS','aileed').replace('aileeds:privacy-choice:v1','aileed:privacy-choice:v1')
 title=source['title'].replace('AiLeeds','aileed');desc=source['description'].replace('AiLeeds','aileed')
 interior=body.strip().removeprefix('<article class="wrap document-page">').removesuffix('</article>')
 lead,separator,sections=interior.partition('<section')
 if not separator: raise ValueError('Missing document sections: '+name)
 doc='<article class="studio-document"><header class="document-lead"><div class="wrap">'+lead+'</div></header>'+reading_layout(separator+sections,'На этой странице')+'</article>'
 page(name,title,desc,doc,date)

# Keep old bookmarks useful while removing the retired page from discovery.
(ROOT/'platforms/index.html').write_text(f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow"><link rel="canonical" href="{BASE}why-geo/"><meta http-equiv="refresh" content="0; url=../why-geo/"><title>Зачем бренду GEO? | aileed</title></head><body><a href="../why-geo/">Зачем бренду GEO?</a></body></html>\n')

(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+escape(BASE+r)+'</loc><lastmod>'+TODAY+'</lastmod></url>' for r,d in PAGES)+'</urlset>\n')
(ROOT/'llms.txt').write_text('# aileed\n\n> GEO-продвижение и аудит брендов в ответах нейросетей.\n\n## Услуги\n- [GEO-продвижение]('+BASE+'): присутствие бренда в выборе клиента внутри AI-ответов.\n- [GEO-аудит]('+BASE+'audit/): AI-видимость, конкуренты и образ бренда.\n\n## Материалы\n- [Зачем бренду GEO]('+BASE+'why-geo/): бизнес-смысл и применимость.\n- [Что такое GEO]('+BASE+'what-is-geo/): определение и отличия от SEO/AEO.\n- [Блог]('+BASE+'blog/): выбор бренда и рекомендации нейросетей.\n- [Упоминание или рекомендация]('+BASE+'blog/mention-or-recommendation/): разница для бизнеса.\n- [Почему ИИ рекомендует конкурентов]('+BASE+'blog/why-ai-recommends-competitors/): как понимать такой ответ.\n\n## Контакты и данные\n- [Контакты]('+BASE+'contacts.html): каналы отправки пока не подключены, бриф сохраняется локально.\n- [Конфиденциальность]('+BASE+'privacy.html)\n- [Обработка данных]('+BASE+'consent.html)\n\nРекомендации сторонних платформ и рост выручки не гарантируются.\n')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+BASE+'sitemap.xml\n')
print('Rendered',len(PAGES),'pages for',BASE)
