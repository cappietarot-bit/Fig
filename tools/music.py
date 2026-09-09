"""
Build Fig's background music.

Source is Musopen's Complete Chopin Collection on archive.org, released under
CC0, which means the recordings themselves are public domain and not only the
compositions. That distinction is the whole reason this list is hand picked
instead of scraped: a Chopin nocturne is free, but most recordings of one are
not.

Twenty calm pieces, downloaded once and cached, then loudness normalised so no
track jumps in volume against the others, and re-encoded to mono AAC so each one
streams in under two megabytes instead of five. AAC because every phone browser
plays it, which is not true of Opus.

Run:
  "C:\\Users\\levia\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" tools/music.py
"""

import io
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "data-src", "audio")
OUT = os.path.join(ROOT, "www", "audio")
MANIFEST = os.path.join(ROOT, "www", "data", "music.json")

ITEM = "musopen-chopin"
BASE = "https://archive.org/download/" + ITEM + "/"

BITRATE = "48k"          # mono, background level. Plenty for solo piano.
LOUDNESS = "-23"         # EBU R128 target, so nothing jumps between tracks.

# (source file on archive.org, title shown in the app)
TRACKS = [
    ("Nocturne Op. 9 no. 2 in E flat major.mp3",       "Nocturne in E flat, Op. 9 No. 2"),
    ("NocturneOp.9No.1InBFlatMinor.mp3",               "Nocturne in B flat minor, Op. 9 No. 1"),
    ("NocturneOp.9No.3.mp3",                           "Nocturne in B, Op. 9 No. 3"),
    ("Nocturne Op. 15 no. 1 In F major.mp3",           "Nocturne in F, Op. 15 No. 1"),
    ("Nocturne Op. 27 no. 1 in C sharp minor.mp3",     "Nocturne in C sharp minor, Op. 27 No. 1"),
    ("NocturneOp27No2.mp3",                            "Nocturne in D flat, Op. 27 No. 2"),
    ("Nocturne Op. 32 no. 1 in B major.mp3",           "Nocturne in B, Op. 32 No. 1"),
    ("Nocturne Op. 32 no. 2 in A flat major.mp3",      "Nocturne in A flat, Op. 32 No. 2"),
    ("Nocturne Op. 48 no. 1 in C minor.mp3",           "Nocturne in C minor, Op. 48 No. 1"),
    ("Nocturne Op. 55 no. 1 in F minor.mp3",           "Nocturne in F minor, Op. 55 No. 1"),
    ("Nocturne Op. 55 no. 2 in E flat major.mp3",      "Nocturne in E flat, Op. 55 No. 2"),
    ("Nocturne Op. 62 no. 2 in E major.mp3",           "Nocturne in E, Op. 62 No. 2"),
    ("NocturneOp.72No.1InEMinor.mp3",                  "Nocturne in E minor, Op. 72 No. 1"),
    ("Nocturne B. 108 in C minor.mp3",                 "Nocturne in C minor, B. 108"),
    ("Nocturne B. 49 in C sharp minor 'Lento con gran espressione' (1).mp3",
                                                       "Nocturne in C sharp minor, B. 49"),
    ("Prelude Op. 28 no. 7.mp3",                       "Prelude in A, Op. 28 No. 7"),
    ("Prelude Op. 28 no. 13.mp3",                      "Prelude in F sharp, Op. 28 No. 13"),
    ("Prelude Op. 28 no. 15.mp3",                      "Prelude in D flat, Op. 28 No. 15"),
    ("Prelude Op. 28 no. 17.mp3",                      "Prelude in A flat, Op. 28 No. 17"),
    ("Prelude Op. 28 no. 19.mp3",                      "Prelude in E flat, Op. 28 No. 19"),
]


def slug(title):
    s = title.lower()
    s = s.replace("sharp", "sharp").replace("flat", "flat")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def fetch(name, dest):
    """Downloads through curl. This machine's Python has an expired CA bundle,
    so urllib fails SSL verification on archive.org while curl is fine."""
    if os.path.exists(dest) and os.path.getsize(dest) > 10000:
        return "cached"
    url = BASE + urllib.parse.quote(name)
    subprocess.run(
        ["curl", "-sS", "-L", "--fail", "--max-time", "300", "-o", dest, url],
        check=True)
    if os.path.getsize(dest) < 10000:
        raise SystemExit("download too small, check the source name: " + name)
    return "downloaded"


def encode(src, dst):
    cmd = [
        "ffmpeg", "-nostdin", "-y", "-loglevel", "error",
        "-i", src,
        "-af", "loudnorm=I=%s:TP=-2:LRA=11" % LOUDNESS,
        "-c:a", "aac", "-b:a", BITRATE, "-ac", "1", "-ar", "44100",
        "-movflags", "+faststart",
        dst,
    ]
    subprocess.run(cmd, check=True)


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def main():
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)

    manifest, total = [], 0
    for i, (name, title) in enumerate(TRACKS, 1):
        cached = os.path.join(CACHE, name)
        final = os.path.join(OUT, slug(title) + ".m4a")

        how = fetch(name, cached)
        if not os.path.exists(final):
            encode(cached, final)

        size = os.path.getsize(final)
        total += size
        secs = duration(final)
        manifest.append({
            "file": os.path.basename(final),
            "title": title,
            "seconds": round(secs, 1),
        })
        print("%2d/%d  %-42s %5.1f min  %4.2f MB  (%s)"
              % (i, len(TRACKS), title[:42], secs / 60, size / 1048576, how))

    with io.open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump({
            "source": "Musopen, The Complete Chopin Collection",
            "license": "CC0 1.0 Universal, public domain dedication",
            "url": "https://archive.org/details/" + ITEM,
            "tracks": manifest,
        }, fh, ensure_ascii=False, indent=1)

    mins = sum(t["seconds"] for t in manifest) / 60
    print("\n%d tracks, %.0f minutes, %.1f MB total, about %.2f MB per track"
          % (len(manifest), mins, total / 1048576, total / 1048576 / len(manifest)))
    print("manifest -> %s" % MANIFEST)


if __name__ == "__main__":
    main()
