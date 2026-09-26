# StickManAllen

Static GitHub Pages site (`index.html` only) for WHY123's stick-figure comic notebooks.

- Pages live at `books/NN/PPP.jpg` (3-digit, filename order is the source of truth).
- After adding or replacing pages, run `python3 tools/optimize_images.py NN`
  (needs Pillow) to shrink pages to 1600px and generate `books/NN/thumbs/`.
- Update the book's `pages` in `BOOKS` in `index.html`.
- Bump `APP_VERSION` in `index.html` on every change to that file (open pages auto-reload on it).
- Commit and push directly to `main`.
