#!/usr/bin/env python3
"""Render aileed's static pages. Use --base-url only when the domain is ready."""
from pathlib import Path
import argparse,json,re,html,hashlib
from xml.sax.saxutils import escape
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
 return f'''<section class="studio-hero studio-{profile}" data-quote-stage>
   <div class="wrap studio-hero-layout"><div class="studio-intro">
   <h1>{h}</h1><p class="short-answer">{a}</p><p class="a-lead">{p}</p>
   <div class="actions"><a class="btn primary" href="{{PRE}}{primary[1]}">{primary[0]} <span aria-hidden="true">↗</span></a>
   <a class="text-link" href="{{PRE}}{secondary[1]}">{secondary[0]} <span aria-hidden="true">→</span></a></div></div>
   <div class="studio-showcase"><div class="studio-floor" aria-hidden="true"></div>
   <div class="quote-objects studio-object"><img class="quote-body" data-profile="{profile}" src="{{PRE}}{product}" width="724" height="724" alt="{alt}" fetchpriority="high">
   <canvas class="quote-canvas" aria-hidden="true"></canvas></div></div></div>
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
     <div class="actions"><a class="btn primary" href="{{PRE}}audit/">Проверить AI-видимость <span aria-hidden="true">↗</span></a>
     <a class="text-link" href="{{PRE}}why-geo/">Зачем бренду GEO <span aria-hidden="true">→</span></a></div>
   </div>

 </section>"""
def chapter(name, content, anchor=''):
 anchor = f' id="{anchor}"' if anchor else ''
 return f'<section class="edition {name}"{anchor}><div class="wrap">{content}</div></section>'

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
 return chapter('question-column',headline('Что важно знать перед началом?','До начала работ определите, какой выбор покупателя вам важно изучить. Ниже — о границах услуги и использовании отчёта.')+'<div class="question-list">'+entries+'</div>','faq'),items

def closing(audit=False):
 question='С чего начать GEO-аудит?' if audit else 'С чего начать продвижение в ИИ?'
 return chapter('brief-stage',headline(question,'Опишите ваш продукт и тех, кто его выбирает. Бриф можно сохранить в TXT и обсудить с командой.')+'''
 <button class="action-pill" type="button" data-open-brief>Составить бриф <span aria-hidden="true">↗</span></button>''','brief')

platforms=[('ChatGPT','chatgpt'),('Claude','claude'),('Grok','grok'),('Gemini','gemini'),('Алиса','alice'),('GigaChat','gigachat')]
def brand_mark(name, key):
 return img('brands/'+key+'.svg','Логотип '+name,'brand-mark'+(' brand-mono' if key in ['grok','gigachat'] else ''))

strip='<nav class="a-model-strip wrap" id="platforms" aria-label="Продвижение по платформам">'+''.join(f'<a href="{{PRE}}platforms/#tab-{k}">'+brand_mark(n,k)+n+'</a>' for n,k in platforms)+'</nav>'

def services(question, answer):
 options=[
  ('audit/','GEO-аудит','Узнайте, в каких ответах появляется ваш бренд, что о нём говорят и кого предлагают рядом.','report','Стеклянные листы отчёта о видимости бренда','Что входит в аудит'),
  ('platforms/','GEO-продвижение','Помогите покупателю встретить ваш продукт в ответе ассистента и понять, чем он подходит.','answer-display','Объёмная реплика из стекла над экраном смартфона','Выбрать платформу')]
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
  ('b2b','Услуги B2B','Кто спроектирует освещение для небольшого отеля?','Заказчику важно увидеть бюро с опытом в гостиницах. Так он решает, у кого запросить портфолио.','scene-hotel','Архитектурный макет отеля с подсветкой фасада и гостевых комнат'),
  ('retail','Товары','Какую кофемолку выбрать для эспрессо на маленькой кухне?','Покупатель ищет подходящую модель. Размер корпуса и качество помола для него важнее известности марки.','scene-grinder','Компактная металлическая кофемолка для эспрессо на кухонной столешнице'),
  ('saas','SaaS','Какой сервис записи подойдёт двум салонам с общей базой клиентов?','Владелец сравнивает сервисы под свой сценарий. Ему важно понимать, можно ли вести расписания двух филиалов вместе.','scene-booking','Планшет с расписанием приёмов на стойке салона')]
 choices=[]; panels=[]
 for i,(key,label,prompt,comment,photo,alt) in enumerate(examples):
  choices.append(f'<label><input type="radio" name="buyer" value="{key}"'+(' checked' if i==0 else '')+f'><span>{label}</span></label>')
  art=scene_image(photo,alt,'(max-width: 700px) 100vw, (max-width: 1400px) 82vw, 1200px')
  panels.append(f'<figure class="buyer-example" data-buyer="{key}"><div class="buyer-photo" data-scene>{art}</div><figcaption><span class="prompt-label">Пример запроса</span><blockquote>{prompt}</blockquote><p>{comment}</p></figcaption></figure>')
 return chapter('buyer-stage',headline('Как покупатель выбирает бренд в ИИ?','Клиент описывает задачу нейросети и получает варианты ещё до перехода на сайт. Выберите свой рынок.')+'<div class="scenario-view" id="business"><fieldset class="buyer-controls"><legend>Сфера бизнеса</legend>'+''.join(choices)+'</fieldset><div class="buyer-examples">'+''.join(panels)+'</div></div>','value')

main=quote_stage()+strip+buyer_scenarios()
main+=services('Аудит или продвижение?','Начните с аудита, если хотите оценить видимость сегодня. Выбирайте продвижение, если задача — чаще попадать в выбор клиента.')
commonfaq=[('Можно гарантировать рекомендацию нейросети?','Нет. Ответы зависят от платформы и контекста пользователя. GEO развивает присутствие бренда, но не даёт контроля над чужой выдачей.'),('GEO заменяет SEO?','Нет. SEO помогает находить страницы в поиске, а GEO обращается к представлению бренда внутри AI-ответа. Для бизнеса эти направления могут дополнять друг друга.'),('Упоминание бренда уже означает продажу?','Нет. Между знакомством, сравнением и обращением есть разница. Пользу GEO для бизнеса нужно оценивать отдельно от самого факта упоминания.'),('Можно начать с отдельного аудита?','Да. Аудит — самостоятельная услуга. Решение о дальнейшем продвижении принимается отдельно.')]
home_questions,mainfaq=faq(commonfaq)
# Detail pages.
why=hero('Зачем бренду <span>GEO?</span>','GEO-продвижение помогает участвовать в выборе покупателя, когда тот обращается за рекомендацией к ИИ.','Ваш продукт может подходить клиенту, но остаться за пределами его списка вариантов. GEO помогает бизнесу развивать присутствие в этой точке выбора.','shortlist','Стеклянная карточка выделена среди двух металлических альтернатив',('Понять текущую видимость','audit/'),('Выбрать платформу','platforms/'))
why+=chapter('choice-story',headline('Где бренд теряет покупателя?','В ответе ассистента выбор может сузиться ещё до знакомства с сайтом.')+"""
 <div class="choice-flow"><figure class="decision-scene" data-scene>"""+scene_image('scene-hotel','Гостиница с подсветкой фасада и номеров','(max-width:700px) 95vw, 55vw')+"""<figcaption><span>Вопрос заказчика</span><blockquote>Кому доверить освещение нового отеля?</blockquote></figcaption></figure><dl class="choice-lines"><div><dt>Вас пропустили</dt><dd>Подходящий заказчик видит других подрядчиков и может вообще не узнать о вашей компании.</dd></div>
 <div><dt>Вас перепутали</dt><dd>Устаревшее описание услуги отсекает клиентов, которым на самом деле подходит ваш продукт.</dd></div>
 <div><dt>Вас не отличили</dt><dd>Название есть среди вариантов, но покупателю неясно, в чём ваше преимущество.</dd></div></dl></div>""")
why+=chapter('platform-priority investment-cases',headline('Когда GEO стоит вложений?','Когда клиент ещё не выбрал поставщика и задаёт ИИ вопрос о категории, условиях или альтернативах.')+"""<div class="priority-note"><strong>Сравнение подрядчиков</strong><p>Если отдел продаж слышит «нам предложили вас и ещё две компании», важно понять, какой аргумент ассистент приводит в пользу каждой. Одного упоминания имени для ответа мало.</p></div>
 <div class="priority-note"><strong>Выбор конкретной модели</strong><p>Если покупателю нужна кофемашина определённой ширины, имеют значение модель, габариты и ссылка на карточку товара. Упоминание категории не решает задачу выбора.</p></div>
 <div class="priority-note"><strong>Решение о бюджете</strong><p>Аудит покажет вопросы, в которых появляются конкуренты без вас. Чтобы связать присутствие с продажами, отдельно смотрят переходы, обращения и данные CRM.</p></div>"""+arrow_link('audit/#competitors','Посмотреть показатели конкурентов'))
why+=services('С какой задачи начать?','Выберите между оценкой текущей видимости и работой над присутствием бренда в рекомендациях.')+closing()
def audit_opening():
 return """<header class="audit-opening wrap"><h1>Называет ли ИИ <span>ваш бренд?</span></h1>
 <p class="short-answer">GEO-аудит покажет, где вас упоминают, кому достаются ссылки и какие конкуренты появляются в ответах вместо вас.</p>
 <div class="actions"><a class="btn primary" href="#sample">Разобрать пример <span aria-hidden="true">↓</span></a>
 <a class="text-link" href="#results">Посмотреть метрики <span aria-hidden="true">↗</span></a></div></header>"""

def metric_sheet():
 metrics=[
  ('text','Упоминание бренда','Название встречается в основном тексте.','Повтор названия в одном ответе засчитывается один раз. Название только в адресе или в подписи ссылки сюда не входит.'),
  ('sources','Сайт в источниках','Домен есть в списке источников ответа.','Несколько страниц одного сайта дают одно попадание за замер. Источник может остаться за пределами текста, который видит покупатель.'),
  ('url','URL в ответе','Полный адрес сайта встроен в сам ответ.','Считается и ссылка под словом. В отчёте видно, на какую страницу ведёт адрес — на карточку продукта, обзор или главную.')]
 rows=''.join(f'<div class="metric-cell"><div class="metric-sculpture"><img src="{{PRE}}{asset("object-"+key+".webp")}" width="512" height="512" loading="lazy" alt="{name}" aria-hidden="true"></div><dt>{name}</dt><dd><strong>{definition}</strong><p>{detail}</p></dd></div>' for key,name,definition,detail in metrics)
 return chapter('metric-sheet',headline('Что измеряет GEO-аудит?','Три показателя отвечают на разные вопросы. Для каждого вы увидите число попаданий и его долю в выбранной группе замеров.')+f'<dl class="metric-ledger">{rows}</dl>'+'''<div class="measure-base"><strong>Откуда берётся процент?</strong><p>Число замеров с признаком делится на все попытки в выбранной группе. Один замер — один вопрос одной модели в одном повторе. Отказы и ошибки остаются в базе и показаны отдельно. Доли трёх признаков могут пересекаться.</p></div>''','results')

def answer_sample():
 samples=[
  ('name','Название','Для команды из пяти человек подойдёт <mark>Линия</mark>. В ней можно назначить ответственного за заявку.','Обзор сервисов поддержки · отраслевое издание','Есть','Нет','Нет','Покупатель узнал название. Чтобы открыть сайт компании, ему придётся искать его отдельно.'),
  ('source','Источник','Сравните, можно ли объединять обращения из почты и чата и назначать ответственного.','<mark>linea.example/help/inbox</mark> · документация сервиса','Нет','Есть','Нет','Страница продукта попала в источники. В тексте ответа покупатель увидел только критерии выбора.'),
  ('link','Ссылка','У <mark>Линии</mark> есть общий ящик для команды. Инструкция по настройке — <mark>https://linea.example/help/inbox</mark>.','Список источников отсутствует в этом примере','Есть','Нет','Есть','У покупателя есть путь к конкретной инструкции. Фактический переход проверяют отдельно в аналитике сайта.')]
 tabs=[];cards=[]
 for i,(key,label,line,refs,brand,src,url,conclusion) in enumerate(samples):
  tabs.append(f'<label><input type="radio" name="sample" value="{key}"'+(' checked' if i==0 else '')+f'><span>{label}</span></label>')
  flags=''.join(f'<div><dt>{name}</dt><dd class="flag-{"yes" if status=="Есть" else "no"}">{status}</dd></div>' for name,status in [('Имя в тексте',brand),('Сайт в источниках',src),('URL в ответе',url)])
  cards.append(f'''<div class="answer-variant" data-variant="{key}">
  <div class="sample-output"><span>Ответ ассистента</span><blockquote>{line}</blockquote>
  <p class="sample-source"><b>Источники</b> {refs}</p></div>
  <div class="sample-coding"><img class="indicator-poster" src="{{PRE}}{asset("indicator-"+key+".webp")}" width="600" height="400" alt="Индикатор присутствия бренда" aria-hidden="true">
  <dl>{flags}</dl></div><p class="sample-result">{conclusion}</p></div>''')
 return f'''<section class="answer-lab wrap" id="sample">
 <header class="console-title"><div><h2>Что видно в одном ответе?</h2>
 <p class="short-answer">Переключите пример и посмотрите, какие признаки попадут в отчёт.</p></div>
 <span class="demo-label">Учебный пример</span></header>
 <div class="sample-board" data-indicator="{{PRE}}{asset("indicator-frames.webp")}">
 <div class="sample-top"><div><span>Вопрос покупателя</span><b>Какой сервис поддержки подойдёт небольшой команде?</b></div>
 <fieldset class="sample-choices"><legend>Вариант ответа</legend>{"".join(tabs)}</fieldset></div>
 <div class="sample-variants">{"".join(cards)}<div class="animated-indicator" aria-hidden="true"><canvas width="420" height="280"></canvas></div></div></div>
 <p class="sample-note">«Линия» — вымышленный сервис.</p></section>'''

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
 ('Маркетингу','Карта спроса','По каждой теме — вопрос покупателя, частота упоминания, конкуренты и страницы, которые появились в источниках. Видно, где у бренда уже есть присутствие, а где его предстоит развивать.'),
 ('Продукту и PR','Контекст репутации','Фрагменты ответов с характеристиками продукта, оговорками и оценками. Условия и спорные утверждения выделены для сверки с действующим предложением.'),
 ('Редакции и разработке','Приоритеты по страницам','Для конкретного URL собраны наблюдение, подтверждающий пример и задача по содержанию или доступности страницы. Команда может вернуться к тому же вопросу после изменений.')]
 return chapter('report-delivery',headline('Что команда получит на руки?','Отчёт с выводами, рабочую таблицу и приложение с ответами. Каждый вывод можно проследить до вопроса, модели, даты и источника.')+
 '<div class="delivery-list">'+''.join(f'<div><div class="report-glyph glyph-{i}" aria-hidden="true"><i></i><i></i><i></i></div><span>{team}</span><strong>{name}</strong><p>{desc}</p></div>' for i,(team,name,desc) in enumerate(rows))+'</div>','report')

platformbody=hero('Где продвигать <span>бренд в ИИ?</span>','Начните с вопросов, которые ваши покупатели задают в ChatGPT, Алисе и других ассистентах.','Здесь — шесть примеров выбора продукта. В каждом разборе есть вопрос клиента, признак видимости и решение для вашей команды.','dialogue','Две реплики из дымчатого стекла и меди',('Сравнить платформы','#compare'),('Посмотреть метрики','audit/#results'))
platform_cases=[
 ('Какие сервисы попадут в шорт-лист?','В ChatGPT покупатель может уточнять требования по ходу диалога. При веб-поиске ответ может содержать ссылки на источники.','Выбор SaaS','Какой сервис записи выбрать для двух салонов? А если нужна единая база клиентов?','Остался ли бренд в списке после уточнения, какую функцию ему приписали и есть ли ссылка на страницу этой функции.','Если продукт исчез после уточнения, маркетинг увидит, какое требование клиента стоит яснее раскрыть на сайте.','https://help.openai.com/en/articles/9237897-searching-the-web-with-chatgpt','О поиске в ChatGPT'),
 ('Какой подрядчик отвечает условиям закупки?','В Claude закупщик может попросить сопоставить предложения по своим критериям и проверить основания для вывода.','Закупка B2B','Сравни подрядчиков для внедрения CRM. Кто поддерживает миграцию истории и фиксирует условия поддержки в договоре?','По какому критерию упомянута компания, какой фрагмент подтверждает вывод и куда ведёт цитата при включённом поиске.','Команда продаж получит список спорных характеристик для сверки с договором и документацией.','https://support.claude.com/en/articles/10684626-enable-and-use-web-search','О веб-поиске Claude'),
 ('Какое впечатление создают отзывы?','В Grok с поиском по X можно исследовать публичное обсуждение продукта и отделить слова пользователей от заявлений компании.','Репутация продукта','Что пишут о стабильности сервиса после обновления? Какие сообщения относятся к новой версии?','Какая претензия повторяется, датирована ли публикация и относится ли она к текущей версии. Подтверждённые факты отмечаются отдельно.','PR увидит, какой вопрос уже получил официальный ответ и где покупателю всё ещё доступен только старый отзыв.','https://docs.x.ai/developers/tools/x-search','О поиске по X'),
 ('Какую модель посоветуют купить?','В Gemini покупатель может сравнить несколько моделей товара. Ссылки в ответе дают возможность проверить отдельные характеристики.','Выбор товара','Сравни узкие посудомоечные машины для кухни шириной 45 см. У какой есть короткая программа?','Какую модификацию назвали, совпадают ли размеры и комплектация, ведёт ли ссылка к производителю или в каталог магазина.','Категорийный менеджер увидит, какую карточку нужно уточнить, если ИИ смешивает соседние модели.','https://support.google.com/gemini/answer/14143489','Об источниках в Gemini'),
 ('Кого найдут рядом с домом?','Для локального бизнеса в ответе Алисы особенно важны филиал, адрес и нужная услуга. Эти сведения покупатель использует, чтобы выбрать, куда обратиться.','Локальные услуги','Где в Казани починят кофемашину с выездом в Советский район?','Назван ли нужный филиал, совпадают ли район и условия выезда, какой источник указан для проверки. Город фиксируется вместе с вопросом.','Владелец увидит, куда может уйти обращение, если ассистент назвал закрытый филиал или чужой телефон.','https://alice.yandex.ru/','Об Алисе'),
 ('Верно ли покупатель понял условия?','В GigaChat можно проверить, как русскоязычному покупателю объясняют условия сервиса и различия между тарифами.','Условия сервиса','На каком тарифе можно подключить второй склад? Входит ли загрузка остатков в базовый пакет?','Что ответ обещает пользователю, упоминает ли ограничения и совпадает ли формулировка с действующим описанием тарифа.','Продуктовая команда увидит конкретную фразу, из-за которой клиент может прийти с неверными ожиданиями.','https://giga.chat/','О GigaChat')]
panel_tabs=''.join(f'<button role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}">{brand_mark(n,k)}{n}</button>' for i,(n,k) in enumerate(platforms))
panel_bodies=[]
for (name,key),(q,answer,topic,prompt,measure,decision,url,ref) in zip(platforms,platform_cases,strict=True):
 panel_bodies.append(f'''<div role="tabpanel" id="panel-{key}" aria-labelledby="tab-{key}" tabindex="0">
 <div class="platform-context"><span>{topic}</span><h3>{q}</h3><p class="short-answer">{answer}</p>
 <figure><figcaption>Пример вопроса покупателя</figcaption><blockquote>{prompt}</blockquote></figure></div>
 <div class="platform-insight"><div class="platform-trace" aria-hidden="true"><i class="trace-question"></i><i class="trace-wire"></i><i class="trace-hub">{brand_mark(name,key)}</i><i class="trace-wire"></i><i class="trace-answer"></i></div><dl><div><dt>Что фиксируем</dt><dd>{measure}</dd></div><div><dt>Решение для команды</dt><dd>{decision}</dd></div></dl><a href="{url}">{ref} ↗</a></div></div>''')
platformbody+=chapter('platform-atlas',headline('Что проверять по платформам?','Выберите ассистента и разберите покупательский вопрос. Это примеры для разных рынков. Для вашего бренда сравнение строится вокруг его продукта и аудитории.')+f'<div class="atlas-stage"><div class="atlas-tabs" role="tablist" aria-label="AI-платформы">{panel_tabs}</div><div class="atlas-panels">{"".join(panel_bodies)}</div></div>','compare')
platform_map='<nav class="assistant-orbit" aria-label="Перейти к разбору платформы"><span class="orbit-core" aria-hidden="true"></span>'+''.join(f'<a href="#tab-{key}" aria-label="Разбор {name}">{brand_mark(name,key)}</a>' for name,key in platforms)+'</nav>'
platformbody+=chapter('platform-priority assistant-choice',headline('С какой площадки начать?','Выберите ту, которую клиенты называют в разговорах с продажами. Если таких данных пока нет, сравните ответы на один коммерческий вопрос в нескольких ассистентах.')+'''<div class="priority-note"><strong>Сравнивайте сопоставимое</strong><p>Сохраните формулировку вопроса, дату, регион и режим поиска. Ответ из API и ответ в приложении могут различаться. Отсутствие списка источников в одном режиме учитывается отдельно.</p></div>'''+arrow_link('audit/#results','Какие метрики войдут в аудит')+platform_map)+closing()
audit='<div class="audit-stage">'+audit_opening()+answer_sample()+'</div>'+strip+metric_sheet()+competitor_sheet()+deliverables()
x,auditfaq=faq([('Можно ли увидеть реальные ответы из моего аудита?','Да. В приложении доступны тексты, ссылки, даты, модели и статусы замеров. По ним команда может проверить выводы отчёта.'),('Что покажут вопросы без названия компании?','В каких ситуациях ассистент сам назвал бренд. Вопросы с названием выделены отдельно — они показывают, как ИИ описывает уже известную покупателю компанию.'),('Аудит покажет продажи из ИИ?','Для выводов о продажах нужны данные аналитики и CRM. Аудит показывает содержание ответов, упоминания и ссылки в пределах исследованной выборки.'),('Можно использовать результат со своей командой?','Да. Таблица связывает наблюдения с вопросами и страницами. Задачи можно передать своей редакции, продуктовой команде или разработчикам.')])
audit+=x+closing(True)

# Editorial pages explain customer choices, not the agency's execution playbook.
posts=[('what-is-geo/','Что такое GEO и зачем оно бизнесу?','GEO — работа с присутствием сайта и бренда в ответах генеративных систем.','studio-dialogue.webp','2026-11-04'),('blog/mention-or-recommendation/','Упоминание бренда — это уже рекомендация?','Нет. Название в ответе ещё не означает, что ассистент предлагает выбрать именно вас.','quote-glass.webp',TODAY),('blog/why-ai-recommends-competitors/','Почему ИИ рекомендует конкурентов?','Ответ может отличаться от привычной картины поисковой выдачи и узнаваемости на рынке.','studio-shortlist.webp',TODAY)]
cover_alt={
 'studio-dialogue.webp':'Реплики из дымчатого стекла и металла',
 'quote-glass.webp':'Объёмная кавычка из янтарного стекла',
 'studio-shortlist.webp':'Стеклянная карточка на переднем плане среди вариантов',
}
def story_shelf(items, heading):
 artwork={
  'what-is-geo/':('prism','Свет преломляется на гранях прозрачной призмы'),
  'blog/mention-or-recommendation/':('mention','Пара металлических и стеклянных кавычек'),
  'blog/why-ai-recommends-competitors/':('choice','Медное ребро выделяет один из трёх объектов'),
 }
 rows=[]
 for route,title,answer,_,date in items:
  cover,alt=artwork[route]
  rows.append(f'''<article class="shelf-story"><a href="{{PRE}}{route}">
  <div class="shelf-art"><img src="{{PRE}}{asset("cover-"+cover+".webp")}" width="1024" height="504" alt="{alt}" loading="lazy"></div>
  <div class="shelf-words"><{heading}>{title}</{heading}><p class="short-answer">{answer}</p></div><span class="shelf-arrow" aria-hidden="true">↗</span></a></article>''')
 return '<div class="story-shelf">'+''.join(rows)+'</div>'

main+=chapter('journal-shelf',headline('Что почитать о выборе бренда в ИИ?','Три материала для тех, кто отвечает за продвижение бизнеса.')+story_shelf(posts,'h3')+arrow_link('blog/','Весь блог'),'blog')+home_questions+closing()
blog='''<section class="journal-opening"><div class="wrap"><h1>Что читать <span>о GEO?</span></h1>
 <p class="short-answer">Блог aileed о видимости, доверии и роли AI-ответов в решениях покупателей.</p></div></section>'''+chapter('journal-shelf archive-edition',story_shelf(posts,'h2'))

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
geo=prose('Чем GEO отличается от SEO?','SEO относится к видимости страниц в поиске, а GEO — к представленности внутри AI-ответа.',['Пользователь может увидеть список ссылок и самостоятельно перейти на сайты. В диалоге с ассистентом он также может получить краткое объяснение, сравнение или несколько подходящих вариантов. Для бизнеса это разные точки контакта.','GEO не отменяет SEO. Google указывает, что для AI Overviews и AI Mode сохраняют актуальность обычные требования к страницам и основы SEO. Специальная разметка не гарантирует присутствие в ответе. <a href="https://developers.google.com/search/docs/appearance/ai-features">Официальная документация Google</a>.'])
geo+=prose('А что означает AEO?','Обычно так называют направление, связанное с прямыми ответами на вопросы пользователя.',['В маркетинговых описаниях GEO и AEO могут пересекаться. При выборе услуги полезнее уточнить, какую задачу бизнеса она решает и какой результат вы получаете, чем ориентироваться только на аббревиатуру.'])
geo+=prose('Зачем это владельцу бизнеса?','Чтобы понимать, участвует ли бренд в выборе клиента внутри AI-ответа.',['Для компании важно не только быть найденной, но и быть правильно понятой. Если ассистент не называет бренд либо неверно описывает продукт, потенциальный покупатель может не рассмотреть предложение.','Это особенно значимо при сравнении подрядчиков, товаров или сервисов. Но само упоминание не равно обращению и не доказывает рост выручки.'])
geo+=prose('Можно ли купить гарантированную рекомендацию?','Обещание контроля над всеми ответами нейросети не соответствует характеру этой среды.',['Ответы зависят от платформы, вопроса и контекста пользователя. Результаты отдельного исследования нельзя автоматически переносить на весь рынок или на всех пользователей.','Исходная научная работа <a href="https://arxiv.org/abs/2311.09735">GEO: Generative Engine Optimization</a> рассматривает видимость контента в генеративных ответах. Её экспериментальные показатели не являются обещанием эффекта для конкретного бизнеса.'])
geo+=prose('С какой услуги начать знакомство с GEO?','С той, которая отвечает на ваше главное неизвестное.',['Если пока непонятно, как ИИ представляет компанию, полезен <a href="{PRE}audit/">GEO-аудит</a>. Если задача — развивать присутствие бренда, рассмотрите <a href="{PRE}platforms/">направления продвижения</a>.','Для оценки бизнес-смысла есть отдельная страница <a href="{PRE}why-geo/">«Зачем бренду GEO-продвижение?»</a>.'])
mention=prose('В чём разница для покупателя?','Упоминание знакомит с названием, рекомендация предлагает рассмотреть его как подходящий выбор.',['Нейтральная справка о компании и предложение обратиться именно к ней выполняют разные роли. В первом случае пользователь узнаёт о существовании бренда. Во втором — получает основание включить его в список вариантов.','Поэтому фраза «наш бренд есть в ответах ИИ» сама по себе мало говорит о коммерческой ценности такого присутствия. Важен смысл, в котором компания представлена.'])
mention+=prose('Как это выглядит в обычном ответе?','У одного названия могут быть разные роли в диалоге.',['Иллюстративные формулировки: «Компания работает в этой категории» — справочное упоминание. «Для вашей задачи можно рассмотреть эту компанию» — предложение альтернативы. «С учётом ваших условий этот вариант подходит» — более выраженная рекомендация.','Это примеры языка ответа, а не результаты исследования конкретного бренда. Ни одна из таких фраз сама по себе не доказывает состоявшуюся продажу.'])
mention+=prose('Всегда ли больше упоминаний лучше?','Нет, если они не связаны с нужной аудиторией или искажают предложение.',['Бренд может встречаться в нерелевантной категории, устаревшем описании или критическом контексте. Такое присутствие нельзя автоматически считать успехом продвижения.','Полезный вопрос для бизнеса: помогает ли это представление компании покупателю рассмотреть подходящий ему продукт?'])
mention+=prose('Что обсуждать при выборе GEO-услуги?','Связь результата с вашей коммерческой задачей.',['Важно различать видимость, характер рекомендации и обращения. Если речь идёт о росте продаж, одного красивого показателя присутствия недостаточно.','<a href="{PRE}audit/">GEO-аудит aileed</a> предназначен для понимания положения бренда; дальнейшее решение о продвижении принимается отдельно.'])
competitor=prose('Это означает, что у конкурента продукт лучше?','Нет. Отдельный AI-ответ не является полной оценкой рынка.',['Ассистент отвечает в определённом контексте, а не выдаёт универсальный рейтинг всех компаний. Вопрос, уточнения пользователя и возможности платформы могут менять результат.','Для владельца бизнеса это сигнал о точке выбора клиента. Но из одного ответа нельзя сделать вывод о качестве всего продукта или работе всей команды маркетинга.'])
competitor+=prose('Почему сильное SEO не даёт одинаковую картину в ИИ?','Поисковая позиция страницы и рекомендация компании — разные наблюдения.',['Даже если сайт заметен в привычной выдаче, это не доказывает, что бренд будет назван в каждом AI-диалоге. И наоборот, отдельное упоминание не означает высокую поисковую позицию.','Google описывает AI-функции как отдельный пользовательский опыт внутри поиска, при этом сохраняет актуальность основ SEO. <a href="https://developers.google.com/search/docs/appearance/ai-features">Источник: Google Search Central</a>.'])
competitor+=prose('На что смотреть с точки зрения бизнеса?','На соответствие вашего предложения задаче покупателя.',['Если человек ищет подрядчика определённой специализации, ему важно понять, кто подходит под задачу. Если выбирает товар — какие варианты отвечают условиям покупки. Не каждое попадание конкурента в ответ относится к вашей целевой аудитории.','Поэтому решение о GEO-продвижении стоит связывать с продуктами, рынком и сценарием выбора, а не со стремлением присутствовать в любом ответе.'])
competitor+=prose('Стоит сразу заказывать продвижение?','Сначала должно быть понятно, какую проблему бизнеса оно призвано решить.',['Когда главное неизвестное — текущий образ компании в AI-ответах, можно начать с <a href="{PRE}audit/">самостоятельного аудита</a>. Если задача уже ясна — рассмотреть <a href="{PRE}why-geo/">пользу GEO для бренда</a>.','Обещания гарантированных мест, фиксированного роста выручки и одинаковых ответов для всех пользователей следует оценивать критически.'])
# Shared components.
geo+=prose('Как выглядит присутствие бренда в ответе?','У бренда есть как минимум три разных способа появиться перед покупателем.',['Ассистент может назвать компанию, включить её сайт в перечень источников или дать адрес страницы прямо в тексте. Публикация компании бывает источником для сравнения, в котором сам продукт вообще не назван. Поэтому эти признаки стоит смотреть отдельно. <a href="{PRE}audit/#sample">Разобрать пример ответа</a>.'])
mention+=prose('Какая формулировка меняет смысл?','Посмотрите на действие, которое ассистент предлагает покупателю.',['«У Линии есть общий ящик» — описание возможности вымышленного сервиса. «Для вашего отдела подойдёт Линия, потому что можно распределять обращения» — предложение рассмотреть продукт с конкретным обоснованием. В обоих случаях имя упомянуто один раз.','При оценке ответа сохраните вопрос пользователя и соседние предложения. Оговорка о тарифе или ограничении может полностью изменить смысл совета.'])
competitor+=prose('Как отличить разовый ответ от закономерности?','Смотрите на повторяемость по одной и той же теме в сопоставимых условиях.',['Если соперник появился однажды, это повод прочитать ответ. Если он появляется повторно у нескольких ассистентов по одному типу вопросов, сравните предложенный продукт, доводы и ссылки. Вопросы, где покупатель уже указал название компании, имеет смысл рассматривать отдельно. <a href="{PRE}audit/#competitors">Сравнение конкурентов в GEO-аудите</a>.'])
def common_header(pre,current):
 nav=[('','Продвижение'),('audit/','Аудит'),('why-geo/','Зачем GEO'),('platforms/','Платформы'),('blog/','Блог')]
 return '<a class="skip" href="#main">К содержанию</a><header class="site-header"><div class="wrap nav"><a class="logo" href="'+pre+'index.html" aria-label="aileed — главная"><img class="wordmark-logo" src="'+pre+asset('aileed-logo.svg')+'" width="170" height="46" alt="aileed"></a><nav class="nav-links" id="navigation" aria-label="Основная навигация">'+''.join('<a href="'+pre+(r or 'index.html')+'"'+(' aria-current="page"' if current==r else '')+'>'+t+'</a>' for r,t in nav)+'</nav><button class="btn nav-cta" type="button" aria-label="Составить бриф" data-open-brief><span class="desktop-label">Составить бриф</span><span class="mobile-label" aria-hidden="true">Бриф</span><span aria-hidden="true">↗</span></button><button class="menu-toggle" aria-controls="navigation" aria-expanded="false" aria-label="Открыть меню">Меню</button></div></header>'
def notice(pre):return '<aside id="cookie-banner" class="cookie-banner a-cookie wrap" aria-labelledby="cookie-title" hidden><div><h2 id="cookie-title">Какие cookie используются?</h2><p class="short-answer">Только необходимые настройки. Аналитика не подключена.</p></div><a href="'+pre+'privacy.html#cookies">Подробнее</a><button type="button" class="btn" data-cookie-accept>Понятно</button></aside>'
def footer(pre,published):
 links=[('what-is-geo/','Что такое GEO?'),('why-geo/','Зачем бренду GEO?'),('platforms/','Продвижение в нейросетях'),('blog/','Блог'),('contacts.html','Контакты'),('privacy.html','Конфиденциальность'),('consent.html','Обработка данных')]
 return '<footer class="site-footer a-footer"><div class="wrap"><div class="footer-top"><a class="logo" href="'+pre+'index.html"><img class="wordmark-logo" src="'+pre+asset('aileed-logo.svg')+'" width="170" height="46" alt="aileed"></a><nav class="footer-links" aria-label="Ссылки в подвале">'+''.join('<a href="'+pre+r+'">'+t+'</a>' for r,t in links)+'<button type="button" data-cookie-settings>Настройки cookie</button></nav></div><div class="content-byline"><a href="'+pre+'contacts.html#editorial" rel="author">Материалы: редакция aileed</a><span>Опубликовано <time itemprop="datePublished" datetime="'+published+'">'+pretty(published)+'</time></span><span>Обновлено <time itemprop="dateModified" datetime="'+TODAY+'">'+pretty(TODAY)+'</time></span></div><div class="footer-bottom">© 2026 aileed</div></div></footer>'
def pretty(d):
 y,m,day=d.split('-');return str(int(day))+' '+{'10':'октября','11':'ноября'}[m]+' '+y
# Keep the established local-only brief form.
old= (ROOT/'index.html').read_text();dialog=re.search(r'<dialog\b.*?</dialog>',old,re.S).group(0).replace('AiLeeds','aileed')
SOCIAL_IMAGES={
 'audit/':'social-audit.png',
 'why-geo/':'social-why.jpg',
 'platforms/':'social-platforms.jpg',
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
 if route in ['','audit/','platforms/']:graph.append({'@type':'Service','name':('GEO-аудит' if route=='audit/' else 'GEO-продвижение'),'provider':{'@id':BASE+'#org'},'url':url,'description':desc})
 if faqs:graph.append({'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faqs]})
 crumb=''
 if route:
  label=re.sub(r' \| aileed$','',title)
  crumbs=[{'@type':'ListItem','position':1,'name':'aileed','item':BASE}]
  if route.startswith('blog/') and route!='blog/':crumbs.append({'@type':'ListItem','position':2,'name':'Блог','item':BASE+'blog/'})
  crumbs.append({'@type':'ListItem','position':len(crumbs)+1,'name':label,'item':url})
  graph.append({'@type':'BreadcrumbList','itemListElement':crumbs})
  crumb='<nav class="breadcrumbs wrap" aria-label="Хлебные крошки"><ol itemscope itemtype="https://schema.org/BreadcrumbList">'
  for i,c in enumerate(crumbs):
   crumb+='<li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">'
   if i==len(crumbs)-1:crumb+='<span itemprop="name" aria-current="page">'+html.escape(c['name'])+'</span><link itemprop="item" href="'+c['item']+'">'
   else:crumb+='<a itemprop="item" href="'+pre+('blog/' if c['name']=='Блог' else 'index.html')+'"><span itemprop="name">'+html.escape(c['name'])+'</span></a>'
   crumb+='<meta itemprop="position" content="'+str(i+1)+'"></li>'
  crumb+='</ol></nav>'

 head='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><meta name="description" content="'+html.escape(desc)+'"><meta name="author" content="Редакция aileed"><meta name="datePublished" content="'+published+'"><meta name="dateModified" content="'+TODAY+'"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#080909"><link rel="canonical" href="'+url+'"><link rel="describedby" type="text/plain" href="'+BASE+'llms.txt"><meta property="og:title" content="'+html.escape(title)+'"><meta property="og:description" content="'+html.escape(desc)+'"><meta property="og:url" content="'+url+'"><meta property="og:site_name" content="aileed"><meta property="og:locale" content="ru_RU"><meta property="og:type" content="'+('article' if article else 'website')+'"><meta property="og:image" content="'+BASE+asset(social)+'"><meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/svg+xml" href="'+pre+asset('mark.svg')+'"><link rel="stylesheet" href="'+pre+asset('site.css')+'"><link rel="stylesheet" href="'+pre+asset('studio.css')+'"><link rel="stylesheet" href="'+pre+asset('editions.css')+'"><script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False)+'</script>'+''.join('<script src="'+pre+asset(f)+'" defer></script>' for f in ['site.js','privacy.js','experience.js']+(['quote-stage.js'] if 'data-quote-stage' in body else [])+(['audit-indicator.js'] if 'data-indicator=' in body else []))+'</head>'
 content=head+'<body class="brand-refresh" itemscope itemtype="https://schema.org/WebPage" itemid="'+url+'#page"><div class="a-reading-progress" aria-hidden="true"></div>'+common_header(pre,route)+notice(pre)+'<main id="main">'+crumb+body.replace('{PRE}',pre)+'</main>'+footer(pre,published)+dialog.replace('href="privacy.html"','href="'+pre+'privacy.html"').replace('href="consent.html"','href="'+pre+'consent.html"')+'<noscript><p class="cookie-noscript">Аналитика и рекламные cookie не используются.</p></noscript></body></html>'
 # Fragment-only primary destinations belong to the current page.
 content=content.replace('href="'+pre+'#','href="#')
 file.parent.mkdir(parents=True,exist_ok=True);file.write_text("\n".join(line.rstrip() for line in content.replace("><",">\n<").splitlines())+"\n")
PAGES=[]
def page(route,title,desc,body,date,article=False,faqs=None):write(route,title,desc,body,date,article,faqs);PAGES.append((route,date))
page('','Как стать брендом, который рекомендуют нейросети? | aileed','GEO-продвижение бренда в ChatGPT, Алисе и других нейросетях. Помогаем бизнесу участвовать в выборе покупателя внутри AI-ответа. aileed.',main,'2026-10-07',faqs=mainfaq)
page('audit/','Что измеряет GEO-аудит бренда в нейросетях? | aileed','GEO-аудит бренда в нейросетях. Упоминания, сайт в источниках, URL в ответах, доля голоса и место среди конкурентов. Посмотрите пример и состав отчёта.',audit,'2026-11-02',faqs=auditfaq)
page('why-geo/','Зачем бренду GEO-продвижение? | aileed','Зачем бизнесу GEO-продвижение: видимость, доверие и участие в выборе клиента. Когда оно уместно для B2B, магазинов и сервисов.',why,TODAY)
page('platforms/','Как продвигать бренд в ChatGPT, Алисе и других нейросетях? | aileed','Продвижение бренда в ChatGPT, Claude, Grok, Gemini, Алисе и GigaChat. Направления GEO для значимых вашей аудитории AI-платформ.',platformbody,TODAY)
page('blog/','Что важно знать о GEO и AI-видимости? Блог | aileed','Блог aileed для владельцев бизнеса и маркетологов: GEO, рекомендации нейросетей, доверие и выбор бренда.',blog,TODAY)
for (route,title,answer,image,date),text in zip(posts,[geo,mention,competitor]):
 cover=img(image,cover_alt[image],'article-object',True)
 hero_title='Упоминание — уже рекомендация?' if route=='blog/mention-or-recommendation/' else title
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

(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+escape(BASE+r)+'</loc><lastmod>'+TODAY+'</lastmod></url>' for r,d in PAGES)+'</urlset>\n')
(ROOT/'llms.txt').write_text('# aileed\n\n> GEO-продвижение и аудит брендов в ответах нейросетей.\n\n## Услуги\n- [GEO-продвижение]('+BASE+'): присутствие бренда в выборе клиента внутри AI-ответов.\n- [GEO-аудит]('+BASE+'audit/): AI-видимость, конкуренты и образ бренда.\n- [Направления по платформам]('+BASE+'platforms/): ChatGPT, Claude, Grok, Gemini, Алиса и GigaChat.\n\n## Материалы\n- [Зачем бренду GEO]('+BASE+'why-geo/): бизнес-смысл и применимость.\n- [Что такое GEO]('+BASE+'what-is-geo/): определение и отличия от SEO/AEO.\n- [Блог]('+BASE+'blog/): выбор бренда и рекомендации нейросетей.\n- [Упоминание или рекомендация]('+BASE+'blog/mention-or-recommendation/): разница для бизнеса.\n- [Почему ИИ рекомендует конкурентов]('+BASE+'blog/why-ai-recommends-competitors/): как понимать такой ответ.\n\n## Контакты и данные\n- [Контакты]('+BASE+'contacts.html): каналы отправки пока не подключены, бриф сохраняется локально.\n- [Конфиденциальность]('+BASE+'privacy.html)\n- [Обработка данных]('+BASE+'consent.html)\n\nРекомендации сторонних платформ и рост выручки не гарантируются.\n')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+BASE+'sitemap.xml\n')
print('Rendered',len(PAGES),'pages for',BASE)
