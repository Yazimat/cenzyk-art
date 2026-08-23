# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "tmp-blog"


def strip_tags(html: str) -> str:
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    html = re.sub(r"</p>", "\n\n", html, flags=re.I)
    html = re.sub(r"</div>", "\n", html, flags=re.I)
    html = re.sub(r"<[^>]+>", "", html)
    text = unescape(html)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    title_m = re.search(r"<title>(.*?)</title>", raw, re.I | re.S)
    title = unescape(re.sub(r"\s+", " ", title_m.group(1))).strip() if title_m else ""
    title = re.sub(r"\s*[|·].*$", "", title).strip()

    # Tilda post text blocks
    texts = []
    for pat in [
        r'class="[^"]*t-feed__post-popup__text[^"]*"[^>]*>(.*?)</div>',
        r'class="[^"]*js-feed-post-text[^"]*"[^>]*>(.*?)</div>',
        r'itemprop="articleBody"[^>]*>(.*?)</div>',
        r'class="[^"]*t-text[^"]*"[^>]*>(.*?)</div>',
        r'data-field="text"[^>]*>(.*?)</div>',
    ]:
        for m in re.finditer(pat, raw, re.I | re.S):
            t = strip_tags(m.group(1))
            if len(t) > 80:
                texts.append(t)

    # og:description fallback
    og = re.search(r'property="og:description"\s+content="([^"]*)"', raw, re.I)
    og_desc = unescape(og.group(1)) if og else ""

    imgs = sorted(set(re.findall(r'https://static\.tildacdn\.com/[^"\'\s>]+\.(?:jpg|jpeg|png|webp)', raw, re.I)))
    vids = sorted(set(re.findall(r'https://[^"\'\s>]+\.(?:mp4|webm|mov)', raw, re.I)))
    # tilda video cdn patterns
    vids += sorted(set(re.findall(r'https://[^"\'\s>]*tildacdn[^"\'\s>]+\.(?:mp4|webm)', raw, re.I)))
    vids = sorted(set(vids))

    # video in data attributes / youtube / vk
    embeds = sorted(set(re.findall(r'https://(?:www\.)?(?:youtube\.com/embed/[^"\'\s]+|youtu\.be/[^"\'\s]+|vk\.com/video_ext\.php[^"\'\s]+)', raw, re.I)))

    # date
    date_m = re.search(r'(\d{2}\.\d{2}\.\d{4})', raw)
    date = date_m.group(1) if date_m else ""

    # pick longest text
    body = max(texts, key=len) if texts else og_desc

    return {
        "file": path.name,
        "title": title,
        "date": date,
        "body_len": len(body),
        "body": body,
        "og_desc": og_desc,
        "imgs": imgs[:30],
        "vids": vids,
        "embeds": embeds,
        "raw_len": len(raw),
    }


def main():
    out = []
    for name in ["post1.html", "post2.html", "post3.html", "post4.html"]:
        p = TMP / name
        if p.exists():
            out.append(extract(p))
    (TMP / "parsed.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    for item in out:
        print("===", item["file"], item["title"], item["date"], "body", item["body_len"], "imgs", len(item["imgs"]), "vids", item["vids"], "embeds", item["embeds"])
        print(item["body"][:400].replace("\n", " | "))
        print()


if __name__ == "__main__":
    main()
