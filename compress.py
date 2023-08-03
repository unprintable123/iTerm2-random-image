from PIL import Image
import os

src_dir = "/Users/admin/Pictures/original"
dst_dir = "/Users/admin/Pictures/BackgroundImage"

pics = os.listdir(src_dir)
for pic in pics:
    if pic.startswith("."):
        continue
    print(pic)
    a = Image.open(os.path.join(src_dir, pic))
    if a.mode != "RGB":
        a = a.convert("RGB")
    width, height = a.size
    if width * height >= 2560 * 1600:
        scale = max(2000 / width, 1500 / height)
        scale = round(scale * 10 + 0.5) / 10
        if scale < 1:
            a = a.resize((round(width * scale), round(height * scale)))
    print(a.size)
    a.save(os.path.join(dst_dir, os.path.splitext(pic)[0] + ".jpg"), "jpeg", quality=80)
