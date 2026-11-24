"""Sample report for the audit and a buyer example for the GEO service page."""


def observation_figure():
    # Illustrative counts, independent of the WINLINE engagement. One feature per answer at most.
    groups = (
        ('Выбор сервиса', 25, (17, 12, 7)),
        ('Тарифы', 25, (11, 10, 5)),
        ('Переезд с другой CRM', 25, (15, 8, 4)),
        ('Связь с почтой и чатом', 25, (9, 6, 3)),
    )
    measures = (
        ('name', 'Упоминания', 'В скольких ответах встретилось название «Линия»?'),
        ('source', 'Источники', 'В скольких ответах сайт «Линии» попал в список источников?'),
        ('link', 'Ссылки', 'В скольких ответах ссылка на сайт была прямо в тексте?'),
    )
    total = sum(size for _, size, _ in groups)
    totals = [sum(values[i] for _, _, values in groups) for i in range(len(measures))]
    controls, plots = [], []
    for i, (key, label, question) in enumerate(measures):
        selected = ' checked' if i == 0 else ''
        controls.append(f'<label><input type="radio" name="measure" value="{key}"{selected}><span>{label}</span></label>')
        bars = ''.join(f'<li><span>{topic}</span><i aria-hidden="true"><b style="--value:{100*numbers[i]/size:g}%"></b></i>'
                       f'<strong>{numbers[i]} <small>из {size}</small></strong></li>' for topic, size, numbers in groups)
        plots.append(f'''<div class="score-plot" data-measure="{key}">
            <div class="score-total"><strong>{totals[i]}<small>/{total}</small></strong><p>{question}</p></div>
            <ol aria-label="{label} по темам">{bars}</ol></div>''')
    rows = ''.join('<tr><th scope="row">'+topic+'</th><td>'+str(size)+'</td>'+
                   ''.join(f'<td>{n}</td>' for n in numbers)+'</tr>' for topic,size,numbers in groups)
    total_cells = ''.join(f'<td>{n}</td>' for n in totals)
    return f'''<section class="audit-report wrap" id="observations"><header><h2>Что покажут 100 вопросов?</h2>
        <p class="short-answer">Учебный отчёт о вымышленном российском сервисе «Линия». Мы задали значения для примера. В каждой теме по 25 вопросов и по одному ответу на вопрос.</p></header>
        <div class="scoreboard"><fieldset class="score-tabs"><legend>Показатель отчёта</legend>{''.join(controls)}</fieldset>
        {''.join(plots)}</div>
        <details class="report-register"><summary>Таблица по всем показателям</summary>
        <div class="register-scroll" tabindex="0" role="region" aria-label="Таблица результатов по четырём темам">
        <table><caption>Число ответов с каждым признаком. Один ответ может попасть в несколько столбцов.</caption><thead>
        <tr><th scope="col">Тема запроса</th><th scope="col">Ответы</th><th scope="col">Упоминания</th><th scope="col">Источники</th><th scope="col">Ссылки</th></tr></thead>
        <tbody>{rows}</tbody><tfoot><tr><th scope="row">Всего</th><td>{total}</td>{total_cells}</tr></tfoot></table></div>
        </details></section>'''


def frequency_figure():
    return '''<section class="edition frequency-edition"><div class="wrap" id="visibility">
      <header class="figure-intro"><h2>Что покупателю даёт ссылка?</h2>
      <p class="short-answer">По названию он узнаёт компанию. По ссылке может открыть конкретный товар и проверить, подходит ли он.</p>
      <a class="edition-link" href="{PRE}audit/#sample-board">Посмотреть пример из отчёта ↗</a></header>
      <div class="intent-example"><span class="mini-caption">Учебный пример · Новосибирск</span><blockquote>Где в Новосибирске примерить зимние ботинки 47-го размера?</blockquote>
      <dl><div><dt>Упоминание</dt><dd>Покупатель узнаёт название магазина.</dd></div>
      <div><dt>Ссылка на товар</dt><dd>Можно проверить размер и наличие в магазине.</dd></div></dl></div></div></section>'''
