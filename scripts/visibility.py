"""Render public teaching figures from the excerpts shown beside them."""
import html
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'content/visibility-example.json'
GROUPS = json.loads(DATA.read_text())
BRAND_FORMS = ('«Линия»', '«Линии»', '«Линию»')
DOMAIN = 'linea.example/'


def has_mention(answer):
    return any(form in answer[0] for form in BRAND_FORMS)


def has_citation(answer):
    return answer[1].startswith(DOMAIN)


SERIES = [('Упоминания', 'mention', has_mention), ('Цитирования', 'citation', has_citation)]


def frequency_figure():
    rows = []
    for group in GROUPS:
        answers = group['answers']
        bars = []
        for label, key, matches in SERIES:
            count = sum(map(matches, answers))
            bars.append(f'<div class="frequency-bar {key}" role="img" aria-label="{label}: {count} из {len(answers)}">'
                        f'<i style="--fraction:{count / len(answers):.3f}"></i><b>{count}</b></div>')
        rows.append(f'<div class="frequency-row"><span>{group["topic"]}</span><div>{"".join(bars)}</div></div>')
    return '''<section class="edition frequency-edition"><div class="wrap" id="visibility">
    <header class="figure-intro"><h2>Называют бренд. А сайт цитируют?</h2>
    <p class="short-answer">Это два отдельных события. Нейросеть может назвать сервис по имени, а ссылку на документацию оставить лишь в источниках.</p>
    <a class="edition-link" href="{PRE}audit/#observations">Посмотреть исходные ответы <span aria-hidden="true">↗</span></a></header>
    <figure class="frequency-paper"><figcaption><strong>Присутствие в ответах</strong><span>Учебная выборка · 12 ответов</span></figcaption>
    <div class="figure-legend"><span class="mention">Упоминания бренда</span><span class="citation">Цитирования сайта</span></div>
    <div class="frequency-plot">''' + ''.join(rows) + '''<div class="frequency-axis" aria-hidden="true">
    <span></span><div><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span></div></div></div>
    <p>По четыре ответа на вопрос. Одна отметка на ответ, сколько бы раз в нём ни встретилось название.</p>
    </figure></div></section>'''


def observation_figure():
    all_answers = [answer for group in GROUPS for answer in group['answers']]
    tracks = []
    for label, key, matches in SERIES:
        marks = []
        for group in GROUPS:
            cells = ''.join('<i class="hit"></i>' if matches(answer) else '<i></i>' for answer in group['answers'])
            marks.append(f'<span>{cells}</span>')
        count = sum(map(matches, all_answers))
        tracks.append(f'<div class="observation-track {key}"><strong>{label}</strong><div class="marks" aria-hidden="true">'
                      + ''.join(marks) + f'</div><span class="track-count">{count}<small> / {len(all_answers)}</small></span></div>')
    source = []
    for group in GROUPS:
        lines = []
        for answer, url in group['answers']:
            excerpt = html.escape(answer)
            for form in BRAND_FORMS:
                excerpt = excerpt.replace(form, f'<mark>{form}</mark>')
            citation = html.escape(url) if url else 'Сайт не указан'
            lines.append(f'<li><p>{excerpt}</p><small>{citation}</small></li>')
        source.append(f'<div><strong>{group["question"]}</strong><ol>{"".join(lines)}</ol></div>')
    return '''<section class="edition observation-edition"><div class="wrap" id="observations">
    <header class="figure-intro"><h2>В скольких ответах появился бренд?</h2>
    <p class="short-answer">На примере вымышленного сервиса «Линия» видно, как часто встречаются название и ссылка на источник. Каждый столбец соответствует одному ответу.</p></header>
    <figure class="observation-plate"><figcaption>Учебная выборка <span>12 ответов · 3 вопроса</span></figcaption>
    <div class="observation-key"><span></span><div><span>Выбор сервиса</span><span>Условия работы</span><span>Короткий список</span></div><span></span></div>''' + ''.join(tracks) + '''
    <p>Закрашенная ячейка — признак есть. Ответ может попасть в обе строки. У одного ответа может быть сколько угодно читателей. Их число в этой выборке неизвестно.</p></figure>
    <details class="source-book"><summary>Открыть 12 учебных ответов</summary><div class="source-pages">''' + ''.join(source) + '''</div></details></div></section>'''


def overview():
    answers = [answer for group in GROUPS for answer in group['answers']]
    items = []
    for label, key, matches in SERIES:
        count = sum(map(matches, answers))
        items.append(f'<div class="signal-count {key}"><dt>{label}</dt><dd>{count}<small> / {len(answers)}</small></dd></div>')
    return '''<section class="edition signal-overview"><div class="wrap">
    <header class="figure-intro"><h2>Есть название. А ссылка?</h2>
    <p class="short-answer">В учебной подборке о сервисе «Линия» название встречается чаще, чем его сайт в источниках. В отчёте эти показатели идут отдельно.</p></header>
    <div class="signal-totals"><dl>''' + ''.join(items) + '''</dl>
    <a class="edition-link" href="{PRE}why-geo/#visibility">Сравнить по вопросам <span aria-hidden="true">↗</span></a></div></div></section>'''
