#!/usr/bin/env python3
"""Warm Postcard - Friday 20 November 2026. One day of world news, one picture.
A warm front page: terracotta frame, ochre and olive accents, three heroes,
thirteen pictured stories, a dot-matrix world map and thirty-two more briefs.
Every drawing is made here with PIL primitives; no photo is used anywhere."""

import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 1600
PAPER = (247, 241, 226)
CREAM = (253, 249, 240)
INK = (34, 29, 22)
TERRA = (176, 72, 44)
TERRA_D = (144, 50, 30)
OCHRE = (198, 142, 52)
OLIVE = (104, 116, 64)
RED = (168, 32, 40)
BLUE = (38, 84, 124)
TEAL = (42, 122, 110)
GREY = (96, 90, 80)
DARK = (26, 32, 40)

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"


def F(name, size):
    try:
        return ImageFont.truetype(FD + name, size)
    except Exception:
        return ImageFont.load_default()


def SF(name, size):
    try:
        return ImageFont.truetype(FL + name, size)
    except Exception:
        return F("DejaVuSerif.ttf", size)


def SANS(sz):
    return F("DejaVuSans.ttf", sz)


def SANSB(sz):
    return F("DejaVuSans-Bold.ttf", sz)


def SERIF(sz):
    return SF("LiberationSerif-Regular.ttf", sz)


def SERIFB(sz):
    return SF("LiberationSerif-Bold.ttf", sz)


def SERIFI(sz):
    return SF("LiberationSerif-Italic.ttf", sz)


def wrap(d, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if d.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, font, width, lh, color, max_lines=None):
    lines = wrap(d, text, font, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=color)
        y += lh
    return y


def grain(im, seed=7, n=4200):
    px = im.load()
    rnd = random.Random(seed)
    for _ in range(n):
        xx = rnd.randrange(W)
        yy = rnd.randrange(H)
        r, g, b = px[xx, yy]
        k = rnd.randint(-9, 9)
        px[xx, yy] = (max(0, min(255, r + k)), max(0, min(255, g + k)),
                      max(0, min(255, b + k)))


def band(d, x, y, w, h, top, bottom):
    for i in range(h):
        t = i / max(1, h - 1)
        c = tuple(int(top[j] + (bottom[j] - top[j]) * t) for j in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=c)


def starburst(d, cx, cy, r1, r2, n, color):
    for k in range(n):
        a = 2 * math.pi * k / n
        x2 = cx + r2 * math.cos(a)
        y2 = cy + r2 * math.sin(a)
        x1 = cx + r1 * math.cos(a)
        y1 = cy + r1 * math.sin(a)
        d.line([(x1, y1), (x2, y2)], fill=color, width=3)


def flag(d, x, y, w, h, stripes):
    for i, col in enumerate(stripes):
        d.rectangle([x, y + i * h // len(stripes), x + w,
                     y + (i + 1) * h // len(stripes)], fill=col)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    d.line([(x, y), (x, y + h + 14)], fill=INK, width=2)


def scene(d, x, y, w, h, idx):
    """Flat drawn scene for story idx, inside box (x, y, w, h)."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    if idx == 1:
        band(d, x, y, w, h, (44, 74, 92), (18, 40, 58))
        for i in range(9):
            d.line([(x + 8 + i * 26, y + 8), (x + 2 + i * 26, y + h - 8)],
                   fill=(150, 180, 200), width=2)
        cx, cy = x + w * 0.62, y + h * 0.5
        for r in (52, 40, 28, 16):
            d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
                  fill=(240, 244, 248), width=5)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(240, 244, 248))
        d.rectangle([x, y + h - 26, x + w, y + h], fill=(20, 34, 48))
    elif idx == 2:
        band(d, x, y, w, h, (32, 30, 52), (70, 44, 60))
        for i, tw in enumerate((34, 52, 44, 60, 38)):
            bx = x + 14 + i * (w - 28) // 5
            d.rectangle([bx, y + h - 34 - tw, bx + 26, y + h - 22],
                        fill=(16, 16, 26))
            for wy in range(4):
                d.rectangle([bx + 5, y + h - 30 - tw + wy * 10, bx + 11,
                             y + h - 26 - tw + wy * 10], fill=(240, 200, 90))
        starburst(d, x + w * 0.78, y + h * 0.32, 10, 34, 12, (255, 150, 40))
        d.ellipse([x + w * 0.78 - 12, y + h * 0.32 - 12,
                   x + w * 0.78 + 12, y + h * 0.32 + 12], fill=(255, 190, 60))
        d.rectangle([x, y + h - 22, x + w, y + h], fill=(24, 20, 30))
    elif idx == 3:
        band(d, x, y, w, h, (96, 92, 130), (52, 56, 84))
        for i in range(6):
            bx = x + 10 + i * (w - 20) // 6
            bh = 26 + (i % 3) * 16
            d.rectangle([bx, y + h - 20 - bh, bx + 24, y + h - 16],
                        fill=(22, 26, 40))
        flag(d, x + w * 0.16, y + 14, 44, 24, [(178, 34, 34), (250, 250, 250),
                                                (178, 34, 34)])
        flag(d, x + w * 0.46, y + 14, 44, 24, [(222, 40, 40), (222, 40, 40),
                                                (222, 40, 40)])
        flag(d, x + w * 0.74, y + 14, 44, 24, [(250, 250, 250), (30, 60, 160),
                                                (222, 40, 40)])
        d.rectangle([x, y + h - 16, x + w, y + h], fill=(30, 28, 40))
    elif idx == 4:
        band(d, x, y, w, h, (120, 170, 205), (70, 120, 160))
        d.ellipse([x + w * 0.78, y + 8, x + w * 0.78 + 34, y + 42],
                  fill=(255, 214, 120))
        d.arc([x + 6, y + h * 0.42, x + w - 6, y + h + 30], 200, 340,
              fill=INK, width=6)
        for px in (0.2, 0.5, 0.8):
            d.line([(x + w * px, y + h * 0.62), (x + w * px, y + h - 14)],
                   fill=INK, width=3)
        d.rectangle([x, y + h - 14, x + w, y + h], fill=(36, 84, 120))
    elif idx == 5:
        band(d, x, y, w, h, (150, 170, 190), (90, 120, 150))
        for i in range(4):
            bx = x + 12 + i * (w - 24) // 4
            d.rectangle([bx, y + h - 46, bx + 30, y + h - 18],
                        fill=(240, 238, 228))
            d.polygon([(bx - 4, y + h - 46), (bx + 15, y + h - 66),
                       (bx + 34, y + h - 46)], fill=TERRA)
        flag(d, x + w * 0.7, y + 10, 40, 22, [(222, 40, 40), (222, 40, 40),
                                               (222, 40, 40)])
    elif idx == 6:
        band(d, x, y, w, h, (170, 200, 190), (110, 160, 130))
        d.ellipse([x + w * 0.5 - 30, y + 6, x + w * 0.5 + 30, y + 66],
                  fill=(70, 130, 80))
        d.line([(x + w * 0.5, y + 66), (x + w * 0.5, y + h - 20)],
               fill=(60, 110, 60), width=4)
        d.polygon([(x + 6, y + h - 18), (x + w * 0.4, y + h - 52),
                   (x + w * 0.7, y + h - 18)], fill=(80, 140, 90))
        d.polygon([(x + w * 0.4, y + h - 18), (x + w * 0.75, y + h - 58),
                   (x + w - 6, y + h - 18)], fill=(60, 120, 75))
    elif idx == 7:
        band(d, x, y, w, h, (200, 190, 170), (160, 150, 130))
        for cx in (0.3, 0.7):
            d.rectangle([x + w * cx - 8, y + 22, x + w * cx + 8, y + h - 24],
                        fill=(240, 236, 224))
        d.rectangle([x + w * 0.2, y + 18, x + w * 0.8, y + 26],
                    fill=(240, 236, 224))
        d.line([(x + w * 0.5, y + 26), (x + w * 0.5, y + h - 24)], fill=INK,
               width=3)
        d.arc([x + w * 0.32, y + 40, x + w * 0.68, y + 76], 0, 180,
              fill=INK, width=3)
    elif idx == 8:
        band(d, x, y, w, h, (245, 240, 228), (225, 215, 195))
        pts = [(x + 8, y + h * 0.3), (x + w * 0.3, y + h * 0.42),
               (x + w * 0.55, y + h * 0.34), (x + w * 0.8, y + h * 0.62),
               (x + w - 8, y + h * 0.78)]
        d.line(pts, fill=RED, width=5, joint="curve")
        d.line([(x + 8, y + h - 14), (x + w - 8, y + h - 14)], fill=GREY,
               width=2)
        for gx in (0.25, 0.5, 0.75):
            d.line([(x + w * gx, y + 6), (x + w * gx, y + h - 14)],
                   fill=(210, 200, 180), width=1)
    elif idx == 9:
        band(d, x, y, w, h, (120, 70, 130), (50, 30, 70))
        for i in range(5):
            bx = x + 8 + i * (w - 16) // 5
            bh = 30 + (i * 13) % 30
            d.rectangle([bx, y + h - 18 - bh, bx + 22, y + h - 14],
                        fill=(24, 18, 36))
            for wy in range(3):
                d.rectangle([bx + 4, y + h - 14 - bh + wy * 10, bx + 10,
                             y + h - 10 - bh + wy * 10], fill=(255, 210, 90))
        d.ellipse([x + w * 0.8, y + 6, x + w * 0.8 + 26, y + 32],
                  fill=(255, 220, 140))
    elif idx == 10:
        band(d, x, y, w, h, (10, 14, 30), (20, 28, 52))
        rnd = random.Random(11)
        for _ in range(26):
            sx = x + rnd.randrange(w)
            sy = y + rnd.randrange(h - 16)
            d.ellipse([sx, sy, sx + 3, sy + 3], fill=(240, 240, 250))
        d.ellipse([x + w * 0.6, y + h * 0.3, x + w * 0.6 + 22,
                   y + h * 0.3 + 22], fill=(200, 210, 230))
        d.line([(x + w * 0.2, y + h * 0.6), (x + w * 0.6, y + h * 0.35)],
               fill=(200, 200, 220), width=2)
        d.ellipse([x + w * 0.16, y + h * 0.56, x + w * 0.16 + 10,
                   y + h * 0.56 + 10], fill=(255, 200, 80))
    elif idx == 11:
        band(d, x, y, w, h, (205, 195, 175), (175, 160, 135))
        d.rectangle([x + w * 0.2, y + h - 30, x + w * 0.8, y + h - 20],
                    fill=(120, 80, 40))
        d.line([(x + w * 0.35, y + 14), (x + w * 0.55, y + h - 32)],
               fill=(90, 60, 30), width=7)
        d.rectangle([x + w * 0.5, y + h - 44, x + w * 0.66, y + h - 30],
                    fill=(90, 60, 30))
        d.ellipse([x + w * 0.72, y + 12, x + w * 0.72 + 26, y + 38],
                  fill=(255, 220, 130))
    elif idx == 12:
        band(d, x, y, w, h, (240, 200, 130), (200, 150, 80))
        d.ellipse([x + w * 0.7, y + 6, x + w * 0.7 + 30, y + 36],
                  fill=(255, 190, 80))
        d.line([(x + 6, y + h - 16), (x + w * 0.35, y + h - 44),
                (x + w * 0.6, y + h - 20), (x + w - 6, y + h - 42)],
               fill=(150, 100, 50), width=3)
        d.rectangle([x, y + h - 14, x + w, y + h], fill=(170, 120, 60))
    elif idx == 13:
        band(d, x, y, w, h, (24, 40, 70), (40, 60, 100))
        cx, cy = x + w / 2, y + h / 2
        for rx, ry in ((44, 16), (36, 26), (16, 40)):
            d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                      outline=(150, 190, 230), width=3)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 190, 60))
    elif idx == 14:
        band(d, x, y, w, h, (150, 180, 200), (100, 140, 170))
        d.ellipse([x + w * 0.3, y + h * 0.3, x + w * 0.3 + 44,
                   y + h * 0.3 + 44], outline=INK, width=4)
        d.ellipse([x + w * 0.52, y + h * 0.3, x + w * 0.52 + 44,
                   y + h * 0.3 + 44], outline=INK, width=4)
        d.line([(x + w * 0.3, y + h * 0.55), (x + w * 0.72, y + h * 0.55)],
               fill=INK, width=3)
        d.polygon([(x + 10, y + h - 16), (x + w * 0.45, y + h - 46),
                   (x + w - 10, y + h - 16)], fill=(90, 130, 90))
    elif idx == 15:
        band(d, x, y, w, h, (90, 140, 170), (50, 100, 140))
        d.polygon([(x + w * 0.2, y + h * 0.55), (x + w * 0.8, y + h * 0.55),
                   (x + w * 0.72, y + h * 0.8), (x + w * 0.28, y + h * 0.8)],
                  fill=(30, 40, 60))
        d.rectangle([x + w * 0.42, y + h * 0.3, x + w * 0.46, y + h * 0.55],
                    fill=(30, 40, 60))
        d.line([(x + w * 0.6, y + h * 0.2), (x + w * 0.72, y + h * 0.32),
                (x + w * 0.6, y + h * 0.4)], fill=(200, 200, 210), width=3)
        d.rectangle([x, y + h - 12, x + w, y + h], fill=(40, 80, 120))
    else:
        band(d, x, y, w, h, (130, 170, 110), (90, 130, 80))
        d.ellipse([x + w * 0.7, y + 8, x + w * 0.7 + 28, y + 36],
                  fill=(255, 220, 130))
        d.line([(x + w * 0.3, y + h - 20), (x + w * 0.62, y + h * 0.35)],
               fill=(120, 80, 40), width=6)
        d.ellipse([x + w * 0.6, y + h * 0.3, x + w * 0.6 + 14,
                   y + h * 0.3 + 14], fill=(200, 40, 40))
        d.rectangle([x, y + h - 12, x + w, y + h], fill=(70, 110, 60))


def tag20(d, x, y, w):
    d.rectangle([x + w - 74, y + 8, x + w - 8, y + 30], fill=RED)
    d.text((x + w - 67, y + 11), "20 NOV", font=SANSB(13), fill=(255, 255, 255))


HEROES = [
    dict(n=1, kicker="1 · ODISHA · STORM", src="IMD · THE HINDU",
         head="Akvan comes ashore on the Odisha coast",
         dek="Cyclone Akvan crossed the coast near Gopalpur at noon, winds "
             "90-100 km/h gusting to 110. Three hundred thousand people are "
             "out of harm's way, 423 rescue teams deployed, red alerts in "
             "11 districts."),
    dict(n=2, kicker="2 · RIYADH · ATTACK", src="ARAB NEWS · REUTERS",
         head="Houthi missile hits Riyadh's KAFD financial district",
         dek="A Houthi missile damaged a wealth-fund tower in the financial "
             "district, one of Riyadh's tallest. No casualties are reported, "
             "as air defences answered the strike."),
    dict(n=3, kicker="3 · SHENZHEN · DIPLOMACY", src="REUTERS · AP",
         head="Trump, Xi and Putin issue a joint declaration",
         dek="No big peace deal from the trilateral's second day. Trump says "
             "the Iran war call waits until 2027, rates the summit '12 out "
             "of 10', and Putin may attend December's G20 in Miami."),
]

PICTURED = [
    dict(n=4, kicker="4 · KERCH STRAIT · WAR", src="CLAIM · KYIV",
         head="Crimean Bridge hit a third time this week; rail halted",
         dek="A Ukrainian naval drone strike disrupted rail traffic on the "
             "bridge. Rail partly resumes; Putin vows retaliation, and Kyiv "
             "was hit by drones."),
    dict(n=5, kicker="5 · SHENZHEN · SUMMIT", src="AP",
         head="APEC leaders meet in Shenzhen",
         dek="Leaders gather in China for the APEC summit. Xi urges APEC "
             "economies to back open trade and new technology."),
    dict(n=6, kicker="6 · ANTALYA · CLIMATE", src="UNFCCC · AFP",
         head="COP31's final day: fossil fuels cut from the text",
         dek="A revised draft strips out every fossil-fuel phase-out pledge. "
             "Delegates push back as the final plenary meets today."),
    dict(n=7, kicker="7 · THE HAGUE · LAW", src="AP · BBC",
         head="The world answers the genocide verdict",
         dek="Britain expels Myanmar's defence attache and seeks an urgent "
             "Security Council meeting. The Gambia hails a 'historic' verdict."),
    dict(n=8, kicker="8 · NEW YORK · MARKETS", src="BLOOMBERG",
         head="Anthropic's debut can't stop the slide",
         dek="The Dow fell 1,084 points, the S&P 2.02% and the Nasdaq 2.25%, "
             "as the AI selloff bit a day after Anthropic's record debut."),
    dict(n=9, kicker="9 · VICE CITY · GAMES", src="SENSOR TOWER",
         head="GTA VI passes The Odyssey's $1.84bn",
         dek="Launch-day sales top The Odyssey's $1.80bn global run, Sensor "
             "Tower estimates. Reviews land; Rockstar calls it the "
             "highest-rated game ever."),
    dict(n=10, kicker="10 · SPACE · SCIENCE", src="NASA · JPL",
         head="NASA confirms Voyager 1's light-day milestone",
         dek="The probe is now a full light-day from Earth - 16 billion miles "
             "out, the farthest any human-made object has ever travelled."),
    dict(n=11, kicker="11 · SEOUL · LAW", src="KOREA TIMES",
         head="South Korea clears ex-PM Han",
         dek="The Supreme Court overturns former prime minister Han Duck-soo's "
             "conviction, in the case tied to the 2024 martial-law declaration."),
    dict(n=12, kicker="12 · SUVA · CLIMATE", src="AFP",
         head="Fiji declares a national disaster over drought",
         dek="Fiji declares a national disaster over drought and water "
             "shortages. El Nino leaves water short across the islands."),
    dict(n=13, kicker="13 · VIENNA · SECURITY", src="IAEA",
         head="North Korea expands uranium enrichment at Yongbyon",
         dek="The UN watchdog reports growth at the nuclear site, in its "
             "latest assessment of the Yongbyon complex."),
    dict(n=14, kicker="14 · CARACAS · DIPLOMACY", src="REUTERS",
         head="US and Venezuela restore military cooperation",
         dek="The two countries sign an agreement to work together again, "
             "restoring a military channel closed for years."),
    dict(n=15, kicker="15 · HORMUZ · CONFLICT", src="REUTERS",
         head="ADNOC vessel attacked in the Strait of Hormuz",
         dek="One crew member is missing after the strike on the ADNOC vessel "
             "in the strait."),
    dict(n=16, kicker="16 · WELLINGTON · CRICKET", src="AP",
         head="Day two at the Basin: Nicholls' 113 anchors New Zealand",
         dek="New Zealand build on Henry Nicholls' unbeaten 113 as India hunt "
             "early wickets, in the first Test at the Basin Reserve."),
]

BRIEFS = [
    (17, "BRUSSELS", "EU-UK summit opens"),
    (18, "NEW DELHI", "Modi meets William and Kate"),
    (19, "DHAKA", "Fire at the Yunus home; arson feared"),
    (20, "MUMBAI", "Sensex +1.21%, Nifty +1.14% on the day"),
    (21, "TOKYO", "Hayabusa2 gives up landing; mission rewritten"),
    (22, "BERLIN", "Coalition of the Willing meets in Berlin"),
    (23, "BERLIN", "Merz hosts Qatar's emir in Berlin"),
    (24, "NEW DELHI", "Pakistan minister leads delegation to Delhi for SCO"),
    (25, "MANILA", "Philippines-Chile trade deal signed"),
    (26, "MANILA", "Musk plans Philippines projects"),
    (27, "HONG KONG", "India beats Malaysia, Asian Hockey Trophy opens"),
    (28, "IPOH", "Harimau Shakti exercise opens in Ipoh"),
    (29, "NEW DELHI", "India's electronics exports jump 44%"),
    (30, "NEW DELHI", "ICMR completes 100 tech transfers"),
    (31, "NEW DELHI", "India unveils its first bird-flu vaccine"),
    (32, "GENEVA", "World Children's Day marked worldwide"),
    (33, "EUROPE", "Youth anti-war protests across Europe"),
    (34, "BRUSSELS", "EU delays its methane rules by 24 months"),
    (35, "COLOGNE", "Bayern Munich beat Koln 3-0"),
    (36, "U17 CUP", "Argentina 0-2 Australia at the U17 Cup"),
    (37, "WASHINGTON", "Jobless claims come in at 203,000"),
    (38, "STRASBOURG", "NATO's assembly opens its 72nd session"),
    (39, "HANOI", "Azerbaijan's Aliyev visits Vietnam"),
    (40, "MARKETS", "Crude futures fall over 3%"),
    (41, "KHARTOUM", "Sudan army: two-year El Obeid siege broken"),
    (42, "MOGADISHU", "Somalia gives UAE ambassador 72 hours to leave"),
    (43, "SAN SALVADOR", "Migrant boat capsizes off El Salvador; dozens missing"),
    (44, "PORT-AU-PRINCE", "Haiti approves Salvadoran troop deal vs gangs"),
    (45, "ARABIAN SEA", "Amur falcons cross the Arabian Sea"),
    (46, "NEW YORK", "Al-Saadi appears in a New York court over a UK plot"),
    (47, "KYIV", "Witkoff and Kushner brief Zelenskyy"),
    (48, "BEIJING", "Xi urges APEC to back open trade, new tech"),
]

# Land spans for the dot-matrix map: (row0, row1, col0, col1) on a 34x96 grid.
LAND = [
    (1, 3, 28, 34), (3, 5, 6, 24), (6, 10, 2, 26), (11, 13, 8, 20),
    (15, 17, 20, 30), (18, 23, 21, 29), (24, 26, 22, 26),
    (4, 6, 44, 46), (3, 9, 46, 56), (11, 14, 45, 58), (15, 19, 47, 57),
    (20, 24, 48, 55), (2, 4, 62, 90), (5, 9, 58, 92), (10, 12, 60, 80),
    (13, 16, 78, 88), (8, 12, 90, 93), (22, 27, 78, 90),
]

PINS = {4: (36, 45), 5: (114, 22), 6: (30, 36), 7: (4, 52), 8: (-74, 40),
        9: (-80, 25), 10: (-118, 34), 11: (127, 37), 12: (178, -18),
        13: (16, 48), 14: (-66, 10), 15: (56, 26), 16: (174, -41)}

REGIONS = [("EUROPE", 11, BLUE), ("THE AMERICAS", 7, TEAL),
           ("ASIA-PACIFIC", 19, TERRA), ("MIDEAST", 4, OCHRE),
           ("AFRICA", 2, OLIVE), ("OCEANIA", 1, GREY), ("WORLD", 4, DARK)]

TIMELINE = ("THE DAY IN UTC — Overnight: Crimean Bridge hit a third time · "
            "~06:00 UTC: APEC leaders meet in Shenzhen · ~10:00 UTC: "
            "Trilateral declaration issued · ~12:00 UTC: Akvan makes landfall "
            "in Odisha · ~14:00 UTC: Houthi missile hits Riyadh KAFD · Late: "
            "Wall Street slides; Dow -1,084")


def hero_panel(d, x, y, w, h, st, dy):
    yy = y + dy
    d.rectangle([x, yy, x + w, yy + h], fill=CREAM, outline=INK, width=2)
    scene(d, x + 6, yy + 6, w - 12, 130, st["n"])
    tag20(d, x + 6, yy + 6, w - 12)
    ky = yy + 144
    d.text((x + 10, ky), st["kicker"], font=SANSB(17), fill=TERRA)
    d.text((x + w - 10 - d.textlength(st["src"], font=SANS(12)), ky + 2),
           st["src"], font=SANS(12), fill=GREY)
    hy = ky + 26
    hy = text_block(d, x + 10, hy, st["head"], SERIFB(27), w - 20, 30,
                    INK, max_lines=2)
    text_block(d, x + 10, hy + 4, st["dek"], SANS(15), w - 20, 18,
               (52, 48, 42), max_lines=3)


def pic_panel(d, x, y, w, h, st, scene_h=62, dek_lines=3):
    d.rectangle([x, y, x + w, y + h], fill=CREAM, outline=INK, width=1)
    scene(d, x + 5, y + 5, w - 10, scene_h, st["n"])
    tag20(d, x + 5, y + 5, w - 10)
    ky = y + scene_h + 11
    d.text((x + 8, ky), st["kicker"], font=SANSB(13), fill=TERRA)
    d.text((x + w - 8 - d.textlength(st["src"], font=SANS(10)), ky + 1),
           st["src"], font=SANS(10), fill=GREY)
    hy = ky + 20
    hy = text_block(d, x + 8, hy, st["head"], SERIFB(19), w - 16, 22,
                    INK, max_lines=2)
    text_block(d, x + 8, hy + 3, st["dek"], SANS(12), w - 16, 15,
               (52, 48, 42), max_lines=dek_lines)


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=DARK, outline=INK, width=2)
    rows, cols = 34, 96
    cw, ch = w / cols, h / rows
    land = set()
    for r0, r1, c0, c1 in LAND:
        for rr in range(r0, r1 + 1):
            for cc in range(c0, c1 + 1):
                land.add((rr, cc))
    for rr, cc in land:
        cx = x + cc * cw + cw / 2
        cy = y + rr * ch + ch / 2
        d.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6],
                  fill=(190, 190, 180))
    for n, (lon, lat) in PINS.items():
        px = x + (lon + 170) / 360 * w
        py = y + (75 - lat) / 130 * h
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.text((px - 3, py - 7), str(n), font=SANSB(11), fill=(255, 255, 255))


def main():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    grain(im)
    # Postcard frame: thick terracotta border, thin olive inner rule.
    d.rectangle([14, 14, W - 14, H - 14], outline=TERRA, width=18)
    d.rectangle([40, 40, W - 40, H - 40], outline=OLIVE, width=2)
    mx, mw = 48, W - 96

    # Top line.
    d.text((mx, 52), "ONE DAY OF WORLD NEWS, ONE PICTURE", font=SANSB(17),
           fill=TERRA)
    right = "48 STORIES - 7 REGIONS"
    d.text((mx + mw - d.textlength(right, font=SANSB(17)), 52), right,
           font=SANSB(17), fill=INK)
    d.line([(mx, 80), (mx + mw, 80)], fill=INK, width=2)

    # Masthead inside a terracotta box.
    d.rectangle([mx, 92, mx + mw, 196], fill=TERRA)
    d.rectangle([mx, 92, mx + mw, 196], outline=TERRA_D, width=3)
    title = "Friday 20 November 2026"
    tf = SERIFB(92)
    d.text(((W - d.textlength(title, font=tf)) / 2, 104), title, font=tf,
           fill=CREAM)
    sub = ("Akvan comes ashore · A missile over Riyadh · Trump puts the Iran "
           "decision off to 2027 · The world answers the genocide verdict")
    d.text((mx, 204), sub, font=SERIFI(20), fill=RED)

    # Timeline strip.
    d.rectangle([mx, 236, mx + mw, 280], fill=(238, 226, 196))
    d.rectangle([mx, 236, mx + mw, 280], outline=OCHRE, width=2)
    text_block(d, mx + 12, 242, TIMELINE, SANS(16), mw - 24, 20, INK,
               max_lines=2)

    # Region strip. Small segments get a minimum width so their labels fit.
    total = sum(c for _, c, _ in REGIONS)
    minw = 72
    widths = [max(minw, int(mw * cnt / total)) for _, cnt, _ in REGIONS]
    over = sum(widths) - mw
    big = [i for i, wdt in enumerate(widths) if wdt > minw]
    while over > 0 and big:
        take = max(1, over // len(big))
        for i in list(big):
            cut = min(take, widths[i] - minw, over)
            widths[i] -= cut
            over -= cut
            if widths[i] <= minw:
                big.remove(i)
            if over <= 0:
                break
    rx = mx
    for (name, cnt, col), seg in zip(REGIONS, widths):
        d.rectangle([rx, 288, rx + seg - 2, 318], fill=col)
        lab = "%s %d" % (name, cnt)
        fnt = SANSB(14) if seg >= 110 else SANSB(11)
        d.text((rx + (seg - d.textlength(lab, font=fnt)) / 2, 296),
               lab, font=fnt, fill=(255, 255, 255))
        rx += seg

    # Three heroes, staggered diagonally.
    hw = (mw - 32) // 3
    for i, st in enumerate(HEROES):
        hero_panel(d, mx + i * (hw + 16), 330, hw, 290, st, dy=i * 8)

    # Pictured rows: 3, then 5, then 5.
    rows = [(3, 632, 180, 62, 3), (5, 824, 164, 54, 2), (5, 1000, 164, 54, 2)]
    k = 0
    for count, ry, rh, sh, dl in rows:
        pw = (mw - (count - 1) * 12) // count
        for j in range(count):
            pic_panel(d, mx + j * (pw + 12), ry, pw, rh, PICTURED[k],
                      scene_h=sh, dek_lines=dl)
            k += 1

    # Where it happened.
    d.text((mx, 1180), "WHERE IT HAPPENED", font=SERIFB(24), fill=TERRA)
    d.line([(mx, 1208), (mx + mw, 1208)], fill=INK, width=2)
    draw_map(d, mx, 1216, 520, 224)
    bx = mx + 540
    d.text((bx, 1180), "ALSO ON FRIDAY 20 NOVEMBER - 32 MORE STORIES",
           font=SERIFB(22), fill=TERRA)
    colw = (mw - 540 - 16) // 2
    for ci in range(2):
        cx = bx + ci * (colw + 16)
        yy = 1218
        for num, place, txt in BRIEFS[ci * 16:(ci + 1) * 16]:
            line = "%d %s · %s" % (num, place, txt)
            d.text((cx, yy), "●", font=SANS(10), fill=TERRA)
            yy = text_block(d, cx + 13, yy, line, SANS(11), colw - 13, 13,
                            INK, max_lines=1)
            yy += 1
        if ci == 0:
            d.line([(cx + colw + 6, 1218), (cx + colw + 6, 1440)],
                   fill=(200, 190, 170), width=1)

    # Date check.
    d.rectangle([mx, 1452, mx + mw, 1498], outline=RED, width=2)
    d.rectangle([mx, 1452, mx + 150, 1498], fill=RED)
    d.text((mx + 10, 1464), "DATE CHECK", font=SANSB(17),
           fill=(255, 255, 255))
    dc = ("Left out - they broke before Friday: the ICJ genocide ruling on "
          "Myanmar itself (Thursday 19 Nov) - Friday's news is the world's "
          "answer to it - Denmark's Greenland-US pact (19 Nov) - Anthropic's "
          "$81.34bn IPO (19 Nov); its first trading day was Thursday - "
          "Germany's electricity-tax cut (18 Nov) - the Crimean Bridge span "
          "collapse (17-18 Nov). Not yet: the trilateral's first meeting was "
          "19 Nov; the joint declaration is Friday's.")
    text_block(d, mx + 162, 1458, dc, SANS(13), mw - 174, 17, INK,
               max_lines=2)

    # Footer.
    d.text((mx, 1506), "Every story here happened, or was first reported, on "
           "Friday 20 November 2026, in some time zone. Disputed claims are "
           "attributed, not stated as fact.", font=SERIFI(13), fill=GREY)
    d.text((mx, 1524), "Sources: Reuters - AP - AFP - BBC - Bloomberg - IMD - "
           "NASA - IAEA - The Hindu - Arab News - Sensor Tower. Original "
           "drawings, drawn for this page.", font=SERIFI(13), fill=GREY)

    out = im.resize((1024, 1024), Image.LANCZOS)
    out.save("entry.png")
    print("wrote entry.png 1024x1024")


if __name__ == "__main__":
    main()
