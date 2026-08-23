# -*- coding: utf-8 -*-
"""Extract richer content from Tilda blog pages into blog-content.json"""
import json
import re
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "tmp-blog"


def strip_tags(html: str) -> str:
    html = re.sub(r"<script[\s\S]*?</script>", "", html, flags=re.I)
    html = re.sub(r"<style[\s\S]*?</style>", "", html, flags=re.I)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    html = re.sub(r"</p>", "\n\n", html, flags=re.I)
    html = re.sub(r"</div>", "\n", html, flags=re.I)
    html = re.sub(r"<li[^>]*>", "• ", html, flags=re.I)
    html = re.sub(r"<[^>]+>", "", html)
    text = unescape(html)
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def field_blocks(raw: str, field: str) -> list[str]:
    out = []
    # field="title" etc.
    for m in re.finditer(rf'field="{field}"[^>]*>(.*?)</div>', raw, re.I | re.S):
        t = strip_tags(m.group(1))
        if t and len(t) > 2:
            out.append(t)
    return out


def extract_mediadata(raw: str) -> list[str]:
    return sorted(set(re.findall(r"mediadata:\s*'([^']+)'", raw)))


def uniq_keep(seq):
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def main():
    # From earlier scrape + HTML
    posts = [
        {
            "slug": "otkrytoe-serdce",
            "file": "post1.html",
            "title": "Открытое Сердце",
            "date": "15.01.2026",
            "preview": "Открытое Сердце — эскиз кашпо",
            "cover_url": "https://static.tildacdn.com/tild6662-3830-4466-b936-363034646535/photo_2026-02-01_12-.jpg",
            "type": "article",
        },
        {
            "slug": "steny-placha",
            "file": "post2.html",
            "title": "Стены плача, как спасти ограждение от ржавчины?",
            "date": "17.11.2025",
            "preview": "Разбираюсь в вопросе «потечет — не должно»",
            "cover_url": "https://static.tildacdn.com/tild3939-6635-4133-a233-353139643463/____.jpg",
            "type": "article",
        },
        {
            "slug": "zachistka-shvov",
            "file": "post3.html",
            "title": "Красивая зачистка сварочных швов — миф или реальность?",
            "date": "19.09.2025",
            "preview": "Разбираюсь в вопросе зачистки сварочных швов",
            "cover_url": "https://static.tildacdn.com/tild6463-6130-4232-b662-383738626161/____.jpg",
            "type": "article",
        },
        {
            "slug": "autentichnaya-podkova",
            "file": "post4.html",
            "title": "Аутентичная подкова",
            "date": "29.03.2025",
            "preview": "Видео: не гайд по изготовлению — как подкова выглядит вживую",
            "cover_url": "https://static.tildacdn.com/tild3561-3862-4938-b734-643336326130/12.jpg",
            "type": "video",
        },
    ]

    for p in posts:
        raw = (TMP / p["file"]).read_text(encoding="utf-8", errors="ignore")
        media = extract_mediadata(raw)
        p["media"] = media

        # feed popup text if present
        feed_texts = []
        for m in re.finditer(
            r'class="[^"]*(?:t-feed__post-popup__text|js-feed-post-text)[^"]*"[^>]*>(.*?)</div>\s*<div',
            raw,
            re.I | re.S,
        ):
            t = strip_tags(m.group(1))
            if len(t) > 40:
                feed_texts.append(t)

        # also try looser
        if not feed_texts:
            for m in re.finditer(
                r't-feed__post-popup__text[^>]*>([\s\S]*?)</div>',
                raw,
                re.I,
            ):
                t = strip_tags(m.group(1))
                if len(t) > 40:
                    feed_texts.append(t)

        titles = field_blocks(raw, "title") + field_blocks(raw, "li_title__\\d+")
        # li_title with digits - regex above escaped wrong; do separate
        li_titles = []
        for m in re.finditer(r'field="li_title__\d+"[^>]*>(.*?)</div>', raw, re.I | re.S):
            t = strip_tags(m.group(1))
            if t:
                li_titles.append(t)
        li_descrs = []
        for m in re.finditer(r'field="li_descr__\d+"[^>]*>(.*?)</div>', raw, re.I | re.S):
            t = strip_tags(m.group(1))
            if t:
                li_descrs.append(t)
        descrs = field_blocks(raw, "descr") + field_blocks(raw, "text")

        # image urls from content (exclude logo png)
        imgs = uniq_keep(
            re.findall(
                r"https://static\.tildacdn\.com/tild[^\"'\s>]+\.(?:jpg|jpeg|png|webp)",
                raw,
                re.I,
            )
        )
        imgs = [u for u in imgs if "3333333.png" not in u and "__-___" not in u]

        # Build body paragraphs
        paragraphs = []
        if feed_texts:
            paragraphs.extend(feed_texts[0].split("\n\n"))

        sections = []
        for t, d in zip(li_titles, li_descrs):
            sections.append({"heading": t, "text": d})

        # For page-style posts, gather more text fields
        extra = []
        for m in re.finditer(
            r'class="[^"]*t268__descr[^"]*"[^>]*>(.*?)</div>',
            raw,
            re.I | re.S,
        ):
            t = strip_tags(m.group(1))
            if len(t) > 40:
                extra.append(t)
        for m in re.finditer(
            r'class="[^"]*t268__title[^"]*"[^>]*>(.*?)</div>',
            raw,
            re.I | re.S,
        ):
            t = strip_tags(m.group(1))
            if t:
                # pair later
                pass

        # Cover from og:image if better
        ogimg = re.search(r'property="og:image"\s+content="([^"]+)"', raw, re.I)
        if ogimg:
            p["og_image"] = ogimg.group(1)

        # Prefer feed body for post1; for 2/3 merge intro + sections
        body_paras = [x.strip() for x in paragraphs if x.strip()]
        if not body_paras and descrs:
            # longest descr-like chunks
            long = sorted(set(descrs), key=len, reverse=True)
            body_paras = [long[0]] if long else []

        # If post2/3 have short feed text but rich sections, keep both
        p["paragraphs"] = uniq_keep(body_paras)
        p["sections"] = sections
        p["extra"] = uniq_keep(extra)
        p["images"] = imgs[:12]

        # Also pull t-descr / t-text long blocks for post2 intro after feed
        if p["slug"] in ("steny-placha", "zachistka-shvov") and len("".join(p["paragraphs"])) < 800:
            long_blocks = []
            for m in re.finditer(
                r'<(?:div|p)[^>]*class="[^"]*(?:t-text|t-descr)[^"]*"[^>]*>(.*?)</(?:div|p)>',
                raw,
                re.I | re.S,
            ):
                t = strip_tags(m.group(1))
                if 80 < len(t) < 2000:
                    long_blocks.append(t)
            # keep unique longest-first limited
            long_blocks = uniq_keep(sorted(set(long_blocks), key=len, reverse=True))[:8]
            # chronological-ish: use appearance order instead
            ordered = []
            for m in re.finditer(
                r'<(?:div|p)[^>]*class="[^"]*(?:t-text|t-descr)[^"]*"[^>]*>(.*?)</(?:div|p)>',
                raw,
                re.I | re.S,
            ):
                t = strip_tags(m.group(1))
                if 80 < len(t) < 2000 and t not in ordered:
                    ordered.append(t)
            p["paragraphs"] = uniq_keep(p["paragraphs"] + ordered[:10])

    out_path = TMP / "blog-content.json"
    out_path.write_text(json.dumps(posts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")
    for p in posts:
        print(
            p["slug"],
            "paras",
            len(p["paragraphs"]),
            "chars",
            sum(len(x) for x in p["paragraphs"]),
            "sections",
            len(p["sections"]),
            "imgs",
            len(p["images"]),
            "media",
            p["media"],
        )


if __name__ == "__main__":
    main()
