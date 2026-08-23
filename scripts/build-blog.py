# -*- coding: utf-8 -*-
"""Download blog media and inject expandable articles into index.html"""
import json
import re
import urllib.request
from html import escape
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "tmp-blog"
IMG_DIR = ROOT / "assets" / "images"
CONTENT = json.loads((TMP / "blog-content.json").read_text(encoding="utf-8"))


def download(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; cenzyk-art-build/1.0)"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def save_cover(url: str, dest: Path, size=(1280, 720)) -> None:
    raw = download(url)
    im = Image.open(BytesIO(raw)).convert("RGB")
    tw, th = size
    # center crop to 16:9 then resize
    w, h = im.size
    target_ratio = tw / th
    ratio = w / h
    if ratio > target_ratio:
        nw = int(h * target_ratio)
        left = (w - nw) // 2
        im = im.crop((left, 0, left + nw, h))
    else:
        nh = int(w / target_ratio)
        top = (h - nh) // 2
        im = im.crop((0, top, w, top + nh))
    im = im.resize(size, Image.Resampling.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "JPEG", quality=88, optimize=True)


def save_sq(url: str, dest: Path, size=1080) -> None:
    raw = download(url)
    im = Image.open(BytesIO(raw)).convert("RGB")
    w, h = im.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    im = im.crop((left, top, left + side, top + side)).resize(
        (size, size), Image.Resampling.LANCZOS
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "JPEG", quality=88, optimize=True)


def paras_html(paras: list[str]) -> str:
    chunks = []
    for p in paras:
        # split on single newlines inside for multi-line paras
        parts = [x.strip() for x in re.split(r"\n+", p) if x.strip()]
        for part in parts:
            if part.startswith("#"):
                chunks.append(f'<p class="blog-hashtags">{escape(part)}</p>')
            else:
                chunks.append(f"<p>{escape(part)}</p>")
    return "\n".join(chunks)


def sections_html(sections: list[dict]) -> str:
    if not sections:
        return ""
    bits = ['<div class="blog-sections">']
    for s in sections:
        bits.append('<div class="blog-section">')
        bits.append(f"<h4>{escape(s['heading'])}</h4>")
        for part in [x.strip() for x in re.split(r"\n+", s["text"]) if x.strip()]:
            bits.append(f"<p>{escape(part)}</p>")
        bits.append("</div>")
    bits.append("</div>")
    return "\n".join(bits)


def gallery_html(paths: list[str], alt: str) -> str:
    if not paths:
        return ""
    bits = ['<div class="blog-gallery">']
    for i, src in enumerate(paths, 1):
        bits.append(
            f'<figure><img src="{escape(src)}" alt="{escape(alt)} — фото {i}" '
            f'width="1080" height="1080" loading="lazy" /></figure>'
        )
    bits.append("</div>")
    return "\n".join(bits)


def build_article(post: dict, cover_rel: str, gallery_rels: list[str]) -> str:
    tag = "Видео" if post["type"] == "video" else "Статья"
    body_parts = []

    # Deduplicate: if sections exist, drop paragraph copies of section texts
    section_texts = {s["text"].strip() for s in post.get("sections") or []}
    paras = []
    for p in post.get("paragraphs") or []:
        # skip JS pollution
        if "function " in p or "dict[" in p or "t_feed_" in p or "var " in p[:20]:
            continue
        if p.strip() in section_texts:
            continue
        # skip exact duplicates of section bodies when paragraph is only that
        paras.append(p)

    # video post: short caption only
    if post["type"] == "video":
        paras = [post["preview"].replace("Видео: ", "")]

    body_parts.append(paras_html(paras))
    body_parts.append(sections_html(post.get("sections") or []))

    for e in post.get("extra") or []:
        if e.strip() and e.strip() not in section_texts and e not in paras:
            body_parts.append(paras_html([e]))

    body_parts.append(gallery_html(gallery_rels, post["title"]))

    if post["type"] == "video" and post.get("media"):
        url = post["media"][0]
        # rutube private -> embed
        m = re.search(r"rutube\.ru/video/private/([a-f0-9]+)/\?p=([^&\s]+)", url)
        if m:
            embed = f"https://rutube.ru/play/embed/{m.group(1)}/?p={m.group(2)}"
        else:
            embed = url
        body_parts.append(
            '<div class="blog-video">'
            f'<iframe src="{escape(embed)}" title="{escape(post["title"])}" '
            'allow="clipboard-write; autoplay" allowfullscreen loading="lazy"></iframe>'
            "</div>"
        )

    body = "\n".join(x for x in body_parts if x)

    return f'''        <details class="blog-article">
          <summary class="blog-summary">
            <div class="blog-media">
              <img src="{escape(cover_rel)}" alt="{escape(post['title'])}" width="1280" height="720" loading="lazy" />
            </div>
            <div class="blog-summary-text">
              <span class="blog-tag">{tag}</span>
              <span class="blog-date">{escape(post["date"])}</span>
              <h3>{escape(post["title"])}</h3>
              <p>{escape(post["preview"])}</p>
            </div>
          </summary>
          <div class="blog-article-body">
{body}
          </div>
        </details>'''


def main():
    articles_html = []
    for i, post in enumerate(CONTENT, 1):
        cover_path = IMG_DIR / f"blog-{i:02d}-cover.jpg"
        cover_url = post.get("cover_url") or post.get("og_image") or (post.get("images") or [None])[0]
        # Prefer real photo over broken feed placeholder ____.jpg if download fails
        candidates = [cover_url, post.get("og_image")] + (post.get("images") or [])
        candidates = [c for c in candidates if c]
        # skip thb resize for better quality when static exists
        saved = False
        last_err = None
        for url in candidates:
            # prefer static full images
            if "thb.tildacdn" in url:
                continue
            try:
                print("cover", post["slug"], url[:80])
                save_cover(url, cover_path)
                saved = True
                break
            except Exception as e:
                last_err = e
                print("  fail", e)
        if not saved:
            # try thb as last resort
            for url in candidates:
                try:
                    save_cover(url, cover_path)
                    saved = True
                    break
                except Exception as e:
                    last_err = e
            if not saved:
                raise RuntimeError(f"cover failed for {post['slug']}: {last_err}")

        gallery_rels = []
        # gallery for articles with multiple images (skip cover duplicate)
        imgs = post.get("images") or []
        # post1: all sketch photos; post2/3: a few process photos
        take = imgs[:5] if post["slug"] == "otkrytoe-serdce" else imgs[:4]
        if post["type"] == "video":
            take = []
        for j, url in enumerate(take, 1):
            if "____.jpg" in url or "3333333" in url:
                continue
            dest = IMG_DIR / f"blog-{i:02d}-{j:02d}.jpg"
            try:
                print("img", dest.name)
                save_sq(url, dest, 1080 if post["slug"] == "otkrytoe-serdce" else 1080)
                gallery_rels.append(f"assets/images/{dest.name}")
            except Exception as e:
                print("  skip", e)

        articles_html.append(
            build_article(post, f"assets/images/{cover_path.name}", gallery_rels)
        )

    block = "\n".join(articles_html)
    index = ROOT / "index.html"
    html = index.read_text(encoding="utf-8")
    new_section = f'''    <section class="section blog" id="blog">
      <div class="wrap">
        <p class="eyebrow">Мой Блог</p>
        <h2>Статьи и превью видео из мастерской</h2>
        <div class="blog-list">
{block}
        </div>
      </div>
    </section>'''

    html2, n = re.subn(
        r'    <section class="section blog" id="blog">[\s\S]*?</section>',
        new_section,
        html,
        count=1,
    )
    if n != 1:
        raise SystemExit(f"blog section replace count={n}")
    html2 = html2.replace("site.css?v=20260814b", "site.css?v=20260814c")
    index.write_text(html2, encoding="utf-8")
    print("Updated index.html")


if __name__ == "__main__":
    main()
