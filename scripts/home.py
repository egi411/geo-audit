"""Commercial chapters for the agency homepage. Project results come from the two case studies."""

FAQ = [
    ("Что мы узнаем на бесплатной консультации?",
     "Обсудим, по каким запросам вас ищут покупатели и какие направления вы хотите продвигать. Подскажем, с чего начать работу над видимостью бренда."),
    ("Чем GEO дополняет SEO?",
     "SEO помогает покупателю найти ваш сайт в результатах поиска. В нейросети покупатель получает готовый ответ. В GEO мы работаем над тем, что нейросеть расскажет о вашем бренде и куда направит покупателя за подробностями."),
    ("Можно ли начать с одного направления?",
     "Да. Вы определяете, какое направление важно для бизнеса. Мы подбираем вопросы покупателей, проверяем ответы нейросетей и составляем план продвижения по этой теме."),
    ("Как понять, что продвижение даёт результат?",
     "До начала работ фиксируем, как часто нейросети называют бренд и ссылаются на его сайт. Повторяем проверку по тем же вопросам. В отчёте вы увидите, по каким темам видимость выросла и где она пока остаётся низкой."),
]


def demand():
    return '''<section class="agency-section demand-story"><div class="wrap agency-grid" id="demand">
    <header><h2>Как покупатели находят бренды в нейросетях</h2>
    <p>В поиске человек сам открывает сайты и сравнивает предложения. В нейросети он может описать, что ему нужно, уточнить условия и за несколько сообщений собрать список компаний. Знакомство с брендом начинается ещё до визита на сайт.</p>
    <p>Мы проверяем, попадает ли ваш бренд в этот список и что покупатель узнаёт о вас при сравнении. Затем работаем с источниками, из которых нейросети берут сведения о компании.</p>
    <a class="agency-link" href="why-geo/">Зачем бренду GEO <span aria-hidden="true">↗</span></a></header>
    <figure class="buyer-notebook"><figcaption>Что важно покупателю</figcaption>
    <ol><li><span>Поиск</span><strong>Узнать, какие компании решают его задачу</strong></li>
    <li><span>Сравнение</span><strong>Разобраться, чем отличаются предложения</strong></li>
    <li><span>Выбор</span><strong>Найти официальный сайт и уточнить условия</strong></li></ol></figure>
    </div></section>'''


def fashion_case(asset):
    return f'''<section class="agency-section fashion-feature"><div class="wrap" id="projects">
    <div class="fashion-canvas"><img src="{asset('shoe-editorial.webp')}" alt="Чёрный кожаный лофер на светлом фоне" width="1440" height="960" loading="lazy">
    <div class="fashion-label">Кейс продвижения <span>Модный бренд · NDA</span></div>
    <div class="fashion-title"><h2><strong>10 000+</strong> переходов из нейросетей за полгода</h2></div>
    <small class="fashion-credit">Иллюстрация к кейсу</small></div>
    <div class="project-byline agency-grid"><h3>Из разговора об изделии в каталог марки</h3>
    <div><p>У международной марки были сайт бренда и отдельный каталог. Мы подготовили журнальные материалы об изделиях и связали их с карточками товаров. Читатель, который интересовался ручной работой, мог сразу открыть подходящую модель.</p>
    <p>Около 10 000 переходов пришлись на запросы без названия бренда. Так к каталогу пришли люди, которые искали изделие и ещё выбирали марку.</p>
    <a class="agency-link" href="cases/fashion/">Как менялся результат по месяцам <span aria-hidden="true">↗</span></a></div></div>
    </div></section>'''


PROMOTION_AREAS = [
    ("site", "Сайт бренда", "Что нейросети могут узнать о вас",
     "Сверяем ответы с тем, что компания действительно предлагает. Находим страницы, где не хватает важных для покупателя сведений, и готовим правки.",
     [("Описание предложения", "Объясняем, кому подходит продукт и почему покупателю стоит его рассмотреть."),
      ("Ответы на вопросы", "Собираем на страницах условия и характеристики, которые влияют на выбор.")]),
    ("media", "Внешние публикации", "Какие источники формируют мнение о бренде",
     "Изучаем публикации, на которые ссылаются нейросети при сравнении компаний. По ним видно, где покупатель встречает ваш бренд, а где читает только о конкурентах.",
     [("Выбор площадок", "Находим издания и отраслевые ресурсы, которые уже появляются в ответах по вашим темам."),
      ("Подготовка материалов", "Готовим публикации о продукте с фактами, которые подтверждает компания.")]),
    ("results", "Динамика видимости", "Что изменилось после публикации",
     "Повторяем замеры по согласованным вопросам. Смотрим, в каких ответах появились бренд и его сайт, как изменилась информация о продукте и кого ещё называют нейросети.",
     [("Отчёт по темам", "Показываем упоминания бренда и ссылки на сайт отдельно. Вы видите, какие темы принесли изменения."),
      ("План дальнейших работ", "Определяем, какие материалы стоит развивать и где покупателю по-прежнему трудно найти вас.")]),
]


def work_scope():
    controls, spreads = [], []
    for i, (key, label, heading, description, outputs) in enumerate(PROMOTION_AREAS):
        checked = ' checked' if i == 0 else ''
        controls.append(f'<label><input type="radio" name="engagement" value="{key}"{checked}><span>{label}</span></label>')
        rows = ''.join(f'<div><dt>{name}</dt><dd>{copy}</dd></div>' for name, copy in outputs)
        spreads.append(f'''<article class="brief-sheet" data-engagement="{key}"><div class="brief-voice">
        <h3>{heading}</h3><p>{description}</p></div><div class="brief-output"><dl>{rows}</dl></div></article>''')
    return f'''<section class="agency-section work-scope"><div class="wrap" id="scope">
    <header class="scope-lead"><h2>Что входит в GEO-продвижение</h2>
    <p>Чтобы покупатель мог найти вас и понять, чем вы ему подходите, мы работаем с информацией о бренде на вашем сайте и за его пределами.</p></header>
    <div class="brief-reader"><fieldset class="brief-switch"><legend>Направление работы</legend>{''.join(controls)}</fieldset>
    {''.join(spreads)}</div></div></section>'''


def services():
    return '''<section class="agency-section service-index"><div class="wrap" id="offers">
    <header><h2>Аудит и продвижение</h2></header><div id="from-answer">
    <article><h3>GEO-аудит</h3><div><p>Узнайте, как покупатели видят вашу компанию сегодня. Проверим, по каким запросам появляется бренд, как нейросети описывают его и какие позиции занимают конкуренты.</p>
    <p>Вы получите отчёт с исходными ответами и список приоритетов для продвижения.</p></div>
    <a class="agency-link" href="audit/">Посмотреть состав аудита <span aria-hidden="true">↗</span></a></article>
    <article><h3>GEO-продвижение</h3><div><p>Поможем покупателям находить ваши продукты и услуги в ответах нейросетей. Выберем приоритетные темы, доработаем страницы сайта и подготовим материалы для внешних площадок.</p>
    <p>По мере публикации будем проверять, что меняется в ответах о бренде, и корректировать план работ.</p></div>
    <a class="agency-link" href="#brief">Обсудить продвижение <span aria-hidden="true">↓</span></a></article></div></div></section>'''


def audit_case(asset):
    return f'''<section class="agency-section research-feature"><div class="wrap" id="winline-study">
    <div class="research-paper"><header><img src="{asset('cases/winline.svg')}" width="483" height="116" alt="WINLINE" loading="lazy"><span>Кейс GEO-аудита</span></header>
    <div class="research-body"><div><h2>Кейс: как мы провели полный GEO-аудит на 15 000 замеров за 10 дней?</h2>
    <p>Покупатель мог спросить об условиях регистрации или акции и получить объяснение посредника. WINLINE нужно было узнать, по каким темам человек доходит до официального сайта и какие страницы стоит доработать.</p>
    <a class="agency-link" href="cases/winline/">Посмотреть выводы и состав отчёта <span aria-hidden="true">↗</span></a></div>
    <dl class="research-numbers"><div><dt>15 000</dt><dd>замеров в ответах нейросетей</dd></div>
    <div><dt>124</dt><dd>темы из вопросов покупателей</dd></div><div><dt>119</dt><dd>адресов сайта связали с этими темами</dd></div></dl></div>
    <figure class="research-split"><figcaption>По 3 000 замеров в каждой модели</figcaption>
    <ul><li>Алиса</li><li>ChatGPT</li><li>Perplexity</li><li>Gemini</li><li>Claude</li></ul></figure>
    <footer><strong>Что получила команда</strong><p>Рабочую книгу на 12 листах и презентацию на 26 слайдах. В книге темы связаны со страницами официального сайта. В презентации собраны выводы и приоритеты для команды WINLINE.</p></footer></div></div></section>'''


def questions(entries):
    return f'''<section class="agency-section agency-questions"><div class="wrap agency-grid" id="faq">
    <h2>До начала проекта</h2><div class="question-list">{entries(FAQ)}</div></div></section>'''


def consultation(contact):
    return f'''<section class="consult-invite"><div class="wrap" id="brief">
    <div><h2>С чего начать продвижение вашего бренда?</h2><p>Оставьте заявку. Мы свяжемся с вами в ближайшее время и проведём бесплатную консультацию. Обсудим ваши цели и предложим первые шаги для продвижения в нейросетях.</p></div>
    <a class="btn primary" href="{contact}" data-open-brief>Записаться на бесплатный разбор <span aria-hidden="true">↗</span></a>
    </div></section>'''


def agency_home(hero, asset, contact, entries):
    return ''.join((hero, demand(), fashion_case(asset), work_scope(), services(),
                    audit_case(asset), questions(entries), consultation(contact)))
