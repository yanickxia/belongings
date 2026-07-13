#!/usr/bin/env python3
# 把 static/images/ 下所有 PNG/JPG 转成 WebP 并删除原图。
# 用法: python3 scripts/to_webp.py
# 依赖: pip install --user --break-system-packages pillow
import glob, os
from PIL import Image

IMG_DIR = os.path.join(os.path.dirname(__file__), "..", "static", "images")

def main():
    total_old = total_new = 0
    for p in sorted(glob.glob(os.path.join(IMG_DIR, "*"))):
        ext = os.path.splitext(p)[1].lower()
        if ext not in (".png", ".jpg", ".jpeg"):
            continue
        name = os.path.basename(p)
        im = Image.open(p).convert("RGB")
        max_edge = 1100 if name.startswith("real-") else 800
        q = 80 if name.startswith("real-") else 82
        w, h = im.size
        s = min(1.0, max_edge / max(w, h))
        if s < 1.0:
            im = im.resize((int(w * s), int(h * s)), Image.LANCZOS)
        out = os.path.splitext(p)[0] + ".webp"
        im.save(out, "WEBP", quality=q, method=6)
        old, new = os.path.getsize(p), os.path.getsize(out)
        os.remove(p)
        total_old += old; total_new += new
        print(f"{name:40s} {old//1024:5d}KB -> {new:5d}B  {os.path.basename(out)}")
    if total_old:
        print(f"\nTOTAL {total_old//1024//1024}MB -> {total_new//1024}KB "
              f"({total_new*100//total_old}%)")
    else:
        print("没有需要转换的 PNG/JPG。")

if __name__ == "__main__":
    main()
