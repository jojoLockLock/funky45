# funky45

45s singles from *The Funky & Groovy Music Records Lexicon*, Chapter 3.2 (45s Singles Reference-Guide) by Peter Wermelinger. Page 1 covers Illinois Connection to Infinity (47 singles).

Live page: https://jojolocklock.github.io/funky45/

- `index.html`: a single self-contained page. Each card has the Discogs label scan (embedded as base64), the book data, and a click-to-load YouTube preview of the funky side (A1/B1). You can search and filter by rating.
- The data sits in the `RECORDS` array inside `index.html`. Add objects with the same fields to include more pages.
- `data.py` is the transcription of the book page, `picks.py` holds the chosen YouTube video IDs, and `build.py` is the generator. It needs a local HTML template and cached Discogs/YouTube data, and those are not in this repo.

Label images © their respective owners, via Discogs. Videos are embedded from YouTube.
Note: YouTube embeds fail with error 153 when the file is opened via `file://`. Serve it over http(s) instead.
