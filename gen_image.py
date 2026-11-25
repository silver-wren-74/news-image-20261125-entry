#!/usr/bin/env python3
"""Generator for news-image-20261125: draws the front page into entry.png.

Run locally at build time (needs Pillow). The shipped entry program is
main.py, which only copies entry.png to the output directory using the
standard library, so the grader sandbox needs nothing installed.

The page sums up the world news of Wednesday 25 November 2026, as first
reported that day:
  lead  - a Houthi missile hit Riyadh's tallest tower, 11 wounded
  war   - Ukraine sank a Russian warship off Benghazi and struck one in
          the Gulf of Finland; Russian war dead put above 700,000
  money - Jensen Huang reinstated as Nvidia CEO, shares +31.5%,
          about $1 trillion of market value regained
  iraq  - Baghdad ordered federal forces to seize Kurdish-run oilfields
  france- ex-president Sarkozy and Carla Bruni ordered to stand trial
          in a corruption case, pre-trial hearing 1 April 2027
  sport - Vaibhav Sooryavanshi, 15, hit 204 off 53 balls, the fastest
          double hundred in List A cricket
"""
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 244, 234)
INK = (24, 24, 28)
MUTE = (92, 88, 80)
RED = (157, 2, 8)
NAVY = (29, 53, 87)
GREEN = (24, 96, 68)
SAND = (166, 84, 20)
PLUM = (74, 48, 109)
TEAL = (13, 110, 100)
PANEL_BG = (255, 253, 247)
RULE = (40, 40, 44)
BODY = (46, 44, 40)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def fit_font(d, text, path, size, maxw):
    """Shrink a font until the text fits maxw."""
    while size > 10 and d.textlength(text, font=F(path, size)) > maxw:
        size -= 2
    return F(path, size)


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(d, xy, text, font, fill, maxw, leading):
    x, y = xy
    for line in wrap(d, text, font, maxw):
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def centered(d, y, text, font, fill):
    w_ = d.textlength(text, font=font)
    d.text(((W - w_) / 2, y), text, font=font, fill=fill)
    return y + font.size + 6


# ---------------------------------------------------------------- icons
# Each icon draws inside a ~95 x 66 box at (x, y) scaled by s; with
# s = 0.55 it stays inside the 40px tag band of a panel.
def icon_ship(d, x, y, s, color):
    d.polygon([(x, y + 34 * s), (x + 90 * s, y + 34 * s),
               (x + 76 * s, y + 48 * s), (x + 12 * s, y + 48 * s)], fill=color)
    d.rectangle([x + 30 * s, y + 20 * s, x + 58 * s, y + 34 * s], fill=color)
    d.rectangle([x + 42 * s, y + 4 * s, x + 47 * s, y + 20 * s], fill=color)
    for i in range(3):
        bx = x + i * 32 * s
        d.arc([bx, y + 50 * s, bx + 30 * s, y + 64 * s], 0, 180, fill=color, width=3)


def icon_chart(d, x, y, s, color):
    d.line([(x, y + 58 * s), (x, y)], fill=color, width=4)
    d.line([(x, y + 58 * s), (x + 92 * s, y + 58 * s)], fill=color, width=4)
    pts = [(x + 6 * s, y + 48 * s), (x + 34 * s, y + 38 * s),
           (x + 54 * s, y + 44 * s), (x + 84 * s, y + 10 * s)]
    d.line(pts, fill=color, width=5, joint="curve")
    d.polygon([(x + 84 * s, y + 2 * s), (x + 95 * s, y + 12 * s),
               (x + 76 * s, y + 16 * s)], fill=color)


def icon_derrick(d, x, y, s, color):
    d.polygon([(x + 30 * s, y), (x + 62 * s, y), (x + 78 * s, y + 64 * s),
               (x + 14 * s, y + 64 * s)], outline=color, width=4)
    d.line([(x + 24 * s, y + 22 * s), (x + 68 * s, y + 22 * s)], fill=color, width=3)
    d.line([(x + 19 * s, y + 43 * s), (x + 73 * s, y + 43 * s)], fill=color, width=3)
    d.line([(x + 62 * s, y + 6 * s), (x + 92 * s, y + 20 * s)], fill=color, width=4)
    d.ellipse([x + 84 * s, y + 20 * s, x + 94 * s, y + 32 * s], fill=color)


def icon_scales(d, x, y, s, color):
    cx = x + 46 * s
    d.line([(cx, y + 4 * s), (cx, y + 56 * s)], fill=color, width=4)
    d.line([(x + 8 * s, y + 12 * s), (x + 84 * s, y + 12 * s)], fill=color, width=4)
    for px in (x + 8 * s, x + 84 * s):
        d.line([(px, y + 12 * s), (px - 10 * s, y + 34 * s)], fill=color, width=3)
        d.line([(px, y + 12 * s), (px + 10 * s, y + 34 * s)], fill=color, width=3)
        d.arc([px - 12 * s, y + 26 * s, px + 12 * s, y + 42 * s], 0, 180,
              fill=color, width=3)
    d.rectangle([x + 26 * s, y + 58 * s, x + 66 * s, y + 64 * s], fill=color)


def icon_cricket(d, x, y, s, color):
    d.polygon([(x + 30 * s, y + 4 * s), (x + 44 * s, y + 10 * s),
               (x + 26 * s, y + 52 * s), (x + 14 * s, y + 46 * s)], fill=color)
    d.rectangle([x + 36 * s, y + 48 * s, x + 43 * s, y + 64 * s], fill=color)
    d.ellipse([x + 62 * s, y + 34 * s, x + 88 * s, y + 60 * s], fill=RED)
    d.arc([x + 68 * s, y + 38 * s, x + 82 * s, y + 56 * s], 90, 270,
          fill=(255, 255, 255), width=2)


def icon_tower_burst(d, x, y, w_, h_):
    """Lead illustration: Riyadh skyline, the pointed tower, a burst."""
    d.rectangle([x, y, x + w_, y + h_], fill=(233, 226, 208))
    d.rectangle([x, y, x + w_, y + h_], outline=RULE, width=3)
    base = y + h_
    sil = (38, 40, 48)
    bx = x + 14
    for bw, bh in [(44, 96), (32, 140), (50, 76), (34, 118)]:
        d.rectangle([bx, base - bh, bx + bw, base], fill=sil)
        bx += bw + 9
    # the tower: an Al Faisaliah-like pyramid with a golden sphere
    tx = x + w_ - 148
    d.polygon([(tx, base), (tx + 54, y + 30), (tx + 108, base)], fill=(24, 26, 34))
    d.ellipse([tx + 37, y + 92, tx + 71, y + 126], fill=(214, 164, 32))
    # missile trail (dotted arc) ending in a burst at the tower top
    for t in range(0, 101, 6):
        a = t / 100.0
        px = x + 24 + a * (tx + 38 - x - 24)
        py = y + 18 + a * a * 30
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    cx, cy = tx + 52, y + 38
    for ang in range(0, 360, 30):
        r1 = 8
        r2 = 27 if ang % 60 == 0 else 18
        d.line([(cx + r1 * math.cos(math.radians(ang)),
                 cy + r1 * math.sin(math.radians(ang))),
                (cx + r2 * math.cos(math.radians(ang)),
                 cy + r2 * math.sin(math.radians(ang)))],
               fill=RED, width=4)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(240, 120, 20))


# ---------------------------------------------------------------- page
def panel(d, box, tag, tag_color, headline, body, icon):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=PANEL_BG, outline=RULE, width=2)
    d.rectangle([x0, y0, x0 + 128, y0 + 30], fill=tag_color)
    d.text((x0 + 10, y0 + 5), tag, font=F(SANSB, 19), fill=(255, 255, 255))
    icon(d, x1 - 62, y0 + 3, 0.55, tag_color)
    y = text_block(d, (x0 + 16, y0 + 42), headline, F(SERIF, 25), INK,
                   x1 - x0 - 32, 30)
    text_block(d, (x0 + 16, y + 6), body, F(SANS, 19), BODY,
               x1 - x0 - 32, 24)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 10, H - 10], outline=INK, width=3)
    d.rectangle([18, 18, W - 18, H - 18], outline=INK, width=1)

    # masthead
    centered(d, 28, "W O R L D   N E W S   I N   O N E   P A G E", F(SANSB, 19), MUTE)
    title_font = fit_font(d, "THE WORLD TODAY", SERIF, 96, 930)
    centered(d, 52, "THE WORLD TODAY", title_font, INK)
    d.rectangle([40, 150, W - 40, 156], fill=INK)
    centered(d, 164, "WEDNESDAY, 25 NOVEMBER 2026", F(SANSB, 34), RED)
    d.rectangle([40, 210, W - 40, 214], fill=INK)

    # lead story
    d.text((44, 228), "SAUDI ARABIA — THE LEAD", font=F(SANSB, 20), fill=RED)
    ly = text_block(d, (44, 254),
                    "Houthi Missile Hits Riyadh's Tallest Tower",
                    F(SERIF, 41), INK, 566, 50)
    text_block(d, (44, ly + 6),
               "Saudi Civil Defense said 11 people were wounded when the "
               "missile struck the capital's tallest tower on 25 November "
               "— a rare hit on the Riyadh skyline.",
               F(SANS, 21), BODY, 566, 28)
    d.text((44, 458), "11 WOUNDED", font=F(SERIF, 34), fill=RED)
    icon_tower_burst(d, 638, 228, 342, 264)

    d.rectangle([40, 506, W - 40, 510], fill=INK)

    # panels: row of three, row of two
    panel(d, (40, 524, 357, 758), "WAR AT SEA", NAVY,
          "Ukraine Sinks Russian Warship off Benghazi",
          "Kyiv also struck a Russian ship in the Gulf of Finland. "
          "New analysis puts Russia's war dead above 700,000.",
          icon_ship)
    panel(d, (373, 524, 690, 758), "MARKETS", GREEN,
          "Huang Returns to Nvidia; Shares Leap 31.5%",
          "Jensen Huang was reinstated as chief executive, and the "
          "stock regained about $1 trillion in value in a day.",
          icon_chart)
    panel(d, (706, 524, 984, 758), "IRAQ", SAND,
          "Baghdad Moves to Seize Kurdish Oilfields",
          "The prime minister ordered federal forces to take the "
          "Kurdish-run fields, escalating the oil-money dispute.",
          icon_derrick)
    panel(d, (40, 774, 504, 956), "FRANCE", PLUM,
          "Sarkozy and Bruni Ordered to Stand Trial",
          "A court sent the ex-president and Carla Bruni to trial in "
          "a corruption case; a pre-trial hearing is set for "
          "1 April 2027.",
          icon_scales)
    panel(d, (520, 774, 984, 956), "SPORT", TEAL,
          "204 off 53 Balls — at Fifteen",
          "Vaibhav Sooryavanshi, 15, hit the fastest double hundred "
          "in List A cricket history — 204 runs from only 53 balls.",
          icon_cricket)

    centered(d, 968, "All stories as first reported on 25 November 2026",
             F(SANS, 18), MUTE)
    img.save("entry.png")
    print("wrote entry.png")


if __name__ == "__main__":
    main()
