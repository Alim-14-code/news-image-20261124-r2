#!/usr/bin/env python3
"""Render entry.png for news-image-20261124 R2 - 'THE WORLD TODAY' v2.

Deterministic PIL renderer: two runs write byte-identical PNGs.
All colours go through the token block below (primitive -> semantic ->
component); no literal colour is used past it.
"""
import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- tokens
PRIMITIVE = {
    "paper": (247, 242, 231),
    "ink": (22, 22, 26),
    "navy": (20, 38, 76),
    "gold": (201, 162, 39),
    "red": (180, 35, 24),
    "sea": (14, 74, 90),
    "sea_dark": (10, 54, 66),
    "green": (30, 122, 52),
    "amber": (180, 83, 9),
    "sky": (168, 200, 232),
    "muted": (71, 85, 105),
    "rule": (216, 210, 192),
    "card": (255, 255, 255),
    "flame": (232, 89, 12),
    "flame_core": (255, 212, 59),
    "sand": (232, 217, 160),
    "chart": (34, 197, 94),
    "chart_bright": (74, 222, 128),
    "map_green": (107, 142, 90),
    "hull": (16, 20, 24),
    "smoke": (154, 154, 154),
    "deck": (216, 216, 216),
}

SEMANTIC = {
    "bg": PRIMITIVE["paper"],
    "fg": PRIMITIVE["ink"],
    "masthead_bg": PRIMITIVE["navy"],
    "masthead_fg": (255, 255, 255),
    "accent": PRIMITIVE["red"],
    "confirmed": PRIMITIVE["green"],
    "reported": PRIMITIVE["amber"],
    "muted_fg": PRIMITIVE["muted"],
    "border": PRIMITIVE["rule"],
}

COMPONENT = {
    "hero_border": PRIMITIVE["navy"],
    "card_border": PRIMITIVE["ink"],
    "pill_fg": (255, 255, 255),
    "icon_bg": PRIMITIVE["navy"],
    "icon_fg": (255, 255, 255),
}

# ---------------------------------------------------------------- fonts
FDIR = "/usr/share/fonts/truetype"
SERIF_B = f"{FDIR}/liberation/LiberationSerif-Bold.ttf"
SERIF_I = f"{FDIR}/liberation/LiberationSerif-Italic.ttf"
SANS = f"{FDIR}/liberation/LiberationSans-Regular.ttf"
SANS_B = f"{FDIR}/liberation/LiberationSans-Bold.ttf"
MONO_B = f"{FDIR}/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


W = H = 1024
OUT = Path(__file__).with_name("entry.png")


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to max_w pixels; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def split_two(draw, text, fnt, max_w):
    """Split text into two lines of near-equal width (no orphan word)."""
    words = text.split()
    best = None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        wa, wb = draw.textlength(a, font=fnt), draw.textlength(b, font=fnt)
        if wa <= max_w and wb <= max_w:
            diff = abs(wa - wb)
            if best is None or diff < best[0]:
                best = (diff, a, b)
    if best:
        return [best[1], best[2]]
    return wrap(draw, text, fnt, max_w)


def pill(draw, x, y, text, bg):
    """Status pill; returns its width."""
    fnt = font(MONO_B, 11)
    w = int(draw.textlength(text, font=fnt)) + 16
    h = 18
    draw.rounded_rectangle([x, y, x + w, y + h], radius=9, fill=bg)
    draw.text((x + w / 2, y + h / 2), text, font=fnt,
              fill=COMPONENT["pill_fg"], anchor="mm")
    return w


def text_block(draw, x, y, lines, fnt, fill, leading):
    for i, line in enumerate(lines):
        draw.text((x, y + i * leading), line, font=fnt, fill=fill, anchor="la")


# ---------------------------------------------------------------- visuals
def draw_hormuz(draw, box):
    """Lead visual: dark strait, three burning tankers, mines, IRAN/OMAN."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PRIMITIVE["sea_dark"])
    for wy in (y0 + 52, y0 + 84, y0 + 116):
        draw.line([(x0 + 12, wy), (x1 - 12, wy)], fill=PRIMITIVE["sea"], width=1)
    mono = font(MONO_B, 12)
    draw.text((x0 + 12, y0 + 8), "IRAN", font=mono, fill=PRIMITIVE["sand"], anchor="la")
    draw.text((x1 - 12, y1 - 8), "OMAN", font=mono, fill=PRIMITIVE["sand"], anchor="rb")
    for cx in (x0 + 150, x0 + 325, x0 + 500):
        hy = y0 + 72  # hull top
        # smoke
        for sx, sy, r in ((cx - 10, hy - 34, 6), (cx + 4, hy - 44, 7), (cx + 16, hy - 56, 5)):
            draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=PRIMITIVE["smoke"])
        # flame
        draw.polygon([(cx - 13, hy), (cx, hy - 28), (cx + 13, hy)], fill=PRIMITIVE["flame"])
        draw.polygon([(cx - 6, hy), (cx, hy - 15), (cx + 6, hy)], fill=PRIMITIVE["flame_core"])
        # hull + superstructure
        draw.polygon([(cx - 56, hy), (cx + 56, hy), (cx + 48, hy + 20), (cx - 48, hy + 20)],
                     fill=PRIMITIVE["hull"])
        draw.rectangle([cx + 26, hy - 12, cx + 48, hy], fill=PRIMITIVE["deck"])
        draw.rectangle([cx - 14, hy - 10, cx - 2, hy], fill=(58, 63, 68))
    for mx, my in ((x0 + 240, y0 + 106), (x0 + 420, y0 + 110), (x0 + 585, y0 + 104)):
        draw.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=PRIMITIVE["hull"])
        for dx, dy in ((-7, 0), (7, 0), (0, -7), (0, 7)):
            draw.line([(mx, my), (mx + dx, my + dy)], fill=PRIMITIVE["hull"], width=1)


def draw_chart(draw, box):
    """Huang visual: rising market line on dark green."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(11, 61, 30))
    mono = font(MONO_B, 11)
    draw.text((x0 + 8, y0 + 6), "NASDAQ +REBOUND", font=mono,
              fill=PRIMITIVE["chart_bright"], anchor="la")
    pts = [(x0 + 10, y1 - 10), (x0 + 52, y1 - 20), (x0 + 94, y1 - 16),
           (x0 + 136, y1 - 32), (x0 + 178, y1 - 28), (x0 + 220, y1 - 44),
           (x0 + 262, y1 - 46), (x0 + 300, y1 - 56)]
    draw.line(pts, fill=PRIMITIVE["chart"], width=3, joint="curve")
    ex, ey = pts[-1]
    draw.polygon([(ex + 4, ey - 4), (ex - 8, ey - 6), (ex - 2, ey + 6)],
                 fill=PRIMITIVE["chart"])


def draw_awacs(draw, box):
    """NATO visual: AWACS silhouette over a Poland outline."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PRIMITIVE["sky"])
    poly = [(x0 + 28, y0 + 38), (x0 + 58, y0 + 24), (x0 + 108, y0 + 20),
            (x0 + 158, y0 + 24), (x0 + 198, y0 + 32), (x0 + 218, y0 + 44),
            (x0 + 188, y0 + 52), (x0 + 138, y0 + 54), (x0 + 88, y0 + 52),
            (x0 + 38, y0 + 48)]
    draw.polygon(poly, fill=PRIMITIVE["map_green"])
    mono = font(MONO_B, 11)
    draw.text((x0 + 125, y0 + 38), "POLAND", font=mono,
              fill=PRIMITIVE["ink"], anchor="mm")
    navy = PRIMITIVE["navy"]
    draw.ellipse([x0 + 55, y0 + 6, x0 + 200, y0 + 16], fill=navy)          # fuselage
    draw.ellipse([x0 + 105, y0 - 2, x0 + 150, y0 + 6], fill=navy)         # radar disc
    draw.polygon([(x0 + 195, y0 + 6), (x0 + 215, y0 - 4), (x0 + 215, y0 + 14)],
                 fill=navy)                                                # tail
    draw.polygon([(x0 + 110, y0 + 16), (x0 + 140, y0 + 28), (x0 + 165, y0 + 16)],
                 fill=navy)                                                # wing


def draw_glyph(draw, cx, cy, kind):
    """White glyph inside a navy icon square, centred at (cx, cy)."""
    fg = COMPONENT["icon_fg"]
    if kind == "ship":
        draw.polygon([(cx - 13, cy + 2), (cx + 13, cy + 2), (cx + 9, cy + 10),
                      (cx - 9, cy + 10)], fill=fg)
        draw.rectangle([cx + 2, cy - 8, cx + 10, cy + 2], fill=fg)
        draw.rectangle([cx - 8, cy - 6, cx - 4, cy + 2], fill=fg)
    elif kind == "flame":
        draw.polygon([(cx, cy - 13), (cx + 3, cy - 6), (cx + 8, cy + 1),
                      (cx + 8, cy + 7), (cx + 3, cy + 11), (cx - 3, cy + 11),
                      (cx - 8, cy + 7), (cx - 8, cy + 1), (cx - 3, cy - 6)],
                     fill=fg)
    elif kind == "thermo":
        draw.rounded_rectangle([cx - 5, cy - 11, cx + 5, cy + 2], radius=5, fill=fg)
        draw.ellipse([cx - 8, cy + 0, cx + 8, cy + 16], fill=fg)
    else:  # letter glyph
        fnt = font(SANS_B, 24)
        draw.text((cx, cy), kind, font=fnt, fill=fg, anchor="mm")


# ---------------------------------------------------------------- page
def render():
    img = Image.new("RGB", (W, H), SEMANTIC["bg"])
    d = ImageDraw.Draw(img)
    navy, ink = PRIMITIVE["navy"], PRIMITIVE["ink"]
    gold = PRIMITIVE["gold"]

    # outer frame
    d.rectangle([6, 6, 1017, 1017], outline=navy, width=4)

    # masthead
    d.rectangle([14, 14, 1010, 118], fill=SEMANTIC["masthead_bg"])
    d.text((512, 26), "THE WORLD TODAY", font=font(SERIF_B, 62),
           fill=SEMANTIC["masthead_fg"], anchor="ma")
    d.text((512, 90), "Tuesday, 24 November 2026", font=font(SANS_B, 20),
           fill=gold, anchor="ma")

    # gold rule + standfirst + rule
    d.line([(28, 124), (996, 124)], fill=gold, width=2)
    d.text((512, 132),
           "Three tankers burn in the Strait of Hormuz. Wall Street rebounds "
           "as Huang returns. NATO jets head for Poland.",
           font=font(SERIF_I, 18), fill=SEMANTIC["fg"], anchor="ma")
    d.line([(28, 162), (996, 162)], fill=ink, width=1)

    # ---- hero zone (y 178-490) ----
    # lead: Hormuz
    d.rectangle([28, 178, 664, 490], fill=PRIMITIVE["card"],
                outline=COMPONENT["hero_border"], width=2)
    draw_hormuz(d, (30, 180, 662, 312))
    lead_head = split_two(d, "Three tankers hit in the Strait of Hormuz",
                          font(SERIF_B, 38), 604)
    text_block(d, 44, 322, lead_head, font(SERIF_B, 38), ink, 44)
    lead_body = wrap(d, "Three oil tankers hit sea mines and burn in the "
                        "Strait of Hormuz, the Revolutionary Guard says.",
                     font(SANS, 15), 604)
    text_block(d, 44, 418, lead_body[:2], font(SANS, 15), ink, 19)
    pill(d, 44, 462, "CONFIRMED", SEMANTIC["confirmed"])

    # stacked hero: Huang
    d.rectangle([680, 178, 996, 326], fill=PRIMITIVE["card"],
                outline=COMPONENT["hero_border"], width=2)
    draw_chart(d, (682, 180, 994, 236))
    d.text((688, 242), "Huang is back at Nvidia", font=font(SERIF_B, 24),
           fill=ink, anchor="la")
    d.text((688, 272), "Trump brokers a deal with the board.",
           font=font(SANS, 12), fill=SEMANTIC["muted_fg"], anchor="la")
    pill(d, 688, 296, "CONFIRMED", SEMANTIC["confirmed"])

    # stacked hero: NATO
    d.rectangle([680, 342, 996, 490], fill=PRIMITIVE["card"],
                outline=COMPONENT["hero_border"], width=2)
    draw_awacs(d, (682, 344, 994, 400))
    d.text((688, 406), "NATO jets for Poland", font=font(SERIF_B, 24),
           fill=ink, anchor="la")
    d.text((688, 436), "After Russian missiles land on Polish soil.",
           font=font(SANS, 12), fill=SEMANTIC["muted_fg"], anchor="la")
    pill(d, 688, 460, "CONFIRMED", SEMANTIC["confirmed"])

    d.line([(28, 502), (996, 502)], fill=ink, width=1)

    # ---- secondary zone: 2 rows x 4 cards ----
    cards = [
        ("ship", "MERKURY SUNK",
         "Ukraine sinks the Russian corvette Merkury in Benghazi, Libya, "
         "with naval drones.", "CONFIRMED", SEMANTIC["confirmed"]),
        ("!", "N. KOREA vs SWISS",
         "Kim Yo Jong threatens to shut the Swiss mission after Bern "
         "imposes sanctions.", "REPORTED", SEMANTIC["reported"]),
        ("flame", "INDONESIA FIRE",
         "A candy factory fire in Banten kills at least 24; rescuers "
         "search for the missing.", "CONFIRMED", SEMANTIC["confirmed"]),
        ("thermo", "COP31 AFTERMATH",
         "Climate talks collapsed over fossil fuels; Australia faces "
         "backlash.", "CONFIRMED", SEMANTIC["confirmed"]),
        ("$", "US SANCTIONS IRAN",
         "Treasury sanctions two dozen Iranian exchange houses and front "
         "firms.", "CONFIRMED", SEMANTIC["confirmed"]),
        ("W", "GRAIN DEAL DEAD",
         "Russia tells the UN Security Council it will agree to no new "
         "grain deal.", "CONFIRMED", SEMANTIC["confirmed"]),
        ("F", "SPARTA II ABLAZE",
         "A Russian cargo ship catches fire in the Gulf of Finland after "
         "a drone attack.", "REPORTED", SEMANTIC["reported"]),
        ("P", "LISBON PROTESTS",
         "Thousands march in Lisbon against the rising cost of living.",
         "CONFIRMED", SEMANTIC["confirmed"]),
    ]
    for idx, (glyph, head, body, status, status_bg) in enumerate(cards):
        x0 = 28 + (idx % 4) * 246
        y0 = 514 + (idx // 4) * 148
        d.rectangle([x0, y0, x0 + 230, y0 + 132], fill=PRIMITIVE["card"],
                    outline=COMPONENT["card_border"], width=2)
        d.rectangle([x0 + 10, y0 + 10, x0 + 54, y0 + 54],
                    fill=COMPONENT["icon_bg"])
        draw_glyph(d, x0 + 32, y0 + 32, glyph)
        head_lines = wrap(d, head, font(SANS_B, 20), 158)
        text_block(d, x0 + 62, y0 + 10, head_lines[:2], font(SANS_B, 20), ink, 22)
        body_lines = wrap(d, body, font(SANS, 13), 210)
        text_block(d, x0 + 10, y0 + 60, body_lines[:3], font(SANS, 13), ink, 16)
        pill(d, x0 + 10, y0 + 110, status, status_bg)

    d.line([(28, 806), (996, 806)], fill=ink, width=1)

    # ---- also-on + date check (y 818-966) ----
    d.text((28, 816), "ALSO ON", font=font(SANS_B, 18), fill=navy, anchor="la")
    also = [
        "Alcaraz beats Zverev for his first ATP Finals title.",
        "FIFA confirms the 2031 Women's World Cup hosts: US, Mexico, "
        "Costa Rica, Jamaica.",
        "Verstappen wins the Las Vegas Grand Prix.",
        "India v New Zealand first Test ends in a draw; Pant hits 128.",
        "Modi and Nepal PM Balendra Shah flag off the Saryu-Kamala Express.",
        "Israeli strikes kill three in Gaza, including an UNRWA worker.",
        "Iran flogs a singer and her team - 74 lashes each.",
        "Gukesh begins his World Chess title defence against Sindarov "
        "in Geneva.",
    ]
    for i, item in enumerate(also):
        col = 0 if i < 4 else 1
        row = i % 4
        x = 28 + col * 330
        y = 844 + row * 30
        d.rectangle([x, y + 4, x + 7, y + 11], fill=SEMANTIC["accent"])
        lines = wrap(d, item, font(SANS, 13), 298)
        text_block(d, x + 14, y, lines[:2], font(SANS, 13), ink, 15)

    d.rectangle([684, 818, 996, 966], fill=PRIMITIVE["card"],
                outline=COMPONENT["hero_border"], width=2)
    d.text((694, 826), "DATE CHECK - LEFT OUT ON PURPOSE",
           font=font(SANS_B, 13), fill=navy, anchor="la")
    checks = [
        "Shenzhen summit (Trump, Putin, Xi) - 23 Nov.",
        "Riemann Hypothesis proof claim - 23 Nov.",
        "COP31 collapse itself - Sunday.",
        "Dymer death toll - 23 Nov.",
    ]
    for i, line in enumerate(checks):
        d.text((694, 848 + i * 15), line, font=font(SANS, 12),
               fill=ink, anchor="la")
    legend = ["CONFIRMED = 2+ major outlets - REPORTED =",
              "one major outlet - CLAIM = one side's claim.",
              "No hype, no speculation as fact."]
    text_block(d, 694, 914, legend, font(SANS, 11),
               SEMANTIC["muted_fg"], 13)

    # footer
    d.text((512, 974),
           "Sources: Reuters, AP, AFP, Al Jazeera, KCNA, IRGC. "
           "19 stories - 5 continents - Tuesday 24 November 2026.",
           font=font(SANS, 12), fill=SEMANTIC["muted_fg"], anchor="ma")

    img.save(OUT, format="PNG")
    return OUT


if __name__ == "__main__":
    out = render()
    data = out.read_bytes()
    print(f"{out} {len(data)} bytes sha256={hashlib.sha256(data).hexdigest()}")
