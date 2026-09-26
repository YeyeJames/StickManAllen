"""把 books/NN/PPP.jpg 縮到適合網頁的大小，並產生縮圖 books/NN/thumbs/PPP.jpg。

用法：python3 tools/optimize_images.py            # 處理所有本
      python3 tools/optimize_images.py 04 05      # 只處理指定的本

可以重複執行：已經縮過的頁面不會再壓一次，縮圖只在缺少或過期時重做。
需要 Pillow（pip install Pillow）。
"""
import glob
import os
import sys

from PIL import Image, ImageOps

PAGE_MAX = 1600   # 頁面長邊上限（px）
PAGE_Q = 80
THUMB_MAX = 480   # 縮圖長邊上限（px），書架封面和縮圖列表用
THUMB_Q = 75

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "books")


def save(im, path, q):
    im.save(path, "JPEG", quality=q, optimize=True, progressive=True)


def process_book(book_dir):
    thumbs_dir = os.path.join(book_dir, "thumbs")
    os.makedirs(thumbs_dir, exist_ok=True)
    pages = sorted(glob.glob(os.path.join(book_dir, "[0-9][0-9][0-9].jpg")))
    shrunk = thumbed = 0
    for page in pages:
        with Image.open(page) as src:
            needs_shrink = max(src.size) > PAGE_MAX or src.getexif().get(274, 1) != 1
            im = ImageOps.exif_transpose(src).convert("RGB")
        if needs_shrink:
            im.thumbnail((PAGE_MAX, PAGE_MAX), Image.LANCZOS)
            save(im, page, PAGE_Q)
            shrunk += 1
        thumb = os.path.join(thumbs_dir, os.path.basename(page))
        if not os.path.exists(thumb) or os.path.getmtime(thumb) < os.path.getmtime(page):
            t = im.copy()
            t.thumbnail((THUMB_MAX, THUMB_MAX), Image.LANCZOS)
            save(t, thumb, THUMB_Q)
            thumbed += 1
    print(f"{os.path.basename(book_dir)}: {len(pages)} 頁，縮小 {shrunk} 張，產生縮圖 {thumbed} 張")


def main():
    ids = sys.argv[1:] or sorted(os.listdir(ROOT))
    for book_id in ids:
        d = os.path.join(ROOT, book_id)
        if os.path.isdir(d):
            process_book(d)


if __name__ == "__main__":
    main()
