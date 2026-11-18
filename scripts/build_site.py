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
def motion_toggle():
 return '''<button class="quote-motion-toggle" type="button" aria-label="Пауза анимации" aria-pressed="false" title="Пауза анимации" hidden>
   <svg viewBox="0 0 16 16" width="14" height="14" fill="currentColor" aria-hidden="true"><path class="pause-glyph" d="M4 3h3v10H4zm5 0h3v10H9z"/><path class="play-glyph" d="m4 2 10 6-10 6z"/></svg>
 </button>'''

def hero(h,a,p,profile,alt,primary,secondary=('Зачем бренду GEO','why-geo/')):
 product=asset('studio-'+profile+'.webp')
 return f'''<section class="studio-hero studio-{profile}" data-quote-stage>
   <div class="wrap studio-hero-layout"><div class="studio-intro">
   <h1>{h}</h1><p class="short-answer">{a}</p><p class="a-lead">{p}</p>
   <div class="actions"><a class="btn primary" href="{{PRE}}{primary[1]}">{primary[0]} <span aria-hidden="true">↗</span></a>
   <a class="text-link" href="{{PRE}}{secondary[1]}">{secondary[0]} <span aria-hidden="true">→</span></a></div></div>
   <div class="studio-showcase"><div class="studio-floor" aria-hidden="true"></div>
   <div class="quote-objects studio-object"><img class="quote-body" data-profile="{profile}" src="{{PRE}}{product}" width="724" height="724" alt="{alt}" fetchpriority="high">
   <canvas class="quote-canvas" aria-hidden="true"></canvas></div>{motion_toggle()}</div></div>
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
   {motion_toggle()}
 </section>"""
def chapter(name, content, anchor=''):
 anchor = f' id="{anchor}"' if anchor else ''
 return f'<section class="edition {name}"{anchor}><div class="wrap">{content}</div></section>'

def headline(question, answer):
 return f'<header class="edition-head"><h2>{question}</h2><p class="short-answer">{answer}</p></header>'

def arrow_link(route, label):
 return f'<a class="edition-link" href="{{PRE}}{route}">{label} <span aria-hidden="true">↗</span></a>'

def press_photo():
 return f'''<picture class="press-photo" data-scene>
 <source media="(max-width: 650px)" srcset="{{PRE}}{asset('letterpress-small.webp')}">
 <img src="{{PRE}}{asset('letterpress.webp')}" width="1536" height="1024" loading="lazy"
 alt="Медная литера с кавычками выступает над рядом графитовых печатных знаков"></picture>'''

def faq(items):
 entries=''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in items)
 return chapter('question-column',headline('Что важно знать перед началом?','О возможностях GEO, границах услуги и результате для бизнеса.')+'<div class="question-list">'+entries+'</div>','faq'),items

def closing(audit=False):
 question='С чего начать GEO-аудит?' if audit else 'С чего начать продвижение бренда?'
 return chapter('brief-sheet', headline(question,'Соберите задачу в бриф. Укажите сайт, продукт и покупателей, которых хотите привлечь.')+'''
 <div class="brief-slip"><span class="slip-format">.TXT</span><button class="slip-button" type="button" data-open-brief>Составить бриф <span aria-hidden="true">↗</span></button>
 <p>Готовый файл сохраняется на вашем устройстве.</p></div>''','brief')

platforms=[('ChatGPT','chatgpt'),('Claude','claude'),('Grok','grok'),('Gemini','gemini'),('Алиса','alice'),('GigaChat','gigachat')]
def brand_mark(name, key):
 return img('brands/'+key+'.svg','Логотип '+name,'brand-mark'+(' brand-mono' if key in ['grok','gigachat'] else ''))

strip='<div class="a-model-strip wrap">'+''.join('<span>'+brand_mark(n,k)+n+'</span>' for n,k in platforms)+'</div>'

def services(question, answer):
 options=[('audit/','GEO-аудит','Хочу узнать, кого рекомендуют вместо нас и как ИИ описывает наш продукт.','studio-lens.webp','Объектив в медной оправе'),
          ('platforms/','GEO-продвижение','Хочу, чтобы покупатели встречали наш бренд, когда ищут решение в нейросетях.','studio-dialogue.webp','Две объёмные реплики диалога')]
 rows=''.join(f'<a class="service-entry" href="{{PRE}}{route}"><span class="service-name">{name}</span><span class="service-reason">{reason}</span>{img(image,alt,"service-object")}<span class="service-arrow" aria-hidden="true">↗</span></a>' for route,name,reason,image,alt in options)
 return chapter('service-directory',headline(question,answer)+rows,'offers')

def buyer_scenarios():
 examples=[
  ('b2b','Услуги B2B','Кто внедряет CRM для сети клиник с несколькими филиалами?','Клиент ищет подрядчика с опытом в своей отрасли. В шорт-лист легче включить компанию, про которую понятно, какие задачи она уже умеет решать.'),
  ('retail','Товары','Какую кофемолку выбрать для эспрессо на маленькой кухне?','Покупатель описывает условия использования. Ему нужен конкретный продукт, который подходит по размеру, функциям и назначению.'),
  ('saas','SaaS','Какую систему записи выбрать для двух салонов с общей базой клиентов?','Команда сравнивает сервисы под свой рабочий сценарий. Решение о пробной регистрации зависит от того, насколько понятны возможности продукта.')]
 choices=[]; panels=[]
 for i,(key,label,prompt,comment) in enumerate(examples):
  choices.append(f'<label><input type="radio" name="buyer" value="{key}"'+(' checked' if i==0 else '')+f'><span>{label}</span></label>')
  panels.append(f'<figure class="buyer-example" data-buyer="{key}"><figcaption>Пример вопроса покупателя</figcaption><blockquote>«{prompt}»</blockquote><p>{comment}</p></figure>')
 return chapter('buyer-desk',headline('Что ваши клиенты спрашивают у ИИ?','Вопрос меняется вместе с покупкой. Выберите свой рынок и посмотрите пример.')+'<fieldset class="buyer-controls"><legend>Сфера бизнеса</legend>'+''.join(choices)+'</fieldset><div class="buyer-examples">'+''.join(panels)+'</div>'+arrow_link('why-geo/','Зачем GEO вашему бизнесу'),'business')

main=quote_stage()+strip
main+=chapter('press-spread', headline('Кто попадает в список покупателя?','Бренды, которые нейросеть предлагает в ответ на его вопрос.')+press_photo()+'''
 <div class="press-caption"><p>Ещё до перехода на сайт клиент может сравнить нескольких поставщиков. Если в ответе есть ваша компания, у покупателя появляется повод узнать о ней больше.</p>'''+arrow_link('audit/','Узнать, виден ли мой бренд')+'</div>', 'value')
main+=buyer_scenarios()+services('Какая услуга нужна вашему бренду?','Начните с вопроса, на который хотите получить ответ.')
platform_links=''.join(f'<a href="{{PRE}}platforms/#tab-{k}">{brand_mark(n,k)}<span>{n}</span><i aria-hidden="true">↗</i></a>' for n,k in platforms)
main+=chapter('platform-register',headline('Где покупатель может встретить ваш бренд?','Выберите нейросеть, чтобы посмотреть, как в ней может начинаться выбор компании.')+'<nav class="model-register" aria-label="Сценарии по платформам">'+platform_links+'</nav>','platforms')
commonfaq=[('Можно гарантировать рекомендацию нейросети?','Нет. Ответы зависят от платформы и контекста пользователя. GEO развивает присутствие бренда, но не даёт контроля над чужой выдачей.'),('GEO заменяет SEO?','Нет. SEO помогает находить страницы в поиске, а GEO обращается к представлению бренда внутри AI-ответа. Для бизнеса эти направления могут дополнять друг друга.'),('Упоминание бренда уже означает продажу?','Нет. Между знакомством, сравнением и обращением есть разница. Пользу GEO для бизнеса нужно оценивать отдельно от самого факта упоминания.'),('Можно начать с отдельного аудита?','Да. Аудит — самостоятельная услуга. Решение о дальнейшем продвижении принимается отдельно.')]
x,mainfaq=faq(commonfaq);main+=x
# Detail pages.
why=hero('Зачем бренду <br><span>GEO-продвижение?</span>','Чтобы участвовать в выборе покупателя, когда тот обращается за рекомендацией к ИИ.','Ваш продукт может подходить клиенту, но остаться за пределами его списка вариантов. GEO помогает бизнесу развивать присутствие в этой точке выбора.','shortlist','Стеклянная карточка выделена среди двух металлических альтернатив',('Понять текущую видимость','audit/'),('Выбрать платформу','platforms/'))
why+=chapter('choice-story',headline('Где бренд теряет покупателя?','В ответе ассистента выбор может сузиться ещё до знакомства с сайтом.')+"""
 <dl class="choice-lines"><div><dt>Вас пропустили</dt><dd>Подходящий заказчик видит других подрядчиков и может вообще не узнать о вашей компании.</dd></div>
 <div><dt>Вас перепутали</dt><dd>Устаревшее описание услуги отсекает клиентов, которым на самом деле подходит ваш продукт.</dd></div>
 <div><dt>Вас не отличили</dt><dd>Название есть среди вариантов, но покупателю неясно, в чём ваше преимущество.</dd></div></dl>""")
why+=chapter('margin-essay',headline('Когда GEO особенно уместно?','Когда покупателю предстоит сравнить варианты и обосновать выбор.')+"""<div class="essay-text"><p>Для клиники это поиск подрядчика со знанием медицины. Для покупателя техники — модель под размер кухни. Для команды — сервис с нужной интеграцией.</p><p>Если клиент уже выбирает вашу компанию, но уходит при оформлении заказа, сначала стоит разобраться с этим этапом.</p></div>""")
why+=services('С какой задачи начать?','Выберите между оценкой текущей видимости и работой над присутствием бренда в рекомендациях.')+closing()
platform_copy=[('ChatGPT','Покупатель ищет решение в диалоге.','Бренду важно оказаться среди подходящих вариантов, когда клиент описывает свою задачу, ограничения и предпочтения.'),('Claude','Клиент разбирается в сложном выборе.','Значимы ясность предложения и то, насколько точно ассистент представляет специализацию компании и возможности продукта.'),('Grok','Пользователь ищет ответы и сравнивает точки зрения.','Важно, чтобы образ бренда сохранял смысл в контексте вопросов о рынке, категории и альтернативах.'),('Gemini','Клиент обращается к AI-экосистеме Google.','Присутствие бренда в AI-ответах дополняет его знакомство с компанией через другие поисковые сценарии.'),('Алиса','Покупатель задаёт вопрос привычному ассистенту.','Для русскоязычной аудитории важно, какой набор компаний и продуктов попадает в ответ на её задачу.'),('GigaChat','Клиент изучает варианты в русскоязычном AI-сервисе.','Имеет значение, насколько узнаваемо и точно представлено предложение вашего бизнеса.')]
platformbody=hero('Как продвигать бренд <br>в ChatGPT, Алисе <span>и других нейросетях?</span>','Развивать его присутствие там, где ваша аудитория выбирает компании, товары и сервисы.','Для бизнеса важны не названия моделей сами по себе, а встречи с потенциальным покупателем. В aileed GEO-продвижение связано с этой задачей.','dialogue','Две реплики из дымчатого стекла и меди',('Начать с аудита','audit/'))
panel_tabs=''.join(f'<button role="tab" id="tab-{k}" aria-controls="panel-{k}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}">{brand_mark(n,k)}{n}</button>' for i,(n,k) in enumerate(platforms))
panel_bodies=''.join(f'<div role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}" tabindex="0"><div class="platform-seal">{brand_mark(n,k)}</div><h3>Что важно для бренда в {n}?</h3><p class="short-answer">{platform_copy[i][1]}</p><p>{platform_copy[i][2]}</p>'+arrow_link('audit/','Проверить видимость бренда')+'</div>' for i,(n,k) in enumerate(platforms))
platformbody+=chapter('platform-atlas',headline('Какая платформа важна вашей аудитории?','Выберите ассистента, чтобы увидеть сценарий покупателя.')+f'<div class="atlas-stage"><div class="atlas-tabs" role="tablist" aria-label="AI-платформы">{panel_tabs}</div><div class="atlas-panels">{panel_bodies}</div></div>')
platformbody+=chapter('margin-essay',headline('Нужно присутствовать сразу везде?','Приоритет зависит от аудитории и коммерческой задачи.')+'<div class="essay-text"><p>Если покупатели упоминают Алису при первом обращении, её ответы заслуживают внимания. Если команда закупок сравнивает подрядчиков в ChatGPT, точкой входа может стать этот диалог.</p><p>Видимость в одном ассистенте ничего не говорит о том, кого предложит другой.</p></div>')+closing()
audit=hero('Кого рекомендуют нейросети: <span>вас или конкурентов?</span>','GEO-аудит даёт ясную картину видимости и образа вашего бренда в AI-ответах.','Вы увидите, где бизнес попадает в выбор клиента, с кем его сравнивают и какие искажения мешают понять предложение.','lens','Оптический объектив из графита с медной оправой и стеклянной линзой',('Что получу после аудита','#results'))
audit+=strip+chapter('report-spread', headline('Что вы получите от GEO-аудита?','Отчёт о том, где появляется ваш бренд, с кем его сравнивают и насколько точно описывают.')+"""
 <article class="report-paper" aria-label="Содержание отчёта"><div class="report-cover"><span>GEO-аудит</span><span>Содержание отчёта</span></div>
 <div class="report-chapter"><h3>Где видно вашу компанию?</h3><p class="short-answer">В каких сценариях покупатель встречает ваш бренд и где рассматривает другие варианты.</p></div>
 <div class="report-chapter"><h3>Кто оказывается рядом?</h3><p class="short-answer">Каких конкурентов называют ассистенты и за какие свойства их выделяют.</p></div>
 <div class="report-chapter"><h3>Как описан ваш продукт?</h3><p class="short-answer">Какие сведения о компании точны и что может ввести будущего клиента в заблуждение.</p></div></article>""",'results')
audit+=chapter('margin-essay',headline('Какое решение можно принять после аудита?','Выбрать, что сейчас важнее для бизнеса.')+'<div class="essay-text"><p>Если ИИ неверно называет вашу специализацию, приоритетом станет образ компании. Если клиенты видят в рекомендациях только конкурентов, стоит обсудить продвижение.</p><p>Отчётом можно пользоваться со своей командой.</p></div>')
x,auditfaq=faq([('Аудит включает дальнейшее продвижение?','Нет. Это самостоятельная услуга. Продвижение обсуждается отдельно.'),('Можно использовать результат со своей командой?','Да. Результат предназначен для решения вашей бизнес-задачи, а не для привязки к одному подрядчику.'),('Аудит гарантирует рекомендации ИИ?','Нет. Он помогает понять текущее положение. Никакой подрядчик не управляет всеми ответами сторонних платформ.'),('Какие нейросети входят в услугу?','Набор определяется задачей и аудиторией. На сайте представлены ChatGPT, Claude, Grok, Gemini, Алиса и GigaChat.')]);audit+=x+closing(True)
# Editorial pages explain customer choices, not the agency's execution playbook.
posts=[('what-is-geo/','Что такое GEO и зачем оно бизнесу?','GEO — работа с присутствием сайта и бренда в ответах генеративных систем.','studio-dialogue.webp','2026-11-04'),('blog/mention-or-recommendation/','Упоминание бренда — это уже рекомендация?','Нет. Название в ответе ещё не означает, что ассистент предлагает выбрать именно вас.','quote-glass.webp',TODAY),('blog/why-ai-recommends-competitors/','Почему ИИ рекомендует конкурентов?','Ответ может отличаться от привычной картины поисковой выдачи и узнаваемости на рынке.','studio-shortlist.webp',TODAY)]
cover_alt={
 'studio-dialogue.webp':'Реплики из дымчатого стекла и металла',
 'quote-glass.webp':'Объёмная кавычка из янтарного стекла',
 'studio-shortlist.webp':'Стеклянная карточка на переднем плане среди вариантов',
}
def story_card(post,heading='h3',eager=False):
 route,title,answer,image,date=post
 return f'''<article class="a-post"><a href="{{PRE}}{route}">
 <div class="story-image">{img(image,cover_alt[image],'a-post-art',eager)}</div>
 <div class="story-copy"><{heading}>{title}</{heading}><p class="short-answer">{answer}</p>
 <span class="a-read">Читать материал <span aria-hidden="true">↗</span></span></div></a></article>'''

def story_shelf(items, heading):
 rows=[]
 for route,title,answer,image,date in items:
  rows.append(f'<article class="shelf-story"><a href="{{PRE}}{route}"><div class="shelf-art">{img(image,cover_alt[image])}</div><div class="shelf-words"><{heading}>{title}</{heading}><p class="short-answer">{answer}</p></div><span class="shelf-arrow" aria-hidden="true">↗</span></a></article>')
 return '<div class="story-shelf">'+''.join(rows)+'</div>'

main+=chapter('journal-shelf',headline('Что почитать о выборе бренда в ИИ?','Три материала для тех, кто отвечает за продвижение бизнеса.')+story_shelf(posts,'h3')+arrow_link('blog/','Весь блог'),'blog')+closing()
blog='''<section class="studio-journal"><div class="wrap journal-front">
 <div class="a-blog-heading"><h1>Что важно знать о GEO и выборе бренда <span>в нейросетях?</span></h1>
 <p class="short-answer">Блог aileed о видимости, доверии и роли AI-ответов в решениях покупателей.</p></div>'''+story_card(posts[0],'h2',True)+'</div></section>'+chapter('journal-shelf archive-edition',story_shelf(posts[1:],'h2'))

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

 head='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><meta name="description" content="'+html.escape(desc)+'"><meta name="author" content="Редакция aileed"><meta name="datePublished" content="'+published+'"><meta name="dateModified" content="'+TODAY+'"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#080909"><link rel="canonical" href="'+url+'"><link rel="describedby" type="text/plain" href="'+BASE+'llms.txt"><meta property="og:title" content="'+html.escape(title)+'"><meta property="og:description" content="'+html.escape(desc)+'"><meta property="og:url" content="'+url+'"><meta property="og:site_name" content="aileed"><meta property="og:locale" content="ru_RU"><meta property="og:type" content="'+('article' if article else 'website')+'"><meta property="og:image" content="'+BASE+asset(social)+'"><meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/svg+xml" href="'+pre+asset('mark.svg')+'"><link rel="stylesheet" href="'+pre+asset('site.css')+'"><link rel="stylesheet" href="'+pre+asset('studio.css')+'"><link rel="stylesheet" href="'+pre+asset('editions.css')+'"><script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False)+'</script>'+''.join('<script src="'+pre+asset(f)+'" defer></script>' for f in ['site.js','privacy.js','experience.js']+(['quote-stage.js'] if 'data-quote-stage' in body else []))+'</head>'
 content=head+'<body class="brand-refresh" itemscope itemtype="https://schema.org/WebPage" itemid="'+url+'#page"><div class="a-reading-progress" aria-hidden="true"></div>'+common_header(pre,route)+notice(pre)+'<main id="main">'+crumb+body.replace('{PRE}',pre)+'</main>'+footer(pre,published)+dialog.replace('href="privacy.html"','href="'+pre+'privacy.html"').replace('href="consent.html"','href="'+pre+'consent.html"')+'<noscript><p class="cookie-noscript">Аналитика и рекламные cookie не используются.</p></noscript></body></html>'
 # Fragment-only primary destinations belong to the current page.
 content=content.replace('href="'+pre+'#','href="#')
 file.parent.mkdir(parents=True,exist_ok=True);file.write_text("\n".join(line.rstrip() for line in content.replace("><",">\n<").splitlines())+"\n")
PAGES=[]
def page(route,title,desc,body,date,article=False,faqs=None):write(route,title,desc,body,date,article,faqs);PAGES.append((route,date))
page('','Как стать брендом, который рекомендуют нейросети? | aileed','GEO-продвижение бренда в ChatGPT, Алисе и других нейросетях. Помогаем бизнесу участвовать в выборе покупателя внутри AI-ответа. aileed.',main,'2026-10-07',faqs=mainfaq)
page('audit/','Кого рекомендуют нейросети? GEO-аудит | aileed','GEO-аудит бренда: AI-видимость, конкуренты и представление бизнеса в нейросетях. Ясная картина для следующего решения.',audit,'2026-11-02',faqs=auditfaq)
page('why-geo/','Зачем бренду GEO-продвижение? | aileed','Зачем бизнесу GEO-продвижение: видимость, доверие и участие в выборе клиента. Когда оно уместно для B2B, магазинов и сервисов.',why,TODAY)
page('platforms/','Как продвигать бренд в ChatGPT, Алисе и других нейросетях? | aileed','Продвижение бренда в ChatGPT, Claude, Grok, Gemini, Алисе и GigaChat. Направления GEO для значимых вашей аудитории AI-платформ.',platformbody,TODAY)
page('blog/','Что важно знать о GEO и AI-видимости? Блог | aileed','Блог aileed для владельцев бизнеса и маркетологов: GEO, рекомендации нейросетей, доверие и выбор бренда.',blog,TODAY)
for (route,title,answer,image,date),text in zip(posts,[geo,mention,competitor]):
 cover=img(image,cover_alt[image],'article-object',True)
 body=f'''<article class="a-article"><header class="studio-article-head"><div class="wrap article-lead">
 <div><h1>{title}</h1><p class="short-answer">{answer}</p>
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
