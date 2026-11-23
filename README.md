[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Cervus121212/quiet-fox-91/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

# THE WORLD TODAY — Monday 23 November 2026

A newspaper front page that sums up Monday 23 November 2026 in one image:
9 verified stories from 7 regions — 1 hero story plus 8 secondary stories —
drawn with a hand-written 5x7 bitmap font and flat vector shapes.

Clean, simple, striking: one nameplate, one hero, one flat illustration,
a 2-column grid of short stories, and a markets strip. Every story names
its source and a confidence tag (CONFIRMED / REPORTED).

## Run

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png (1024x1024, deterministic)
```

`main.py` uses only the Python 3.13 standard library (`os`, `sys`, `struct`,
`zlib`). No network, no image libraries. Running it twice produces
byte-identical output.

## The 9 stories

| # | Story | Source | Confidence |
|---|-------|--------|------------|
| 01 | COP31 climate talks collapse in Antalya — no pact, longest COP on record | Reuters, UN News | CONFIRMED |
| 02 | Democrats win 258 House seats, largest US majority since 1992 | AP | CONFIRMED |
| 03 | Mexico captures "El Chapo Isidro", FBI Top-10 fugitive; 11 dead | AP | CONFIRMED |
| 04 | Russian warship sunk off Libya; cargo ship hit in the Baltic | WSJ | REPORTED |
| 05 | Candy factory fire in Banten, Indonesia: 3 dead, dozens missing | AP | CONFIRMED |
| 06 | South Korea education minister quits over AI exam-cheating scandal | The Guardian | CONFIRMED |
| 07 | Nepal PM Balendra Shah holds first bilateral talks with Modi in Delhi | DW | CONFIRMED |
| 08 | India declare 720-9 in Wellington, a record Test total in New Zealand | DW | CONFIRMED |
| 09 | Nations agree to keep negotiating curbs on lethal AI weapons | UN | REPORTED |

Markets strip (Friday close, reported 23 Nov): S&P 500 6,910.39 (-3.7%),
Nasdaq 22,617.73 (-5.3%), Brent $92.57, Bitcoin $60,900; futures rebound
as Asia opens.
