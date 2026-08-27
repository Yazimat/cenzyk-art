# -*- coding: utf-8 -*-
"""Inject production favicon links into site HTML; copy mark into docs/brand."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"preview", "drafts", "tmp-blog", "assets", "scripts"}
MARKER = "<!-- favicon:v1b -->"
BLOCK_RE = re.compile(
    r"\n?  <!-- favicon:v1b -->\n(?:  <link rel=\"(?:icon|apple-touch-icon)\"[^>]*>\n)+"
)


def snippet(prefix: str) -> str:
    return (
        f"  {MARKER}\n"
        f'  <link rel="icon" href="{prefix}assets/favicon/favicon.svg" type="image/svg+xml" />\n'
        f'  <link rel="icon" href="{prefix}assets/favicon/favicon-32.png" type="image/png" sizes="32x32" />\n'
        f'  <link rel="apple-touch-icon" href="{prefix}assets/favicon/apple-touch-icon.png" sizes="180x180" />\n'
    )


def depth_prefix(rel: Path) -> str:
    return "../" * (len(rel.parts) - 1)


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


def inject_pages() -> None:
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if any(part in SKIP for part in rel.parts):
            continue
        text = path.read_text(encoding="utf-8")
        text2 = BLOCK_RE.sub("\n", text)
        prefix = depth_prefix(rel)
        block = snippet(prefix)
        m = re.search(r'[ \t]*<link rel="stylesheet"', text2)
        if not m:
            m = re.search(r"[ \t]*</head>", text2)
        if not m:
            print("SKIP", rel)
            continue
        text2 = text2[: m.start()] + block + text2[m.start() :]
        path.write_text(text2, encoding="utf-8", newline="\n")
        print("ok", rel.as_posix(), "prefix=", repr(prefix or "./"))


if __name__ == "__main__":
    copy_brand()
    inject_pages()
