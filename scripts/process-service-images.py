from PIL import Image, ImageFilter, ImageEnhance
from pathlib import Path

OUT = Path(r"C:\Users\Илья\cenzyk-art\assets\images")
OUT.mkdir(parents=True, exist_ok=True)


def save_web(img: Image.Image, path: Path, width: int = 1400) -> None:
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    if img.width > width:
        ratio = width / img.width
        img = img.resize((width, int(img.height * ratio)), Image.Resampling.LANCZOS)
    img.save(path, "JPEG", quality=88, optimize=True)
    print(f"saved {path} ({img.size[0]}x{img.size[1]})")


# 1) Балкон — вернуть идеальную композицию (без сильного кропа; только ресайз)
bal = Image.open(r"C:\Users\Илья\Downloads\711039f9-dbe9-4c69-a72d-0fe54f5080f9.jfif")
save_web(bal, OUT / "service-balkony.jpg")


# 2) Забор — вернуть идеальный кадр (без обрезки; только ресайз)
fence = Image.open(
    r"C:\Users\Илья\.cursor\projects\c-Users-cenzyk-art\assets\c__Users______AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_2026-08-07_11-18-37_1786283673-0543acc8-64e7-40b7-bab0-fd01b0c8dd22.png"
)
save_web(fence, OUT / "service-zabory.jpg")


# 3) Лестницы/перила — новый кроп + цвет/резкость, чтобы акцент был именно на перила
rail = Image.open(
    r"C:\Users\Илья\.cursor\projects\c-Users-cenzyk-art\assets\c__Users______AppData_Roaming_Cursor_User_workspaceStorage_empty-window_images_2024-12-09_14-32-26-62fe3ca1-5749-42e5-813c-1ad7f2769969.png"
).convert("RGB")

rw, rh = rail.size

# Сдвиг/кроп: чуть выше, срезаем часть справа (люди/инструменты) и убираем лишний низ
left = int(rw * 0.00)
top = int(rh * 0.055)
right = int(rw * 0.82)
bottom = int(rh * 0.92)
rail = rail.crop((left, top, right, bottom))

# Лёгкая «премиальная» коррекция цвета + резкости
rail = ImageEnhance.Contrast(rail).enhance(1.08)
rail = ImageEnhance.Color(rail).enhance(1.06)
rail = ImageEnhance.Brightness(rail).enhance(1.03)
rail = rail.filter(ImageFilter.UnsharpMask(radius=1.7, percent=170, threshold=4))

save_web(rail, OUT / "service-lestnicy.jpg")
