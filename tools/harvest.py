"""
Harvest the Fig candidate verse pool out of the KJV.

Reads   data-src/kjv.json      (public domain KJV, array of 66 books in canon order)
Writes  www/data/candidates.json

Three streams: receive, gratitude, restoration. Every verse is scored against a
lexicon for each stream, then the best ones are kept. Nothing here decides what
ships. It builds the pile Ryan reviews in tools/review.html.

Run:
  "C:\\Users\\levia\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" tools/harvest.py
"""

import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data-src", "kjv.json")
OUT = os.path.join(ROOT, "www", "data", "candidates.json")

BOOKS = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua",
    "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings",
    "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job",
    "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah",
    "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai",
    "Zechariah", "Malachi", "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation",
]

# Phrases carry the theme on their own. Words only hint at it.
LEX = {
    "receive": {
        "phrases": [
            "believe that ye receive", "shall be done unto you",
            "according to your faith", "whatsoever ye shall ask",
            "ask, and it shall be given", "ask, and ye shall receive",
            "all things are possible", "if thou canst believe",
            "nothing shall be impossible", "as thou hast believed",
            "thy faith hath made thee whole", "what things soever ye desire",
            "calleth those things which be not", "faith is the substance",
            "must believe that he is", "according to thy faith",
            "seek, and ye shall find", "the prayer of faith",
            "he shall have whatsoever he saith", "desire of thine heart",
            "before they call, i will answer", "shall be opened unto you",
        ],
        "strong": [
            "receive", "receiveth", "received", "believe", "believeth",
            "believed", "faith", "ask", "asketh", "asked",
        ],
        "weak": ["desire", "granted", "given", "seek", "whatsoever", "shall have"],
    },
    "gratitude": {
        "phrases": [
            "give thanks", "giving thanks", "i thank thee", "we give thee thanks",
            "in every thing give thanks", "enter into his gates with thanksgiving",
            "offer unto god thanksgiving", "sacrifice of thanksgiving",
            "bless the lord", "o give thanks unto the lord", "rejoice evermore",
            "rejoice in the lord", "with thanksgiving", "let the people praise thee",
            "praise ye the lord", "my soul doth magnify", "thanks be to god",
        ],
        "strong": [
            "thank", "thanks", "thanked", "thanksgiving", "thankful",
            "praise", "praised", "rejoice", "magnify",
        ],
        "weak": ["bless", "blessed", "glorify", "glad", "joy", "sing"],
    },
    "restoration": {
        "phrases": [
            "restore to you the years", "i will restore", "restoreth my soul",
            "blotteth out thy transgressions", "will not remember thy sins",
            "remember them no more", "remember ye not the former things",
            "behold, i make all things new", "old things are passed away",
            "a new heart", "renewing of your mind", "renew a right spirit",
            "beauty for ashes", "repairer of the breach", "build the old wastes",
            "his mercies are new every morning", "as far as the east is from the west",
            "cast all their sins into the depths", "healeth all thy diseases",
            "restore the years", "raise up the former desolations",
        ],
        "strong": [
            "restore", "restored", "restoreth", "restitution", "renew", "renewed",
            "renewing", "redeem", "redeemed", "redeemeth", "redemption",
            "blotteth", "blot", "revive", "reviving", "quicken", "quickened",
            "healeth", "healed", "forgiven", "forgiveth", "pardon", "pardoned",
            "captivity", "delivered", "deliverance", "cleanse", "cleansed",
        ],
        "weak": ["heal", "forgive", "mercy", "mercies", "new", "again",
                 "repair", "whole", "return", "turn", "raise", "comfort",
                 "loose", "loosed", "liberty", "free", "wash", "ashes"],
    },
}

# Phrases that carry restoration without using any of the words above.
LEX["restoration"]["phrases"] += [
    "turn again the captivity", "bring again the captivity",
    "brought again", "raise up the former", "revive us again",
    "make you whole", "set at liberty", "the acceptable year",
    "white as snow", "no condemnation", "all things are become new",
    "he restoreth", "thy youth is renewed", "give unto them beauty",
]

BRACE = re.compile(r"\{([^}]*)\}")
SPACE = re.compile(r"\s+")

# This KJV source puts two different things in braces. Margin notes, which always
# carry a colon ("{the light from...: Heb. between the light...}"), and words the
# translators supplied that are italicised in print ("{them}", "{it is}", "{endureth}").
# Notes get dropped. Supplied words are scripture and stay, or Mark 11:24 reads
# "believe that ye receive , and ye shall have".
def _brace(match):
    inner = match.group(1)
    return "" if ":" in inner else inner

# A card holds roughly this much text comfortably.
MIN_CHARS, MAX_CHARS = 45, 230
MAX_PER_CHAPTER = 3                     # force spread instead of 40 verses from one psalm
KEEP_PER_STREAM = 1500


def clean(text):
    text = BRACE.sub(_brace, text)
    text = text.replace("[", "").replace("]", "")
    text = re.sub(r"\s+([,;:.!?])", r"\1", text)   # tidy gaps left by dropped notes
    return SPACE.sub(" ", text).strip()


def score(low, lex):
    total = 0
    for phrase in lex["phrases"]:
        if phrase in low:
            total += 10
    for word in lex["strong"]:
        if re.search(r"\b" + word + r"\b", low):
            total += 3
    for word in lex["weak"]:
        if re.search(r"\b" + word + r"\b", low):
            total += 1
    return total


def write_bible(books):
    """Ship the whole KJV with the app so tapping a verse opens its chapter offline.

    Keys are single letters because this file is repeated 31,100 times and the
    long names would cost close to a megabyte on their own.
    """
    out = {"translation": "King James Version", "license": "public domain", "books": []}
    for i, book in enumerate(books):
        out["books"].append({
            "n": BOOKS[i],
            "c": [[clean(v) for v in chapter] for chapter in book["chapters"]],
        })

    path = os.path.join(ROOT, "www", "data", "bible.json")
    with io.open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))

    mb = os.path.getsize(path) / (1024.0 * 1024.0)
    chapters = sum(len(b["c"]) for b in out["books"])
    print("bible       %d books, %d chapters, %.1f MB -> www/data/bible.json"
          % (len(out["books"]), chapters, mb))


def main():
    with io.open(SRC, encoding="utf-8-sig") as fh:
        books = json.load(fh)

    if len(books) != len(BOOKS):
        raise SystemExit("expected 66 books, got %d" % len(books))

    verses = []
    for b_i, book in enumerate(books):
        name = BOOKS[b_i]
        for c_i, chapter in enumerate(book["chapters"]):
            for v_i, raw in enumerate(chapter):
                text = clean(raw)
                if not text:
                    continue
                verses.append({
                    "ref": "%s %d:%d" % (name, c_i + 1, v_i + 1),
                    "book": name,
                    "chapter": c_i + 1,
                    "verse": v_i + 1,
                    "text": text,
                })

    out = {"source": "KJV, public domain", "total_verses": len(verses), "streams": {}}

    for stream, lex in LEX.items():
        scored = []
        for v in verses:
            s = score(v["text"].lower(), lex)
            if s < 3:                # one strong word is the floor; rank sorts the rest
                continue
            n = len(v["text"])
            if n < MIN_CHARS or n > MAX_CHARS:
                s -= 2               # still allowed, just outranked by card sized ones
            scored.append((s, v))

        scored.sort(key=lambda p: (-p[0], p[1]["book"], p[1]["chapter"], p[1]["verse"]))

        kept, per_chapter = [], {}
        for s, v in scored:
            key = (v["book"], v["chapter"])
            if per_chapter.get(key, 0) >= MAX_PER_CHAPTER:
                continue
            per_chapter[key] = per_chapter.get(key, 0) + 1
            kept.append({
                "ref": v["ref"], "book": v["book"],
                "chapter": v["chapter"], "verse": v["verse"],
                "text": v["text"], "score": s,
            })
            if len(kept) >= KEEP_PER_STREAM:
                break

        out["streams"][stream] = kept
        books_hit = len(set(k["book"] for k in kept))
        print("%-12s %4d verses, %2d books, top score %d"
              % (stream, len(kept), books_hit, kept[0]["score"] if kept else 0))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)

    write_bible(books)

    total = sum(len(v) for v in out["streams"].values())
    print("\n%d verses scanned -> %d candidates -> %s" % (len(verses), total, OUT))
    print("%.1f years of three-a-day cards" % (total / 3.0 / 365.0))


if __name__ == "__main__":
    main()
