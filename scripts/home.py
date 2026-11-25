"""Marketing homepage and its visibility target."""
from math import cos, radians, sin

FAQ = [
    ("Что мы узнаем на бесплатном разборе?",
     "Обсудим, какие продукты вы хотите продвигать и что покупатели спрашивают о них до покупки. Покажем, с каких тем стоит начать и что для этого уже есть у вашей компании."),
    ("Чем GEO дополняет SEO?",
     "В поиске покупатель открывает несколько страниц и сравнивает предложения. В диалоге он может сначала выбрать компании по ответу нейросети, а уже потом зайти на сайт. GEO помогает бренду стать заметным на этом этапе."),
    ("Можно начать с одного продукта?",
     "Да. Подойдёт и отдельная услуга, и товарная категория. Выберите направление, в котором сейчас важнее всего привлечь новых покупателей. Его и обсудим на первом разборе."),
    ("Как мы поймём, что изменилось?",
     "Вы увидите, в каких сравнениях появился бренд, точнее ли нейросети описывают продукт и куда ведут ссылки. Переходы и обращения оценивают отдельно по данным сайта и отдела продаж."),
    ("Можно гарантировать рекомендацию?",
     "Нейросети сами выбирают, какие компании назвать. До начала работ согласуем, какие изменения важны для вашего бизнеса и по каким признакам можно будет их проверить."),
]


def visibility_dial():
    # Each segment represents one percent of the target, rather than a measured result.
    marks, graduations = [], []
    def point(angle, radius):
        return f'{238 + cos(angle) * radius:.2f} {231 + sin(angle) * radius:.2f}'
    for i in range(100):
        mid = radians(-227 + i * 274 / 99)
        edge = radians(.96)
        path = (f'M{point(mid-edge, 204)} L{point(mid+edge, 204)} '
                f'L{point(mid+edge, 158)} L{point(mid-edge, 158)} Z')
        marks.append(f'<path d="{path}"/>')
        end = 221 if i % 10 == 0 or i == 99 else 216
        graduations.append(f'M{point(mid, 212)} L{point(mid, end)}')
    return ('''<svg class="coverage-dial" viewBox="0 0 476 415" aria-hidden="true" focusable="false">
      <defs><linearGradient id="coverage-ink" gradientUnits="userSpaceOnUse" x1="38" y1="290" x2="425" y2="95">
      <stop stop-color="#5883ff"/><stop offset=".45" stop-color="#8faaff"/><stop offset=".78" stop-color="#b8ceff"/><stop offset="1" stop-color="#f0f5ff"/></linearGradient></defs>
      <g class="coverage-guide" fill="none">
      <circle cx="238" cy="231" r="229"/><circle cx="238" cy="231" r="147"/>
      <path d="M15 231H461 M238 8V141 M238 337V402 M79 72L145 138 M331 324L394 387 M79 390L145 324 M331 138L397 72"/>
      </g>
      <g class="coverage-crosshair"><path d="M30 30h13m-6.5 -6.5v13 M432 30h13m-6.5 -6.5v13 M30 383h13m-6.5 -6.5v13 M432 383h13m-6.5 -6.5v13"/></g>
      <g class="coverage-segments" fill="url(#coverage-ink)">''' + ''.join(marks) + '</g>'
      + '<path fill="none" stroke="#7c879e" stroke-width="1" d="' + ' '.join(graduations) + '"/>'
      + '<g fill="#aaafbc" font-family="inherit" font-size="11"><text x="84" y="395">0%</text>'
        '<text x="391" y="395" text-anchor="end">100%</text></g></svg>')


def home_hero(contact):
    return f'''<section class="home-hero front-cover" id="value"><div class="wrap cover-layout">
    <div class="cover-copy"><h1>Продвижение брендов <span>в нейросетях</span></h1>
    <p class="short-answer">Помогаем вашему бренду попасть в круг компаний, которые покупатель сравнивает в нейросети перед заказом.</p>
    <div class="front-actions"><a class="btn primary" href="{contact}" data-open-brief>Получить бесплатный разбор <span aria-hidden="true">↗</span></a>
    <a class="front-link" href="#projects">Смотреть кейсы <span aria-hidden="true">↓</span></a></div></div>
    <figure class="visibility-scene" id="business">{visibility_dial()}
    <figcaption class="visibility-caption"><strong aria-label="100 процентов"><span data-coverage-value aria-hidden="true">100</span><small aria-hidden="true">%</small></strong>
    <b>Цель продвижения</b><p>Присутствовать в ответах на выбранные вопросы покупателей.</p></figcaption></figure>
    </div><div class="wrap cover-foot"><span>Из практики aileed</span>
    <a href="cases/fashion/"><strong>10 000+</strong><span>переходов из ИИ</span><i aria-hidden="true">↗</i></a>
    <a href="cases/winline/"><strong>15 000</strong><span>замеров для WINLINE</span><i aria-hidden="true">↗</i></a></div></section>'''


def demand():
    return '''<section class="buyer-section" id="demand"><div class="wrap buyer-layout">
    <div class="buyer-intro"><h2>Выбор начинается до визита на сайт</h2>
    <p>Когда покупатель ещё не знает названия компании, он описывает задачу и свои условия. Ответ нейросети может определить, чьи предложения он откроет.</p>
    <a class="front-link" href="why-geo/">Когда бизнесу стоит заниматься GEO <span aria-hidden="true">↗</span></a></div>
    <dl class="buyer-decisions">
    <div><dt>Кого включить в сравнение?</dt><dd>Компания может быть известна по имени и при этом отсутствовать в ответах, где покупатель впервые ищет поставщика.</dd></div>
    <div><dt>Кто подходит по условиям?</dt><dd>Нейросеть пересказывает условия и различия. Устаревшие сведения могут исключить компанию из выбора ещё до визита.</dd></div>
    <div><dt>Где узнать подробности?</dt><dd>Если ответ ведёт на обзор или агрегатор, покупатель видит ваше предложение рядом с другими. Ссылка на сайт даёт ему доступ к информации из первых рук.</dd></div>
    </dl></div></section>'''


def projects(asset):
    return f'''<section class="front-projects" id="projects">
    <header class="wrap section-top"><h2>Кейсы</h2><a class="front-link" href="cases/">Все проекты <span aria-hidden="true">↗</span></a></header>
    <article class="project-feature project-fashion"><div class="wrap project-spread">
    <a class="project-picture shoe" href="cases/fashion/" aria-label="Открыть кейс модного бренда"><img src="{asset('shoe-editorial.webp')}" alt="Чёрный кожаный лофер на светлом подиуме" width="1440" height="960" loading="lazy"><small>Иллюстрация к кейсу под NDA</small></a>
    <div class="project-description"><p class="project-byline">Модный бренд · GEO и SEO</p>
    <h3><a href="cases/fashion/"><strong>10 000+</strong> переходов из нейросетей в журнал и каталог</a></h3>
    <p>В начале проекта нейросети путали даже род деятельности компании. Через полгода покупатели находили её изделия, в том числе по запросам без названия марки.</p>
    <a class="front-link" href="cases/fashion/">Читать кейс модного бренда <span aria-hidden="true">↗</span></a></div></div></article>
    <article class="project-feature project-winline" id="winline-study"><div class="wrap project-spread"><a class="project-picture stadium" href="cases/winline/" aria-label="Открыть кейс WINLINE">
    <img src="{asset('cases/stadium.webp')}" alt="Ряды трибун и прожектор стадиона" width="1152" height="1438" loading="lazy">
    <img class="client-mark" src="{asset('cases/winline.svg')}" width="483" height="116" alt="WINLINE"></a>
    <div class="project-description"><p class="project-byline">WINLINE · GEO-аудит</p><h3><a href="cases/winline/"><strong>15 000</strong> замеров за десять дней</a></h3>
    <p>Ответы о WINLINE вели в том числе на сайты посредников. Команда получила карту из 124 тем и задачи по 119 страницам.</p>
    <a class="front-link" href="cases/winline/">Читать кейс WINLINE <span aria-hidden="true">↗</span></a></div></div></article></section>'''


def scope():
    items = (
        ('Сайт бренда', 'Что покупатель может узнать из первых рук',
         'Дополняем страницы фактами, которые влияют на выбор: характеристики, условия, ограничения и отличия от других предложений. Покупатель сможет проверить важные детали на вашем сайте.'),
        ('Внешние публикации', 'Где о вашем продукте читают за пределами сайта',
         'Помогаем подготовить материалы для отраслевых изданий и обзоров. Читатель получает возможность сопоставить то, что компания говорит о себе, с информацией на независимых площадках.'),
        ('Видимость бренда', 'По каким вопросам изменились ответы',
         'Проверяем, стало ли чаще встречаться ваше название, как описывают предложение и на какие страницы ведут ссылки. По этим наблюдениям вместе выбираем следующее направление работы.'),
    )
    entries = ''.join(f'<details name="scope-item"{" open" if i == 0 else ""}><summary>{title}</summary><div><h3>{heading}</h3><p>{body}</p></div></details>'
                      for i, (title, heading, body) in enumerate(items))
    return f'''<section id="scope" class="scope-section"><div class="wrap scope-layout"><header>
    <h2>Что входит в продвижение</h2><p>Работаем с официальным сайтом и публикациями о бренде. Показываем, какие изменения видны покупателю в ответах нейросетей.</p></header>
    <div class="scope-items">{entries}</div></div></section>'''


def agency_home(hero, asset, contact, entries):
    offers = f'''<section class="choice-section" id="offers"><div class="wrap choice-layout"><h2>С чего начать</h2>
    <div class="choice-links" id="from-answer"><a href="audit/"><p class="offer-intent">Проверить текущую видимость</p><h3>GEO-аудит</h3><p>Получите ответы о вашей компании, сравнение с конкурентами и приоритеты по страницам сайта.</p><span>Что входит в аудит ↗</span></a>
    <a href="{contact}" data-open-brief><p class="offer-intent">Развить видимость продукта</p><h3>GEO-продвижение</h3><p>Дополняем материалы о продукте, чтобы у покупателя было больше оснований включить его в сравнение.</p><span>Обсудить продвижение ↗</span></a></div></div></section>'''
    questions = f'''<section class="front-questions" id="faq"><div class="wrap faq-layout">
    <h2>Перед началом работы</h2><div class="question-list">{entries(FAQ)}</div></div></section>'''
    invite = f'''<section class="front-invite" id="brief"><div class="wrap invite-layout"><div>
    <h2>Выберите продукт для разбора</h2><p>Пришлите ссылку на сайт и скажите, в каком направлении нужны новые клиенты. На бесплатной консультации обсудим, что стоит проверить в первую очередь.</p></div>
    <a class="btn primary" href="{contact}" data-open-brief>Записаться на консультацию <span aria-hidden="true">↗</span></a></div></section>'''
    return ''.join((hero, projects(asset), demand(), scope(), offers, questions, invite))
