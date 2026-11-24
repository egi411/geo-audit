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
 return f'''<section class="home-hero line-hero"><div class="wrap line-layout">
 <div class="line-intro"><div class="line-offer"><h1>Как стать брендом, который рекомендуют нейросети?</h1>
 <p class="short-answer">На бесплатной консультации покажем, с каких вопросов покупателей и страниц вашего сайта начать GEO-продвижение.</p>
 <div class="actions"><a class="btn primary" href="{CONSULT_LINK}" data-open-brief>Получить консультацию ↗</a>
 <a class="text-link" href="{{PRE}}cases/">Кейсы →</a></div></div>
 <div class="line-target"><strong>100<span>%</span></strong><span>Цель продвижения</span><p>Видимость в ответах на вопросы о вашем продукте.</p></div></div>
 <figure class="line-machine"><div class="machine-stage">
 <picture><source media="(max-width: 600px) and (prefers-reduced-motion: no-preference)" srcset="{{PRE}}{asset('neural-line-mobile.webp')}"><img src="{{PRE}}{asset('neural-line.webp')}" width="1280" height="440" fetchpriority="high" alt="Конвейер aileed подаёт карточки вопросов в вычислительный модуль и выводит ответ на экран."></picture>
 <video muted playsinline preload="none" aria-hidden="true" data-line-src="{{PRE}}{asset('neural-line.mp4')}" data-line-mobile="{{PRE}}{asset('neural-line-mobile.mp4')}"></video></div>
 <figcaption><span>Вопрос покупателя</span><span>Нейросеть и источники</span><span>Ответ с брендом</span></figcaption></figure>
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

def faq(items, heading='Что важно знать перед началом?', lead='Начните с продукта или услуги, по которым покупатель сравнивает вас с другими. Так будет понятно, какие ответы имеют значение для бизнеса.'):
 entries=''.join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><div class="faq-answer"><p>{a}</p></div></details>' for i,(q,a) in enumerate(items))
 return chapter('question-column',headline(heading,lead)+'<div class="question-list">'+entries+'</div>','faq'),items

def closing(audit=False):
 question='С чего начать GEO-аудит?' if audit else 'С чего начать продвижение в ИИ?'
 return chapter('brief-stage',headline(question,'На бесплатной консультации покажем, какие вопросы о вашем продукте уже задают покупатели и где стоит начать продвижение.')+f'''
 <a class="action-pill" href="{CONSULT_LINK}" data-open-brief>Записаться на консультацию <span aria-hidden="true">↗</span></a>''','brief')

def services(question, answer):
 options=[
  ('audit/','GEO-аудит','Узнайте, в каких ответах появляется ваш бренд, что о нём говорят и кого предлагают рядом.','Что входит в аудит'),
  ('why-geo/#investment','GEO-продвижение','Покупатель спрашивает про сроки, совместимость или условия. Дайте ему повод включить ваш продукт в список и посмотреть предложение.','Когда нужно продвижение')]
 figures=['<div class="service-figure audit-mini"><span class="mini-caption">GEO-аудит WINLINE</span><div class="audit-stats"><span><b>300</b> вопросов</span><i>×</i><span><b>5</b> моделей</span><i>×</i><span><b>10</b> прогонов</span></div></div>',
          '<div class="service-figure intent-mini"><span class="mini-caption">Пример выбора подрядчика</span><div class="query-slip">Кто спроектирует свет для отеля?</div><div class="proof-slip"><span aria-hidden="true">↳</span><span>Портфолио бюро<small>Освещение гостиниц</small></span></div></div>']
 items=[]
 for (route,name,reason,link),figure in zip(options,figures):
  fields='<div class="dossier-fields"><span>В отчёте</span><b>Упоминания</b><b>Источники</b><b>Ссылки</b></div>' if route=='audit/' else ''
  items.append(f'<a class="service-tile" href="{{PRE}}{route}">{figure}<div class="service-description">{fields}<strong>{name}</strong><p>{reason}</p></div><span class="tile-action">{link} <span aria-hidden="true">↗</span></span></a>')
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

main=home_hero()+buyer_scenarios()
main+=services('Аудит или продвижение?','Аудит покажет, что покупатели видят сейчас. Продвижение помогает бренду появляться в ответах о тех товарах и услугах, которые он продаёт.')
commonfaq=[('Можно гарантировать рекомендацию нейросети?','Нет. Даже один покупатель может получить другой список, когда уточнит город, бюджет или требования к продукту.'),('GEO заменяет SEO?','Нет. SEO помогает покупателю найти вашу страницу через поиск. GEO помогает ему встретить ваш бренд, когда он просит нейросеть сравнить варианты.'),('Упоминание бренда уже означает продажу?','Покупатель может увидеть знакомое название и уйти к конкуренту. Продажу подтверждает сделка, а связь с рекомендацией помогают проверить переходы и обращения.'),('Можно начать с отдельного аудита?','Да. Вы получите отчёт и сможете передать его своей команде. Продвижение можно обсудить отдельно.')]
home_questions,mainfaq=faq(commonfaq)
# Detail pages.
why=hero('Зачем бренду <span>GEO?</span>','Чтобы покупатель учитывал вашу компанию, когда спрашивает у нейросети, к кому обратиться или что купить.','Если нейросеть назвала двух конкурентов, именно их предложения клиент может открыть первыми. Стоит узнать, попадаете ли вы в этот список и что о вас говорят.',('Посмотреть пример аудита','audit/#observations'),('Упоминания и цитирования','#visibility'))
why+=frequency_figure()
why+=chapter('investment-feature',f"""
 <div class="investment-spread" id="investment">{scene_image('scene-hotel','Модель гостиницы с подсвеченными окнами и фасадом','(max-width: 700px) 95vw, 80vw')}
 <div class="investment-copy"><h2>Когда GEO стоит вложений?</h2>
 <p class="short-answer">Когда вас сравнивают до первого звонка.</p>
 <p>Владелец отеля спрашивает, кому заказать освещение фасада. В ответе два бюро. Оба делают свет, но только у одного есть ссылка на готовую гостиницу. Именно этот проект заказчик может переслать архитектору.</p>
 <p>Если клиенты уже приходят с таким списком, начните с одного вопроса из переговоров. Посмотрите, кого назвали и чей проект привели в пример.</p>
 {arrow_link('audit/#sample-board','Разобрать пример ответа')}</div></div>""")
why+=chapter('demand-guide', headline('Когда GEO помогает продажам?','Когда покупатель сравнивает варианты до звонка или заявки. Посмотрите, что ему нужно узнать, чтобы включить вашу компанию в короткий список.')+"""
 <dl class="demand-list"><div><dt>Услуги для бизнеса</dt><dd>Заказчик ищет подрядчика с опытом в своей отрасли. Если нейросеть называет бюро и ссылается на кейс похожего отеля, у заказчика появляется конкретный проект для обсуждения с коллегами.</dd></div>
 <div><dt>Товары</dt><dd>Покупателю нужна кофемолка определённой ширины. Названия марки мало: важны модель, габариты и ссылка на карточку, где их можно сверить.</dd></div>
 <div><dt>Онлайн-сервисы</dt><dd>У сети салонов общая база клиентов и два расписания. При сравнении сервисов решающим может стать один факт — умеет ли продукт вести оба филиала в одной учётной записи.</dd></div></dl>""",'demand')
why+=chapter('decision-guide',headline('Как понять, окупается ли продвижение?','Разберите путь от вопроса до обращения. На каждом шаге бизнесу нужны свои данные.')+"""
 <ol class="decision-path"><li><strong>Вопрос</strong><p>Выберите ситуацию из реальных переговоров. По каким вопросам нейросети называют вас, а по каким — только конкурентов?</p></li>
 <li><strong>Переход</strong><p>Проверьте, на какую страницу ведёт ссылка. В аналитике посмотрите, сколько посещений удалось отнести к нейросетям и что посетители делали дальше.</p></li>
 <li><strong>Обращение</strong><p>Сопоставьте обращения с записями в CRM. Если клиент позвонил напрямую, спросите, где он впервые услышал о вас. Особенно ценны заявки по тем услугам, которые вы хотите продавать.</p></li></ol>"""+arrow_link('cases/fashion/','Посмотреть кейс с переходами'),'outcome')
why_questions,whyfaq=faq([
 ('С какого продукта начать?', 'С продукта, который покупатель сравнивает с альтернативами. Возьмите вопрос из переговоров и посмотрите, какие компании и источники покупатель увидит в ответе.'),
 ('Когда можно отложить GEO?', 'Если большинство заказов приходит по персональному приглашению и клиенты уже выбрали поставщика, сначала выясните, участвуют ли нейросети в вашем цикле продаж.'),
 ('Что считать результатом для бизнеса?', 'Сначала проверьте, появляется ли бренд в ответах на вопросы покупателей. Затем посмотрите на переходы, целевые обращения и сделки, для которых удалось установить источник.')],
 'Что учесть перед вложениями в GEO?', 'Выбор зависит от того, как покупатели ищут ваш продукт и какие обращения важны для продаж.')
why+=why_questions+closing()
def audit_opening():
 return """<header class="audit-opening wrap"><h1>Называет ли ИИ <span>ваш бренд?</span></h1>
 <p class="short-answer">GEO-аудит покажет, где вас упоминают, кому достаются ссылки и какие конкуренты появляются в ответах вместо вас.</p>
 <div class="actions"><a class="btn primary" href="#observations">Посмотреть отчёт на 100 промптах <span aria-hidden="true">↓</span></a>
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
  <div class="sample-coding">
  <dl>{flags}</dl></div><p class="sample-result">{conclusion}</p></div>''')
 return f'''<section class="answer-lab wrap" id="sample">
 <header class="console-title"><div><h2>Что видно в одном ответе?</h2>
 <p class="short-answer">Переключите пример и посмотрите, какие признаки попадут в отчёт.</p></div>
 <span class="demo-label">Учебный пример</span></header>
 <div id="sample-board" class="sample-board">
 <div class="sample-top"><div><span>Вопрос покупателя</span><b>Какой сервис поддержки подойдёт небольшой команде?</b></div>
 <fieldset class="sample-choices"><legend>Вариант ответа</legend>{"".join(tabs)}</fieldset></div>
 <div class="sample-variants">{"".join(cards)}</div></div>
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
 return chapter('report-delivery',headline('Что команда получит на руки?','Отчёт с выводами, таблицу для команды и исходные ответы. В аудите WINLINE выводы заняли 26 слайдов, а данные и рекомендации — 12 листов рабочей книги.')+
 '<div class="delivery-list">'+''.join(f'<div><span>{team}</span><strong>{name}</strong><p>{desc}</p></div>' for team,name,desc in rows)+'</div>','report')

audit=audit_opening()+observation_figure()+answer_sample()+metric_sheet()+competitor_sheet()+deliverables()
x,auditfaq=faq([('Можно ли увидеть реальные ответы из моего аудита?','Да. В приложении доступны тексты, ссылки, даты, модели и статусы замеров. По ним команда может проверить выводы отчёта.'),('Что покажут вопросы без названия компании?','В каких ситуациях ассистент сам назвал бренд. Вопросы с названием мы разбираем отдельно. По ним видно, как ИИ описывает уже известную покупателю компанию.'),('Аудит покажет продажи из ИИ?','Для выводов о продажах нужны данные аналитики и CRM. Аудит показывает содержание ответов, упоминания и ссылки в пределах исследованной выборки.'),('Можно использовать результат со своей командой?','Да. Таблица связывает наблюдения с вопросами и страницами. Задачи можно передать своей редакции, продуктовой команде или разработчикам.')])
audit+=x+closing(True)

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

main+=home_questions+closing()
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
def notice(pre):return '<aside id="cookie-banner" class="cookie-banner a-cookie wrap" aria-labelledby="cookie-title" hidden><div><h2 id="cookie-title">Какие cookie используются?</h2><p class="short-answer">Только необходимые настройки. Аналитика не подключена.</p></div><a href="'+pre+'privacy.html#cookies">Подробнее</a><button type="button" class="btn" data-cookie-accept>Понятно</button></aside>'
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
page('','Как стать брендом, который рекомендуют нейросети? | aileed','GEO-продвижение бренда в ChatGPT, Алисе и других нейросетях. Бесплатный разбор, кейсы и реальные показатели упоминаний и цитирований.',main,'2026-10-07',faqs=mainfaq)
page('audit/','Что измеряет GEO-аудит бренда в нейросетях? | aileed','GEO-аудит бренда в нейросетях. Упоминания, сайт в источниках, URL в ответах, доля голоса и место среди конкурентов. Посмотрите пример и состав отчёта.',audit,'2026-11-02',faqs=auditfaq)
page('why-geo/','Зачем бренду GEO-продвижение? | aileed','Зачем бизнесу GEO-продвижение: видимость, доверие и участие в выборе клиента. Когда оно уместно для B2B, магазинов и сервисов.',why,FIRST_EDITION,faqs=whyfaq)
page('cases/','Что GEO дало бизнесу? Кейсы продвижения и аудита | aileed','Два кейса с исходными презентациями: модный бренд под NDA и GEO-аудит WINLINE. Переходы из нейросетей, упоминания и цитирование.',case_index(asset),UPDATED)
case_links = f'''<div class="story-next wrap">
 <a class="btn primary" href="{CONSULT_LINK}" data-open-brief>Обсудить свой проект ↗</a>
 <a class="edition-link" href="{{PRE}}cases/">Все кейсы →</a></div>'''
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
 <div class="editorial-object">{cover}</div></div></header>'''+reading_layout(text,'В этой статье')+'''<div class="wrap a-article-cta">
 <a class="btn" href="{PRE}audit/">Об услуге GEO-аудита <span aria-hidden="true">↗</span></a><a class="text-link" href="{PRE}blog/">Весь блог <span aria-hidden="true">→</span></a></div></article>'''
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
