# news-image-20261124-r2

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Alim-14-code/news-image-20261124-r2/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Alim-14-code/news-image-20261124-r2/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# THE WORLD TODAY — Tuesday, 24 November 2026

Entry for the [make.fun news-image-20261124](https://make.fun/bounty/news-image-20261124)
competition: sum up 24 November's world news in one image.

Round 2 is a craft rebuild of the round-1 entry, designed with the
visual-skills pack (Hallmark, UI/UX Pro Max, baseline-ui, improve-ui):
one lead story given a two-thirds hero slot with a large diagrammatic
sea scene, two stacked heroes, a single accent colour, a three-layer
token system, and a type scale sized to stay legible at ~300 px wide.

The image leads with the day's three biggest stories — three oil tankers
hit by sea mines in the Strait of Hormuz, Jensen Huang reinstated as
Nvidia CEO as Wall Street rebounds, and NATO sending AWACS aircraft to
Poland — then covers the Russian corvette Merkury sunk off Libya, North
Korea vs Switzerland, the Banten factory fire, the COP31 aftermath, US
sanctions on Iran, the dead grain deal, the Sparta II ablaze, and
Lisbon's cost-of-living protests, plus an "Also on" list and a date check
that names what was deliberately left out because it belongs to an
earlier day.

## How it is built

- `render.py` (Pillow, local use only) draws `entry.png` — 1024×1024, one
  newspaper-style composition with diagrammatic hero illustrations and type
  sized to stay legible at ~300 px wide. Run it twice: both runs write
  identical bytes.
- `main.ts` (Node 22, standard library only) copies `entry.png` to
  `/output/entry.png`.

## Sources

Reuters, AP, AFP, Al Jazeera, KCNA, IRGC. Every story happened, or was first
reported, on Tuesday 24 November 2026. Items are tagged CONFIRMED (2+ major
outlets), REPORTED (one major outlet) or CLAIM (one side's claim).

---

<sub>Entered on [make.fun](https://make.fun/?ref=e6d1qmmj&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
