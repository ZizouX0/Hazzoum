"""Full-wrap KDP paperback cover (back + spine + front) for the activity book."""
import math, random
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from make_activity_book import make_maze, draw_maze, make_ws, draw_ws  # noqa (rebuilds interior too)

PAGES = 58
BLEED = 0.125 * inch
SPINE = PAGES * 0.002252 * inch          # white paper, black ink
TW, TH = 8.5 * inch, 11 * inch
W, H = 2 * TW + SPINE + 2 * BLEED, TH + 2 * BLEED
random.seed(7)
c = canvas.Canvas("activity-book-cover.pdf", pagesize=(W, H), initialFontName="R")
BLUE, YEL, ORG, PINK, GRN = map(HexColor, ("#2B7FD9", "#FFD23F", "#FF7A30", "#FF5C8A", "#3DBE7B"))

def star(cx, cy, r, col):
    p = c.beginPath()
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        (p.moveTo if k == 0 else p.lineTo)(cx + rr * math.cos(a), cy + rr * math.sin(a))
    p.close(); c.setFillColor(col); c.setStrokeColor(black); c.setLineWidth(2.5); c.drawPath(p, fill=1)

def card(x, y, w, h, rot=0):
    c.saveState(); c.translate(x + w / 2, y + h / 2); c.rotate(rot)
    c.setFillColor(HexColor("#1B5FAE")); c.roundRect(-w / 2 + 6, -h / 2 - 6, w, h, 18, stroke=0, fill=1)
    c.setFillColor(white); c.setStrokeColor(black); c.setLineWidth(3); c.roundRect(-w / 2, -h / 2, w, h, 18, fill=1)
    c.translate(-w / 2, -h / 2)

c.setFillColor(BLUE); c.rect(0, 0, W, H, stroke=0, fill=1)
c.setFillColor(HexColor("#3A8DE6"))
for _ in range(90):
    c.circle(random.uniform(0, W), random.uniform(0, H), random.uniform(4, 16), stroke=0, fill=1)

# ----- front -----
fx = BLEED + TW + SPINE; cx = fx + TW / 2
c.setFillColor(YEL); c.setStrokeColor(black); c.setLineWidth(4)
c.roundRect(fx + 0.55 * inch, H - 4.75 * inch, TW - 1.1 * inch, 3.9 * inch, 34, fill=1)
c.setFillColor(black); c.setFont("B", 74); c.drawCentredString(cx, H - 2.05 * inch, "FUN")
c.setFillColor(ORG); c.setFont("B", 54); c.drawCentredString(cx, H - 3.05 * inch, "ACTIVITY BOOK")
c.setFillColor(black); c.setFont("B", 44); c.drawCentredString(cx, H - 3.85 * inch, "for Kids")
c.setFont("B", 22); c.drawCentredString(cx, H - 4.4 * inch, "Mazes  •  Word Searches  •  Sudoku")
card(fx + 0.75 * inch, 2.35 * inch, 3.5 * inch, 3.5 * inch, 5)
draw_maze(c, make_maze(9, 9), 0.3 * inch, 0.3 * inch, 2.9 * inch, lw=3.2); c.restoreState()
card(fx + 4.35 * inch, 2.9 * inch, 3.3 * inch, 3.3 * inch, -6)
c.setFillColor(black); draw_ws(c, make_ws("STAR MOON FUN PLAY GAME".split(), 6, False), 0.3 * inch, 0.3 * inch, 2.7 * inch, lw=3); c.restoreState()
c.setFillColor(PINK); c.setStrokeColor(black); c.setLineWidth(4); c.circle(fx + 1.75 * inch, 1.45 * inch, 0.95 * inch, fill=1)
c.setFillColor(white); c.setFont("B", 22); c.drawCentredString(fx + 1.75 * inch, 1.6 * inch, "AGES")
c.setFont("B", 38); c.drawCentredString(fx + 1.75 * inch, 1.1 * inch, "6-8")
c.setFillColor(GRN); c.roundRect(fx + 3.2 * inch, 0.85 * inch, 4.5 * inch, 1.2 * inch, 24, fill=1)
c.setFillColor(white); c.setFont("B", 25); c.drawCentredString(fx + 5.45 * inch, 1.5 * inch, "47 Puzzles")
c.setFont("B", 17); c.drawCentredString(fx + 5.45 * inch, 1.1 * inch, "with answers in the back")
for sx, sy, r, col in ((0.75, 6.45, .33, YEL), (7.85, 6.55, .3, PINK), (7.95, 2.45, .28, YEL), (0.6, 2.0, .2, GRN)):
    star(fx + sx * inch, sy * inch, r * inch, col)

# ----- back -----
bx = BLEED; bcx = bx + TW / 2
c.setFillColor(white); c.setStrokeColor(black); c.setLineWidth(4)
c.roundRect(bx + 0.9 * inch, 3.3 * inch, TW - 1.8 * inch, 6.6 * inch, 30, fill=1)
c.setFillColor(ORG); c.setFont("B", 31); c.drawCentredString(bcx, 9.1 * inch, "Hours of screen-free fun!")
c.setFillColor(black); c.setFont("R", 17)
for i, line in enumerate(["Keep little minds busy with 47 puzzles", "that grow harder page by page.", "",
                          "★  20 mazes, from easy to tricky", "★  15 themed word searches",
                          "★  12 sudoku puzzles for beginners", "★  Big, clear print on large pages",
                          "★  Every answer in the back", "", "Great for travel, rainy days,",
                          "quiet time and gifts."]):
    c.drawCentredString(bcx, 8.45 * inch - i * 0.42 * inch, line)
star(bx + 1.0 * inch, 10.0 * inch, 0.38 * inch, YEL); star(bx + 7.6 * inch, 3.3 * inch, 0.36 * inch, PINK)
c.save()
print("cover inches: %.3f x %.3f, spine %.3f" % (W / inch, H / inch, SPINE / inch))
