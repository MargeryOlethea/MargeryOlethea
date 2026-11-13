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

# the pattern's colour key doubles as the stack list
KEY = [("typescript", "#3b5bdb"), ("react", "#0f8a7e"), ("next.js", INK), ("python", "#f2a134"), ("swift", "#e8442e"), ("mcp + llms", "#ff4f8b")]
x, k = 18, []
for label, col in KEY:
    k.append(f'{stitch(x, 12, col)}{stitch(x + CELL, 12, col)}<text x="{x + 28}" y="21" font-family="{FONT}" font-size="14" fill="{INK}">{label}</text>')
    x += 46 + len(label) * 8.6
open(f"{out}/key.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {x:.0f} 34" width="{x:.0f}" height="34" role="img" aria-label="Colour key: '
    + ", ".join(l for l, _ in KEY) + f'"><rect x="1" y="1" width="{x - 2:.0f}" height="32" rx="8" fill="{CREAM}" stroke="{INK}" stroke-width="1.5" stroke-dasharray="4 3"/>' + "".join(k) + "</svg>")
