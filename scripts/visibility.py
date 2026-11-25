"""Interactive sample report for the audit. One mark per answer and indicator."""

GROUPS = (
    ('Выбор сервиса', 25, (17, 12, 7)),
    ('Тарифы', 25, (11, 10, 5)),
    ('Переезд с другой CRM', 25, (15, 8, 4)),
    ('Связь с почтой и чатом', 25, (9, 6, 3)),
)
MEASURES = (
    ('name', 'Упоминания', 'ответов с названием «Линия»', 'Покупатель увидел название сервиса. Чтобы понять, советовала ли его нейросеть, откройте текст ответа.'),
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
        readings.append(f'<div class="preview-reading reading-{key}"><strong>{TOTALS[i]}<small>/{TOTAL}</small></strong><p>{caption}</p></div>')
    cells = []
    for n in range(TOTAL):
        active = ' '.join(key for i, (key, *_) in enumerate(MEASURES) if n < TOTALS[i])
        cells.append(f'<i class="{active}"></i>')
    return f'''<div class="audit-preview" aria-label="Фрагмент учебного отчёта">
    <div class="preview-meta"><b>Видимость бренда</b><span>Учебный отчёт</span></div>
    <div class="preview-body"><div class="preview-readings">{''.join(readings)}</div><div class="preview-grid" aria-hidden="true">{''.join(cells)}</div></div>
    <p class="preview-key">Одна ячейка — один ответ нейросети.</p>
    <fieldset class="preview-select"><legend>Показатель учебной выборки</legend>{''.join(options)}</fieldset>
    </div>'''


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
        <img src="{{PRE}}{photo}" width="1350" height="962" alt="Ноутбук с графиками веб-аналитики на экране" decoding="async">
        <div class="report-title"><span>Учебный отчёт</span><h2 id="audit-report-title">Видимость по 100 промптам</h2></div></header>
        <div class="report-pocket"><div class="scoreboard">
        <p class="report-context">Вымышленный сервис «Линия». По каждой из четырёх тем задали 25 вопросов. Переключите показатель, чтобы сравнить темы, или откройте таблицу со всеми результатами.</p>
        <fieldset class="score-tabs"><legend>Показатель отчёта</legend>{''.join(controls)}</fieldset>
        {''.join(plots)}</div></div></div>
        <details class="report-register"><summary>Таблица по всем показателям</summary>
        <div class="register-scroll" tabindex="0" role="region" aria-label="Таблица результатов по четырём темам">
        <table><caption>Число ответов с каждым признаком. Один ответ может попасть в несколько столбцов.</caption><thead>
        <tr><th scope="col">Тема запроса</th><th scope="col">Ответы</th><th scope="col">Упоминания</th><th scope="col">Источники</th><th scope="col">Ссылки</th></tr></thead>
        <tbody>{rows}</tbody><tfoot><tr><th scope="row">Всего</th><td>{TOTAL}</td>{total_cells}</tr></tfoot></table></div>
        </details></section>'''
