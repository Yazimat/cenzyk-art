# -*- coding: utf-8 -*-
"""Rasterize brand favicon v1B — narrow И, balanced in square for tabs."""
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

    draw.polygon(
        [
            p(14, 6),
            p(25, 6),
            p(25, 28),
            p(38, 6),
            p(50, 6),
            p(50, 45),
            p(39, 45),
            p(39, 23),
            p(26, 45),
            p(14, 45),
        ],
        fill=INK,
    )
    draw.rectangle([14 * s, 50 * s, 50 * s, 57 * s], fill=YELLOW)


def favicon_16() -> Image.Image:
    im = canvas(16)
    px = im.load()
    for y in range(1, 11):
        for x in (3, 4):
            px[x, y] = INK
        for x in (11, 12):
            px[x, y] = INK
    for y in range(1, 11):
        t = (y - 1) / 9.0
        cx = int(round(11 - t * 7))
        for dx in (0, 1):
            x = cx + dx
            if 4 <= x <= 11:
                px[x, y] = INK
    for y in (12, 13, 14):
        for x in range(3, 13):
            px[x, y] = YELLOW
    return im


def favicon_32() -> Image.Image:
    im = canvas(32)
    d = ImageDraw.Draw(im)
    d.rectangle([6, 3, 11, 22], fill=INK)
    d.rectangle([20, 3, 25, 22], fill=INK)
    for y in range(3, 23):
        t = (y - 3) / 19.0
        cx = int(round(21 - t * 12))
        d.rectangle([cx - 1, y, cx + 1, y], fill=INK)
    d.rectangle([6, 25, 25, 29], fill=YELLOW)
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
