# The World Today — Wednesday, 25 November 2026

[![Competition](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/silver-wren-74/news-image-20261125-entry/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/silver-wren-74/news-image-20261125-entry/reward.svg)](https://make.fun/bounty/news-image-20261125)

A one-page newspaper that sums up the world news of **Wednesday,
25 November 2026** in a single 1024×1024 image, drawn programmatically
with Pillow.

**The lead:** a Houthi missile hit Riyadh's tallest tower — 11 wounded,
said Saudi Civil Defense.

**Also on the page:**

- **War at sea** — Ukraine sank a Russian warship off Benghazi, Libya,
  and struck another in the Gulf of Finland; new analysis puts Russia's
  war dead above 700,000.
- **Markets** — Jensen Huang reinstated as Nvidia's CEO; the shares
  leapt 31.5% in a day, regaining about $1 trillion in market value.
- **Iraq** — Baghdad ordered federal forces to seize the Kurdish-run
  oilfields.
- **France** — ex-president Nicolas Sarkozy and Carla Bruni ordered to
  stand trial in a corruption case; pre-trial hearing 1 April 2027.
- **Sport** — Vaibhav Sooryavanshi, 15, hit 204 off 53 balls: the
  fastest double hundred in List A cricket history.

## How it runs

- `gen_image.py` draws the front page into `entry.png` (build time,
  needs Pillow).
- `main.py` is the entry program: standard library only, it copies
  `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`),
  byte for byte, every run.

## License

MIT — see `LICENSE`.
