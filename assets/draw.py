"""Draws the profile artwork: the film-strip banner, the link buttons and the colour key. Usage: python3 assets/draw.py assets"""
import sys

INK, CREAM, RED = "#1d1b2f", "#fbf3e4", "#ff3b3b"
COLORS = {"K": INK, "W": "#ffffff", "S": "#ffffff", "T": "#e8442e", "D": "#a82a18", "M": "#3b5bdb", "G": "#0f8a7e", "O": "#f2a134", "P": "#ff4f8b"}
PAPER = ["#ffd0df", "#d5e3ff", "#fff0b8", "#c9efe4", "#fbf3e4"]  # one fabric colour per frame
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
CELL = 10
W, H = 1200, 300

FRAMES = [
    ("the producer", [
        ".KK.........KK.", "KOOK.......KOOK", "KOPOK.....KOPOK", "KOOOOKKKKKOOOOK", "KOOOOOOOOOOOOOK",
        "KKKKKKKKKKKKKKK", "KKKSKKKOKKKSKKK", "KOKKKKOOOKKKKOK", "KOOOOOOPOOOOOOK", "KOOOOKOOOKOOOOK",
        ".KOOOOKKKOOOOK.", "..KKOOOOOOOKK..", "....KKKKKKK...."]),
    ("film school", [
        "TTWWTTWWTTWWTTW", "TWWTTWWTTWWTTWW", "KKKKKKKKKKKKKKK", "KKKKKKKKKKKKKKK", "KKWWWWKKWWWKKKK",
        "KKKKKKKKKKKKKKK", "KKWWWKKWWWWWKKK", "KKKKKKKKKKKKKKK", "KKWWKKKKKKWWKKK", "KKKKKKKKKKKKKKK"]),
    ("crashed into code", [
        "...........", ".......M...", "..M...M.M..", ".M....M..M.", "M....M....M",
        ".M..M....M.", "..M.M...M..", "...M.......", "..........."]),
    ("now: ships products", [
        ".GGGGGGGGG.", "GGGGGGGGGGG", "GGWGGWGGWGG", "GGGGGGGGGGG", "GGGGGGGGGGG",
        ".GGGGGGGGG.", "...GG......", "..GG.......", "..G........"]),
    ("off screen: crochet", [
        "...TTTTT...", "..TTDTTTT..", ".TTDTTTDTT.", "TTDTTTDTTTT", "TDTTTDTTTDT",
        "TTTTDTTTDTT", ".TTDTTTDTT.", "..TTTTDTT..", "...TTTTT..."]),
]


def stitch(x, y, fill, cell=CELL):
    return (f'<rect x="{x}" y="{y}" width="{cell - 0.6}" height="{cell - 0.6}" rx="1.8" fill="{fill}"/>'
            f'<rect x="{x + 1.5}" y="{y + 1}" width="{cell - 5}" height="1.4" rx=".7" fill="#fff" opacity=".3"/>')


def banner():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="A film strip of five crocheted '
         f'frames: the producer, a cat in sunglasses; film school, crashed into code, now ships products, off screen crochet. Produced by Margery Olethea.">',
         f'<rect width="{W}" height="{H}" rx="20" fill="{INK}"/>']
    for x in range(34, W - 40, 44):  # sprocket holes
        p.append(f'<rect x="{x}" y="16" width="22" height="14" rx="3" fill="{CREAM}"/>')
        p.append(f'<rect x="{x}" y="270" width="22" height="14" rx="3" fill="{CREAM}"/>')
    fw, fh, gap = 212, 168, 16
    n = len(FRAMES)
    x0 = (W - (n * fw + (n - 1) * gap)) // 2
    for i, (caption, rows) in enumerate(FRAMES):
        fx, fy = x0 + i * (fw + gap), 46
        p.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="8" fill="{PAPER[i]}"/>')
        p += [f'<circle cx="{fx + dx}" cy="{fy + dy}" r="1" fill="{INK}" opacity=".14"/>'
              for dx in range(14, fw - 6, 18) for dy in range(14, fh - 6, 18)]
        cell = 8 if len(rows[0]) > 11 else CELL  # the detailed icon uses a finer grid
        ix, iy = fx + (fw - len(rows[0]) * cell) // 2, fy + (126 - len(rows) * cell) // 2 + 8
        for r, row in enumerate(rows):
            for c, ch in enumerate(row):
                if ch != ".":
                    g = stitch(ix + c * cell, iy + r * cell, COLORS[ch], cell)
                    if ch == "S":  # the glint on the sunglasses twinkles
                        g = f'<g>{g}<animate attributeName="opacity" values="1;1;.1;1" dur="2.4s" repeatCount="indefinite"/></g>'
                    p.append(g)
        p.append(f'<text x="{fx + fw / 2}" y="{fy + fh - 16}" text-anchor="middle" font-family="{FONT}" font-size="15" fill="{INK}">{caption}</text>')
    p.append(f'<text x="{x0}" y="246" font-family="{FONT}" font-size="17" fill="{CREAM}">produced by margery olethea · frontend engineer, jakarta</text>')
    rx = x0 + n * fw + (n - 1) * gap
    p.append(f'<circle cx="{rx - 52}" cy="240" r="6" fill="{RED}"><animate attributeName="opacity" values="1;.15;1" dur="1.6s" repeatCount="indefinite"/></circle>')
    p.append(f'<text x="{rx}" y="246" text-anchor="end" font-family="{FONT}" font-size="17" fill="{CREAM}">REC</text>')
    p.append("</svg>")
    return "\n".join(p)


def button(label, dot):
    w = 38 + len(label) * 9.7
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} 34" width="{w:.0f}" height="34" role="img" aria-label="{label}">'
            f'<rect x="1" y="1" width="{w - 2:.0f}" height="32" rx="8" fill="{CREAM}" stroke="{INK}" stroke-width="2"/>'
            f'{stitch(12, 13, dot)}<text x="28" y="22" font-family="{FONT}" font-size="15" fill="{INK}">{label}</text></svg>')


out = sys.argv[1]
open(f"{out}/banner.svg", "w").write(banner())
for name, label, dot in [("linkedin", "linkedin", "#3b5bdb"), ("instagram", "instagram", "#ff4f8b"), ("email", "email", "#e8442e"), ("site", "mulaibelajarai.com", "#0f8a7e")]:
    open(f"{out}/btn-{name}.svg", "w").write(button(label, dot))

# posters, legend and end credits
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
CAT, BUBBLE = FRAMES[0][1], FRAMES[3][1]
GLASS = ["..MMMMM....", ".MWWWWWM...", "MWWWWWWWM..", "MWWSWWWWM..", "MWWWWWWWM..", "MWWWWWWWM..",
         "MWWWWWWWM..", ".MWWWWWM...", "..MMMMMK...", ".......KK..", "........KK.", ".........KK"]
PENCIL = ["........PP.", ".......POOP", "......OOOP.", ".....OOO...", "....OOO....", "...OOO.....",
          "..OOO......", ".WOO.......", "KWW........", "KK........."]
# bead-pattern legend: every technology gets a symbol, reused on the posters
LEGEND = [("typescript", "#3b5bdb", "×"), ("react", "#0f8a7e", "●"), ("next.js", INK, "▲"),
          ("python", "#f2a134", "◆"), ("swift", "#e8442e", "■"), ("mcp + llms", "#ff4f8b", "♥")]
BY_NAME = {n: (c, g) for n, c, g in LEGEND}


def bead(x, y, name, size=22):
    col, glyph = BY_NAME[name]
    return (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="5" fill="{col}" stroke="{INK}" stroke-width="1.5"/>'
            f'<text x="{x + size / 2}" y="{y + size * .72}" text-anchor="middle" font-family="{SANS}" font-size="{size * .62}" font-weight="700" fill="#fff">{glyph}</text>')


def icon(rows, x, y, cell):
    return "".join(stitch(x + c * cell, y + r * cell, COLORS[ch], cell)
                   for r, row in enumerate(rows) for c, ch in enumerate(row) if ch != ".")


def yarn(x, y, on=True):
    fill = "#e8442e" if on else "none"
    return (f'<circle cx="{x}" cy="{y}" r="10" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M{x - 7} {y - 2} Q{x} {y - 9} {x + 7} {y - 2} M{x - 8} {y + 3} Q{x} {y - 4} {x + 8} {y + 3}" fill="none" stroke="{INK}" stroke-width="1.5"/>')


def poster(name, genre, bg, fg, rows, cell, ipos, title, tx, anchor, ty, blurb, stack, extra="", after=""):
    pw, ph = 400, 480
    q = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {pw} {ph}" role="img" aria-label="{" ".join(title).title()}, {genre.lower()}. {" ".join(blurb)}">',
         f'<clipPath id="c"><rect x="4" y="4" width="{pw - 8}" height="{ph - 8}" rx="16"/></clipPath><g clip-path="url(#c)">', bg, extra,
         icon(rows, ipos[0], ipos[1], cell)]
    px = {"start": 30, "middle": 200 - len(genre) * 4.4 - 14, "end": pw - 30 - len(genre) * 8.8 - 28}[anchor]
    q.append(f'<rect x="{px}" y="24" width="{len(genre) * 8.8 + 28}" height="28" rx="14" fill="{fg}"/>'
             f'<text x="{px + 14}" y="43" font-family="{FONT}" font-size="14" fill="{CREAM if fg == INK else INK}">{genre}</text>')
    for i, line in enumerate(title):
        q.append(f'<text x="{tx}" y="{ty + i * 36}" text-anchor="{anchor}" font-family="{SANS}" font-size="31" font-weight="900" fill="{fg}">{line}</text>')
    by = ty + len(title) * 36 + 2
    for i, line in enumerate(blurb):
        q.append(f'<text x="{tx}" y="{by + i * 24}" text-anchor="{anchor}" font-family="{SANS}" font-size="19" font-style="italic" fill="{fg}">{line}</text>')
    q.append("".join(yarn(42 + i * 26, ph - 38) for i in range(5)))  # the cat critic rates in yarn balls
    q.append("".join(bead(pw - 34 - (len(stack) - i) * 28, ph - 49, n) for i, n in enumerate(stack)))
    q.append(after + f'</g><rect x="2" y="2" width="{pw - 4}" height="{ph - 4}" rx="18" fill="none" stroke="{INK}" stroke-width="4"/></svg>')
    open(f"{out}/poster-{name}.svg", "w").write("\n".join(q).replace("'", "&#39;"))


W, H = 400, 480
dots = "".join(f'<circle cx="{x}" cy="{y}" r="1.2" fill="{INK}" opacity=".12"/>' for x in range(26, W - 14, 22) for y in range(26, H - 14, 22))
# 1. comedy: centred, bright, tilted confetti stitches
confetti = "".join(stitch(x, y, c, 9) for x, y, c in [(46, 96, "#ff4f8b"), (332, 84, "#3b5bdb"), (70, 196, "#f2a134"), (318, 204, "#e8442e"), (352, 142, "#ff4f8b"), (30, 150, "#3b5bdb")])
poster("bot", "A SCREWBALL COMEDY", f'<rect width="{W}" height="{H}" fill="#c9efe4"/>{dots}', INK, BUBBLE, 14, (123, 82),
       ["THE BOT THAT", "ANSWERS SO I", "DON'T HAVE TO"], 200, "middle", 272,
       ["“1,149 tests. Excessive,", "in a reassuring way.”"], ["next.js", "typescript", "mcp + llms"], confetti)
# 2. detective: noir, spotlight, left aligned, the cat peeks in as a witness
spot = f'<circle cx="250" cy="150" r="150" fill="{CREAM}" opacity=".10"/><circle cx="250" cy="150" r="96" fill="{CREAM}" opacity=".12"/>'
peek = f'<rect x="252" y="{H - 138}" width="140" height="84" rx="10" fill="{CREAM}"/>' + icon(CAT[:9], 262, H - 128, 8)
poster("reader", "A DETECTIVE STORY", f'<rect width="{W}" height="{H}" fill="{INK}"/>', CREAM, GLASS, 15, (160, 62),
       ["THE READER", "THAT NEVER", "GETS TIRED"], 30, "start", 290,
       ["“Six gates, zero patience", "for weak ideas.”"], ["python", "mcp + llms"], spot, peek)
# 3. thriller: sunrise bands, title at the top right, pencil rising from the corner
bands = "".join(f'<rect y="{y}" width="{W}" height="{h}" fill="{c}"/>'
                for y, h, c in [(0, 170, "#2f2350"), (170, 80, "#8a3b6b"), (250, 70, "#e8442e"), (320, 70, "#f2a134"), (390, 90, "#fff0b8")])
poster("writer", "A PRE-DAWN THRILLER", bands, CREAM, PENCIL, 14, (44, 262),
       ["THE SCRIPTWRITER", "WHO IS UP", "BEFORE YOU"], 370, "end", 96,
       ["“665 tests. It marks", "its own homework.”"], ["python", "mcp + llms"])

# colour key as a real bead legend
x, k = 16, []
for name, _, _ in LEGEND:
    k.append(bead(x, 8, name) + f'<text x="{x + 30}" y="24" font-family="{FONT}" font-size="14" fill="{INK}">{name}</text>')
    x += 50 + len(name) * 8.6
open(f"{out}/key.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x:.0f} 38" width="{x:.0f}" height="38" role="img" aria-label="Pattern legend: '
    + ", ".join(n for n, _, _ in LEGEND) + f'"><rect x="1" y="1" width="{x - 2:.0f}" height="36" rx="8" fill="{CREAM}" stroke="{INK}" stroke-width="1.5" stroke-dasharray="4 3"/>' + "".join(k) + "</svg>")

# end credits with the cat
c = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 150" role="img" aria-label="Written, produced, coded and tested by Margery. Craft services: crochet.">',
     f'<rect width="700" height="150" rx="14" fill="{INK}"/>', f'<rect x="28" y="22" width="130" height="106" rx="12" fill="#ffd0df"/>', icon(CAT, 40, 30, 7),
     f'<text x="190" y="64" font-family="{FONT}" font-size="19" fill="{CREAM}">written · produced · coded · tested</text>',
     f'<text x="190" y="92" font-family="{FONT}" font-size="19" fill="{CREAM}">by margery</text>',
     f'<text x="190" y="122" font-family="{FONT}" font-size="15" fill="#f2a134">craft services: crochet</text></svg>']
open(f"{out}/credits.svg", "w").write("\n".join(c))
