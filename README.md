# Fig

Faith In God. Three cards a day: **Receive**, **Gratitude**, **Restoration**.

Each card is a quote, then a story underneath it, then the verse the whole thing
rests on. Tapping the verse opens that chapter of the KJV inside the app, with
no signal needed.

## Run it

```
run.cmd
```

Opens the app at `http://localhost:8777/www/index.html`.

```
review.cmd
```

Opens the verse review screen, where you keep or drop candidates from the
harvested pool. Decisions save as you go, so you can stop anywhere. Export
approved when a batch is done.

Both need a local server because a page opened straight off the disk is not
allowed to read its own data files. Nothing touches the internet.

## Preview any day

`http://localhost:8777/www/index.html?day=140` shows day 140. Useful for reading
ahead while writing cards.

## Layout

| Path | What it is |
|---|---|
| `www/index.html` | The app. One file, no build step, no libraries. |
| `www/data/content.json` | The 90 cards. Generated, never edited by hand. |
| `www/data/bible.json` | The whole KJV, 66 books, 1189 chapters, 4.1 MB. |
| `www/data/candidates.json` | 2034 harvested verses waiting for review. |
| `tools/harvest.py` | Scans the KJV, scores every verse against the three streams, writes candidates and bible. |
| `tools/seed.py` | Turns the authored card list into content.json. |
| `tools/build_single.py` | Bakes everything into one shareable HTML file. |
| `tools/review.html` | The verse review screen. |
| `data-src/kjv.json` | The raw download. Public domain. |

## Adding cards

Open `tools/seed.py`, append to `CARDS`, run it:

```
"C:\Users\levia\AppData\Local\Programs\Python\Python312\python.exe" tools/seed.py
```

An entry is stream, reference, quote, gloss, and an optional story. **You never
type scripture.** The reference is looked up in `bible.json` at build time, so a
misquote is structurally impossible. A bad reference stops the build with the
reason.

A story is a pair: the badge and the body. `Parable` for ones we write, with no
name. `Sent in` for a real one, which also carries a first name and a city.
Keeping those two labelled differently is what makes a real testimony worth
something when it arrives.

## Rebuilding the verse pool

```
"C:\Users\levia\AppData\Local\Programs\Python\Python312\python.exe" tools/harvest.py
```

Rewrites `candidates.json` and `bible.json` from the raw KJV. Only needed if the
lexicons in `harvest.py` change.

## Wiring the Share button

Set `FORM_URL` near the top of the script in `www/index.html` to a Google Form
link. Until it is set the button says so instead of doing nothing.

## Skins

Four, picked with the small circle beside the streak counter. **Bloom** (plum and
rose gold), **Cedar** (deep blue green), **Iron** (charcoal and bronze), **Linen**
(daylight, where the scripture card goes dark so it still lifts off the page).

A skin is a block of CSS variables plus four cloud colours for the canvas. Adding
a fifth means adding one `:root[data-skin="..."]` block and one entry in `SKINBG`.

## Storage

`localStorage` under the key `fig_v1`: streak, saved cards, which of today's
three you have opened, and the chosen skin. The review screen uses
`fig_review_v1`. **Do not rename these keys once anyone has installed the app**,
because that orphans their data.

## Not done yet

1. A notification, aimed at bedtime rather than morning
2. The Google Form and the `testimonies.json` fetch that puts real stories in
   without shipping an update
3. Spanish
4. Capacitor wrapper and the APK
5. Paid archive

## Music

Twenty Chopin nocturnes and preludes play in the background, shuffled so all
twenty go by before any repeats. Build or rebuild them with:

```
"C:\Users\levia\AppData\Local\Programs\Python\Python312\python.exe" tools/music.py
```

That downloads the originals once into `data-src/audio/` (gitignored, about
100 MB), loudness normalises them so no track jumps against another, and writes
mono AAC into `www/audio/` at roughly 1.7 MB each. Only the playing track is
ever downloaded by a listener.

**Source and licence.** Musopen's Complete Chopin Collection, released under
CC0 1.0, which puts the *recordings* in the public domain and not only the
compositions. That distinction matters: a Chopin nocturne is free to use, but
most recordings of one are owned by the performer and the label. Anything added
later has to clear the same bar. `www/data/music.json` carries the source and
licence with the track list.

The music does not play in the Artifact preview, because that sandbox blocks
media loaded from anywhere. It works on the Pages site and will work in the app.

## Live

The public site is served by GitHub Pages from `main` at the repository root,
where `index.html` redirects into `www/`.

https://cappietarot-bit.github.io/Fig/
