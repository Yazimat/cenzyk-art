from PIL import Image
from pathlib import Path

SRC = Path(r"C:\Users\Илья\Desktop\Новый сайт")
OUT = Path(r"C:\Users\Илья\cenzyk-art\assets\images")
OUT.mkdir(parents=True, exist_ok=True)

# Order matches user's upload / desktop listing intent
FILES = [
    "527d1048-ade2-4237-b2b7-535da3e9da26.jfif",
    "123124.jpg",
    "2026-08-07 11-18-37.JPG",
    "2026-05-15 13-00-08.JPG",
    "IMG_20260707_170305.jpg",
    "-2147483648_-215553 (1).jpg",
    "-2147483648_-215547.jpg",
    "2024-11-27 14-34-38.JPG",
    "2026-07-18 16-37-50 (1).JPG",
    "IMG_20260605_144536.jpg",
    "IMG_20260427_101958.jpg",
]


def to_square(img: Image.Image, size: int = 1080) -> Image.Image:
    img = img.convert("RGB")
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    return img.resize((size, size), Image.Resampling.LANCZOS)


for i, name in enumerate(FILES, start=1):
    src = SRC / name
    if not src.exists():
        raise SystemExit(f"Missing: {src}")
    out = OUT / f"gallery-{i:02d}.jpg"
    img = to_square(Image.open(src))
    img.save(out, "JPEG", quality=88, optimize=True)
    print(f"saved {out.name} from {name}")
