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
     "Мы покажем, в каких сравнениях появился бренд, как нейросети описывают продукт и куда ведут ссылки. Переходы и обращения можно оценить по данным сайта и отдела продаж."),
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


def fit():
    return '''<section class="fit-section" id="demand" aria-labelledby="fit-title"><div class="wrap">
    <header class="fit-heading"><h2 id="fit-title">Когда мы можем помочь?</h2>
    <p>Начинаем с&nbsp;одного продукта или услуги, по&nbsp;которым вам важно получать новые обращения.</p></header>
    <dl class="fit-cases">
    <div><dt>Покупатели ещё не&nbsp;знают о&nbsp;продукте</dt><dd>Помогаем сделать так, чтобы они могли найти предложение по&nbsp;своей задаче, прежде чем узнают название бренда.</dd></div>
    <div><dt>В&nbsp;сравнениях называют конкурентов</dt><dd>Помогаем раскрыть, кому подходит ваш продукт и&nbsp;что может стать причиной выбрать именно его.</dd></div>
    <div><dt>О&nbsp;вас говорят по&nbsp;устаревшим данным</dt><dd>Помогаем обновить сведения о&nbsp;продукте, чтобы покупателю было проще проверить актуальные условия.</dd></div>
    </dl><a class="front-link" href="why-geo/">Когда GEO имеет смысл <span aria-hidden="true">↗</span></a>
    </div></section>'''


def projects(asset):
    return f'''<section class="front-projects" id="projects"><div class="project-opening">
    <header class="wrap section-top"><h2>Что показали наши проекты?</h2><a class="front-link" href="cases/">Все проекты <span aria-hidden="true">↗</span></a></header>
    <article class="project-feature project-fashion"><div class="wrap project-spread">
    <a class="project-picture shoe" href="cases/fashion/" aria-label="Открыть кейс модного бренда"><img src="{asset('shoe-editorial.webp')}" alt="Чёрный кожаный лофер на светлом подиуме" width="1440" height="960" loading="lazy"><small>Иллюстрация к кейсу под NDA</small></a>
    <div class="project-description"><p class="project-byline">Модный бренд · GEO и SEO</p>
    <h3><a href="cases/fashion/"><strong>10&nbsp;000+</strong> переходов из&nbsp;нейросетей в&nbsp;журнал и&nbsp;каталог</a></h3>
    <p>В&nbsp;начале проекта нейросети путали даже род деятельности компании. Мы доработали журнал и&nbsp;каталог. Через полгода покупатели находили изделия и&nbsp;по&nbsp;запросам без&nbsp;названия марки.</p>
    <a class="front-link" href="cases/fashion/">Читать кейс модного бренда <span aria-hidden="true">↗</span></a></div></div></article></div>
    <article class="project-feature project-winline" id="winline-study"><div class="wrap project-spread"><a class="project-picture stadium" href="cases/winline/" aria-label="Открыть кейс WINLINE">
    <img src="{asset('cases/stadium.webp')}" alt="Ряды трибун и прожектор стадиона" width="1152" height="1438" loading="lazy">
    <img class="client-mark" src="{asset('cases/winline.svg')}" width="483" height="116" alt="WINLINE"></a>
    <div class="project-description"><p class="project-byline">WINLINE · GEO-аудит</p><h3><a href="cases/winline/"><strong>15&nbsp;000</strong> замеров за&nbsp;десять дней</a></h3>
    <p>В&nbsp;рамках аудита мы выяснили, куда вели ответы о&nbsp;WINLINE, и&nbsp;передали команде карту из&nbsp;124 тем и&nbsp;задачи по&nbsp;119 страницам.</p>
    <a class="front-link" href="cases/winline/">Читать кейс WINLINE <span aria-hidden="true">↗</span></a></div></div></article></section>'''


def scope():
    return '''<section class="scope-section" id="scope" aria-labelledby="scope-title"><div class="wrap work-layout">
    <div class="work-intro">
    <h2 id="scope-title">Что мы меняем в&nbsp;ответах нейросетей?</h2>
    <p>Работаем с&nbsp;тем, что компания рассказывает о&nbsp;себе, и&nbsp;с&nbsp;тем, что покупатель может узнать из&nbsp;других публикаций.</p>
    <div class="work-display" data-current="mention" aria-hidden="true">
    <span class="display-line display-mention">Упоминают</span>
    <span class="display-line display-citation">Цитируют</span>
    <span class="display-line display-link">Переходят <i>↗</i></span>
    </div></div>
    <div class="work-items">
    <article class="work-item" data-result="mention"><h3>Бренд включают в&nbsp;сравнение</h3>
    <p>Мы раскрываем условия и&nbsp;отличия предложения по&nbsp;тем вопросам, с&nbsp;которых покупатель начинает выбор. У&nbsp;него появляется больше оснований рассмотреть ваш продукт, даже если он ещё не&nbsp;знает названия компании.</p></article>
    <article class="work-item" data-result="citation"><h3>На&nbsp;ваши материалы ссылаются</h3>
    <p>Мы добавляем на&nbsp;страницы проверяемые условия, характеристики и&nbsp;ответы на&nbsp;частые вопросы. Эти сведения можно процитировать. Так у&nbsp;нейросетей появляется источник, на&nbsp;который можно сослаться.</p></article>
    <article class="work-item" data-result="link"><h3>На&nbsp;ваш сайт переходят за&nbsp;деталями</h3>
    <p>Мы помогаем сделать полезной саму страницу назначения. По&nbsp;ссылке из&nbsp;ответа покупатель может проверить условия, посмотреть товар или обратиться в&nbsp;компанию.</p></article>
    </div></div></section>'''


def agency_home(hero, asset, contact, entries):
    offers = f'''<section class="choice-section" id="offers"><div class="wrap choice-layout"><h2>С&nbsp;чего мы предлагаем начать?</h2>
    <div class="choice-links" id="from-answer">
    <a class="choice-primary" href="{contact}" data-open-brief><h3>GEO-продвижение</h3><p>Если вы уже знаете, какой продукт нужно продвигать. Мы работаем над&nbsp;тем, чтобы бренд чаще называли в&nbsp;ответах и&nbsp;давали ссылки на&nbsp;ваши страницы.</p><span>Обсудить продвижение ↗</span></a>
    <a href="audit/"><h3>GEO-аудит</h3><p>Если сначала нужно выяснить, как вас описывают сейчас, с&nbsp;кем сравнивают и&nbsp;откуда берут сведения. Мы покажем, с&nbsp;чего начать работу.</p><span>Что входит в&nbsp;аудит ↗</span></a>
    </div></div></section>'''
    questions = f'''<section class="front-questions" id="faq"><div class="wrap faq-layout">
    <h2>Что важно знать перед началом?</h2><div class="question-list">{entries(FAQ)}</div></div></section>'''
    invite = f'''<section class="front-invite" id="brief"><div class="wrap invite-layout"><div>
    <h2>Как мы можем помочь вашему бренду?</h2><p>На&nbsp;бесплатной консультации обсудим, какой продукт вы хотите продвигать и&nbsp;что о&nbsp;нём важно знать покупателю.</p></div>
    <a class="btn primary" href="{contact}" data-open-brief>Записаться на консультацию <span aria-hidden="true">↗</span></a></div></section>'''
    return ''.join((hero, scope(), projects(asset), fit(), offers, questions, invite))
