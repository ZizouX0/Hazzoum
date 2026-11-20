"""Generates a kids' activity book interior (mazes, word searches, sudoku) as a
print-ready 8.5 x 11 in PDF for Amazon KDP, with an answer key at the back."""
import random
from collections import deque
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

random.seed(2026)
pdfmetrics.registerFont(TTFont("B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("R", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
W, H = letter
TITLE = "Fun Activity Book for Kids"
SUB = "Mazes, Word Searches and Sudoku  •  Ages 6-8"


# ---------- mazes ----------
def make_maze(n, m):
    """Walls as sets of open passages between cells; depth-first carve."""
    open_ = set()
    seen = {(0, 0)}
    stack = [(0, 0)]
    while stack:
        x, y = stack[-1]
        nb = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
              if 0 <= x + dx < n and 0 <= y + dy < m and (x + dx, y + dy) not in seen]
        if not nb:
            stack.pop()
            continue
        c = random.choice(nb)
        open_.add(frozenset(((x, y), c)))
        seen.add(c)
        stack.append(c)
    prev = {(0, 0): None}
    q = deque([(0, 0)])
    while q:
        cur = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            c = (cur[0] + dx, cur[1] + dy)
            if c not in prev and frozenset((cur, c)) in open_:
                prev[c] = cur
                q.append(c)
    path, cur = [], (n - 1, m - 1)
    while cur:
        path.append(cur)
        cur = prev[cur]
    return {"n": n, "m": m, "open": open_, "path": path[::-1]}


def draw_maze(c, mz, x0, y0, size, solved=False, lw=3):
    n, m = mz["n"], mz["m"]
    s = size / max(n, m)
    x0 += (size - s * n) / 2
    top = y0 + s * m  # row 0 at the top
    c.setLineWidth(lw)
    c.setLineCap(1)
    c.setStrokeGray(0)
    for x in range(n):
        for y in range(m):
            if y == 0 and x != 0:
                c.line(x0 + x * s, top, x0 + (x + 1) * s, top)
            if x == 0:
                c.line(x0, top - y * s, x0, top - (y + 1) * s)
            if frozenset(((x, y), (x + 1, y))) not in mz["open"]:
                c.line(x0 + (x + 1) * s, top - y * s, x0 + (x + 1) * s, top - (y + 1) * s)
            if frozenset(((x, y), (x, y + 1))) not in mz["open"] and not (y == m - 1 and x == n - 1):
                c.line(x0 + x * s, top - (y + 1) * s, x0 + (x + 1) * s, top - (y + 1) * s)
    if solved:
        c.setStrokeGray(0.55)
        c.setLineWidth(max(1.2, s * 0.25))
        p = c.beginPath()
        pts = [(x0 + (x + .5) * s, top - (y + .5) * s) for x, y in mz["path"]]
        p.moveTo(pts[0][0], top + s * .2)
        for pt in pts:
            p.lineTo(*pt)
        p.lineTo(pts[-1][0], y0 - s * .2)
        c.drawPath(p)
        c.setStrokeGray(0)
    return x0, top, s


# ---------- word searches ----------
THEMES = [
    ("Farm Animals", "COW PIG HEN DUCK GOAT SHEEP HORSE DONKEY"),
    ("Fruit", "APPLE PEAR PLUM GRAPE LEMON MANGO PEACH CHERRY"),
    ("Colors", "RED BLUE PINK GREEN BROWN WHITE YELLOW PURPLE"),
    ("Pets", "CAT DOG FISH BIRD BUNNY PUPPY KITTEN HAMSTER"),
    ("Weather", "SUN RAIN WIND SNOW CLOUD STORM FOGGY RAINBOW"),
    ("At School", "PEN BOOK DESK GLUE CHALK PAPER PENCIL TEACHER"),
    ("Ocean", "CRAB FISH SEAL WHALE SHARK SHELL TURTLE DOLPHIN"),
    ("Space", "SUN MOON STAR MARS EARTH COMET ROCKET PLANET"),
    ("Bugs", "ANT BEE FLY MOTH WORM SNAIL BEETLE SPIDER"),
    ("Things That Go", "CAR BUS BIKE BOAT TRAIN TRUCK PLANE ROCKET SCOOTER"),
    ("Zoo", "LION BEAR ZEBRA TIGER PANDA KOALA MONKEY GIRAFFE HIPPO"),
    ("Dinosaurs", "EGG CLAW TAIL BONE HORN ROAR FOSSIL RAPTOR GIANT"),
    ("Sports", "RUN SWIM JUMP KICK GOAL TEAM TENNIS SOCCER HOCKEY"),
    ("Yummy Food", "EGG RICE SOUP CAKE PIZZA BREAD PASTA CHEESE COOKIE"),
    ("In the Garden", "BUD SEED LEAF ROOT TREE GRASS FLOWER BUTTERFLY"),
]


def make_ws(words, n, diag):
    dirs = [(1, 0), (0, 1)] + ([(1, 1)] if diag else [])
    for _ in range(200):
        g = [[None] * n for _ in range(n)]
        placed = {}
        ok = True
        for w in sorted(words, key=len, reverse=True):
            for _ in range(400):
                dx, dy = random.choice(dirs)
                x = random.randrange(n - dx * (len(w) - 1))
                y = random.randrange(n - dy * (len(w) - 1))
                cells = [(x + dx * i, y + dy * i) for i in range(len(w))]
                if all(g[b][a] in (None, ch) for (a, b), ch in zip(cells, w)):
                    for (a, b), ch in zip(cells, w):
                        g[b][a] = ch
                    placed[w] = cells
                    break
            else:
                ok = False
                break
        if ok:
            for r in g:
                for i, v in enumerate(r):
                    if v is None:
                        r[i] = random.choice("ABCDEFGHIKLMNOPRSTUWY")
            return {"g": g, "placed": placed, "n": n, "words": words}
    raise RuntimeError("could not place words")


def draw_ws(c, ws, x0, y0, size, solved=False, lw=2.5):
    n = ws["n"]
    s = size / n
    top = y0 + size
    if solved:
        c.setFillGray(0.78)
        for cells in ws["placed"].values():
            for a, b in cells:
                c.rect(x0 + a * s, top - (b + 1) * s, s, s, stroke=0, fill=1)
        c.setFillGray(0)
    c.setLineWidth(lw)
    c.roundRect(x0, y0, size, size, s * 0.3)
    c.setFont("B", s * 0.58)
    for b, row in enumerate(ws["g"]):
        for a, ch in enumerate(row):
            c.drawCentredString(x0 + (a + .5) * s, top - (b + .5) * s - s * 0.2, ch)


# ---------- sudoku ----------
def make_sudoku(bw, bh, blanks):
    n = bw * bh

    def count(g, limit=2):
        for i in range(n * n):
            r, col = divmod(i, n)
            if g[r][col] == 0:
                tot = 0
                for v in range(1, n + 1):
                    br, bc = r - r % bh, col - col % bw
                    if (v not in g[r] and all(g[k][col] != v for k in range(n)) and
                            all(g[br + i2][bc + j2] != v for i2 in range(bh) for j2 in range(bw))):
                        g[r][col] = v
                        tot += count(g, limit - tot)
                        g[r][col] = 0
                        if tot >= limit:
                            break
                return tot
        return 1

    def fill(g):
        for i in range(n * n):
            r, col = divmod(i, n)
            if g[r][col] == 0:
                vals = list(range(1, n + 1))
                random.shuffle(vals)
                for v in vals:
                    br, bc = r - r % bh, col - col % bw
                    if (v not in g[r] and all(g[k][col] != v for k in range(n)) and
                            all(g[br + i2][bc + j2] != v for i2 in range(bh) for j2 in range(bw))):
                        g[r][col] = v
                        if fill(g):
                            return True
                        g[r][col] = 0
                return False
        return True

    sol = [[0] * n for _ in range(n)]
    fill(sol)
    puz = [r[:] for r in sol]
    cells = [(r, c2) for r in range(n) for c2 in range(n)]
    random.shuffle(cells)
    removed = 0
    for r, c2 in cells:
        if removed >= blanks:
            break
        keep = puz[r][c2]
        puz[r][c2] = 0
        if count([row[:] for row in puz]) == 1:
            removed += 1
        else:
            puz[r][c2] = keep
    return {"puz": puz, "sol": sol, "bw": bw, "bh": bh, "n": n}


def draw_sudoku(c, sd, x0, y0, size, solved=False, lw=4):
    n, bw, bh = sd["n"], sd["bw"], sd["bh"]
    s = size / n
    top = y0 + size
    for i in range(n + 1):
        c.setLineWidth(lw if i % bw == 0 else lw * 0.3)
        c.line(x0 + i * s, y0, x0 + i * s, top)
        c.setLineWidth(lw if i % bh == 0 else lw * 0.3)
        c.line(x0, top - i * s, x0 + size, top - i * s)
    for r in range(n):
        for k in range(n):
            given = sd["puz"][r][k]
            if given or solved:
                c.setFont("B", s * 0.55)
                c.setFillGray(0 if given else 0.5)
                c.drawCentredString(x0 + (k + .5) * s, top - (r + .5) * s - s * 0.2, str(sd["sol"][r][k]))
    c.setFillGray(0)


# ---------- book ----------
puzzles = []
for i in range(20):
    n = 6 + i  # 6x6 up to 25x25
    puzzles.append(("maze", f"Maze {i + 1}", make_maze(n, n)))
for i, (name, words) in enumerate(THEMES):
    n = 9 if i < 5 else 10 if i < 10 else 11
    puzzles.append(("ws", f"Word Search {i + 1}: {name}", make_ws(words.split(), n, diag=i >= 8)))
for i in range(12):
    if i < 7:
        puzzles.append(("sd", f"Sudoku {i + 1}", make_sudoku(2, 2, 6 + i // 2)))
    else:
        puzzles.append(("sd", f"Sudoku {i + 1}", make_sudoku(3, 2, 14 + (i - 7) * 2)))

HINT = {
    "maze": "Help the star find the way out! Start at the top and finish at the bottom.",
    "ws": "Find and circle every word. Words go across, down{}.",
    "sd": "Fill every box so each row, column and thick-lined block has the numbers 1 to {} once.",
}

c = canvas.Canvas("activity-book-interior.pdf", pagesize=letter, initialFontName="R")
c.setTitle(TITLE)
c.setAuthor("")
page = [0]


def footer():
    page[0] += 1
    if page[0] > 2:
        c.setFont("R", 11)
        c.drawCentredString(W / 2, 0.45 * inch, str(page[0]))
    c.showPage()


def star(cx, cy, r):
    import math
    p = c.beginPath()
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        (p.moveTo if k == 0 else p.lineTo)(cx + rr * math.cos(a), cy + rr * math.sin(a))
    p.close()
    c.setLineWidth(2)
    c.drawPath(p)


# title page
c.setLineWidth(5)
c.roundRect(0.7 * inch, 0.7 * inch, W - 1.4 * inch, H - 1.4 * inch, 30)
c.setFont("B", 50)
for k, line in enumerate(["Fun", "Activity Book", "for Kids"]):
    c.drawCentredString(W / 2, H - 2.6 * inch - k * 0.85 * inch, line)
c.setFont("R", 19)
c.drawCentredString(W / 2, H - 5.3 * inch, "20 Mazes  •  15 Word Searches  •  12 Sudoku")
c.drawCentredString(W / 2, H - 5.75 * inch, "Ages 6-8  •  Answers in the back")
draw_maze(c, make_maze(7, 7), W / 2 - 1.4 * inch, 1.5 * inch, 2.8 * inch)
for sx in (1.9, 6.6):
    star(sx * inch, 2.9 * inch, 0.4 * inch)
footer()

# belongs-to page
c.setFont("B", 34)
c.drawCentredString(W / 2, H - 3.5 * inch, "This book belongs to")
c.setLineWidth(3)
c.line(1.7 * inch, H - 5 * inch, W - 1.7 * inch, H - 5 * inch)
star(W / 2, H - 6.8 * inch, 0.8 * inch)
c.setFont("R", 10)
c.drawCentredString(W / 2, 1.1 * inch, "Copyright © 2026. All rights reserved.")
c.drawCentredString(W / 2, 0.9 * inch, "No part of this book may be reproduced without written permission of the publisher.")
footer()

SIZE = 6.3 * inch
X0 = (W - SIZE) / 2 + 0.06 * inch  # nudge away from the binding edge
for kind, title, data in puzzles:
    c.setFont("B", 24)
    c.drawCentredString(W / 2, H - 1.0 * inch, title)
    c.setFont("R", 12.5)
    hint = HINT[kind]
    if kind == "ws":
        hint = hint.format(" and diagonally" if any(a != b and a2 != b2 for cells in data["placed"].values()
                                                    for (a, a2), (b, b2) in [(cells[0], cells[-1])]) else "")
    if kind == "sd":
        hint = hint.format(data["n"])
    c.drawCentredString(W / 2, H - 1.4 * inch, hint)
    if kind == "maze":
        y0 = H - 2.2 * inch - SIZE
        mx, top, s = draw_maze(c, data, X0, y0, SIZE, lw=max(2.2, 4.5 - data["n"] * 0.1))
        star(mx + s / 2, top + 0.28 * inch, 0.17 * inch)
        c.setFont("B", 13)
        c.drawString(mx + s / 2 + 0.28 * inch, top + 0.2 * inch, "START")
        c.drawRightString(mx + s * (data["n"] - 1) - 4, y0 - 0.32 * inch, "FINISH")
    elif kind == "ws":
        ws_size = 5.6 * inch
        y0 = H - 1.9 * inch - ws_size
        draw_ws(c, data, (W - ws_size) / 2 + 0.06 * inch, y0, ws_size)
        c.setFont("B", 16)
        words = data["words"]
        cols = 3
        for i, w in enumerate(words):
            col, row = i % cols, i // cols
            c.drawCentredString(W / 2 + (col - 1) * 2.1 * inch, y0 - 0.55 * inch - row * 0.42 * inch, w)
    else:
        sd_size = (4.8 if data["n"] == 4 else 5.8) * inch
        draw_sudoku(c, data, (W - sd_size) / 2 + 0.06 * inch, H - 2.3 * inch - sd_size, sd_size)
    footer()

# answer key: 6 per page
PER = 6
for start in range(0, len(puzzles), PER):
    c.setFont("B", 24)
    c.drawCentredString(W / 2, H - 0.95 * inch, "Answers")
    for i, (kind, title, data) in enumerate(puzzles[start:start + PER]):
        col, row = i % 2, i // 2
        sz = 2.45 * inch
        x = 1.25 * inch + col * 3.5 * inch
        y = H - 1.75 * inch - sz - row * 3.05 * inch
        c.setFont("B", 10.5)
        c.drawCentredString(x + sz / 2, y + sz + 0.14 * inch, title)
        if kind == "maze":
            draw_maze(c, data, x, y, sz, solved=True, lw=1)
        elif kind == "ws":
            draw_ws(c, data, x, y, sz, solved=True, lw=1)
        else:
            draw_sudoku(c, data, x, y, sz, solved=True, lw=2)
    footer()
if page[0] % 2:
    footer()
c.save()
print("pages:", page[0])
