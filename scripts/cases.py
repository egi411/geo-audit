"""Selected public results from the client-provided case decks."""
from visibility import PROMPTS, METRICS


def case_studies():
    return f'''<section class="edition case-edition"><div class="wrap" id="cases">
      <header class="case-heading"><h2>Что GEO дало бизнесу?</h2><p class="short-answer">Для бренда одежды результатом стали переходы из нейросетей. Для WINLINE — отчёт, по которому редакция и разработчики могут выбрать страницы для доработки.</p></header>
      <div class="case-pair">
      <article class="case-story case-fashion" id="case-fashion"><div class="case-credit">Международный модный бренд <span>NDA</span></div>
      <h3>Сколько переходов принесли нейросети?</h3><p class="short-answer"><strong>10 000+</strong> переходов из нейросетей за шесть месяцев</p>
      <div class="case-evidence"><span>≈ 1 500 переходов</span><p>По запросам, в которых покупатель ещё не назвал бренд.</p></div>
      <details><summary>Что изменилось за полгода?</summary><p>На старте нейросети редко предлагали изделия бренда. К пятому месяцу ChatGPT и Perplexity уже называли его первым в отдельных ответах о выборе изделия ручной работы в Дубае.</p>
      <p>В октябрьской выборке из {PROMPTS} промптов бренд назвали по {METRICS[0][2]} вопросам, его сайты попали в источники по {METRICS[1][2]}. Мы засчитывали появление хотя бы в одной из двух нейросетей.</p>
      <a href="{{PRE}}audit/#observations">Таблица контрольного замера ↗</a></details></article>
      <article class="case-story case-winline" id="case-winline"><div class="case-credit">WINLINE <span>GEO-аудит</span></div>
      <h3>Сколько замеров сделали для WINLINE?</h3><p class="short-answer"><strong>15 000</strong> замеров ответов на вопросы аудитории</p>
      <div class="case-equation"><span><b>300</b> вопросов</span><i>×</i><span><b>5</b> моделей</span><i>×</i><span><b>10</b> прогонов</span></div>
      <details><summary>Что получила команда?</summary><p>Связали 124 темы со 119 страницами WINLINE. В отчёте видно, кого нейросети называют при сравнении брендов, какие страницы цитируют и насколько точно описывают условия регистрации и акций.</p>
      <p>Редакция получила рекомендации по содержанию страниц, разработчики — задачи по разметке и работе URL. К выводам приложили исходные ответы и ссылки.</p></details></article>
      </div></div></section>'''
