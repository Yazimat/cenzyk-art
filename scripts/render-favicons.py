# -*- coding: utf-8 -*-
"""Rasterize brand favicon v1B — pixel-hinted 16/32 for crisp browser tabs."""
from __future__ import annotations

import io
import struct
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1] / "assets" / "favicon"
ROOT = Path(__file__).resolve().parents[1]
CREAM = (242, 239, 231, 255)
INK = (20, 22, 19, 255)
YELLOW = (232, 184, 0, 255)


def canvas(size: int) -> Image.Image:
    return Image.new("RGBA", (size, size), CREAM)


def draw_i_hires(draw: ImageDraw.ImageDraw, size: int) -> None:
    s = size / 64.0

    def p(x: float, y: float) -> tuple[float, float]:
        return (x * s, y * s)

    # Cyrillic И (/ diagonal) — matches favicon.svg
    draw.polygon(
        [
            p(9, 5),
            p(23, 5),
            p(23, 29),
            p(39, 5),
            p(55, 5),
            p(55, 47),
            p(41, 47),
            p(41, 23),
            p(23, 47),
            p(9, 47),
        ],
        fill=INK,
    )
    draw.rectangle([9 * s, 50 * s, 55 * s, 58 * s], fill=YELLOW)


def favicon_16() -> Image.Image:
    im = canvas(16)
    px = im.load()
    for y in range(0, 12):
        for x in (1, 2, 3):
            px[x, y] = INK
        for x in (12, 13, 14):
            px[x, y] = INK
    # / diagonal (И): top-right → bottom-left
    for y in range(0, 12):
        t = y / 11.0
        cx = int(round(12 - t * 9))
        for dx in (-1, 0, 1):
            x = cx + dx
            if 3 <= x <= 12:
                px[x, y] = INK
    for y in (13, 14, 15):
        for x in range(1, 15):
            px[x, y] = YELLOW
    return im


def favicon_32() -> Image.Image:
    im = canvas(32)
    d = ImageDraw.Draw(im)
    d.rectangle([2, 1, 9, 24], fill=INK)
    d.rectangle([22, 1, 29, 24], fill=INK)
    for y in range(1, 25):
        t = (y - 1) / 23.0
        cx = int(round(24 - t * 18))
        d.rectangle([cx - 2, y, cx + 2, y], fill=INK)
    d.rectangle([2, 26, 29, 31], fill=YELLOW)
    return im


def v1(size: int) -> Image.Image:
    if size == 16:
        return favicon_16()
    if size == 32:
        return favicon_32()
    im = canvas(size)
    draw_i_hires(ImageDraw.Draw(im), size)
    return im


def write_ico(path: Path, images: list[Image.Image]) -> None:
    images = [im.convert("RGBA") for im in images]
    count = len(images)
    offset = 6 + 16 * count
    data = b""
    entries = []
    for im in images:
        buf = io.BytesIO()
        im.save(buf, format="PNG")
        raw = buf.getvalue()
        w, h = im.size
        entries.append((w if w < 256 else 0, h if h < 256 else 0, len(raw), offset + len(data)))
        data += raw
    out = struct.pack("<HHH", 0, 1, count)
    for w, h, size, off in entries:
        out += struct.pack("<BBBBHHII", w, h, 0, 0, 1, 32, size, off)
    path.write_bytes(out + data)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    im16, im32 = favicon_16(), favicon_32()
    for s, name in (
        (16, "favicon-16.png"),
        (32, "favicon-32.png"),
        (180, "apple-touch-icon.png"),
        (512, "favicon-512.png"),
    ):
        im = v1(s)
        path = OUT / name
        im.save(path, optimize=True)
        print("primary", name, path.stat().st_size)
    write_ico(ROOT / "favicon.ico", [im16, im32])
    print("ico", (ROOT / "favicon.ico").stat().st_size)


if __name__ == "__main__":
    main()
