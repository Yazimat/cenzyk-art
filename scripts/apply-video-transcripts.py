# -*- coding: utf-8 -*-
"""Inject Whisper-based read versions into index.html and blog pages."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "scripts" / "video-transcripts.json").read_text(encoding="utf-8"))


def read_html(key: str) -> str:
    paras = DATA[key]["paragraphs"]
    lines = [
        '            <div class="bp-read">',
        '              <p class="bp-section-label">Версия для чтения</p>',
        '              <p class="bp-read-note">Текст расшифрован с ролика (Whisper), вычитка по смыслу.</p>',
    ]
    for p in paras:
        lines.append(f"              <p>{p}</p>")
    lines.append("            </div>")
    return "\n".join(lines)


def replace_read_block(html: str, template_id: str, read_block: str) -> str:
    pattern = (
        rf'(<template id="{re.escape(template_id)}">[\s\S]*?)'
        rf'<div class="bp-read">[\s\S]*?</div>\n'
        rf'(\s*</div>\n\s*<footer class="bp-foot">)'
    )

    def repl(m):
        return m.group(1) + read_block + "\n" + m.group(2)

    new_html, n = re.subn(pattern, repl, html, count=1)
    if n != 1:
        raise SystemExit(f"replace failed for {template_id}: {n}")
    return new_html


def main():
    index = ROOT / "index.html"
    html = index.read_text(encoding="utf-8")
    html = replace_read_block(html, "blog-popup-video-1", read_html("cold-forge"))
    html = replace_read_block(html, "blog-popup-video-2", read_html("horseshoe"))
    html = replace_read_block(html, "blog-popup-video-3", read_html("acceptance"))
    index.write_text(html, encoding="utf-8")
    print("updated index.html")

    # blog SEO pages
    mapping = {
        "kholodnaya-kovka": "cold-forge",
        "priemka-izdeliya": "acceptance",
        "autentichnaya-podkova": "horseshoe",
    }
    for slug, key in mapping.items():
        path = ROOT / "blog" / slug / "index.html"
        page = path.read_text(encoding="utf-8")
        read = read_html(key).replace("            ", "          ")
        read = read.replace('class="bp-read-note"', 'class="bp-read-note tiny"')
        pattern = (
            r"(<p><a href=\"https://vk\.ru/[^\"]+\"[^>]*>[^<]+</a></p>|"
            r"<p>Не гайд по изготовлению[^<]*</p>)\n"
            r"(?:\s*<div class=\"bp-read\">[\s\S]*?</div>\n)?"
        )
        page2, n = re.subn(pattern, r"\1\n" + read + "\n", page, count=1)
        if n != 1:
            # horseshoe page different structure
            page2, n2 = re.subn(
                r"(<p>Не гайд по изготовлению[\s\S]*?</p>)\n(?:\s*<div class=\"bp-read\">[\s\S]*?</div>\n)?",
                r"\1\n" + read + "\n",
                page,
                count=1,
            )
            if n2 != 1:
                raise SystemExit(f"blog replace failed {slug}")
            page = page2
        else:
            page = page2
        path.write_text(page, encoding="utf-8")
        print("updated", slug)


if __name__ == "__main__":
    main()
