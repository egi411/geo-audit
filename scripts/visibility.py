"""Interactive sample report for the audit."""


def observation_figure(photo):
    # Illustrative counts, independent of the WINLINE engagement. One feature per answer at most.
    groups = (
        ('Выбор сервиса', 25, (17, 12, 7)),
        ('Тарифы', 25, (11, 10, 5)),
        ('Переезд с другой CRM', 25, (15, 8, 4)),
        ('Связь с почтой и чатом', 25, (9, 6, 3)),
    )
    measures = (
        ('name', 'Упоминания', 'ответов с названием «Линия»', 'Покупатель увидел название сервиса. Чтобы понять, советовала ли его нейросеть, откройте текст ответа.'),
        ('source', 'Источники', 'ответов со ссылкой в источниках', 'Сайт указан среди источников. Нейросеть могла использовать его документацию, даже если в самом ответе предложила другой сервис.'),
        ('link', 'Ссылки', 'ответов с прямой ссылкой в тексте', 'Читатель может перейти на сайт из текста. Это возможность перехода. Число состоявшихся визитов покажет веб-аналитика.'),
    )
    total = sum(size for _, size, _ in groups)
    totals = [sum(values[i] for _, _, values in groups) for i in range(len(measures))]
    controls, plots = [], []
    for i, (key, label, caption, reading) in enumerate(measures):
        selected = ' checked' if i == 0 else ''
        controls.append(f'<label><input type="radio" name="measure" value="{key}"{selected}><span>{label}</span></label>')
        bars = ''.join(f'<li><span>{topic}</span><i aria-hidden="true"><b style="--value:{100*numbers[i]/size:g}%"></b></i>'
                       f'<strong>{numbers[i]} <small>из {size}</small></strong></li>' for topic, size, numbers in groups)
        plots.append(f'''<div class="score-plot" data-measure="{key}">
            <div class="score-total"><strong>{totals[i]}<small>/{total}</small></strong><p>{caption}</p></div>
            <ol aria-label="{label} по темам">{bars}</ol><p class="plot-reading">{reading}</p></div>''')
    rows = ''.join('<tr><th scope="row">'+topic+'</th><td>'+str(size)+'</td>'+
                   ''.join(f'<td>{n}</td>' for n in numbers)+'</tr>' for topic,size,numbers in groups)
    total_cells = ''.join(f'<td>{n}</td>' for n in totals)
    return f'''<section class="audit-report wrap" id="observations" aria-labelledby="audit-report-title">
        <div class="report-spread"><header class="report-cover">
        <img src="{{PRE}}{photo}" width="1350" height="962" alt="Ноутбук с графиками веб-аналитики на экране" decoding="async">
        <div class="report-title"><span>Учебный отчёт</span><h2 id="audit-report-title">Видимость по 100 промптам</h2></div></header>
        <div class="report-pocket"><div class="scoreboard">
        <p class="report-context">Как часто нейросеть называет сервис «Линия» и даёт ссылку на его сайт? В этой учебной выборке четыре темы по 25 вопросов. Сервис вымышлен.</p>
        <fieldset class="score-tabs"><legend>Показатель отчёта</legend>{''.join(controls)}</fieldset>
        {''.join(plots)}</div></div></div>
        <details class="report-register"><summary>Таблица по всем показателям</summary>
        <div class="register-scroll" tabindex="0" role="region" aria-label="Таблица результатов по четырём темам">
        <table><caption>Число ответов с каждым признаком. Один ответ может попасть в несколько столбцов.</caption><thead>
        <tr><th scope="col">Тема запроса</th><th scope="col">Ответы</th><th scope="col">Упоминания</th><th scope="col">Источники</th><th scope="col">Ссылки</th></tr></thead>
        <tbody>{rows}</tbody><tfoot><tr><th scope="row">Всего</th><td>{total}</td>{total_cells}</tr></tfoot></table></div>
        </details></section>'''
