"""Builds "My Big Fun Activity Book" (ages 4-8): a print-ready 8.5 x 11 in KDP
interior starring ten cartoon animal friends, with 13 kinds of activities and
an answer key. Run: python3 make_fun_book.py"""
import math
import random
from collections import deque
from reportlab.lib.colors import white, black, Color
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from art import (FRIENDS, NAME, SNACK, face, item, star, heart, shape, sun, cloud, flower, ell, poly, smile)

random.seed(11)
W, H = letter
IN = inch
GRAY = Color(0.6, 0.6, 0.6)
KINDS = [k for k, _, _ in FRIENDS]
SHAPES = ["star", "heart", "circle", "triangle"]


# ====================== puzzle generators ======================
def make_maze(n):
    open_, seen, stack = set(), {(0, 0)}, [(0, 0)]
    while stack:
        x, y = stack[-1]
        nb = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
              if 0 <= x + dx < n and 0 <= y + dy < n and (x + dx, y + dy) not in seen]
        if not nb:
            stack.pop()
            continue
        nx = random.choice(nb)
        open_.add(frozenset(((x, y), nx)))
        seen.add(nx)
        stack.append(nx)
    prev, q = {(0, 0): None}, deque([(0, 0)])
    while q:
        cur = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx = (cur[0] + dx, cur[1] + dy)
            if nx not in prev and frozenset((cur, nx)) in open_:
                prev[nx] = cur
                q.append(nx)
    path, cur = [], (n - 1, n - 1)
    while cur:
        path.append(cur)
        cur = prev[cur]
    return {"n": n, "open": open_, "path": path[::-1]}


def make_ws(words, n, diag):
    dirs = [(1, 0), (0, 1)] + ([(1, 1)] if diag else [])
    for _ in range(300):
        g, placed, ok = [[None] * n for _ in range(n)], {}, True
        for w in sorted(words, key=len, reverse=True):
            for _ in range(400):
                dx, dy = random.choice(dirs)
                x, y = random.randrange(n - dx * (len(w) - 1)), random.randrange(n - dy * (len(w) - 1))
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
            return {"g": g, "placed": placed, "n": n, "words": words, "diag": diag}
    raise RuntimeError("could not place words")


def make_sudoku(bw, bh, blanks):
    n = bw * bh

    def ok(g, r, k, v):
        br, bc = r - r % bh, k - k % bw
        return (v not in g[r] and all(g[i][k] != v for i in range(n)) and
                all(g[br + i][bc + j] != v for i in range(bh) for j in range(bw)))

    def count(g, limit=2):
        for i in range(n * n):
            r, k = divmod(i, n)
            if g[r][k] == 0:
                tot = 0
                for v in range(1, n + 1):
                    if ok(g, r, k, v):
                        g[r][k] = v
                        tot += count(g, limit - tot)
                        g[r][k] = 0
                        if tot >= limit:
                            break
                return tot
        return 1

    def fill(g):
        for i in range(n * n):
            r, k = divmod(i, n)
            if g[r][k] == 0:
                vals = list(range(1, n + 1))
                random.shuffle(vals)
                for v in vals:
                    if ok(g, r, k, v):
                        g[r][k] = v
                        if fill(g):
                            return True
                        g[r][k] = 0
                return False
        return True

    sol = [[0] * n for _ in range(n)]
    fill(sol)
    puz = [r[:] for r in sol]
    cells = [(r, k) for r in range(n) for k in range(n)]
    random.shuffle(cells)
    removed = 0
    for r, k in cells:
        if removed >= blanks:
            break
        keep, puz[r][k] = puz[r][k], 0
        if count([row[:] for row in puz]) == 1:
            removed += 1
        else:
            puz[r][k] = keep
    return {"puz": puz, "sol": sol, "bw": bw, "bh": bh, "n": n}


# ====================== drawing helpers ======================
c = canvas.Canvas("fun-activity-book-interior.pdf", pagesize=letter, initialFontName="H")
c.setTitle("My Big Fun Activity Book")
page = [0]
answers_thumb, answers_text = [], []


def text(x, y, s, size=16, font="H", align="c", fill=black):
    c.setFont(font, size)
    c.setFillColor(fill)
    {"c": c.drawCentredString, "l": c.drawString, "r": c.drawRightString}[align](x, y, s)


def finish(numbered=True, done_star=True):
    page[0] += 1
    if numbered:
        text(W / 2, 0.62 * IN, str(page[0]), 13)
    if done_star:
        text(W - 1.25 * IN, 0.66 * IN, "I did it!", 13, align="r")
        c.setStrokeColor(black)
        star(c, W - 0.95 * IN, 0.72 * IN, 0.17 * IN, white, lw=1.6)
    c.showPage()


def chrome(title, hint, kind=None, hint2=None):
    c.setStrokeColor(black)
    c.setLineWidth(2.5)
    c.roundRect(0.45 * IN, 0.45 * IN, W - 0.9 * IN, H - 0.9 * IN, 26)
    if kind:
        face(c, kind, 1.15 * IN, H - 1.2 * IN, 0.33 * IN)
    c.setLineWidth(1.6)
    star(c, W - 1.05 * IN, H - 1.05 * IN, 0.2 * IN)
    star(c, W - 0.85 * IN, H - 1.42 * IN, 0.11 * IN)
    text(W / 2, H - 1.22 * IN, title, 31, "T")
    text(W / 2, H - 1.62 * IN, hint, 17)
    if hint2:
        text(W / 2, H - 1.9 * IN, hint2, 17)


def draw_maze(mz, x0, y0, size, solved=False, lw=4):
    n = mz["n"]
    s = size / n
    top = y0 + size
    c.setLineWidth(lw)
    c.setLineCap(1)
    c.setStrokeColor(black)
    for x in range(n):
        for y in range(n):
            if y == 0 and x != 0:
                c.line(x0 + x * s, top, x0 + (x + 1) * s, top)
            if x == 0:
                c.line(x0, top - y * s, x0, top - (y + 1) * s)
            if frozenset(((x, y), (x + 1, y))) not in mz["open"]:
                c.line(x0 + (x + 1) * s, top - y * s, x0 + (x + 1) * s, top - (y + 1) * s)
            if frozenset(((x, y), (x, y + 1))) not in mz["open"] and not (y == n - 1 and x == n - 1):
                c.line(x0 + x * s, top - (y + 1) * s, x0 + (x + 1) * s, top - (y + 1) * s)
    if solved:
        c.setStrokeColor(GRAY)
        c.setLineWidth(max(1.2, s * 0.25))
        p = c.beginPath()
        pts = [(x0 + (x + .5) * s, top - (y + .5) * s) for x, y in mz["path"]]
        p.moveTo(pts[0][0], top)
        for pt in pts:
            p.lineTo(*pt)
        p.lineTo(pts[-1][0], y0)
        c.drawPath(p)
        c.setStrokeColor(black)
    return s


def draw_ws(ws, x0, y0, size, solved=False, lw=3):
    n = ws["n"]
    s = size / n
    top = y0 + size
    if solved:
        c.setFillColor(Color(.78, .78, .78))
        for cells in ws["placed"].values():
            for a, b in cells:
                c.rect(x0 + a * s, top - (b + 1) * s, s, s, stroke=0, fill=1)
    c.setLineWidth(lw)
    c.setStrokeColor(black)
    c.roundRect(x0, y0, size, size, s * 0.35)
    for b, row in enumerate(ws["g"]):
        for a, ch in enumerate(row):
            text(x0 + (a + .5) * s, top - (b + .5) * s - s * 0.2, ch, s * 0.58, "T")


def draw_sudoku(sd, x0, y0, size, solved=False, lw=4.5, shapes=False):
    n, bw, bh = sd["n"], sd["bw"], sd["bh"]
    s = size / n
    top = y0 + size
    c.setStrokeColor(black)
    c.setLineCap(1)
    for i in range(n + 1):
        c.setLineWidth(lw if i % bw == 0 else lw * 0.3)
        c.line(x0 + i * s, y0, x0 + i * s, top)
        c.setLineWidth(lw if i % bh == 0 else lw * 0.3)
        c.line(x0, top - i * s, x0 + size, top - i * s)
    for r in range(n):
        for k in range(n):
            given = sd["puz"][r][k]
            if not (given or solved):
                continue
            cx, cy = x0 + (k + .5) * s, top - (r + .5) * s
            if shapes:
                c.setLineWidth(max(1, s * 0.05))
                c.setStrokeColor(black if given else GRAY)
                shape(c, SHAPES[sd["sol"][r][k] - 1], cx, cy, s * 0.3)
                c.setStrokeColor(black)
            else:
                text(cx, cy - s * 0.2, str(sd["sol"][r][k]), s * 0.6, "T", fill=black if given else GRAY)


# ====================== activity pages ======================
def maze_page(num, n, kind):
    mz = make_maze(n)
    chrome(f"Maze {num}", f"Help {NAME[kind]} the {kind} get to the {SNACK[kind]}!", kind)
    size = 5.5 * IN
    x0, y0 = (W - size) / 2 + 0.05 * IN, 2.2 * IN
    s = draw_maze(mz, x0, y0, size, lw=max(2.6, 5.5 - n * 0.18))
    face(c, kind, x0 + s / 2, y0 + size + 0.5 * IN, 0.34 * IN)
    item(c, SNACK[kind], x0 + size - s / 2, y0 - 0.5 * IN, 0.33 * IN)
    finish()
    answers_thumb.append((f"Maze {num}", "maze", mz))


WS_THEMES = [
    ("On the Farm", "COW PIG HEN DUCK GOAT SHEEP", "pig"),
    ("Yummy Fruit", "APPLE PEAR PLUM GRAPE LEMON MANGO", "bear"),
    ("My Pets", "CAT DOG FISH BIRD BUNNY PUPPY KITTEN", "cat"),
    ("Rainbow Colors", "RED BLUE PINK GREEN BROWN YELLOW PURPLE", "chick"),
    ("Under the Sea", "CRAB FISH SEAL WHALE SHARK SHELL TURTLE", "frog"),
    ("Out in Space", "SUN MOON STAR MARS EARTH COMET ROCKET PLANET", "mouse"),
    ("At the Zoo", "LION BEAR ZEBRA TIGER PANDA KOALA MONKEY GIRAFFE", "lion"),
    ("Party Time", "CAKE GIFT GAME HATS DANCE CANDY FRIEND BALLOON", "dog"),
]


def ws_page(num):
    name, words, kind = WS_THEMES[num - 1]
    words = words.split()
    n = 8 if num <= 2 else 9 if num <= 5 else 10
    ws = make_ws(words, n, diag=num >= 6)
    chrome(f"Word Search: {name}", "Find and circle every word. Words go across" +
           (", down and diagonally." if ws["diag"] else " and down."), kind)
    size = 5.0 * IN
    y0 = H - 2.05 * IN - size
    draw_ws(ws, (W - size) / 2 + 0.05 * IN, y0, size)
    c.setLineWidth(2)
    c.setDash(6, 5)
    rows = math.ceil(len(words) / 4)
    bh_ = rows * 0.5 * IN + 0.35 * IN
    c.roundRect(1.2 * IN, y0 - 0.3 * IN - bh_, W - 2.4 * IN, bh_, 16)
    c.setDash()
    for i, w in enumerate(words):
        col, row = i % 4, i // 4
        text(W / 2 + 0.05 * IN + (col - 1.5) * 1.45 * IN, y0 - 0.85 * IN - row * 0.5 * IN, w, 21, "T")
    for i, k in enumerate(random.sample([k for k in KINDS if k != kind], 3)):
        face(c, k, W / 2 + (i - 1) * 1.6 * IN, (y0 - 0.3 * IN - bh_ + 0.75 * IN) / 2 + 0.1 * IN, 0.38 * IN, mood="happy" if i == 1 else "smile")
    finish()
    answers_thumb.append((f"Word Search: {name}", "ws", ws))


def sudoku_page(num, shapes, bw, bh, blanks, kind):
    sd = make_sudoku(bw, bh, blanks)
    n = bw * bh
    if shapes:
        chrome(f"Shape Sudoku {num}", "Draw the missing shapes. Every row, column and", kind,
               "thick box needs one of each shape.")
    else:
        chrome(f"Number Sudoku {num}", f"Write the missing numbers. Every row, column and", kind,
               f"thick box needs the numbers 1 to {n}.")
    size = (4.6 if n == 4 else 5.4) * IN
    y0 = H - 2.4 * IN - size
    draw_sudoku(sd, (W - size) / 2 + 0.05 * IN, y0, size, shapes=shapes)
    if shapes:
        c.setLineWidth(2.5)
        for i, sh in enumerate(SHAPES):
            shape(c, sh, W / 2 + (i - 1.5) * 1.1 * IN, y0 - 0.95 * IN, 0.3 * IN)
    else:
        for i, k in enumerate(random.sample(KINDS, 3)):
            face(c, k, W / 2 + (i - 1) * 1.5 * IN, y0 - 0.9 * IN, 0.4 * IN, mood="happy")
    finish()
    answers_thumb.append((("Shape" if shapes else "Number") + f" Sudoku {num}", "ssd" if shapes else "sd", sd))


def count_page(num, kinds, lo, hi):
    snacks = [SNACK[k] for k in kinds]
    chrome(f"Count the Snacks {num}", "How many of each can you find? Write the number in the box.", kinds[0])
    bx, by, bw_, bh_ = 0.95 * IN, 3.35 * IN, W - 1.9 * IN, 4.75 * IN
    c.setLineWidth(2.5)
    c.roundRect(bx, by, bw_, bh_, 20)
    counts = [random.randint(lo, hi) for _ in snacks]
    pts = []
    for si, n in enumerate(counts):
        for _ in range(n):
            for _ in range(2000):
                p = (random.uniform(bx + 0.5 * IN, bx + bw_ - 0.5 * IN), random.uniform(by + 0.5 * IN, by + bh_ - 0.5 * IN))
                if all(math.hypot(p[0] - q[0], p[1] - q[1]) > 0.84 * IN for q in pts):
                    pts.append(p)
                    item(c, snacks[si], p[0], p[1], 0.31 * IN)
                    break
            else:
                raise RuntimeError("no room")
    for i, sn in enumerate(snacks):
        x = W / 2 + (i - 1) * 2.2 * IN
        item(c, sn, x - 0.7 * IN, 2.3 * IN, 0.34 * IN)
        text(x - 0.12 * IN, 2.17 * IN, "=", 30, "T")
        c.setLineWidth(2.5)
        c.roundRect(x + 0.12 * IN, 1.85 * IN, 0.85 * IN, 0.9 * IN, 10)
    finish()
    answers_text.append(f"Count the Snacks {num}: " + ", ".join(f"{n} {s}" for n, s in zip(counts, snacks)))


def odd_page(num, mode):
    chrome(f"Odd One Out {num}", "One friend in each row is different. Circle it!", "frog")
    ans = []
    for row in range(5):
        kind = random.choice(KINDS)
        odd = random.randrange(5)
        m = mode if mode != "mix" else random.choice(["animal", "wink", "happy"])
        y = H - 2.75 * IN - row * 1.42 * IN
        text(1.0 * IN, y - 0.1 * IN, str(row + 1), 26, "T")
        for i in range(5):
            x = 1.85 * IN + i * 1.3 * IN
            if i == odd:
                if m == "animal":
                    face(c, random.choice([k for k in KINDS if k != kind]), x, y, 0.44 * IN)
                else:
                    face(c, kind, x, y, 0.44 * IN, wink=m == "wink", mood="happy" if m == "happy" else "smile")
            else:
                face(c, kind, x, y, 0.44 * IN)
        ans.append(f"row {row + 1} is number {odd + 1}")
    finish()
    answers_text.append(f"Odd One Out {num}: " + ", ".join(ans))


def match_page(num, kinds):
    chrome(f"Snack Time Match {num}", "Draw a line from each friend to the snack they love.", kinds[0])
    order = kinds[:]
    while any(a == b for a, b in zip(order, kinds)):
        random.shuffle(order)
    for i, k in enumerate(kinds):
        y = H - 2.8 * IN - i * 1.42 * IN
        face(c, k, 1.7 * IN, y, 0.48 * IN)
        text(2.4 * IN, y - 0.08 * IN, NAME[k], 20, align="l")
        item(c, SNACK[order[i]], 6.75 * IN, y, 0.4 * IN)
        c.setFillColor(black)
        c.circle(3.35 * IN, y, 5, fill=1)
        c.circle(5.8 * IN, y, 5, fill=1)
    finish()
    answers_text.append(f"Snack Time Match {num}: " + ", ".join(f"{NAME[k]} loves the {SNACK[k]}" for k in kinds))


def heart_grid():
    rows = []
    for j in range(11):
        row = ""
        for i in range(13):
            x, y = (i - 6) / 4.6, (5.2 - j) / 4.4
            v = (x * x + y * y - 1) ** 3 - x * x * y ** 3
            row += "2" if v < 0 else "."
        rows.append(row)
    rows[2] = rows[2][:3] + "3" + rows[2][4:]
    rows[3] = rows[3][:2] + "33" + rows[3][4:]
    return rows


CBN = [
    ("A Big Heart", heart_grid(), {"1": "light blue", "2": "red", "3": "pink"}, "bunny"),
    ("A Spotty Mushroom", ["....22222....", "..223222322..", ".22333223322.", ".22232222222.", "2222222322222",
                           "2222223332222", "2222222322222", "....44444....", "....44444....", "....44444....",
                           "...4444444..."], {"1": "green", "2": "red", "3": "white (leave it)", "4": "yellow"}, "mouse"),
    ("A Happy Fish", ["....222222.....", "..2222222222..3", ".22422222222.33", "222222222222333", "222222222222333",
                      ".22222222222.33", "..2222222222..3", "....222222....."],
     {"1": "blue", "2": "orange", "3": "yellow", "4": "black"}, "cat"),
    ("A Pretty Flower", ["...22.22...", "..2222222..", "..2233322..", "...23332...", "..2233322..", "..2222222..",
                         "...22522...", ".....5.....", ".55..5..55.", "..55.5.55..", "...55555...", ".....5....."],
     {"1": "yellow", "2": "pink", "3": "orange", "5": "green"}, "pig"),
    ("A Zooming Rocket", [".....2.....", "....222....", "...22222...", "...23332...", "...23332...", "...22222...",
                          "...22222...", "..4222224..", ".442222244.", ".44.222.44.", "....555....", "...55555...",
                          "....555....", ".....5....."],
     {"1": "dark blue", "2": "red", "3": "light blue", "4": "gray", "5": "orange"}, "panda"),
]


def cbn_page(num):
    name, rows, key, kind = CBN[num - 1]
    assert len({len(r) for r in rows}) == 1, name
    rows = ["." * (len(rows[0]) + 2)] + ["." + r + "." for r in rows] + ["." * (len(rows[0]) + 2)]
    chrome(f"Color by Number {num}", "Color each square using the key. What picture appears?", kind)
    nc, nr = len(rows[0]), len(rows)
    s = min(6.2 * IN / nc, 5.6 * IN / nr)
    x0, top = (W - s * nc) / 2 + 0.05 * IN, H - 2.05 * IN
    c.setLineWidth(1.2)
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            c.setFillColor(white)
            c.rect(x0 + i * s, top - (j + 1) * s, s, s, fill=1)
            text(x0 + (i + .5) * s, top - (j + .5) * s - s * 0.17, "1" if ch == "." else ch, s * 0.5)
    c.setLineWidth(3)
    c.rect(x0, top - nr * s, nc * s, nr * s)
    keys = sorted(key.items())
    ky = top - nr * s - 0.55 * IN
    per = 3
    for i, (k, v) in enumerate(keys):
        x = 1.2 * IN + (i % per) * 2.25 * IN
        y = ky - (i // per) * 0.5 * IN
        c.setLineWidth(2)
        c.rect(x, y - 0.08 * IN, 0.36 * IN, 0.36 * IN)
        text(x + 0.18 * IN, y, k, 17, "T")
        text(x + 0.5 * IN, y, "= " + v, 18, align="l")
    finish()
    answers_text.append(f"Color by Number {num}: the picture is {name[0].lower() + name[1:]}")


def dot_shapes():
    out = []
    pts = [((1 if k % 2 == 0 else .45) * math.cos(math.pi / 2 - k * math.pi / 5),
            (1 if k % 2 == 0 else .45) * math.sin(math.pi / 2 - k * math.pi / 5)) for k in range(10)]
    out.append(("a star", pts, "face", "chick"))
    pts = []
    for k in range(200):
        t = k * 2 * math.pi / 200
        pts.append((16 * math.sin(t) ** 3 / 17, (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) / 17 + 0.15))
    out.append(("a heart", resample(pts, 20), "face", "bunny"))
    pts = [(-0.15 + 0.8 * math.cos(math.radians(a)), 0.55 * math.sin(math.radians(a))) for a in range(42, 320, 23)]
    pts += [(1.0, -0.55), (0.72, 0.0), (1.0, 0.55)]
    out.append(("a fish", pts, "fish", "cat"))
    r = [(0, 1.0), (0.22, 0.72), (0.34, 0.4), (0.36, 0.0), (0.36, -0.35), (0.72, -0.75), (0.72, -1.0), (0.36, -0.8),
         (0.18, -0.8), (0, -1.05)]
    pts = r + [(-x, y) for x, y in r[-2:0:-1]]
    out.append(("a rocket", pts, "rocket", "panda"))
    pts = []
    for k in range(24):
        t = k * 2 * math.pi / 24
        rr = 0.72 + 0.28 * math.cos(6 * t)
        pts.append((rr * math.sin(t), rr * math.cos(t)))
    out.append(("a flower", pts, "face", "pig"))
    return out


def resample(pts, n):
    """n points evenly spaced along the closed outline through pts."""
    loop = pts + [pts[0]]
    seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(loop, loop[1:])]
    total, out, i, acc = sum(seg), [], 0, 0.0
    for k in range(n):
        d = k * total / n
        while acc + seg[i] < d:
            acc += seg[i]
            i += 1
        t = (d - acc) / seg[i]
        out.append((loop[i][0] + t * (loop[i + 1][0] - loop[i][0]), loop[i][1] + t * (loop[i + 1][1] - loop[i][1])))
    return out


DOTS = dot_shapes()


def dots_page(num):
    name, pts, extra, kind = DOTS[num - 1]
    chrome(f"Dot to Dot {num}", f"Join the dots from 1 to {len(pts)}, then back to 1.", kind, "What did you draw? Color it in!")
    R = 2.55 * IN
    cx, cy = W / 2 + 0.05 * IN, 4.55 * IN
    P = [(cx + x * R, cy + y * R) for x, y in pts]
    gx, gy = sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P)
    for i, (x, y) in enumerate(P):
        c.setFillColor(black)
        c.circle(x, y, 3.2, fill=1, stroke=0)
        d = math.hypot(x - gx, y - gy) or 1
        text(x + (x - gx) / d * 15, y + (y - gy) / d * 15 - 5, str(i + 1), 14)
    c.setLineWidth(3)
    c.setStrokeColor(black)
    c.setLineCap(1)
    if extra == "face":
        e = 0.2 * R
        for s in (-1, 1):
            ell(c, gx + s * e, gy + 0.05 * R, 0.045 * R, 0.045 * R, black)
        smile(c, gx, gy - 0.08 * R, 0.14 * R, 0.1 * R)
    elif extra == "fish":
        ell(c, cx - 0.55 * R, cy + 0.12 * R, 0.05 * R, 0.05 * R, black)
        smile(c, cx - 0.62 * R, cy - 0.12 * R, 0.12 * R, 0.08 * R)
    elif extra == "rocket":
        c.setFillColor(white)
        c.circle(cx, cy + 0.25 * R, 0.17 * R, fill=1)
        face(c, "mouse", cx, cy + 0.23 * R, 0.1 * R)
    finish()
    answers_text.append(f"Dot to Dot {num}: you drew {name}")


def pattern_page(num, patterns, blanks):
    chrome(f"What Comes Next? {num}", "Look at each pattern. Draw the shapes that come next.", "lion")
    names = SHAPES + ["square"]
    ans = []
    for row, pat in enumerate(patterns):
        sh = random.sample(names, len(set(pat)))
        seq = [sh["ABCD".index(pat[i % len(pat)])] for i in range(8)]
        y = H - 2.75 * IN - row * 1.42 * IN
        for i, s in enumerate(seq):
            x = 1.3 * IN + i * 0.85 * IN
            if i >= 8 - blanks:
                c.setLineWidth(2)
                c.setDash(5, 4)
                c.roundRect(x - 0.36 * IN, y - 0.36 * IN, 0.72 * IN, 0.72 * IN, 8)
                c.setDash()
            else:
                c.setLineWidth(2.6)
                shape(c, s, x, y, 0.27 * IN)
        ans.append(" then ".join(seq[8 - blanks:]))
    finish()
    answers_text.append(f"What Comes Next? {num}: " + "; ".join(f"row {i + 1}: {a}" for i, a in enumerate(ans)))


JOKES = [
    ("Why did the teddy bear say no to cake?", "SHE WAS STUFFED", "bear"),
    ("What is a cat's favorite color?", "PURRPLE", "cat"),
    ("What do you call a bear with no teeth?", "A GUMMY BEAR", "bear"),
    ("Why did the banana go to the doctor?", "IT WAS NOT PEELING WELL", "pig"),
    ("What do you call a sleeping dinosaur?", "A DINO SNORE", "frog"),
    ("How do bees get to school?", "ON THE SCHOOL BUZZ", "chick"),
    ("What do you call a dog magician?", "A LABRACADABRADOR", "dog"),
    ("Where do cows go on Friday night?", "TO THE MOOVIES", "lion"),
]


def code_page(num):
    chrome(f"Secret Code Jokes {num}", "Each number stands for a letter. Crack the code", "mouse", "to read the funny answer!")
    c.setLineWidth(1.6)
    cw = 0.5 * IN
    for i in range(26):
        x = (W - 13 * cw) / 2 + 0.05 * IN + (i % 13) * cw
        y = H - 2.75 * IN - (i // 13) * 0.82 * IN
        c.rect(x, y, cw, 0.36 * IN)
        c.rect(x, y - 0.36 * IN, cw, 0.36 * IN)
        text(x + cw / 2, y + 0.08 * IN, chr(65 + i), 19, "T")
        text(x + cw / 2, y - 0.28 * IN, str(i + 1), 15)
    y = H - 5.0 * IN
    for q, a, kind in JOKES[(num - 1) * 2:(num - 1) * 2 + 2]:
        face(c, kind, 1.25 * IN, y + 0.08 * IN, 0.3 * IN, mood="happy")
        text(1.75 * IN, y, q, 22, align="l")
        slot = 0.38 * IN
        lines, cur = [], []
        for w in a.split():
            if cur and sum(len(x) + 1 for x in cur) + len(w) > 17:
                lines.append(cur)
                cur = []
            cur.append(w)
        lines.append(cur)
        for li, ws_ in enumerate(lines):
            total = (sum(len(w) for w in ws_) + len(ws_) - 1) * slot
            x = (W - total) / 2 + 0.05 * IN
            yy = y - 0.95 * IN - li * 0.95 * IN
            for w in ws_:
                for ch in w:
                    c.setLineWidth(2.2)
                    c.line(x + 3, yy, x + slot - 3, yy)
                    text(x + slot / 2, yy - 0.25 * IN, str(ord(ch) - 64), 14)
                    x += slot
                x += slot
        y -= (1.3 + 0.95 * len(lines)) * IN
        answers_text.append(f"Joke: {q} {a.capitalize()}!")
    finish()


def ttt_page(num):
    chrome("Tic-Tac-Toe", "Grab a friend! One of you is X, the other is O.", "dog", "Three in a row wins.")
    c.setLineCap(1)
    for i in range(6):
        x0 = 1.25 * IN + (i % 2) * 3.4 * IN
        y0 = 1.25 * IN + (i // 2) * 2.55 * IN
        s = 0.72 * IN
        c.setLineWidth(4)
        for k in (1, 2):
            c.line(x0 + k * s, y0, x0 + k * s, y0 + 3 * s)
            c.line(x0, y0 + k * s, x0 + 3 * s, y0 + k * s)
    finish()


def boxes_page():
    chrome("Dots and Boxes", "Take turns drawing one line between two dots.", "dog",
           "Finish a box? Write your letter in it and go again!")
    for bi in range(2):
        for i in range(7):
            for j in range(5):
                c.setFillColor(black)
                c.circle(1.55 * IN + i * 0.92 * IN, 1.35 * IN + bi * 3.6 * IN + j * 0.68 * IN, 5, fill=1, stroke=0)
    finish()


def half_page(kind):
    chrome(f"Finish {NAME[kind]}!", f"Draw the other half of {NAME[kind]} the {kind}, then color.", None)
    cx, cy, r = W / 2 + 0.05 * IN, 4.6 * IN, 2.2 * IN
    face(c, kind, cx, cy, r, half=True)
    c.setLineWidth(1.5)
    c.setDash(7, 6)
    c.line(cx, cy - 1.35 * r, cx, cy + 1.45 * r)
    c.setDash()
    finish()


def color_page(kind, i):
    loves = {"honey": "honey", "carrot": "carrots", "fish": "fish", "bug": "bugs", "apple": "apples", "bamboo": "bamboo",
             "worm": "worms", "cheese": "cheese", "crown": "a shiny crown", "bone": "bones"}[SNACK[kind]]
    chrome(f"Color {NAME[kind]} the {kind.title()}!", f"{NAME[kind]} loves {loves}. Use your brightest colors!")
    c.setLineWidth(3)
    c.setLineCap(1)
    c.setStrokeColor(black)
    sun(c, 1.55 * IN, H - 2.75 * IN, 0.42 * IN)
    c.setLineWidth(3)
    cloud(c, 6.55 * IN, H - 2.7 * IN, 0.45 * IN)
    cloud(c, 4.3 * IN, H - 2.45 * IN, 0.3 * IN)
    c.setLineWidth(3)
    c.line(0.75 * IN, 1.75 * IN, W - 0.75 * IN, 1.75 * IN)
    for x in (1.3, 2.3, 6.3, 7.25):
        c.setLineWidth(2.5)
        flower(c, x * IN, 2.55 * IN + (0.25 * IN if int(x * 10) % 2 else 0), 0.2 * IN)
    face(c, kind, W / 2 + 0.05 * IN, 4.75 * IN, 1.85 * IN, mood="happy" if i % 2 and kind != "frog" else "smile")
    item(c, SNACK[kind], W / 2 + 0.05 * IN, 2.3 * IN, 0.45 * IN)
    finish()


# ====================== front pages ======================
c.setStrokeColor(black)
c.setLineWidth(5)
c.roundRect(0.6 * IN, 0.6 * IN, W - 1.2 * IN, H - 1.2 * IN, 34)
text(W / 2, H - 2.0 * IN, "My Big", 54, "T")
text(W / 2, H - 2.95 * IN, "FUN ACTIVITY", 62, "T")
text(W / 2, H - 3.8 * IN, "BOOK", 62, "T")
text(W / 2, H - 4.45 * IN, "Mazes • Puzzles • Coloring • Dot to Dots • Jokes", 20)
for i, k in enumerate(["bear", "bunny", "cat"]):
    face(c, k, W / 2 + (i - 1) * 2.1 * IN, 4.3 * IN, 0.78 * IN, mood="happy" if i == 1 else "smile")
for i, k in enumerate(["frog", "panda", "lion", "chick"]):
    face(c, k, W / 2 + (i - 1.5) * 1.65 * IN, 2.35 * IN, 0.6 * IN)
c.setLineWidth(2)
for x, y, r in ((1.2, 9.6, .2), (7.3, 9.7, .25), (1.3, 5.9, .16), (7.25, 6.0, .18)):
    star(c, x * IN, y * IN, r * IN)
text(W / 2, 1.05 * IN, "Ages 4-8", 24, "T")
finish(False, False)

c.setLineWidth(2.5)
c.roundRect(0.45 * IN, 0.45 * IN, W - 0.9 * IN, H - 0.9 * IN, 26)
text(W / 2, H - 2.6 * IN, "This book belongs to", 40, "T")
c.setLineWidth(3)
c.line(1.7 * IN, H - 4.0 * IN, W - 1.7 * IN, H - 4.0 * IN)
text(W / 2, H - 5.0 * IN, "I am ______ years old.", 26)
face(c, "dog", W / 2, 3.9 * IN, 1.0 * IN, mood="happy")
text(W / 2, 1.2 * IN, "Copyright © 2026. All rights reserved. No part of this book may be", 11)
text(W / 2, 1.02 * IN, "reproduced without written permission of the publisher.", 11)
finish(False, False)

chrome("Meet the Friends!", "They will help you on every page. Color them in!")
for i, (k, n, s) in enumerate(FRIENDS):
    x = 2.25 * IN + (i % 2) * 3.6 * IN
    y = H - 2.75 * IN - (i // 2) * 1.5 * IN
    face(c, k, x - 0.5 * IN, y, 0.5 * IN)
    text(x + 0.3 * IN, y + 0.05 * IN, n, 24, "T", align="l")
    text(x + 0.3 * IN, y - 0.3 * IN, f"the {k}", 17, align="l")
    item(c, s, x + 1.55 * IN, y - 0.05 * IN, 0.27 * IN)
finish(done_star=False)

# ====================== schedule ======================
Q = {
    "color": [lambda k=k, i=i: color_page(k, i) for i, k in enumerate(["bunny", "frog", "panda", "chick", "mouse", "lion", "dog"])],
    "maze": [lambda i=i: maze_page(i + 1, 5 + i, KINDS[i % 10]) for i in range(12)],
    "count": [lambda i=i: count_page(i + 1, random.sample(KINDS, 3), 2 + i, min(5 + i, 7)) for i in range(5)],
    "ws": [lambda i=i: ws_page(i + 1) for i in range(8)],
    "dots": [lambda i=i: dots_page(i + 1) for i in range(5)],
    "odd": [lambda i=i, m=m: odd_page(i + 1, m) for i, m in enumerate(["animal", "wink", "happy", "mix"])],
    "ssd": [lambda i=i: sudoku_page(i + 1, True, 2, 2, 5 + i, None) for i in range(4)],
    "cbn": [lambda i=i: cbn_page(i + 1) for i in range(5)],
    "pattern": [lambda: pattern_page(1, ["AB", "AAB", "ABB", "ABC", "AABB"], 2),
                lambda: pattern_page(2, ["ABC", "AABB", "ABAC", "ABBC", "ABCD"], 2),
                lambda: pattern_page(3, ["ABCD", "AABC", "ABCB", "ABBA", "AABBC"], 3)],
    "code": [lambda i=i: code_page(i + 1) for i in range(4)],
    "half": [lambda k=k: half_page(k) for k in ["bear", "cat", "pig"]],
    "match": [lambda: match_page(1, KINDS[:5]), lambda: match_page(2, KINDS[5:])],
    "nsd": [lambda: sudoku_page(1, False, 2, 2, 6, "bear"), lambda: sudoku_page(2, False, 2, 2, 8, "cat"),
            lambda: sudoku_page(3, False, 3, 2, 14, "lion"), lambda: sudoku_page(4, False, 3, 2, 18, "dog")],
    "ttt": [lambda: ttt_page(1), boxes_page],
}
ROUND = ["color", "maze", "ws", "count", "dots", "odd", "ssd", "maze", "cbn", "pattern", "ws", "code", "half", "match", "nsd", "ttt"]
while any(Q.values()):
    for t in ROUND:
        if Q[t]:
            Q[t].pop(0)()

# ====================== certificate and answers ======================
c.setLineWidth(6)
c.roundRect(0.55 * IN, 0.55 * IN, W - 1.1 * IN, H - 1.1 * IN, 30)
c.setLineWidth(2)
c.roundRect(0.72 * IN, 0.72 * IN, W - 1.44 * IN, H - 1.44 * IN, 22)
c.setLineWidth(3)
star(c, W / 2, H - 2.0 * IN, 0.6 * IN)
text(W / 2, H - 3.5 * IN, "SUPER STAR AWARD", 46, "T")
text(W / 2, H - 4.2 * IN, "This award goes to", 24)
c.setLineWidth(3)
c.line(1.8 * IN, H - 5.2 * IN, W - 1.8 * IN, H - 5.2 * IN)
text(W / 2, H - 5.9 * IN, "for finishing every puzzle in this book.", 24)
text(W / 2, H - 6.35 * IN, "You are amazing!", 24)
for i, k in enumerate(["bear", "bunny", "cat", "frog", "pig"]):
    face(c, k, W / 2 + (i - 2) * 1.3 * IN, 3.0 * IN, 0.5 * IN, mood="happy")
for i, k in enumerate(["panda", "chick", "mouse", "lion", "dog"]):
    face(c, k, W / 2 + (i - 2) * 1.3 * IN, 1.75 * IN, 0.5 * IN, mood="happy")
finish(False, False)

for start in range(0, len(answers_thumb), 6):
    chrome("Answers", "No peeking until you have tried your best!")
    for i, (title, kind, data) in enumerate(answers_thumb[start:start + 6]):
        sz = 2.2 * IN
        x = 1.45 * IN + (i % 2) * 3.4 * IN
        y = H - 2.35 * IN - sz - (i // 2) * 2.75 * IN
        text(x + sz / 2, y + sz + 0.1 * IN, title, 13)
        if kind == "maze":
            draw_maze(data, x, y, sz, solved=True, lw=1)
        elif kind == "ws":
            draw_ws(data, x, y, sz, solved=True, lw=1)
        else:
            draw_sudoku(data, x, y, sz, solved=True, lw=2, shapes=kind == "ssd")
    finish(done_star=False)

chrome("More Answers", "Here are the rest.")
y = H - 2.3 * IN
for line in answers_text:
    words, cur = line.split(), ""
    for w in words:
        if c.stringWidth(cur + " " + w, "H", 13.5) > W - 2.2 * IN:
            text(1.1 * IN, y, cur, 13.5, align="l")
            y -= 0.215 * IN
            cur = "    " + w
        else:
            cur = (cur + " " + w).strip() if cur.strip() else cur + w
    text(1.1 * IN, y, cur, 13.5, align="l")
    y -= 0.27 * IN
    if y < 1.1 * IN:
        finish(done_star=False)
        chrome("More Answers", "Here are the rest.")
        y = H - 2.3 * IN
finish(done_star=False)
if page[0] % 2:
    c.setLineWidth(2.5)
    c.roundRect(0.45 * IN, 0.45 * IN, W - 0.9 * IN, H - 0.9 * IN, 26)
    text(W / 2, H - 1.5 * IN, "My Own Drawing Page", 34, "T")
    text(W / 2, H - 1.95 * IN, "Draw your favorite friend from this book!", 18)
    finish(done_star=False)
c.save()
print("pages:", page[0])
