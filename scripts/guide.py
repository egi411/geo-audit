"""Show what GEO can change in the buyer's decision."""

from icons import topic_icon

BUYER_QUESTION = 'Кто обслуживает складские ворота в&nbsp;Казани с&nbsp;выездом в&nbsp;выходные?'
BEFORE = 'В&nbsp;Казани можно поискать подрядчика в&nbsp;каталогах ремонтных компаний. Уточните по&nbsp;телефону, обслуживает ли он складские ворота и&nbsp;выезжает ли по&nbsp;выходным.'
AFTER = (
    'Рассмотрите <mark data-part="brand">«Сервис А»</mark>. Компания обслуживает складские ворота в&nbsp;Казани '
    'и&nbsp;<mark data-part="terms">выезжает по&nbsp;субботам и&nbsp;воскресеньям</mark>.'
)
SOURCE = 'Условия выезда на&nbsp;странице услуги'

FAQ = [
    ('Чем GEO отличается от&nbsp;SEO?',
     'SEO помогает покупателю найти страницу в&nbsp;поиске. В&nbsp;GEO мы работаем над тем, чтобы нейросеть могла включить бренд в&nbsp;сравнение, объяснить условия и&nbsp;дать полезную ссылку. Для обоих направлений нужна доступная страница с&nbsp;точными сведениями.'),
    ('Подойдёт ли GEO известному бренду?',
     'Да. Мы проверяем, как нейросети описывают уже знакомый покупателю продукт. Если в&nbsp;ответах остались старые условия или ссылка ведёт на&nbsp;неподходящую страницу, начинаем с&nbsp;уточнения этих сведений.'),
    ('Можно ли гарантировать рекомендацию?',
     'Ответы меняются, и&nbsp;нейросети сами выбирают компании и&nbsp;источники. Мы согласуем вопросы и&nbsp;признаки результата, чтобы после работ сравнить ответы на&nbsp;сопоставимых условиях.'),
]


def comparison(dock):
    return f'''<section id="before-after" class="why-band why-comparison" aria-labelledby="why-compare-title"><div class="wrap">
    <header class="why-story-head"><div><h2 id="why-compare-title">Как меняется ответ на&nbsp;один и&nbsp;тот же вопрос?</h2>
    <p class="short-answer">Покупатель ищет подрядчика для склада. Сравним, что он сможет узнать из&nbsp;двух ответов на&nbsp;свой вопрос.</p></div>
    <figure class="why-dock"><img src="{{PRE}}{dock}" width="1120" height="747" loading="lazy" decoding="async"
    alt="Секционные ворота на погрузочной площадке склада"><figcaption>Иллюстрация к&nbsp;учебному примеру</figcaption></figure></header>
    <figure class="why-dialogue">
    <figcaption><span>Вопрос покупателя</span><b>{BUYER_QUESTION}</b>
    <p>Оба ответа смоделированы, компания условная.</p></figcaption>
    <div class="why-answer-pair">
    <article class="why-answer" id="before-geo"><h3>До GEO</h3><blockquote>{BEFORE}</blockquote>
    <p class="why-answer-effect">Покупателю нужно искать компании и&nbsp;уточнять график.</p></article>
    <article class="why-answer why-answer-after" id="after-geo"><h3>После GEO</h3><blockquote>{AFTER}</blockquote>
    <p class="why-source"><span aria-hidden="true">↗</span> {SOURCE}</p>
    <p class="why-answer-effect">Есть кандидат для сравнения, причина рассмотреть его и&nbsp;страница для проверки.</p></article>
    </div></figure></div></section>'''


def response_lenses():
    lenses = (
        ('brand', 'Бренд', 'Кого покупатель увидел?',
         'В&nbsp;ответе появился конкретный подрядчик. Покупатель может включить его в&nbsp;свой список.'),
        ('terms', 'Условие', 'Почему предложение подходит?',
         'Выезд в&nbsp;выходные отвечает на&nbsp;условие из&nbsp;вопроса. Мы проверяем, совпадает ли эта деталь с&nbsp;тем, что компания предлагает.'),
        ('source', 'Источник', 'Где проверить детали?',
         'Ссылка указывает на&nbsp;страницу услуги. Там покупатель может уточнить условия и&nbsp;связаться с&nbsp;компанией.'),
    )
    choices = []
    annotations = []
    for index, (key, label, question, summary) in enumerate(lenses):
        checked = ' checked' if index == 0 else ''
        choices.append(f'<label><input type="radio" name="answer-lens" value="{key}"{checked}><span>{label}</span></label>')
        annotations.append(f'<div class="why-annotation" data-note="{key}"><h3>{question}</h3><p>{summary}</p></div>')
    return f'''<section class="why-band why-reading" id="visibility" aria-labelledby="why-reading-title"><div class="wrap">
    <header class="why-section-head"><h2 id="why-reading-title">Что именно меняется в&nbsp;ответе?</h2>
    <p class="short-answer">Разберите учебный ответ по&nbsp;частям. Мы смотрим, появился ли бренд, верно ли описано предложение и&nbsp;куда ведёт ссылка.</p></header>
    <div class="why-inspector"><fieldset class="why-lens-options"><legend>Что выделить в&nbsp;ответе?</legend>{''.join(choices)}</fieldset>
    <figure class="why-annotation-sheet"><figcaption>Фрагмент учебного ответа</figcaption>
    <blockquote>{AFTER}</blockquote><p data-part="source"><span aria-hidden="true">↗</span> {SOURCE}</p></figure>
    <div class="why-inspect-detail">{''.join(annotations)}</div></div></div></section>'''


def fit():
    options = (
        ('compare', 'Покупатели сравнивают подрядчиков', 'Попасть в&nbsp;сравнение',
         'Проверим запросы без названия бренда по&nbsp;услуге, которая важна для продаж. В&nbsp;примере это обслуживание ворот в&nbsp;выходные.'),
        ('refresh', 'Покупатели уже знают компанию', 'Уточнить условия',
         'Сверим, как нейросети описывают географию, график и&nbsp;ограничения услуги. Вы увидите, что на&nbsp;сайте стоит прояснить.'),
        ('checklist', 'Условия ещё уточняются', 'Подготовить предложение',
         'Зафиксируйте, где и&nbsp;на&nbsp;каких условиях можете принять заказ. С&nbsp;этими сведениями мы сможем выбрать вопросы для продвижения.'),
    )
    rows = ''.join(f'''<div><dt>{topic_icon(glyph)}{situation}</dt><dd><span>{goal}</span><p>{detail}</p></dd></div>'''
                   for glyph, situation, goal, detail in options)
    return f'''<section class="why-band why-fit" id="investment" aria-labelledby="why-fit-title"><div class="wrap">
    <header class="why-section-head"><h2 id="why-fit-title">Когда GEO имеет смысл?</h2>
    <p class="short-answer">Начинаем с&nbsp;одной услуги или категории, по&nbsp;которой покупатель сравнивает предложения, а&nbsp;вам важно получать обращения.</p></header>
    <dl class="why-fit-map" id="demand">{rows}</dl>
    <a class="why-text-link" href="{{PRE}}audit/">Что покажет GEO-аудит <span aria-hidden="true">↗</span></a>
    </div></section>'''


def outcomes():
    return f'''<section class="why-band why-outcomes" id="outcome" aria-labelledby="why-outcome-title"><div class="wrap why-outcome-board">
    <header class="why-section-head"><h2 id="why-outcome-title">Как понять, что GEO приносит пользу?</h2>
    <p class="short-answer">Мы сравниваем ответы по&nbsp;тем же вопросам. Переходы и&nbsp;обращения проверяем отдельно по&nbsp;данным бизнеса.</p></header>
    <ol class="why-progress">
    <li><span class="why-progress-dot" aria-hidden="true"></span><h3>{topic_icon('chat')}Ответы</h3><p>Появился ли бренд в&nbsp;сравнении, корректны ли условия и&nbsp;на&nbsp;какую страницу ссылаются.</p><b>Смотрим выборку ответов</b></li>
    <li><span class="why-progress-dot" aria-hidden="true"></span><h3>{topic_icon('cursor')}Переходы</h3><p>Сколько было переходов из&nbsp;нейросетей на&nbsp;страницу услуги среди визитов с&nbsp;известным источником.</p><b>Смотрим веб-аналитику</b></li>
    <li><span class="why-progress-dot" aria-hidden="true"></span><h3>{topic_icon('mail')}Обращения</h3><p>Приходят ли клиенты с&nbsp;подходящей задачей и&nbsp;говорят ли, что нашли компанию через нейросеть.</p><b>Сверяем с&nbsp;CRM и&nbsp;отделом продаж</b></li>
    </ol></div></section>'''


def practice(asset):
    return f'''<section class="why-band why-practice" id="practice" aria-labelledby="why-practice-title"><div class="wrap">
    <header class="why-section-head"><h2 id="why-practice-title">Как это выглядит в&nbsp;нашей работе?</h2>
    <p class="short-answer">В&nbsp;одном проекте мы продвигали бренд и&nbsp;видели переходы. В&nbsp;другом изучили ответы и&nbsp;передали команде задачи по&nbsp;сайту.</p></header>
    <div class="why-case-pair">
    <article class="why-case why-case-fashion"><a href="{{PRE}}cases/fashion/">
    <div class="why-case-art"><img src="{{PRE}}{asset('shoe-editorial.webp')}" width="1440" height="960" loading="lazy" decoding="async"
    alt="Чёрный лофер на светлом подиуме"><span>Иллюстрация к&nbsp;кейсу</span></div>
    <div class="why-case-copy"><p>Модный бренд · GEO и&nbsp;SEO</p><h3>10&nbsp;000+ переходов из&nbsp;нейросетей</h3><span>Читать кейс ↗</span></div>
    </a></article>
    <article class="why-case why-case-winline"><a href="{{PRE}}cases/winline/">
    <div class="why-case-art"><img src="{{PRE}}{asset('cases/stadium.webp')}" width="1152" height="1438" loading="lazy" decoding="async"
    alt="Трибуны стадиона и прожектор"><span>Иллюстрация к&nbsp;кейсу</span></div>
    <div class="why-case-copy"><p>WINLINE · GEO-аудит</p><h3>15&nbsp;000 замеров ответов</h3><span>Читать кейс ↗</span></div>
    </a></article></div></div></section>'''


def brand_guide(contact, asset, faq_entries):
    cover = f'''<section class="why-opening">
    <div class="wrap why-cover-grid"><div class="why-cover-copy"><h1>Зачем бренду <span>GEO?</span></h1>
    <p class="short-answer">Мы помогаем бренду появиться там, где покупатель уже сравнивает компании в&nbsp;нейросети. Так покупателю проще понять, подходит ли ваше предложение, и&nbsp;проверить условия.</p>
    <div class="why-actions"><a class="btn primary" href="#before-after">Сравнить ответы <span aria-hidden="true">↓</span></a>
    <a class="why-text-link" href="{contact}" data-open-brief>Обсудить бренд <span aria-hidden="true">↗</span></a></div></div>
    <figure class="why-hero-art"><img src="{{PRE}}{asset('geo-answer-objects.webp')}" width="1250" height="938" fetchpriority="high" decoding="async"
    alt="Две объёмные карточки ответа, на синей выделена одна строка"></figure></div></section>'''
    questions = f'''<section class="why-band why-questions" id="faq" aria-labelledby="why-faq-title"><div class="wrap">
    <header class="why-section-head"><h2 id="why-faq-title">Что уточнить перед началом?</h2></header>
    <figure class="why-faq-visual"><figcaption>Один продукт в&nbsp;двух каналах</figcaption>
    <dl><div><dt>Поиск</dt><dd>Запрос <span aria-hidden="true">→</span> список страниц</dd></div>
    <div><dt>Нейросеть</dt><dd>Вопрос <span aria-hidden="true">→</span> ответ и&nbsp;источники</dd></div></dl>
    <a class="why-text-link" href="{{PRE}}what-is-geo/">Что такое GEO <span aria-hidden="true">↗</span></a>
    </figure><div class="question-list">{faq_entries(FAQ)}</div></div></section>'''
    invite = f'''<section class="why-band why-invite" id="brief" aria-labelledby="why-brief-title"><div class="wrap">
    <header class="why-section-head"><h2 id="why-brief-title">С&nbsp;чего мы начнём?</h2>
    <p class="short-answer">Пришлите сайт и&nbsp;название продукта или услуги. На&nbsp;бесплатной консультации обсудим, в&nbsp;каких сравнениях важно появиться вашей компании.</p>
    <a class="btn primary" href="{contact}" data-open-brief>Записаться на консультацию <span aria-hidden="true">↗</span></a></header>
    <div class="why-brief-preview"><p>Для первого разбора</p><dl>
    <div><dt>Сайт</dt><dd>Где проверить условия</dd></div>
    <div><dt>Продукт или услуга</dt><dd>Что должен найти покупатель</dd></div>
    </dl></div></div></section>'''
    return '<div class="why-page">' + ''.join((
        cover, comparison(asset('geo-warehouse-dock.webp')), response_lenses(), fit(), outcomes(), practice(asset), questions, invite,
    )) + '</div>'
