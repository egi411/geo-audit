#!/usr/bin/env python3
"""Render aileed's static pages. Use --base-url only when the domain is ready."""
from pathlib import Path
import argparse,json,re,html,hashlib
from xml.sax.saxutils import escape
from visibility import frequency_figure, observation_figure
from cases import PROJECTS, case_index, case_article
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--base-url',default='https://egi411.github.io/geo-audit/');args=ap.parse_args();BASE=args.base_url.rstrip('/')+'/'
FIRST_EDITION='2026-11-18'
UPDATED='2026-11-24'
def asset(name):
 p=ROOT/'assets'/name
 return 'assets/'+name+'?v='+hashlib.sha256(p.read_bytes()).hexdigest()[:12] if p.exists() else 'assets/'+name
def hero(h,a,p,primary,secondary):
 return f'''<section class="inner-hero wrap"><h1>{h}</h1><div><p class="short-answer">{a}</p>
 <p class="a-lead">{p}</p><div class="actions"><a class="btn primary" href="{{PRE}}{primary[1]}">{primary[0]} <span aria-hidden="true">↗</span></a>
 <a class="text-link" href="{{PRE}}{secondary[1]}">{secondary[0]} <span aria-hidden="true">→</span></a></div></div></section>'''

CONSULT_EMAIL = "egorkl2307@gmail.com"
CONSULT_SUBJECT = "Заявка%20на%20бесплатную%20консультацию"
CONSULT_LINK = f"mailto:{CONSULT_EMAIL}?subject={CONSULT_SUBJECT}&amp;body=Здравствуйте!%20Хочу%20записаться%20на%20бесплатную%20консультацию."

def home_hero():
 examples = [
  ('shop', 'Магазин', 'Москва', 'Где в Москве купить кофемолку для эспрессо с самовывозом сегодня?', 'scene-grinder', 'Кофемолка на кухонной столешнице'),
  ('bureau', 'Услуги', 'Казань', 'Кто в Казани спроектирует освещение для гостиницы?', 'scene-hotel', 'Архитектурная модель гостиницы с подсветкой фасада'),
  ('software', 'Онлайн-сервис', 'Екатеринбург', 'Открываем второй салон в Екатеринбурге. Как вести запись клиентов в одной базе?', 'scene-booking', 'Расписание приёма клиентов на планшете'),
 ]
 controls, views = [], []
 for i,(key,label,city,question,photo,alt) in enumerate(examples):
  checked = ' checked' if i==0 else ''
  priority = 'fetchpriority="high"' if i==0 else 'loading="lazy"'
  controls.append(f'<label><input type="radio" name="market" value="{key}"{checked}><span>{label}</span></label>')
  views.append(f'''<figure class="market-view" data-market="{key}">
   <img src="{{PRE}}{asset(photo+"-small.webp")}" srcset="{{PRE}}{asset(photo+"-small.webp")} 720w, {{PRE}}{asset(photo+".webp")} 1440w"
    sizes="(max-width: 760px) 94vw, 48vw" width="1440" height="960" alt="{alt}" {priority}>
   <figcaption><small>Пример запроса покупателя · {city}</small><blockquote>{question}</blockquote></figcaption></figure>''')
 return f'''<section class="home-hero market-hero"><div class="market-layout wrap" id="value">
 <div class="market-offer"><h1>Продвижение брендов в нейросетях</h1>
 <p class="short-answer">Помогаем покупателям в России находить ваши товары и услуги в Алисе, ChatGPT и других нейросетях. На бесплатной консультации разберём ваш сайт и выберем, с какого направления начать.</p>
 <div class="actions"><a class="btn primary" href="{CONSULT_LINK}" data-open-brief>Получить консультацию ↗</a>
 <a class="text-link" href="{{PRE}}cases/">Наши кейсы →</a></div></div>
 <div class="market-examples" id="business"><fieldset class="market-controls"><legend>Учебные примеры для российского рынка</legend>{''.join(controls)}</fieldset>
 {''.join(views)}</div>
 <div class="visibility-goal"><strong>100<span>%</span></strong><p>Наша цель по видимости бренда в ответах на выбранные вопросы покупателей.</p></div>
 </div></section>'''


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

def services(question, answer):
 options=[
  ('audit/#observations','GEO-аудит','Узнайте, где покупатели встречают ваш бренд и с кем его сравнивают. Вы получите ответы нейросетей и список страниц, которые стоит доработать в первую очередь. По этому отчёту может работать ваша команда.','Посмотреть образец отчёта'),
  ('#scope','GEO-продвижение','Выберите продукт или услугу, по которым хотите получать заказы. Мы поможем представить их в каталоге, на страницах услуг и в публикациях, чтобы покупатели могли найти вас, даже когда ищут без названия бренда.','Что входит в продвижение')]
 figures=['<div class="service-figure audit-mini"><span class="mini-caption">GEO-аудит WINLINE</span><div class="audit-stats"><span><b>300</b> вопросов</span><i>×</i><span><b>5</b> моделей</span><i>×</i><span><b>10</b> прогонов</span></div></div>',
          '<div class="service-figure intent-mini"><span class="mini-caption">Пример выбора подрядчика</span><div class="query-slip">Кому заказать свет для отеля в Казани?</div><div class="proof-slip"><span aria-hidden="true">↳</span><span>Портфолио бюро<small>Освещение гостиниц</small></span></div></div>']
 items=[]
 for (route,name,reason,link),figure in zip(options,figures):
  fields='<div class="dossier-fields"><span>В отчёте</span><b>Упоминания</b><b>Источники</b><b>Ссылки</b></div>' if route.startswith('audit/') else ''
  items.append(f'<a class="service-tile" href="{route}">{figure}<div class="service-description">{fields}<strong>{name}</strong><p>{reason}</p></div><span class="tile-action">{link} <span aria-hidden="true">↗</span></span></a>')
 return chapter('service-gallery',headline(question,answer)+'<div class="service-pair" id="from-answer">'+''.join(items)+'</div>','offers')

def promotion_scope():
 return chapter('promotion-scope', f'''<header><h2>Что входит в GEO-продвижение</h2>
 <p>Представим поставщика печей в Самаре. Ему интересны заказы с монтажом, но об этой услуге покупатели узнают только в разговоре с менеджером. Что можно сделать для такого бизнеса?</p></header>
 <div class="scope-spread">
 <figure class="scope-question"><figcaption>Пример запроса покупателя · Самара</figcaption>
 <blockquote>Где заказать печь для пекарни, чтобы её привезли, подключили и взяли на обслуживание?</blockquote>
 <a class="edition-link" href="{CONSULT_LINK}" data-open-brief>Разобрать мой проект <span aria-hidden="true">↗</span></a></figure>
 <div class="scope-delivery"><h3>Что получит поставщик</h3>
 <dl><dt>Подборку печей для небольших пекарен</dt>
 <dd>В карточках укажем размеры, мощность и число противней. Владелец сможет отобрать модели, которые поместятся на кухне.</dd>
 <dt>Страницу о поставке и подключении</dt>
 <dd>Соберём в одном месте условия доставки по Самаре, требования к помещению и порядок вызова мастера. Покупатель увидит, за что отвечает поставщик.</dd>
 <dt>Рассказ о монтаже у клиента</dt>
 <dd>Если у поставщика есть такой проект, по его фотографиям и данным покажем, какую печь выбрали и как прошёл запуск. Из публикации можно будет перейти к этой модели.</dd></dl></div></div>''','scope')

def home_projects():
 return chapter('home-projects', headline('Два проекта aileed', 'Для WINLINE мы разобрали ответы о регистрации и акциях. Для модного бренда связали публикации в журнале с каталогом, чтобы читатели могли перейти к конкретному изделию.')+f'''
 <div class="evidence-pair">
 <article class="audit-evidence"><img src="{{PRE}}{asset('cases/winline.svg')}" width="483" height="116" alt="WINLINE" loading="lazy">
 <p class="evidence-stat">15 000 <small>замеров в пяти нейросетях</small></p>
 <div class="evidence-copy"><h3>Какие страницы WINLINE попадают в ответы</h3>
 <p class="short-answer">Выяснили, в каких ответах нейросети ссылаются на WINLINE, а в каких отправляют к посредникам. В отчёте связали 124 темы со 119 страницами бренда.</p>
 {arrow_link('cases/winline/', 'Кейс WINLINE')}</div></article>
 <article class="fashion-evidence"><figure class="evidence-photo"><img src="{{PRE}}{asset('shoe-editorial.webp')}" width="1440" height="960" loading="lazy" alt="Чёрный кожаный лофер"><figcaption>Иллюстрация к кейсу</figcaption></figure>
 <div class="evidence-copy"><span>Модный бренд · NDA</span><h3>Больше 10 000 переходов из нейросетей</h3>
 <p class="short-answer">Это результат двух сайтов марки за полгода. Около 1 500 переходов пришлись на запросы покупателей, которые искали изделие без названия бренда.</p>
 {arrow_link('cases/fashion/', 'Кейс модного бренда')}</div></article></div>''', 'projects')


def home_footer_offer():
 questions=[
  ('Что разберём на бесплатной консультации?', 'Возьмём один товар или услугу, которые вы хотите продвигать. Посмотрим страницу глазами покупателя и обсудим, где начать работу. Для первого разговора достаточно адреса сайта.'),
  ('Можно заказать только аудит?', 'Да. Вы получите отчёт с ответами нейросетей и списком страниц для доработки. Внедрение можно поручить своей команде.'),
  ('У нас несколько филиалов. С какого начать?', 'Выберите город, где хотите получать больше обращений. Например, московской сети с новым филиалом в Туле имеет смысл начать разбор с вопросов покупателей в Туле.'),
  ('У нас уже есть SEO-подрядчик. Как работать вместе?', 'Если ваш подрядчик уже переделывает каталог, обсудим с ним, какие сведения добавить в карточки. Отдельно договоримся, кто возьмёт на себя тексты и публикацию.'),
  ('От чего зависит стоимость продвижения?', 'Важны размер каталога, география и состояние сайта. Если описание товара уже есть, его можно дополнить. Для новой линейки может понадобиться целый раздел. Обсудим объём на консультации.'),
  ('Как быстро видны изменения?', 'В проекте модного бренда нейросети верно описывали компанию уже в первый месяц. Переходы мы считали за полгода. Это сроки одного проекта. Чтобы дать ориентир для вашего, сначала посмотрим, как покупатели находят вас сегодня.')
 ]
 entries=faq_entries(questions)
 block=chapter('enquiry-section',f'''<header><h2>С чего начать работу?</h2></header>
 <div class="enquiry-layout"><div class="question-list">{entries}</div>
 <aside id="brief"><h3>Обсудим ваш проект?</h3><p>Оставьте заявку. Мы свяжемся с вами в ближайшее время и проведём бесплатную консультацию.</p>
 <a class="btn primary" href="{CONSULT_LINK}" data-open-brief>Оставить заявку ↗</a></aside></div>''','faq')
 return block,questions


main=home_hero()+services('Аудит или продвижение?', 'Аудит подойдёт, если вам нужен план для своей команды. Продвижение можно начать с одной услуги или линейки товаров, для которой вы ищете новых покупателей.')+promotion_scope()+home_projects()
home_questions,mainfaq=home_footer_offer()

# Detail pages.
why=hero('Зачем бренду <span>GEO?</span>','Чтобы покупатель учитывал вашу компанию, когда спрашивает у нейросети, к кому обратиться или что купить.','Если нейросеть назвала двух конкурентов, именно их предложения клиент может открыть первыми. Стоит узнать, попадаете ли вы в этот список и что о вас говорят.',('Посмотреть пример аудита','audit/#observations'),('Упоминания и цитирования','#visibility'))
why+=frequency_figure()
why+=chapter('investment-feature',f"""
 <div class="investment-spread" id="investment">{scene_image('scene-hotel','Модель гостиницы с подсвеченными окнами и фасадом','(max-width: 700px) 95vw, 80vw')}
 <div class="investment-copy"><h2>Когда GEO стоит вложений?</h2>
 <p class="short-answer">Когда заказчик выбирает подрядчика до первого звонка.</p>
 <p>Например, владелец отеля в Казани спрашивает, кому заказать освещение фасада. В ответе два бюро. Оба делают свет, но только у одного есть ссылка на готовую гостиницу. Именно этот проект заказчик может переслать архитектору.</p>
 <p>Если клиенты уже приходят с таким списком, начните с одного вопроса из переговоров. Посмотрите, кого назвали и чей проект привели в пример.</p>
 {arrow_link('audit/#sample-board','Разобрать пример ответа')}</div></div>""")
why+=chapter('return-story', '''<header id="demand"><h2>Как выбрать регион для старта?</h2>
 <p class="short-answer">Начните с территории, где можете выполнить заказ. При выборе подрядчика заказчику важны выезд на объект и проекты поблизости. Для товара важнее наличие и срок доставки.</p></header>
 <div class="region-spread"><blockquote>Кто изготовит кухню по моим размерам и привезёт её в Тулу?</blockquote>
 <div><strong>Учебный пример · Россия</strong><p>Клиент может заказать кухню у местной фабрики или у московской, если та берёт на себя замер и монтаж в Туле. Обоим производителям пригодится страница с условиями выезда и примерами готовых кухонь.</p></div></div>''','outcome')
why_questions,whyfaq=faq([
 ('С какого продукта начать?', 'С продукта, который покупатель сравнивает с альтернативами. Возьмите вопрос из переговоров и посмотрите, какие компании и источники покупатель увидит в ответе.'),
 ('Когда можно отложить GEO?', 'Если большинство заказов приходит по персональному приглашению и клиенты уже выбрали поставщика, сначала выясните, участвуют ли нейросети в вашем цикле продаж.'),
 ('Что считать результатом для бизнеса?', 'Сначала проверьте, появляется ли бренд в ответах на вопросы покупателей. Затем посмотрите на переходы, целевые обращения и сделки, для которых удалось установить источник.')],
 'Что учесть перед вложениями в GEO?', 'Выбор зависит от того, как покупатели ищут ваш продукт и какие обращения важны для продаж.')
why+=why_questions+closing()
def audit_opening():
 models = ('Алиса', 'ChatGPT', 'Perplexity', 'Gemini', 'Claude')
 rounds = ''.join('<i></i>' for _ in range(10))
 matrix = ''.join(f'<li><span>{name}</span><div aria-hidden="true">{rounds}</div></li>' for name in models)
 return f'''<header class="audit-cover wrap"><div class="audit-pitch"><h1>GEO-аудит бренда</h1>
 <p class="short-answer">Узнайте, по каким вопросам нейросети называют вашу компанию, кого ставят рядом и на чьи сайты ведут покупателей. Вы получите исходные ответы и список страниц для доработки.</p>
 <div class="actions"><a class="btn primary" href="{CONSULT_LINK}" data-open-brief>Обсудить аудит ↗</a>
 <a class="text-link" href="#observations">Посмотреть пример ↓</a></div></div>
 <figure class="audit-case"><figcaption><img src="{{PRE}}{asset('cases/winline.svg')}" alt="WINLINE" width="483" height="116"><span>Из клиентского аудита</span></figcaption>
 <div class="audit-case-total"><strong>15 000</strong><span>замеров</span></div>
 <ol aria-label="Пять моделей, десять прогонов в каждой">{matrix}</ol>
 <div class="audit-case-foot"><span>Каждая метка обозначает прогон 300 вопросов</span>{arrow_link('cases/winline/', 'Весь кейс')}</div></figure></header>'''


def metric_sheet():
 metrics=[
  ('text','Упоминание бренда','Название встречается в основном тексте.','Повтор названия в одном ответе засчитывается один раз. Название только в адресе или в подписи ссылки сюда не входит.'),
  ('sources','Сайт в источниках','Домен есть в списке источников ответа.','Несколько страниц одного сайта дают одно попадание за замер. Источник может остаться за пределами текста, который видит покупатель.'),
  ('url','URL в ответе','Полный адрес сайта встроен в сам ответ.','Считается и ссылка под словом. В отчёте видно, куда попадёт покупатель по ссылке. Это может быть карточка продукта, обзор или главная страница.')]
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
 ('Продукту и PR','Что говорят о продукте','Фрагменты ответов с характеристиками продукта, оговорками и оценками. Команда сможет сверить спорное утверждение с условиями, которые предлагает клиентам сейчас.'),
 ('Редакции и разработке','Приоритеты по страницам','Для конкретного URL собраны наблюдение, подтверждающий пример и задача по содержанию или доступности страницы. Команда может вернуться к тому же вопросу после изменений.')]
 return chapter('report-delivery',headline('Что команда получит на руки?','Отчёт с выводами, таблицу для команды и исходные ответы. Для WINLINE мы собрали выводы на 26 слайдах. Данные и задачи по страницам передали в рабочей книге из 12 листов.')+
 '<div class="delivery-list">'+''.join(f'<div><span>{team}</span><strong>{name}</strong><p>{desc}</p></div>' for team,name,desc in rows)+'</div>','report')

audit='<div class="audit-edition">'+audit_opening()+observation_figure()+answer_sample()+metric_sheet()+competitor_sheet()+deliverables()
x,auditfaq=faq([('Можно ли увидеть реальные ответы из моего аудита?','Да. В приложении доступны тексты, ссылки, даты, модели и статусы замеров. По ним команда может проверить выводы отчёта.'),('Что покажут вопросы без названия компании?','В каких ситуациях ассистент сам назвал бренд. Вопросы с названием мы разбираем отдельно. По ним видно, как ИИ описывает уже известную покупателю компанию.'),('Аудит покажет продажи из ИИ?','Для выводов о продажах нужны данные аналитики и CRM. Аудит показывает содержание ответов, упоминания и ссылки в пределах исследованной выборки.'),('Можно использовать результат со своей командой?','Да. Таблица связывает наблюдения с вопросами и страницами. Редакция или разработчики могут взять задачи в работу.')])
audit+=x+closing(True)+'</div>'

# Editorial pages explain customer choices, not the agency's execution playbook.
posts=[('what-is-geo/','Что такое GEO и зачем оно бизнесу?','GEO помогает бренду и его сайту появляться в ответах нейросетей на вопросы покупателей.','prism','2026-11-04'),('blog/mention-or-recommendation/','Означает ли упоминание бренда рекомендацию?','Нет. Нейросеть может назвать компанию в справке о рынке. Для рекомендации нужен совет, кому и почему подойдёт её продукт.','mention',FIRST_EDITION),('blog/why-ai-recommends-competitors/','Почему ИИ рекомендует конкурентов?','Покупатель может увидеть конкурента, даже когда ваш сайт выше в поиске. Имеет значение, какую задачу он описал и чем нейросеть объяснила свой совет.','choice',FIRST_EDITION)]
def cover_art(motif):
 return f'<div class="print-art print-{motif}" aria-hidden="true"><i></i><i></i><i></i><i></i></div>'

def story_shelf(items, heading, journal=False):
 rows=[]
 for route,title,answer,cover,date in items:
  topics={'prism':'Основы GEO','mention':'Разбор ответа','choice':'Конкуренты'}
  meta=f'<div class="story-meta"><span>{topics[cover]}</span><time datetime="{date}">{date[8:]}.{date[5:7]}.{date[:4]}</time></div>' if journal else ''
  rows.append(f'''<article class="shelf-story"><a href="{{PRE}}{route}">
  {cover_art(cover)}
  <div class="shelf-words">{meta}<{heading}>{title}</{heading}><p class="short-answer">{answer}</p></div><span class="shelf-arrow" aria-hidden="true">↗</span></a></article>''')
 return '<div class="story-shelf">'+''.join(rows)+'</div>'

main+=home_questions
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
geo=prose('Чем GEO отличается от SEO?','SEO помогает найти страницу в поиске. При GEO смотрят, кого нейросеть назвала в ответе и на какие сайты сослалась.',['В поиске покупатель сам открывает ссылки. В диалоге он может сначала попросить сравнить несколько поставщиков, а уже потом открыть один сайт.','GEO не отменяет SEO. Google указывает, что для AI Overviews и AI Mode сохраняют актуальность обычные требования к страницам и основы SEO. Специальная разметка не гарантирует присутствие в ответе. <a rel="nofollow" href="https://developers.google.com/search/docs/appearance/ai-features">Как это описывает Google</a>.'])
geo+=prose('А что означает AEO?','Обычно так называют направление, связанное с прямыми ответами на вопросы пользователя.',['В маркетинговых описаниях GEO и AEO могут пересекаться. При выборе услуги полезнее уточнить, какую задачу бизнеса она решает и какой результат вы получаете, чем ориентироваться только на аббревиатуру.'])
geo+=prose('Зачем это владельцу бизнеса?','Чтобы знать, встречает ли покупатель ваш бренд, когда просит совета у нейросети.',['Покупатель должен понять, что именно вы предлагаете. Если ассистент не называет бренд либо неверно описывает продукт, потенциальный покупатель может не рассмотреть предложение.','Это особенно значимо при сравнении подрядчиков, товаров или сервисов. Но само упоминание не равно обращению и не доказывает рост выручки.'])
geo+=prose('Можно ли купить гарантированную рекомендацию?','Нет. Агентство не управляет ответами сторонней нейросети.',['Ответы зависят от платформы, вопроса и контекста пользователя. Результаты отдельного исследования нельзя автоматически переносить на весь рынок или на всех пользователей.'])
geo+=prose('С какой услуги начать знакомство с GEO?','Начните с аудита, если ещё не видели, что нейросети пишут о вас.',['<a href="{PRE}audit/">В отчёте аудита</a> видно, кто попадает в ответы на вопросы о вашем продукте.','О выборе между услугами читайте в материале <a href="{PRE}why-geo/">«Зачем бренду GEO-продвижение?»</a>.'])
mention=prose('В чём разница для покупателя?','Упоминание знакомит с названием, рекомендация предлагает рассмотреть его как подходящий выбор.',['Нейтральная справка о компании и предложение обратиться именно к ней выполняют разные роли. В первом случае пользователь узнаёт о существовании бренда. Во втором у него появляется причина присмотреться к продукту.','Уточните, какими словами нейросеть описала компанию. Это поможет понять, получил ли покупатель повод обратиться к вам.'])
mention+=prose('Как это выглядит в обычном ответе?','У одного названия могут быть разные роли в диалоге.',['Фраза «Компания работает в этой категории» знакомит с названием. Слова «Для вашей задачи можно рассмотреть эту компанию» добавляют бренд в список вариантов. В ответе «С учётом ваших условий этот вариант подходит» уже есть совет.','Это учебные примеры. Чтобы узнать, состоялась ли продажа, нужны данные о сделке.'])
mention+=prose('Всегда ли больше упоминаний лучше?','Нет, если они не связаны с нужной аудиторией или искажают предложение.',['Бренд может встречаться в нерелевантной категории, устаревшем описании или критическом контексте. Такое присутствие нельзя автоматически считать успехом продвижения.','Полезный вопрос для бизнеса: помогает ли это представление компании покупателю рассмотреть подходящий ему продукт?'])
mention+=prose('Что обсуждать при выборе GEO-услуги?','Связь результата с вашей коммерческой задачей.',['Важно различать видимость, характер рекомендации и обращения. Если речь идёт о росте продаж, одного красивого показателя присутствия недостаточно.','<a href="{PRE}audit/">GEO-аудит aileed</a> покажет, какие доводы получает ваш покупатель. Отчёт можно обсудить со своей командой.'])
competitor=prose('Это означает, что у конкурента продукт лучше?','Нет. По одному ответу нельзя судить о качестве всех продуктов на рынке.',['Ассистент отвечает в определённом контексте, а не выдаёт универсальный рейтинг всех компаний. Вопрос, уточнения пользователя и возможности платформы могут менять результат.','Посмотрите, какое требование покупателя нейросеть связала с конкурентом. Например, рекомендация местного подрядчика может объясняться городом, а не качеством услуги.'])
competitor+=prose('Почему сильное SEO не даёт одинаковую картину в ИИ?','Место страницы в поиске ничего не говорит о том, посоветует ли нейросеть компанию в ответе.',['Даже если сайт заметен в привычной выдаче, это не доказывает, что бренд будет назван в каждом AI-диалоге. И наоборот, отдельное упоминание не означает высокую поисковую позицию.'])
competitor+=prose('Относится ли этот запрос к вашим продажам?','Сравните требования в вопросе с тем, что вы продаёте.',['Если человек ищет подрядчика определённой специализации, ему важно понять, кто подходит под задачу. При выборе товара он ищет модели, которые подходят ему по условиям покупки. Не каждое попадание конкурента в ответ относится к вашей целевой аудитории.','Поэтому решение о GEO-продвижении стоит связывать с продуктами, рынком и сценарием выбора, а не со стремлением присутствовать в любом ответе.'])
competitor+=prose('Стоит сразу заказывать продвижение?','Сначала выясните, почему появление конкурента важно для ваших продаж.',['Если вы ещё не видели, как нейросети описывают вашу компанию, начните с <a href="{PRE}audit/">самостоятельного аудита</a>. Если задача уже ясна, оцените <a href="{PRE}why-geo/">пользу GEO для бренда</a>.','Обещания гарантированных мест, фиксированного роста выручки и одинаковых ответов для всех пользователей следует оценивать критически.'])
# Shared components.
geo+=prose('Как выглядит присутствие бренда в ответе?','У бренда есть как минимум три разных способа появиться перед покупателем.',['Ассистент может назвать компанию, включить её сайт в перечень источников или дать адрес страницы прямо в тексте. Публикация компании бывает источником для сравнения, в котором сам продукт вообще не назван. Поэтому эти признаки стоит смотреть отдельно. <a href="{PRE}audit/#sample">Разобрать пример ответа</a>.'])
mention+=prose('Как понять, что вас посоветовали?','Посмотрите на действие, которое ассистент предлагает покупателю.',['Фраза «У Линии есть общий ящик» описывает функцию вымышленного сервиса. А в предложении «Для вашего отдела подойдёт Линия, потому что можно распределять обращения» есть и совет, и довод в пользу продукта. В обоих случаях название встретилось один раз.','При оценке ответа сохраните вопрос пользователя и соседние предложения. Оговорка о тарифе или ограничении может полностью изменить смысл совета.'])
competitor+=prose('Как отличить разовый ответ от закономерности?','Смотрите на повторяемость по одной и той же теме в сопоставимых условиях.',['Если соперник появился однажды, это повод прочитать ответ. Если он появляется повторно у нескольких ассистентов по одному типу вопросов, сравните предложенный продукт, доводы и ссылки. Вопросы, где покупатель уже указал название компании, имеет смысл рассматривать отдельно. <a href="{PRE}audit/#competitors">Сравнение конкурентов в GEO-аудите</a>.'])
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
def footer(pre,published):
 groups=[
  ('Услуги', [('','GEO-продвижение'),('audit/','GEO-аудит')]),
  ('Кейсы', [('cases/','Все кейсы'),('cases/fashion/','Модный бренд под NDA'),('cases/winline/','WINLINE')]),
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
 head='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><meta name="description" content="'+html.escape(desc)+'"><meta name="author" content="aileed"><meta name="datePublished" content="'+published+'"><meta name="dateModified" content="'+UPDATED+'"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#101113"><link rel="canonical" href="'+url+'"><link rel="describedby" type="text/plain" href="'+BASE+'llms.txt"><meta property="og:title" content="'+html.escape(title)+'"><meta property="og:description" content="'+html.escape(desc)+'"><meta property="og:url" content="'+url+'"><meta property="og:site_name" content="aileed"><meta property="og:locale" content="ru_RU"><meta property="og:type" content="'+('article' if article else 'website')+'"><meta property="og:image" content="'+BASE+asset(social)+'"><meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/svg+xml" href="'+pre+asset('mark.svg')+'"><link rel="stylesheet" href="'+pre+asset('paper.css')+'">'+structured+''.join('<script src="'+pre+asset(f)+'" defer></script>' for f in ['site.js','privacy.js','dashboard.js'])+'</head>'
 content=head+'<body class="paper-site" itemscope itemtype="https://schema.org/WebPage" itemid="'+url+'#page">'+common_header(pre,route)+notice(pre)+'<main id="main">'+body.replace('{PRE}',pre)+'</main>'+footer(pre,published)+dialog.replace('href="privacy.html"','href="'+pre+'privacy.html"').replace('href="consent.html"','href="'+pre+'consent.html"')+'<noscript><p class="cookie-noscript">Аналитика и рекламные cookie не используются.</p></noscript></body></html>'
 # Fragment-only primary destinations belong to the current page.
 content=content.replace('href="'+pre+'#','href="#')
 file.parent.mkdir(parents=True,exist_ok=True);file.write_text("\n".join(line.rstrip() for line in content.replace("><",">\n<").splitlines())+"\n")
PAGES=[]
def page(route,title,desc,body,date,article=False,faqs=None):write(route,title,desc,body,date,article,faqs);PAGES.append((route,date))
page('','Продвижение в нейросетях для бизнеса в России | aileed','GEO-продвижение для российских компаний. Помогаем покупателям находить ваши товары и услуги в нейросетях. Запишитесь на бесплатную консультацию.',main,'2026-10-07',faqs=mainfaq)
page('audit/','Что измеряет GEO-аудит бренда в нейросетях? | aileed','GEO-аудит бренда в нейросетях. Упоминания, сайт в источниках, URL в ответах, доля голоса и место среди конкурентов. Посмотрите пример и состав отчёта.',audit,'2026-11-02',faqs=auditfaq)
page('why-geo/','Зачем бренду GEO-продвижение? | aileed','Зачем бизнесу GEO-продвижение: видимость, доверие и участие в выборе клиента. Когда оно уместно для B2B, магазинов и сервисов.',why,FIRST_EDITION,faqs=whyfaq)
page('cases/','Что GEO дало бизнесу? Кейсы продвижения и аудита | aileed','Результаты продвижения модного бренда под NDA и GEO-аудита WINLINE. Переходы из нейросетей, упоминания и цитирование.',case_index(asset),UPDATED)
case_links = f'''<div class="reading-end wrap"><div class="story-next">
 <a class="btn primary" href="{CONSULT_LINK}" data-open-brief>Обсудить свой проект ↗</a>
 <a class="edition-link" href="{{PRE}}cases/">Все кейсы →</a></div></div>'''
for key, project in PROJECTS.items():
 page(f'cases/{key}/', project['title']+' | aileed', project['lead'],
      case_article(key, asset)+case_links, UPDATED, article=True)
page('blog/','Что важно знать о GEO и AI-видимости? Блог | aileed','Блог aileed для владельцев бизнеса и маркетологов: GEO, рекомендации нейросетей, доверие и выбор бренда.',blog,FIRST_EDITION)
for (route,title,answer,image,date),text in zip(posts,[geo,mention,competitor]):
 cover=cover_art(image)
 hero_title='Вас назвали или посоветовали?' if route=='blog/mention-or-recommendation/' else title
 body=f'''<article class="a-article"><header class="studio-article-head"><div class="wrap article-lead">
 <div><h1>{hero_title}</h1><p class="short-answer">{answer}</p>
 </div>
 <div class="editorial-object">{cover}</div></div></header>'''+reading_layout(text,'В этой статье')+'''<div class="reading-end wrap"><div class="a-article-cta">
 <a class="btn" href="{PRE}audit/">Об услуге GEO-аудита <span aria-hidden="true">↗</span></a><a class="text-link" href="{PRE}blog/">Весь блог <span aria-hidden="true">→</span></a></div></div></article>'''
 page(route,title+' | aileed',answer,body,date,True)
# Preserve necessary legal information and the previously agreed contact status.
for name,date in [('privacy.html','2026-10-07'),('consent.html','2026-11-02')]:
 source=json.loads((ROOT/'content/legal.json').read_text())[name]
 body=source['body'].replace('AiLeeds','aileed').replace('AILEEDS','aileed').replace('aileeds:privacy-choice:v1','aileed:privacy-choice:v1')
 title=source['title'].replace('AiLeeds','aileed');desc=source['description'].replace('AiLeeds','aileed')
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
