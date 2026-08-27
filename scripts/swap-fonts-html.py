# -*- coding: utf-8 -*-
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
pat = re.compile(
    r"\s*<link rel=\"preconnect\" href=\"https://fonts\.googleapis\.com\" />\s*"
    r"<link rel=\"preconnect\" href=\"https://fonts\.gstatic\.com\" crossorigin />\s*"
    r"<link href=\"https://fonts\.googleapis\.com/css2\?[^\"]+\" rel=\"stylesheet\" />\s*",
    re.I,
)
pat2 = re.compile(
    r"\s*<link href=\"https://fonts\.googleapis\.com/css2\?[^\"]+\" rel=\"stylesheet\" />\s*",
    re.I,
)

files = list((root / "blog").rglob("index.html"))
files += [root / "kontakty" / "index.html", root / "privacy" / "index.html"]

for f in files:
    t = f.read_text(encoding="utf-8")
    if f.parent.name == "blog":
        rel = "../"
    elif f.parent.parent.name == "blog":
        rel = "../../"
    else:
        rel = "../"
    repl = f'  <link rel="stylesheet" href="{rel}assets/fonts/site-fonts.css?v=20260827b" />\n'
    nt, n = pat.subn(repl, t, count=1)
    if n == 0:
        nt, n = pat2.subn(repl, t, count=1)
    if n:
        nt = re.sub(r"(assets/css/site\.css\?v=)[^\"\s]+", r"\g<1>20260827b", nt)
        if 'name="referrer"' not in nt:
            nt = nt.replace(
                "<meta charset=\"UTF-8\" />",
                "<meta charset=\"UTF-8\" />\n  <meta name=\"referrer\" content=\"strict-origin-when-cross-origin\" />",
                1,
            )
        f.write_text(nt, encoding="utf-8")
        print("ok", f.relative_to(root))
    else:
        print("skip", f.relative_to(root))
