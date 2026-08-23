from PIL import Image, ImageEnhance, ImageFilter
from pathlib import Path

SRC = Path(
    r"C:\Users\Илья\.cursor\projects\c-Users-cenzyk-art\assets\c__Users______AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_2026-02-17_16-43-43-3a0ce104-3d4b-4fe6-b612-4eb04408fc8c.png"
)
OUT = Path(r"C:\Users\Илья\cenzyk-art\assets\images\service-lestnicy.jpg")

img = Image.open(SRC).convert("RGB")
w, h = img.size

# Максимально сохраняем кадр: чуть убрать пустоту сверху/снизу,
# но не "рубить" композицию — перила должны остаться читаемыми.
left = 0
top = int(h * 0.03)
right = w
bottom = int(h * 0.97)
img = img.crop((left, top, right, bottom))

# Аккуратная коррекция под "премиальный" вид на сайте
img = ImageEnhance.Brightness(img).enhance(1.03)
img = ImageEnhance.Color(img).enhance(1.06)
img = ImageEnhance.Contrast(img).enhance(1.07)
img = img.filter(ImageFilter.UnsharpMask(radius=1.6, percent=170, threshold=3))

# Ресайз для веба
max_w = 1200
if img.width > max_w:
    ratio = max_w / img.width
    img = img.resize((max_w, int(img.height * ratio)), Image.Resampling.LANCZOS)

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "JPEG", quality=88, optimize=True)
print("saved", OUT)

