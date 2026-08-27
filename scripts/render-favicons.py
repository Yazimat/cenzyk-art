# -*- coding: utf-8 -*-
"""Rasterize brand favicon v1 (refined) + archive variants."""
from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1] / "assets" / "favicon"
CREAM = (242, 239, 231, 255)
INK = (20, 22, 19, 255)
YELLOW = (232, 184, 0, 255)


def canvas(size: int) -> Image.Image:
    return Image.new("RGBA", (size, size), CREAM)


def frame(draw: ImageDraw.ImageDraw, size: int) -> None:
    m = max(1, round(size * 3.5 / 64))
    w = max(1, round(size * 2.5 / 64))
    draw.rectangle([m, m, size - m - 1, size - m - 1], outline=INK, width=w)


def draw_i_cyrillic(draw: ImageDraw.ImageDraw, size: int) -> None:
    """Cyrillic И (v1B production): stems + rising diagonal. 64-grid."""
    s = size / 64.0

    def p(x: float, y: float) -> tuple[float, float]:
        return (x * s, y * s)

    # Matches favicon.svg / v1b-no-frame.svg
    draw.polygon(
        [
            p(12, 7),
            p(20.5, 7),
            p(20.5, 32),
            p(41, 7),
            p(52, 7),
            p(52, 48),
            p(43.5, 48),
            p(43.5, 23),
            p(20.5, 48),
            p(12, 48),
        ],
        fill=INK,
    )


def v1(size: int) -> Image.Image:
    """Production mark = variant B (no frame)."""
    im = canvas(size)
    d = ImageDraw.Draw(im)
    draw_i_cyrillic(d, size)
    s = size / 64.0
    d.rectangle([14 * s, 51.5 * s, 50 * s, 56 * s], fill=YELLOW)
    return im


# --- archive variants (unchanged intent, for preview.html archive) ---

def draw_i_letter_legacy(draw: ImageDraw.ImageDraw, size: int, pad: float = 0.22) -> None:
    left = int(size * pad)
    right = size - left
    top = int(size * 0.18)
    bot = int(size * 0.72)
    tw = max(2, size // 9)
    draw.rectangle([left, top, left + tw, bot], fill=INK)
    draw.rectangle([right - tw, top, right, bot], fill=INK)
    t = tw * 0.9
    x0, y0 = left + tw, top
    x1, y1 = right - tw, bot
    draw.polygon(
        [(x0, y0), (x0 + t, y0), (x1, y1 - t * 0.15), (x1, y1), (x1 - t, y1), (x0, y0 + t * 0.15)],
        fill=INK,
    )


def v2(size: int) -> Image.Image:
    im = canvas(size)
    d = ImageDraw.Draw(im)
    w = max(2, size // 12)
    d.rectangle([int(size * 0.28), int(size * 0.22), int(size * 0.28) + w, int(size * 0.78)], fill=INK)
    d.arc([int(size * 0.28), int(size * 0.22), int(size * 0.78), int(size * 0.55)], 200, 20, fill=INK, width=w)
    d.arc([int(size * 0.22), int(size * 0.48), int(size * 0.72), int(size * 0.82)], 20, 200, fill=INK, width=w)
    d.rectangle([int(size * 0.52), int(size * 0.44), int(size * 0.72), int(size * 0.44) + w], fill=YELLOW)
    return im


def v3(size: int) -> Image.Image:
    im = Image.new("RGBA", (size, size), YELLOW)
    d = ImageDraw.Draw(im)
    draw_i_cyrillic(d, size)
    return im


def v4(size: int) -> Image.Image:
    im = canvas(size)
    d = ImageDraw.Draw(im)
    w = max(2, size // 11)
    y = int(size * 0.36)
    d.line([(int(size * 0.18), y), (int(size * 0.42), y)], fill=INK, width=w)
    d.arc([int(size * 0.28), y, int(size * 0.72), int(size * 0.78)], 0, 180, fill=INK, width=w)
    d.line([(int(size * 0.72), int(size * 0.58)), (int(size * 0.72), int(size * 0.28))], fill=INK, width=w)
    s = max(3, size // 9)
    d.rectangle([int(size * 0.72) - s // 2, int(size * 0.22), int(size * 0.72) + s // 2, int(size * 0.22) + s], fill=YELLOW)
    return im


def v5(size: int) -> Image.Image:
    im = canvas(size)
    d = ImageDraw.Draw(im)
    m = max(2, size // 16)
    d.rectangle([m, m, size - m - 1, size - m - 1], outline=INK, width=max(1, size // 28))
    tw = max(2, size // 9)
    d.rectangle([int(size * 0.22), int(size * 0.22), int(size * 0.22) + tw, int(size * 0.7)], fill=INK)
    d.rectangle([int(size * 0.22), int(size * 0.7), int(size * 0.48), int(size * 0.7) + tw], fill=INK)
    d.rectangle([int(size * 0.55), int(size * 0.22), int(size * 0.55) + tw, int(size * 0.78)], fill=INK)
    s = max(3, size // 8)
    d.rectangle([size - s - int(size * 0.08), int(size * 0.08), size - int(size * 0.08), int(size * 0.08) + s], fill=YELLOW)
    return im


def v6(size: int) -> Image.Image:
    im = canvas(size)
    d = ImageDraw.Draw(im)
    m = int(size * 0.08)
    d.ellipse([m, m, size - m, size - m], outline=INK, width=max(1, size // 22))
    d.arc([m, m, size - m, size - m], -40, 50, fill=YELLOW, width=max(2, size // 16))
    draw_i_cyrillic(d, size)
    return im


def save_set(fn, name: str) -> None:
    for s, suffix in ((32, "32"), (180, "180"), (512, "512")):
        im = fn(s)
        path = OUT / f"{name}-{suffix}.png"
        im.save(path, optimize=True)
        print("wrote", path.name, path.stat().st_size)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    variants = [
        ("v1-letter-i", v1),
        ("v2-monogram-is", v2),
        ("v3-yellow-block", v3),
        ("v4-metal-curve", v4),
        ("v5-stencil-il", v5),
        ("v6-stamp-seal", v6),
    ]
    for name, fn in variants:
        save_set(fn, name)

    # Production set from refined v1
    for s, name in ((16, "favicon-16.png"), (32, "favicon-32.png"), (180, "apple-touch-icon.png"), (512, "favicon-512.png")):
        v1(s).save(OUT / name, optimize=True)
        print("primary", name, (OUT / name).stat().st_size)


if __name__ == "__main__":
    main()
