# -*- coding: utf-8 -*-
"""Inject production favicon links into site HTML; copy mark into docs/brand."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"preview", "drafts", "tmp-blog", "assets", "scripts"}
MARKER = "<!-- favicon:v1b -->"
VER = "20260827d"

# Old / broken / current favicon link blocks
BLOCK_RE = re.compile(
    r"(?:\n)?[ \t]*<!-- favicon:v1b -->\n"
    r"(?:[ \t]*<link rel=\"(?:shortcut )?icon|apple-touch-icon\"[^>]*>\n)*"
    r"|"
    r"(?:\n)?[ \t]*\" href=\"[^\"]*favicon[^\"]*\"[^>]*>\n"
    r"(?:[ \t]*<link rel=\"(?:icon|apple-touch-icon)\"[^>]*>\n)+",
    re.MULTILINE,
)
ORPHAN_RE = re.compile(
    r"(?:\n)?[ \t]*(?:<link rel=\"(?:shortcut )?icon|apple-touch-icon\"[^>]*favicon[^>]*>\n"
    r"|\" href=\"[^\"]*favicon[^\"]*\"[^>]*>\n)",
)


def snippet() -> str:
    return (
        f"  {MARKER}\n"
        f'  <link rel="icon" href="/favicon.ico?v={VER}" sizes="any" />\n'
        f'  <link rel="icon" href="/assets/favicon/favicon.svg?v={VER}" type="image/svg+xml" />\n'
        f'  <link rel="icon" href="/assets/favicon/favicon-32.png?v={VER}" type="image/png" sizes="32x32" />\n'
        f'  <link rel="icon" href="/assets/favicon/favicon-16.png?v={VER}" type="image/png" sizes="16x16" />\n'
        f'  <link rel="apple-touch-icon" href="/assets/favicon/apple-touch-icon.png?v={VER}" sizes="180x180" />\n'
    )


def copy_brand() -> None:
    brand_dir = ROOT / "docs" / "brand"
    brand_dir.mkdir(parents=True, exist_ok=True)
    for name in (
        "favicon.svg",
        "favicon-512.png",
        "favicon-32.png",
        "apple-touch-icon.png",
        "v1b-no-frame.svg",
    ):
        src = ROOT / "assets" / "favicon" / name
        if src.exists():
            shutil.copy2(src, brand_dir / name)
            print("brand", name)
    ico = ROOT / "favicon.ico"
    if ico.exists():
        shutil.copy2(ico, brand_dir / "favicon.ico")
        print("brand favicon.ico")


def clean_favicon_lines(text: str) -> str:
    # Remove any favicon-related link lines and marker
    text = re.sub(r"[ \t]*<!-- favicon:v1b -->\n?", "", text)
    text = re.sub(
        r"[ \t]*<link rel=\"(?:shortcut )?icon\"[^>]*>\n?",
        "",
        text,
    )
    text = re.sub(
        r"[ \t]*<link rel=\"apple-touch-icon\"[^>]*>\n?",
        "",
        text,
    )
    # Broken remnant from bad regex: `" href="...favicon..." />`
    text = re.sub(
        r"[ \t]*\" href=\"[^\"]*favicon[^\"]*\"[^>]*>\n?",
        "",
        text,
    )
    return text


def inject_pages() -> None:
    block = snippet()
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if any(part in SKIP for part in rel.parts):
            continue
        text = path.read_text(encoding="utf-8")
        text2 = clean_favicon_lines(text)
        m = re.search(r'[ \t]*<link rel="stylesheet"', text2)
        if not m:
            m = re.search(r"[ \t]*</head>", text2)
        if not m:
            print("SKIP", rel)
            continue
        text2 = text2[: m.start()] + block + text2[m.start() :]
        path.write_text(text2, encoding="utf-8", newline="\n")
        print("ok", rel.as_posix())


if __name__ == "__main__":
    copy_brand()
    inject_pages()
