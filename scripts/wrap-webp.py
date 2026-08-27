# -*- coding: utf-8 -*-
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
img_dir = root / "assets" / "images"
index = root / "index.html"
text = index.read_text(encoding="utf-8")

names = []
for webp in img_dir.glob("*.webp"):
    jpg = webp.with_suffix(".jpg")
    if not jpg.exists():
        continue
    if webp.stat().st_size <= int(jpg.stat().st_size * 1.02):
        names.append(webp.stem)
    else:
        webp.unlink(missing_ok=True)
        print("removed larger", webp.name)

print("use webp for", sorted(names))
v = "20260827b"


def repl(m: re.Match) -> str:
    full = m.group(0)
    src = m.group(1)
    path = src.split("?")[0]
    base = path.split("/")[-1]
    stem, ext = base.rsplit(".", 1)
    if ext.lower() != "jpg" or stem not in names:
        return full
    img2 = re.sub(
        r'src="[^"]+"',
        f'src="assets/images/{stem}.jpg?v={v}"',
        full,
        count=1,
    )
    return (
        "<picture>"
        f'<source type="image/webp" srcset="assets/images/{stem}.webp?v={v}" />'
        f"{img2}"
        "</picture>"
    )


pattern = re.compile(
    r'<img\b[^>]*src="(assets/images/[^"]+\.jpg[^"]*)"[^>]*>',
    re.I,
)
new_text, n = pattern.subn(repl, text)
index.write_text(new_text, encoding="utf-8")
print("wrapped", n, "picture count", new_text.count("<picture>"))
