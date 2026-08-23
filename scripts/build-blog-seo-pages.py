# -*- coding: utf-8 -*-
"""Generate static SEO blog pages from article definitions."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = "../../assets/css/site.css?v=20260823u"
SITE = "https://илай-металл.рф"
TRANSCRIPTS = json.loads((ROOT / "scripts" / "video-transcripts.json").read_text(encoding="utf-8"))


def video_read_block(key: str) -> str:
    paras = TRANSCRIPTS[key]["paragraphs"]
    lines = [
        '<div class="bp-read">',
        '  <p class="bp-section-label">Версия для чтения</p>',
        '  <p class="bp-read-note tiny">Текст расшифрован с ролика (Whisper), вычитка по смыслу.</p>',
    ]
    for p in paras:
        lines.append(f"  <p>{p}</p>")
    lines.append("</div>")
    return "\n".join(lines)

ARTICLES = [
    {
        "slug": "otkrytoe-serdce",
        "title": "Открытое Сердце — эскиз кашпо | Блог Илай Саматов",
        "h1": "Открытое Сердце",
        "date": "15.01.2026",
        "description": "Эскиз кашпо «Открытое Сердце»: референсы заказчика, буквы «Л», крепление в проём. Илай Саматов — изделия из металла, Калининград.",
        "cover": "../../assets/images/blog-01-cover.jpg",
        "body": """
<p>— Накопилось достаточно эскизов! — А достаточно — это сколько? — Достаточно для того, чтобы делать из этого контент.</p>
<p>Открывает рубрику «Эскизы» работа «Открытое сердце». Эскиз выполнен исходя из референсов и пожеланий заказчика. В углах кашпо — буквы «Л», отсылка к имени собственника. Сердце в центре символизирует открытость хозяев дома.</p>
<blockquote class="bp-pull">Крепление — боковое, в проём. Материал — 10‑мм квадрат и рамка из 15‑мм профиля</blockquote>
<p>Усики выполнены методом горячей обработки металла и «завязаны» посредством нагрева газом. Сердце намеренно оставил с пространством внутри — «живое», цветы, станет вишенкой композиции.</p>
""",
    },
    {
        "slug": "steny-placha",
        "title": "Стены плача: как спасти ограждение от ржавчины | Блог",
        "h1": "Стены плача, как спасти ограждение от ржавчины?",
        "date": "17.11.2025",
        "description": "Жидкий цинк, цинкование и защита швов от ржавчины. Илай Саматов — специалист по изготовлению изделий из металла, Калининград.",
        "cover": "../../assets/images/blog-02-cover.jpg",
        "body": """
<p>Здравствуйте! Я — Илай Саматов: специалист по изготовлению изделий из металла, сварщик, слесарь, кузнец. Сегодня разберём ржавчину: тревожные звоночки и как предотвратить металлический абьюз вашего изделия.</p>
<p>Ржавчина — красно‑бурая зараза, что пожирает железо и сталь. Кислород с водой — и на поверхности рыхлый налёт. Вчера — блестящая деталь, сегодня — трухлявый скелет.</p>
<blockquote class="bp-pull">Не жди ржавых подтёков — нанеси цинк туда, куда краска не заглянет</blockquote>
<p>Ржавых подтёков можно избежать: в процессе сборки обрабатываем труднодоступные места жидким цинком. Правило простое: наносим цинк везде, куда впоследствии не сможет проникнуть краска.</p>
<h2>Жидкий цинк 96%</h2>
<p>Защищает активно и пассивно. Проливай в щели, мажь перед установкой поручня.</p>
<h2>Цинкование</h2>
<p>Труднодоступные места — туда, куда не попадёт краска после сборки.</p>
""",
    },
    {
        "slug": "zachistka-shvov",
        "title": "Зачистка сварочных швов — миф или реальность? | Блог",
        "h1": "Красивая зачистка сварочных швов — миф или реальность?",
        "date": "19.09.2025",
        "description": "Почему финишная зачистка швов удваивает стоимость изделия. Илай Саматов — изделия из металла под ключ, Калининград.",
        "cover": "../../assets/images/blog-03-cover.jpg",
        "body": """
<p>Сварочные швы в малом металлопроизводстве — дёшево и быстро. Но заказчик спросит: «Если всё так шустро — отчего цена кусается?» На сцену выходят зачистка и обработка.</p>
<p>Довести дело до блеска — на финишную зачистку уходит порой столько же времени, сколько на само изготовление. Цена не просто растёт — она удваивается. Чем незаметнее труд — тем дороже стоит.</p>
<h2>Лепесток P40 с цирконом</h2>
<p>Циркон — против некрасивых швов. Зерно P40 — для быстрой зачистки.</p>
<h2>Абразивный диск с тарелкой</h2>
<p>Вторым номером — идеальная плоскость, зерно P60–P100.</p>
""",
    },
    {
        "slug": "kholodnaya-kovka",
        "title": "Холодной ковки не существует — видео | Блог Илай Саматов",
        "h1": "Холодной ковки не существует",
        "date": "25.06.2026",
        "description": "Видео из мастерской: почему «холодной ковки» не бывает. Илай Саматов — изготовление изделий из металла, Калининград.",
        "cover": "../../assets/images/blog-video-cold-forge.jpg",
        "body": f"""
<div class="bp-video bp-video-portrait">
  <iframe src="https://vk.com/video_ext.php?oid=28068378&amp;id=456239171&amp;hd=2" title="Холодной ковки не существует" allow="autoplay; encrypted-media; fullscreen; picture-in-picture" allowfullscreen loading="lazy"></iframe>
</div>
<p><a href="https://vk.ru/wall28068378_2115" rel="noopener" target="_blank">Открыть во ВКонтакте</a></p>
{video_read_block("cold-forge")}
""",
    },
    {
        "slug": "autentichnaya-podkova",
        "title": "Аутентичная подкова — видео | Блог",
        "h1": "Аутентичная подкова",
        "date": "29.03.2025",
        "description": "Как подкова выглядит вживую — не гайд по изготовлению. Илай Саматов, Калининград.",
        "cover": "../../assets/images/blog-04-cover.jpg",
        "body": f"""
<div class="bp-video bp-video-portrait">
  <iframe src="https://vk.com/video_ext.php?oid=28068378&amp;id=456239152&amp;hd=2" title="Аутентичная подкова" allow="autoplay; encrypted-media; fullscreen; picture-in-picture" allowfullscreen loading="lazy"></iframe>
</div>
<p><a href="https://vk.ru/clip28068378_456239152" rel="noopener" target="_blank">Открыть клип во ВКонтакте</a></p>
{video_read_block("horseshoe")}
""",
    },
    {
        "slug": "priemka-izdeliya",
        "title": "Куда смотреть при приёмке изделия — видео | Блог",
        "h1": "Куда смотреть при приёмке изделия",
        "date": "06.08.2026",
        "description": "Что проверить, когда изделие из металла уже у вас в руках. Видео Илай Саматов, Калининград.",
        "cover": "../../assets/images/blog-video-acceptance.jpg",
        "body": f"""
<div class="bp-video bp-video-portrait">
  <iframe src="https://vk.com/video_ext.php?oid=28068378&amp;id=456239182&amp;hd=2" title="Куда смотреть при приёмке изделия" allow="autoplay; encrypted-media; fullscreen; picture-in-picture" allowfullscreen loading="lazy"></iframe>
</div>
<p><a href="https://vk.ru/clip28068378_456239182" rel="noopener" target="_blank">Открыть клип во ВКонтакте</a></p>
{video_read_block("acceptance")}
""",
    },
]


def shell(article: dict) -> str:
    url = f"{SITE}/blog/{article['slug']}/"
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <script src="../../assets/js/domain-redirect.js"></script>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{article['title']}</title>
  <meta name="description" content="{article['description']}" />
  <link rel="canonical" href="{url}" />
  <meta property="og:title" content="{article['h1']}" />
  <meta property="og:description" content="{article['description']}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{SITE}/assets/images/blog-01-cover.jpg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Space+Grotesk:wght@500;700&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{CSS}" />
</head>
<body class="grain page-blog-article">
  <header class="site-header">
    <a class="brand" href="../../">
      <span class="brand-name">Илай Саматов</span>
      <span class="brand-role">Дизайн / Проектирование / Производство</span>
    </a>
    <nav class="nav" aria-label="Основное меню">
      <a href="../../#services">Направления</a>
      <a href="../../#portfolio">Портфолио</a>
      <a href="../../#blog" aria-current="page">Блог</a>
      <a class="nav-phone" href="tel:+79520589278">+7 952 058-92-78</a>
      <a class="nav-cta" href="../../#meeting">Связь</a>
    </nav>
  </header>
  <main class="section">
    <div class="wrap narrow">
      <p class="eyebrow"><a href="../../#blog">← Блог на главной</a> · {article['date']}</p>
      <article class="bp-post">
        <header class="bp-head">
          <h1>{article['h1']}</h1>
        </header>
        <figure class="bp-cover">
          <img src="{article['cover']}" alt="{article['h1']}" width="1280" height="720" loading="eager" />
        </figure>
        <div class="bp-body">
{article['body'].strip()}
        </div>
        <footer class="bp-foot">
          <a class="btn btn-primary" href="../../#meeting">Обсудить задачу</a>
          <p class="bp-follow"><a href="https://t.me/CenzykT_G" rel="noopener" target="_blank">Telegram-канал с работами</a></p>
        </footer>
      </article>
    </div>
  </main>
  <footer class="site-footer">
    <p class="copy">© Саматов И. В. / 2026 · <a href="../../">На главную</a></p>
  </footer>
</body>
</html>
"""


def main():
    for article in ARTICLES:
        dest = ROOT / "blog" / article["slug"] / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(shell(article), encoding="utf-8")
        print("wrote", dest.relative_to(ROOT))


if __name__ == "__main__":
    main()
