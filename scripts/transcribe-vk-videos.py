# -*- coding: utf-8 -*-
"""Download VK video MP4 URLs and transcribe with Whisper."""
import json
import re
import ssl
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "tmp-blog"
TMP.mkdir(exist_ok=True)
ctx = ssl._create_unverified_context()
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0"}

VIDEOS = [
    ("cold-forge", "https://vk.com/video_ext.php?oid=28068378&id=456239171&hd=2"),
    ("acceptance", "https://vk.com/video_ext.php?oid=28068378&id=456239182&hd=2"),
    ("horseshoe", "https://rutube.ru/video/private/2b882ccae4195cea3b3fd06eef558215/?p=uxAhoj2mJ9xk-Qbz75cJxQ"),
]


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=30, context=ctx).read().decode("utf-8", "replace")


def extract_mp4(html: str) -> str | None:
    # video_ext.php embeds JSON with url240/360/480/720
    for pat in [
        r'"url720"\s*:\s*"([^"]+)"',
        r'"url480"\s*:\s*"([^"]+)"',
        r'"url360"\s*:\s*"([^"]+)"',
        r'"mp4_\d+"\s*:\s*"([^"]+)"',
        r'"(https:\\/\\/[^"]+\.mp4[^"]*)"',
    ]:
        m = re.search(pat, html)
        if m:
            return m.group(1).replace("\\/", "/")
    return None


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers=UA)
    data = urllib.request.urlopen(req, timeout=120, context=ctx).read()
    dest.write_bytes(data)
    print("downloaded", dest.name, len(data))


def transcribe(audio: Path) -> str:
    import whisper

    model = whisper.load_model("small")
    result = model.transcribe(str(audio), language="ru", fp16=False)
    return result.get("text", "").strip()


def main():
    results = {}
    for slug, page_url in VIDEOS:
        print("===", slug, page_url)
        try:
            html = fetch(page_url)
            (TMP / f"{slug}-embed.html").write_text(html[:50000], encoding="utf-8")
            mp4 = extract_mp4(html)
            if not mp4 and "rutube" in page_url:
                print("rutube skip - need yt-dlp")
                continue
            if not mp4:
                print("no mp4 in embed, html len", len(html))
                continue
            print("mp4", mp4[:80])
            vid = TMP / f"{slug}.mp4"
            download(mp4, vid)
            # whisper can read mp4 directly if ffmpeg in path
            text = transcribe(vid)
            results[slug] = text
            (TMP / f"{slug}-transcript.txt").write_text(text, encoding="utf-8")
            print("TRANSCRIPT:", text[:500])
        except Exception as e:
            print("ERR", slug, e)
            results[slug] = f"ERROR: {e}"

    (TMP / "transcripts.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
