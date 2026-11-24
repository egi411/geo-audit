"""Accessible slide readers for the two approved public case decks."""
from html import escape

SLIDES = {
    "fashion": [
        "За шесть месяцев два сайта модного бренда получили более 10 000 переходов из нейросетей.",
        "До начала работ бренд редко появлялся в ответах о выборе изделий.",
        "Два сайта на трёх языках: 300 запросов и 100 тематических кластеров.",
        "Первые зафиксированные рекомендации появились к пятому месяцу.",
        "Около 1 500 переходов пришли по небрендовому спросу.",
        "В отдельных ответах об изделиях ручной работы бренд назвали первым.",
        "Из 100 вопросов по 33 встретилось имя бренда, по 31 — сайты в источниках. Всего 20 разных URL.",
        "Два сайта получили 135 159 кликов и 1 368 682 показа в Google за доступный период.",
        "Присутствие расширилось на четыре географических рынка.",
        "Покупатели встречают бренд в журнале, каталоге, поиске изделий и рекомендациях ИИ.",
    ],
    "winline": [
        "WINLINE в ответах ИИ. Исследование видимости и план действий для команды.",
        "300 вопросов, пять моделей и десять прогонов дали 15 000 замеров.",
        "Исследование охватило спортивную справку, вопросы о ставках, выбор и условия продукта.",
        "В отчёте отдельно учтены бренд в тексте, домен в источниках, ссылка и целевая страница.",
        "Упоминания и полные URL сравнили с показателями конкурентов.",
        "У каждого замера сохранены вопрос, дата, версия модели, ответ и источники.",
        "Редакция и разработчики получили рекомендации по тексту и реализации страниц.",
        "124 темы и 300 вопросов связаны со 119 URL.",
        "В комплекте 12 листов рабочей книги и 26 слайдов аудита.",
        "Команда получила задачи по материалам, доступности контента, разметке и работе URL.",
        "Какие вопросы покупателей стоит исследовать в вашей нише?",
    ],
}


def deck(key, name, asset):
    slides = []
    for index, caption in enumerate(SLIDES[key], 1):
        src = '{PRE}' + asset(f'cases/{key}-{index:02d}.webp')
        slides.append(f'''<figure class="deck-slide">
          <a href="{src}" target="_blank" rel="noopener" aria-label="Открыть слайд {index} в полном размере">
          <img src="{src}" width="1600" height="900" loading="lazy" decoding="async" alt="{escape(caption)}"></a>
          <figcaption>{escape(caption)}</figcaption></figure>''')
    size = len(slides)
    return f'''<div class="slide-reader" role="region" aria-label="Презентация: {name}">
      <div class="slide-track" id="slides-{key}" tabindex="0" aria-label="Слайды презентации">{''.join(slides)}</div>
      <div class="deck-nav"><span>Презентация · {size} слайдов</span><div class="deck-controls" hidden>
      <button type="button" data-back aria-controls="slides-{key}" aria-label="Предыдущий слайд">←</button>
      <output aria-live="polite" aria-atomic="true">1 / {size}</output>
      <button type="button" data-next aria-controls="slides-{key}" aria-label="Следующий слайд">→</button></div></div></div>'''


def case_studies(asset):
    logo = '{PRE}' + asset('cases/winline.svg')
    return f'''<header class="wrap portfolio-head"><h1>Что GEO дало бизнесу?</h1>
      <p class="short-answer">Для модного бренда мы проследили путь от первых рекомендаций до переходов на сайт. Для WINLINE проверили ответы пяти нейросетей и связали выводы с конкретными страницами.</p>
      <nav class="case-jumps" aria-label="Выбрать кейс"><a href="#case-fashion">Модный бренд · NDA ↓</a><a href="#case-winline">WINLINE ↓</a></nav></header>
      <section class="portfolio-project wrap" id="case-fashion"><div class="project-intro">
      <span class="nda-stamp" aria-label="Название клиента закрыто">NDA</span>
      <h2>Как покупатели нашли модный бренд через ИИ?</h2>
      <p class="short-answer"><strong class="case-number">10 000+</strong> переходов из нейросетей за шесть месяцев.</p>
      <p>На старте нейросети редко предлагали изделия бренда. К пятому месяцу в отдельных ответах о ручной работе в Дубае бренд уже называли первым. Около 1 500 переходов пришли по запросам без его названия.</p>
      <a class="edition-link" href="{{PRE}}audit/#observations">Посмотреть замер по 100 вопросам ↗</a>
      </div>{deck("fashion","Международный модный бренд",asset)}</section>
      <section class="portfolio-project wrap" id="case-winline"><div class="project-intro">
      <img class="case-logo" width="483" height="116" src="{logo}" alt="WINLINE">
      <h2>Что показал аудит WINLINE?</h2>
      <p class="short-answer"><strong class="case-number">15 000</strong> замеров по 300 вопросам в пяти моделях, по десять прогонов в каждой.</p>
      <p>Команда получила карту из 124 тем для 119 страниц. Редакция видит, какие условия продукта нейросети передают неточно. Разработчики получили задачи по доступности контента, разметке и адресам страниц.</p>
      <div class="project-delivery"><span><b>12</b> листов рабочей книги</span><span><b>26</b> слайдов аудита</span></div>
      </div>{deck("winline","WINLINE",asset)}</section>'''
