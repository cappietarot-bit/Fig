"""
Bake Fig into one self contained HTML file.

The app normally reads content.json and bible.json from beside itself. A preview
link has no folder to read from, so this inlines both into window.FIG_INLINE and
writes a single file that runs anywhere.

Pass a path to write somewhere else. Default lands next to the app.

Run:
  "C:\\Users\\levia\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" tools/build_single.py [out.html]
"""

import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "www", "index.html")
DATA = os.path.join(ROOT, "www", "data")
DEFAULT_OUT = os.path.join(ROOT, "fig-single.html")

ANCHOR = "<script>"


def compact(path):
    with io.open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT

    with io.open(SRC, encoding="utf-8") as fh:
        html = fh.read()

    payload = {
        "content": compact(os.path.join(DATA, "content.json")),
        "bible": compact(os.path.join(DATA, "bible.json")),
    }

    # </script> inside a string would close the tag early, so neutralise it.
    blob = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    blob = blob.replace("</", "<\\/")

    inline = '<script>window.FIG_INLINE=' + blob + ';</script>\n'

    i = html.index(ANCHOR)
    html = html[:i] + inline + html[i:]

    with io.open(out_path, "w", encoding="utf-8") as fh:
        fh.write(html)

    mb = os.path.getsize(out_path) / (1024.0 * 1024.0)
    cards = sum(len(v) for v in payload["content"]["streams"].values())
    print("%d cards + %d books baked in -> %.1f MB\n%s"
          % (cards, len(payload["bible"]["books"]), mb, out_path))


if __name__ == "__main__":
    main()
