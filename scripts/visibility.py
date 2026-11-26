"""Figures in the audit’s demonstration report."""
from home import visibility_dial

GROUPS = (
    ('Выбор поставщика', 25, (17, 12, 7)),
    ('Стоимость', 25, (11, 10, 5)),
    ('Условия обслуживания', 25, (15, 8, 4)),
    ('Сравнение предложений', 25, (9, 6, 3)),
)
MEASURES = (
    ('name', 'Упоминания', 'ответов с упоминанием бренда', 'Покупатель увидел название компании. Из полного ответа можно понять, советует ли её нейросеть и почему.'),
    ('source', 'Источники', 'ответов с сайтом в источниках', 'Сайт указан среди источников. Нейросеть могла использовать его документацию, даже если в самом ответе предложила другой сервис.'),
    ('link', 'Ссылки', 'ответов с прямой ссылкой в тексте', 'Читатель может перейти на сайт из текста. Это возможность перехода. Число состоявшихся визитов покажет веб-аналитика.'),
)
TOTAL = sum(size for _, size, _ in GROUPS)
TOTALS = [sum(values[i] for _, _, values in GROUPS) for i in range(len(MEASURES))]

def report_preview():
    options, readings = [], []
    for i, (key, label, caption, _) in enumerate(MEASURES):
        checked = ' checked' if i == 0 else ''
        options.append(f'<label><input type="radio" name="preview-metric" value="{key}"{checked}><span>{label}</span></label>')
        readings.append(f'''<div class="preview-reading reading-{key}">
        <strong>{TOTALS[i]}<small> из {TOTAL}</small></strong><p>{caption}</p></div>''')
    dial = visibility_dial(tuple((measure[0], count) for measure, count in zip(MEASURES, TOTALS)))
    return f'''<figure class="audit-preview" aria-labelledby="audit-preview-title">
    <div class="audit-dial">{dial}
    <div class="audit-dial-caption"><span id="audit-preview-title">Учебный срез</span>
    {''.join(readings)}</div></div>
    <fieldset class="preview-select"><legend>Показатель учебной выборки</legend>{''.join(options)}</fieldset>
    </figure>'''

def observation_figure(photo):
    controls, plots = [], []
    for i, (key, label, caption, reading) in enumerate(MEASURES):
        selected = ' checked' if i == 0 else ''
        controls.append(f'<label><input type="radio" name="measure" value="{key}"{selected}><span>{label}</span></label>')
        bars = ''.join(f'<li><span>{topic}</span><i aria-hidden="true"><b style="--value:{100*numbers[i]/size:g}%"></b></i>'
                       f'<strong>{numbers[i]} <small>из {size}</small></strong></li>' for topic, size, numbers in GROUPS)
        plots.append(f'''<div class="score-plot" data-measure="{key}">
            <div class="score-total"><strong>{TOTALS[i]}<small>/{TOTAL}</small></strong><p>{caption}</p></div>
            <ol aria-label="{label} по темам">{bars}</ol><p class="plot-reading">{reading}</p></div>''')
    rows = ''.join('<tr><th scope="row">'+topic+'</th><td>'+str(size)+'</td>'+
                   ''.join(f'<td>{n}</td>' for n in numbers)+'</tr>' for topic,size,numbers in GROUPS)
    total_cells = ''.join(f'<td>{n}</td>' for n in TOTALS)
    return f'''<section class="audit-report wrap" id="observations" aria-labelledby="audit-report-title">
        <div class="report-spread"><header class="report-cover">
        <img src="{{PRE}}{photo}" width="1350" height="962" alt="Графики на экране ноутбука" decoding="async" loading="lazy">
        <div class="report-title"><span>Учебный отчёт</span><h2 id="audit-report-title">По каким темам виден бренд?</h2></div></header>
        <div class="report-pocket"><div class="scoreboard">
        <p class="report-context">В учебной выборке 100 ответов, по 25 на каждую тему. Переключите показатель, чтобы сравнить темы, или откройте общую таблицу.</p>
        <fieldset class="score-tabs"><legend>Показатель отчёта</legend>{''.join(controls)}</fieldset>
        {''.join(plots)}</div></div></div>
        <details class="report-register"><summary>Таблица по всем показателям</summary>
        <div class="register-scroll" tabindex="0" role="region" aria-label="Таблица результатов по четырём темам">
        <table><caption>Число ответов с каждым признаком. Один ответ может попасть в несколько столбцов.</caption><thead>
        <tr><th scope="col">Тема запроса</th><th scope="col">Ответы</th><th scope="col">Упоминания</th><th scope="col">Источники</th><th scope="col">Ссылки</th></tr></thead>
        <tbody>{rows}</tbody><tfoot><tr><th scope="row">Всего</th><td>{TOTAL}</td>{total_cells}</tr></tfoot></table></div>
        </details></section>'''


def tone_figure():
    counts = (
        ('positive', 'Положительная', 24, 'Компания подойдёт, если нужен выезд к заказчику в выходные.'),
        ('neutral', 'Нейтральная', 18, 'У компании есть услуга выездного обслуживания.'),
        ('critical', 'Критическая', 10, 'Для срочного заказа стоит рассмотреть других поставщиков.'),
    )
    total = sum(count for _, _, count, _ in counts)
    first_end = counts[0][2] * 100 / total
    second_end = (counts[0][2] + counts[1][2]) * 100 / total
    items = ''.join(f'''<li class="tone-{key}"><b>{count}</b><div><h3>{label}</h3>
    <blockquote>«{quote}»</blockquote></div></li>''' for key, label, count, quote in counts)
    return f'''<section class="tone-section" id="tone"><div class="wrap">
    <header class="edition-head"><h2>Как нейросети описывают бренд?</h2>
    <p class="short-answer">Мы отмечаем, что нейросети называют преимуществом и почему советуют выбрать другую компанию. Если ассистент ссылается на ограничение, сверяем его с&nbsp;действующими условиями.</p></header>
    <figure class="tone-figure"><figcaption>Учебный пример · ответы с упоминанием бренда</figcaption>
    <div class="tone-ring" style="--tone-first:{first_end:.2f}%;--tone-second:{second_end:.2f}%">
    <div><b>{total}</b><span>ответа</span></div></div><ul>{items}</ul></figure>
    </div></section>'''


def source_map():
    paths = (
        ('official', 'Официальный сайт', 'Карточка услуги', 'На сайте компании указаны график выездов и условия обслуживания.',
         'Покупатель видит актуальные условия и может обратиться напрямую.'),
        ('review', 'Отраслевой обзор', 'Сравнение компаний', 'В отраслевом обзоре перечислены поставщики, которые выезжают в выходные.',
         'Покупатель видит несколько компаний и читает, чем они отличаются.'),
        ('directory', 'Каталог', 'Профиль поставщика', 'В каталоге есть телефон компании, но график выезда не указан.',
         'До обращения покупателю придётся уточнить, подходит ли ему график.'),
    )
    controls, readings = [], []
    for i, (key, label, title, quote, consequence) in enumerate(paths):
        checked = ' checked' if i == 0 else ''
        controls.append(f'''<label><input type="radio" name="source-route" value="{key}"{checked}>
        <span>{label}<span aria-hidden="true">→</span></span></label>''')
        readings.append(f'''<div class="route-reading" data-route="{key}">
        <span>Куда ведёт ссылка</span><h3>{title}</h3><p>{consequence}</p>
        <blockquote>«{quote}»</blockquote></div>''')
    return f'''<section class="source-section wrap" id="sample">
    <header class="edition-head"><h2>Куда ведут ссылки из ответов?</h2>
    <p class="short-answer">В отчёте мы показываем страницу назначения. Так видно, может ли покупатель проверить условия и&nbsp;обратиться к&nbsp;вам. Выберите источник, чтобы посмотреть разницу.</p></header>
    <figure id="sample-board" class="source-map">
    <figcaption>Учебный пример · ссылки в тексте ответа</figcaption>
    <div class="route-question"><span>Вопрос покупателя</span><b>Кто обслуживает оборудование с выездом в выходные?</b></div>
    <fieldset class="route-options"><legend>Выбрать направление ссылки</legend>{''.join(controls)}</fieldset>
    <div class="route-readings">{''.join(readings)}</div></figure></section>'''
