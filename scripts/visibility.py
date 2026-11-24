"""Public, aggregated case figures. The October sample counts prompts, not individual answers."""
from math import cos, radians, sin

# October control sample, NDA case, slide 7. Counts can overlap.
PROMPTS = 100
UNIQUE_URLS = 20
METRICS = (
    ("mention", "Упоминания", 33, "Бренд назван в ответе", "Нейросеть назвала бренд"),
    ("citation", "Цитирования", 31, "Сайт указан в источниках", "Сайт бренда попал в источники"),
)


def instrument():
    """An accessible 0–100 dial with a fixed scale for both measures."""
    def point(distance, angle):
        angle = radians(angle)
        return f"{170 + distance * cos(angle):.2f} {149 + distance * sin(angle):.2f}"

    ticks = []
    for index in range(51):
        angle = 150 + index * 4.8
        start = 120 if index % 5 == 0 else 124
        ticks.append(f'<path d="M{point(start, angle)} L{point(130, angle)}"/>')
    states, choices = [], []
    for i, (key, label, value, _, result) in enumerate(METRICS):
        radius = 104
        track = f"M{point(radius,150)} A{radius} {radius} 0 1 1 {point(radius,390)}"
        reading = point(radius, 150 + 240 * value / PROMPTS).split()
        states.append(f'''<g class="meter-state meter-{key}">
          <path class="meter-track" d="{track}"/>
          <path class="meter-ink" d="{track}" pathLength="100" stroke-dasharray="{value} 100"/>
          <circle class="meter-pin" cx="{reading[0]}" cy="{reading[1]}" r="4"/>
          <text class="meter-value" x="170" y="154">{value}%</text>
          <text class="meter-label" x="170" y="177">вопросов</text></g>''')
        choices.append(f'<label><input type="radio" name="meter" value="{key}"'
                       + (' checked' if i == 0 else '') + f'><span>{label}</span></label>')
    readings = ''.join(f'<span class="meter-state meter-{key}">{result} · <b>{value} из {PROMPTS}</b></span>'
                       for key, _, value, _, result in METRICS)
    return f'''<figure class="instrument">
      <figcaption><strong>Видимость модного бренда</strong><span>Октябрь · {PROMPTS} промптов</span></figcaption>
      <fieldset class="meter-switch"><legend>Показатель графика</legend>{''.join(choices)}</fieldset>
      <svg viewBox="0 0 340 224" aria-hidden="true" focusable="false"><g class="meter-ticks">{''.join(ticks)}</g>
      {''.join(states)}<g class="meter-ends"><text x="56" y="204">0</text><text x="282" y="204">100</text></g></svg>
      <div class="meter-reading" aria-live="polite">{readings}</div>
      <a class="meter-source" href="{{PRE}}audit/#observations">Посмотреть весь замер <span aria-hidden="true">↗</span></a></figure>'''


def comparison_bars():
    bars = []
    for key, _, value, label, _ in METRICS:
        bars.append(f'''<div class="bar-row {key}"><span>{label}</span><strong>{value}%</strong>
          <div class="bar-rail" aria-hidden="true"><i style="--length:{value}%"></i></div></div>''')
    return f'''<figure class="compare-plot"><figcaption>Доля вопросов <span>из {PROMPTS}</span></figcaption>
      {''.join(bars)}<div class="bar-scale" aria-hidden="true"><span>0%</span><span>50%</span><span>100%</span></div></figure>'''


def observation_figure():
    rows = [
        (METRICS[0][3], f"{METRICS[0][2]} из {PROMPTS}", "Хотя бы одна из двух нейросетей назвала бренд."),
        (METRICS[1][3], f"{METRICS[1][2]} из {PROMPTS}", "Хотя бы одна нейросеть привела страницу одного из сайтов бренда в источниках."),
        ("Разные страницы в источниках", f"{UNIQUE_URLS} URL", "Число уникальных адресов двух сайтов за весь замер."),
    ]
    table = ''.join(f'<tr><th scope="row">{label}</th><td>{value}</td><td>{meaning}</td></tr>'
                    for label, value, meaning in rows)
    return f'''<section class="edition report-spread"><div class="wrap" id="observations">
      <header class="report-heading"><h2>Что показали 100 промптов?</h2>
      <p class="short-answer">В октябрьском замере для международного бренда одежды и аксессуаров нейросети назвали бренд по 33 вопросам. По 31 вопросу в источниках появился его сайт.</p></header>
      <div class="report-canvas"><div class="report-context"><strong>Контрольный замер</strong>
      <span>ChatGPT и Perplexity · октябрь</span></div>
      <div class="report-layout">{comparison_bars()}<div class="url-count"><b>{UNIQUE_URLS}</b><span>разных URL бренда<br>в источниках</span></div></div>
      <table class="report-table"><caption>Как читать показатели</caption><thead><tr><th scope="col">Показатель</th><th scope="col">Результат</th><th scope="col">Что учитывали</th></tr></thead><tbody>{table}</tbody></table>
      <p class="report-note">Один вопрос учитывается один раз в каждом показателе. Упоминания и источники могут пересекаться. Название клиента и исходные запросы закрыты по NDA.</p></div>
      <a class="edition-link" href="{{PRE}}index.html#case-fashion">Результаты проекта за шесть месяцев ↗</a></div></section>'''


def frequency_figure():
    return f'''<section class="edition frequency-edition"><div class="wrap" id="visibility">
    <header class="figure-intro"><h2>Называют бренд. А сайт цитируют?</h2>
    <p class="short-answer">Это два отдельных события. В октябрьской проверке бренд одежды упомянули по 33 из 100 вопросов. Ссылки на его сайты встретились в источниках по 31 вопросу.</p>
    <a class="edition-link" href="{{PRE}}audit/#observations">Открыть таблицу аудита ↗</a></header>
    {comparison_bars()}</div></section>'''
