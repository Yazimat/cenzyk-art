# -*- coding: utf-8 -*-
from pathlib import Path
import re
import urllib.request

fonts = Path(__file__).resolve().parents[1] / "assets" / "fonts"
ua = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
css_url = (
    "https://fonts.googleapis.com/css2?family=Archivo+Black"
    "&family=Space+Grotesk:wght@500;700"
    "&family=IBM+Plex+Mono:wght@400;600&display=swap"
)
req = urllib.request.Request(css_url, headers={"User-Agent": ua})
raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
(fonts / "_google.css").write_text(raw, encoding="utf-8")

faces = re.findall(
    r"(/\*\s*([^*]+?)\s*\*/\s*)?@font-face\s*\{([^}]+)\}",
    raw,
    flags=re.S,
)
keep_labels = {"cyrillic", "cyrillic-ext", "latin", "latin-ext"}
out_blocks = []
for _c, label, body in faces:
    lab = (label or "").strip().lower()
    if lab and lab not in keep_labels:
        continue
    url_m = re.search(r"url\((https://fonts\.gstatic\.com/s/[^)]+\.woff2)\)", body)
    if not url_m:
        continue
    url = url_m.group(1)
    name = url.rsplit("/", 1)[-1]
    dest = fonts / name
    if not dest.exists() or dest.stat().st_size < 1000:
        fr = urllib.request.Request(url, headers={"User-Agent": ua})
        dest.write_bytes(urllib.request.urlopen(fr, timeout=30).read())
        print("dl", name, dest.stat().st_size)
    body2 = body.replace(url, name)
    fam = re.search(r"font-family:\s*'([^']+)'", body2)
    weight = re.search(r"font-weight:\s*(\d+)", body2)
    print(
        "keep",
        lab or "?",
        fam.group(1) if fam else "?",
        weight.group(1) if weight else "?",
        name,
    )
    out_blocks.append(f"/* {lab or 'subset'} */\n@font-face {{{body2}}}")

(fonts / "site-fonts.css").write_text(
    "/* Self-hosted site fonts */\n\n" + "\n\n".join(out_blocks) + "\n",
    encoding="utf-8",
)
print("faces", len(out_blocks))
(fonts / "_google.css").unlink(missing_ok=True)
