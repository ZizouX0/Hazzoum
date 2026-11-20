"""Full-wrap KDP paperback cover (back + spine + front) for My Big Fun Activity Book.
Sized for 80 pages on white paper, 8.5 x 11 in trim, with 0.125 in bleed."""
import random
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import inch as IN
from reportlab.pdfgen import canvas
from art import FRIENDS, face, item, star, heart, cloud

PAGES = 80
BLEED = 0.125 * IN
SPINE = PAGES * 0.002252 * IN
TW, TH = 8.5 * IN, 11 * IN
W, H = 2 * TW + SPINE + 2 * BLEED, TH + 2 * BLEED
random.seed(5)
c = canvas.Canvas("fun-activity-book-cover.pdf", pagesize=(W, H), initialFontName="H")
SKY, SKY2, YEL, ORG, PINK, GRN, NAVY = map(HexColor, ("#35B6F2", "#5CC6F7", "#FFD23F", "#FF7A30", "#FF5C8A", "#57C465", "#17335C"))


def text(x, y, s, size, font="T", fill=black, align="c"):
    c.setFont(font, size)
    c.setFillColor(fill)
    {"c": c.drawCentredString, "l": c.drawString}[align](x, y, s)


def outlined(x, y, s, size, fill, stroke=NAVY, sw=7):
    """Chunky title lettering: a thick dark outline under a bright fill."""
    t = c.beginText()
    c.setFont("T", size)
    wd = c.stringWidth(s, "T", size)
    c.saveState()
    c.setLineJoin(1)
    c.setStrokeColor(stroke)
    c.setLineWidth(sw)
    t.setTextOrigin(x - wd / 2, y)
    t.setFont("T", size)
    t.setTextRenderMode(1)
    t.textOut(s)
    c.drawText(t)
    c.restoreState()
    text(x, y, s, size, fill=fill)


# background: sky, soft dots, grassy hill along the bottom
c.setFillColor(SKY)
c.rect(0, 0, W, H, stroke=0, fill=1)
c.setFillColor(SKY2)
for _ in range(70):
    c.circle(random.uniform(0, W), random.uniform(3 * IN, H), random.uniform(5, 18), stroke=0, fill=1)
c.setFillColor(GRN)
c.ellipse(-2 * IN, -3.2 * IN, W + 2 * IN, 1.9 * IN, stroke=0, fill=1)
c.setStrokeColor(black)

# ---------------- front ----------------
fx = BLEED + TW + SPINE
cx = fx + TW / 2
c.setLineWidth(3)
c.setStrokeColor(white)
for x, y, r in ((1.2, 9.9, .5), (7.0, 10.2, .42)):
    c.setFillColor(white)
    for dx, dy, rr in ((-0.9, 0, 0.6), (-0.2, 0.35, 0.8), (0.7, 0.1, 0.65), (0, -0.2, 0.7)):
        c.circle(fx + x * IN + dx * r * IN, y * IN + dy * r * IN, rr * r * IN, stroke=0, fill=1)
c.setStrokeColor(black)
outlined(cx, H - 2.15 * IN, "My Big", 62, white)
outlined(cx, H - 3.3 * IN, "FUN ACTIVITY", 76, YEL, sw=9)
outlined(cx, H - 4.5 * IN, "BOOK", 96, ORG, sw=9)
c.setFillColor(NAVY)
c.roundRect(fx + 0.8 * IN, H - 5.3 * IN, TW - 1.6 * IN, 0.62 * IN, 0.31 * IN, stroke=0, fill=1)
text(cx, H - 5.12 * IN, "Mazes  •  Puzzles  •  Coloring  •  Dot to Dots  •  Jokes", 22, "H", white)
kinds = [k for k, _, _ in FRIENDS]
row1 = ["cat", "bear", "bunny", "panda"]
row2 = ["frog", "lion", "pig", "chick", "dog"]
for i, k in enumerate(row1):
    face(c, k, cx + (i - 1.5) * 1.8 * IN, 4.4 * IN, 0.7 * IN, color=True, mood="happy" if i % 2 else "smile")
for i, k in enumerate(row2):
    face(c, k, cx + (i - 2) * 1.5 * IN, 2.72 * IN, 0.62 * IN, color=True, wink=i == 2, mood="happy" if i in (0, 4) else "smile")
c.setLineWidth(4)
c.setFillColor(PINK)
c.circle(fx + 1.2 * IN, 0.95 * IN + BLEED, 0.72 * IN, fill=1)
text(fx + 1.2 * IN, 1.2 * IN + BLEED, "AGES", 19, fill=white)
text(fx + 1.2 * IN, 0.72 * IN + BLEED, "4-8", 34, fill=white)
c.setFillColor(YEL)
c.setLineWidth(4)
c.roundRect(fx + 2.5 * IN, 0.5 * IN + BLEED, 5.4 * IN, 0.95 * IN, 22, fill=1)
text(fx + 5.2 * IN, 0.98 * IN + BLEED, "65+ fun activities", 27)
text(fx + 5.2 * IN, 0.65 * IN + BLEED, "with answers in the back", 18, "H")
c.setLineWidth(2.5)
for x, y, r, col in ((0.75, 6.2, .26, YEL), (7.8, 6.3, .24, PINK), (0.65, 8.3, .18, white), (7.9, 8.6, .2, YEL)):
    star(c, fx + x * IN, y * IN, r * IN, col)

# ---------------- back ----------------
bx = BLEED
bcx = bx + TW / 2
c.setFillColor(white)
c.setLineWidth(4)
c.roundRect(bx + 0.85 * IN, 3.9 * IN, TW - 1.7 * IN, 6.3 * IN, 30, fill=1)
text(bcx, 9.45 * IN, "Hours of happy,", 34, fill=ORG)
text(bcx, 8.95 * IN, "screen-free fun!", 34, fill=ORG)
lines = ["Join Benny the bear, Bella the bunny and", "their friends for 65+ activities that get", "a little trickier as you go:", ""]
feats = ["12 mazes and 8 word searches", "Color by number and dot to dots", "Shape sudoku and number sudoku",
         "Secret code jokes to crack", "Counting, matching and patterns", "Coloring pages and games to play",
         "A Super Star Award at the end!"]
y = 8.4 * IN
for ln in lines:
    text(bcx, y, ln, 19, "H")
    y -= 0.33 * IN
y += 0.12 * IN
for f in feats:
    c.setLineWidth(1.5)
    star(c, bx + 2.0 * IN, y + 0.08 * IN, 0.12 * IN, YEL)
    text(bx + 2.3 * IN, y, f, 20, "H", align="l")
    y -= 0.4 * IN
for i, k in enumerate(["mouse", "bear", "bunny"]):
    face(c, k, bx + 1.6 * IN + i * 1.75 * IN, 2.7 * IN, 0.62 * IN, color=True, mood="happy" if i == 1 else "smile")
for i, s in enumerate(["cheese", "honey", "carrot"]):
    item(c, s, bx + 2.45 * IN + i * 1.75 * IN, 2.25 * IN, 0.22 * IN, color=True)
c.setLineWidth(2.5)
star(c, bx + 0.95 * IN, 10.3 * IN, 0.36 * IN, YEL)
heart(c, bx + 7.55 * IN, 3.95 * IN, 0.26 * IN, PINK)
c.save()
print("cover inches: %.3f x %.3f, spine %.3f" % (W / IN, H / IN, SPINE / IN))
