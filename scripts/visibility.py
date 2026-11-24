"""Homepage illustration and published aggregate scope of the October audit."""


def observation_figure():
    return '''<section class="edition report-spread"><div class="wrap" id="observations">
      <header class="report-heading"><h2>Куда ведут ссылки из ответов ИИ?</h2>
      <p class="short-answer">В октябрьской проверке по 100 вопросам мы нашли в источниках 20 разных страниц модного бренда. В выборку вошли два его сайта.</p></header>
      <div class="report-canvas"><div class="report-context"><strong>Кейс модного бренда</strong><span>Контрольный замер · октябрь</span></div>
      <table class="report-table scope-table"><caption>Какие данные вошли в отчёт?</caption><thead><tr><th scope="col">Что проверили</th><th scope="col">Количество</th><th scope="col">Что показывает</th></tr></thead><tbody>
      <tr><th scope="row">Вопросы</th><td>100</td><td>Запросы покупателей об обуви, одежде и аксессуарах.</td></tr>
      <tr><th scope="row">Сайты бренда</th><td>2</td><td>Оба домена учитывали при проверке источников.</td></tr>
      <tr><th scope="row">Страницы в источниках</th><td>20</td><td>Разные URL. Если один адрес встречался несколько раз, в эту строку он попал один раз.</td></tr></tbody></table>
      </div><a class="edition-link" href="{PRE}cases/fashion/">Прочитать, откуда пришли покупатели ↗</a></div></section>'''


def frequency_figure():
    return '''<section class="edition frequency-edition"><div class="wrap" id="visibility">
      <header class="figure-intro"><h2>Что покупателю даёт ссылка?</h2>
      <p class="short-answer">По названию он узнаёт компанию. По ссылке может открыть конкретный товар и проверить, подходит ли он.</p>
      <a class="edition-link" href="{PRE}audit/#sample-board">Посмотреть пример из отчёта ↗</a></header>
      <div class="intent-example"><span class="mini-caption">Пример вопроса об обуви</span><blockquote>Где в Дубае купить обувь ручной работы?</blockquote>
      <dl><div><dt>Упоминание</dt><dd>Покупатель видит название марки.</dd></div>
      <div><dt>Ссылка на коллекцию</dt><dd>Можно посмотреть модели, размеры и наличие.</dd></div></dl></div></div></section>'''
