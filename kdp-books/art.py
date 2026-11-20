"""Cartoon art drawn with plain vector shapes: ten animal friends, their snacks
and a few simple shapes. Everything is white-filled with bold outlines so it can
be colored in; pass color=True for the full-color cover versions."""
import math
import os
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
pdfmetrics.registerFont(TTFont("T", os.path.join(HERE, "fonts", "LilitaOne-Regular.ttf")))
pdfmetrics.registerFont(TTFont("H", os.path.join(HERE, "fonts", "PatrickHand-Regular.ttf")))

FRIENDS = [  # kind, name, snack
    ("bear", "Benny", "honey"), ("bunny", "Bella", "carrot"), ("cat", "Coco", "fish"),
    ("frog", "Freddy", "bug"), ("pig", "Penny", "apple"), ("panda", "Pip", "bamboo"),
    ("chick", "Chip", "worm"), ("mouse", "Milo", "cheese"), ("lion", "Leo", "crown"),
    ("dog", "Daisy", "bone"),
]
NAME = {k: n for k, n, _ in FRIENDS}
SNACK = {k: s for k, _, s in FRIENDS}
SNACK_WORD = {"honey": "honey", "carrot": "carrot", "fish": "fish", "bug": "bug", "apple": "apple",
              "bamboo": "bamboo", "worm": "worm", "cheese": "cheese", "crown": "crown", "bone": "bone"}
BODY = {"bear": "#C98F5E", "bunny": "#FFFFFF", "cat": "#F7A94B", "frog": "#77CC6D", "pig": "#FBB1C8",
        "panda": "#FFFFFF", "chick": "#FFDB4D", "mouse": "#C3C8D1", "lion": "#F8C04E", "dog": "#E3BE94"}
PINK = HexColor("#FF9DB5")


def _f(color, hexv):
    return HexColor(hexv) if color else white


def ell(c, cx, cy, rx, ry, fill=white, rot=0, stroke=1):
    c.saveState()
    c.translate(cx, cy)
    c.rotate(rot)
    c.setFillColor(fill)
    c.ellipse(-rx, -ry, rx, ry, stroke=stroke, fill=1)
    c.restoreState()


def poly(c, pts, fill=white, close=True, stroke=1, dofill=1):
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    if close:
        p.close()
    c.setFillColor(fill)
    c.drawPath(p, stroke=stroke, fill=dofill if close else 0)


def smile(c, cx, cy, w, depth):
    """A U-shaped curve from (cx-w, cy) to (cx+w, cy) dipping by depth."""
    c.bezier(cx - w, cy, cx - w * 0.5, cy - depth * 1.33, cx + w * 0.5, cy - depth * 1.33, cx + w, cy)


def face(c, kind, cx, cy, r, color=False, wink=False, mood="smile", half=False, tongue=False):
    """Draw one friend's head, roughly inside a circle of radius r (ears may poke out)."""
    c.saveState()
    if half:
        p = c.beginPath()
        p.rect(cx - 3 * r, cy - 3 * r, 3 * r, 6 * r)
        c.clipPath(p, stroke=0, fill=0)
    c.translate(cx, cy)
    lw = max(1.1, r * 0.075)
    c.setLineWidth(lw)
    c.setLineJoin(1)
    c.setLineCap(1)
    c.setStrokeColor(black)
    body = _f(color, BODY[kind])
    inner = PINK if color else white
    hs = 1.0
    # ---- ears and things behind the head
    if kind == "bear":
        for s in (-1, 1):
            ell(c, s * 0.7 * r, 0.66 * r, 0.33 * r, 0.33 * r, body)
            ell(c, s * 0.7 * r, 0.66 * r, 0.16 * r, 0.16 * r, inner)
    elif kind == "bunny":
        for s in (-1, 1):
            ell(c, s * 0.4 * r, 1.2 * r, 0.22 * r, 0.66 * r, body, rot=-s * 8)
            ell(c, s * 0.4 * r, 1.2 * r, 0.1 * r, 0.45 * r, inner, rot=-s * 8)
    elif kind == "cat":
        for s in (-1, 1):
            poly(c, [(s * 0.93 * r, 0.25 * r), (s * 0.8 * r, 1.18 * r), (s * 0.2 * r, 0.8 * r)], body)
            poly(c, [(s * 0.78 * r, 0.55 * r), (s * 0.72 * r, 0.95 * r), (s * 0.45 * r, 0.78 * r)], inner)
    elif kind == "frog":
        for s in (-1, 1):
            ell(c, s * 0.5 * r, 0.72 * r, 0.37 * r, 0.37 * r, body)
    elif kind == "pig":
        for s in (-1, 1):
            poly(c, [(s * 0.9 * r, 0.35 * r), (s * 0.82 * r, 1.05 * r), (s * 0.3 * r, 0.8 * r)], body)
    elif kind == "panda":
        for s in (-1, 1):
            ell(c, s * 0.7 * r, 0.68 * r, 0.32 * r, 0.32 * r, black)
    elif kind == "chick":
        for dx, rot in ((-0.16, 25), (0, 0), (0.16, -25)):
            ell(c, dx * r, 0.98 * r, 0.09 * r, 0.22 * r, body, rot=rot)
    elif kind == "mouse":
        for s in (-1, 1):
            ell(c, s * 0.8 * r, 0.7 * r, 0.48 * r, 0.48 * r, body)
            ell(c, s * 0.8 * r, 0.7 * r, 0.28 * r, 0.28 * r, inner)
    elif kind == "lion":
        mane = _f(color, "#E0762B")
        for k in range(12):
            a = k * math.pi / 6
            ell(c, 0.86 * r * math.cos(a), 0.86 * r * math.sin(a), 0.3 * r, 0.3 * r, mane)
        hs = 0.8
        for s in (-1, 1):
            ell(c, s * 0.56 * r, 0.58 * r, 0.2 * r, 0.2 * r, body)
    elif kind == "dog":
        for s in (-1, 1):
            ell(c, s * 0.95 * r, 0.12 * r, 0.27 * r, 0.62 * r, _f(color, "#8A5A33"), rot=s * 14)
    # ---- head
    R = r * hs
    ell(c, 0, 0, R, R * 0.9, body)
    ey, ex = 0.12 * R, 0.38 * R
    # ---- kind-specific face parts
    nose_y = -0.16 * R
    if kind == "panda":
        for s in (-1, 1):
            ell(c, s * ex, ey - 0.02 * R, 0.2 * R, 0.26 * R, black, rot=s * 20)
    if kind in ("bear", "dog", "lion", "panda"):
        ell(c, 0, -0.3 * R, 0.4 * R, 0.3 * R, white)
    if kind == "frog":
        ey, ex = 0.74 * r, 0.5 * r
        for s in (-1, 1):
            ell(c, s * ex, ey, 0.24 * r, 0.24 * r, white)
    # ---- eyes
    er = 0.095 * R
    for s in (-1, 1):
        if mood == "happy" or (wink and s == 1):
            c.setLineWidth(lw)
            c.setStrokeColor(white if kind == "panda" else black)
            smile(c, s * ex, ey - er * 0.6, er * 1.5, -er * 1.6)
            c.setStrokeColor(black)
        else:
            ell(c, s * ex, ey, er, er, black)
            ell(c, s * ex + er * 0.35, ey + er * 0.35, er * 0.33, er * 0.33, white, stroke=0)
    # ---- blush
    if kind != "frog":
        c.setLineWidth(lw * 0.5)
        for s in (-1, 1):
            ell(c, s * 0.63 * R, -0.2 * R, 0.13 * R, 0.08 * R, PINK if color else white)
        c.setLineWidth(lw)
    # ---- nose and mouth
    if kind == "chick":
        poly(c, [(-0.17 * R, -0.12 * R), (0, 0.0), (0.17 * R, -0.12 * R), (0, -0.3 * R)], _f(color, "#FF8A2A"))
    elif kind == "frog":
        for s in (-1, 1):
            ell(c, s * 0.08 * R, 0.1 * R, 0.02 * R, 0.02 * R, black)
        smile(c, 0, -0.12 * R, 0.55 * R, 0.3 * R)
    elif kind == "pig":
        ell(c, 0, -0.22 * R, 0.33 * R, 0.24 * R, _f(color, "#F78DAA"))
        for s in (-1, 1):
            ell(c, s * 0.12 * R, -0.22 * R, 0.05 * R, 0.08 * R, black)
        smile(c, 0, -0.56 * R, 0.16 * R, 0.1 * R)
    else:
        nfill = black if kind in ("bear", "dog", "panda", "lion") else (PINK if color else black)
        if kind in ("cat", "bunny", "mouse"):
            poly(c, [(-0.09 * R, nose_y), (0.09 * R, nose_y), (0, nose_y - 0.1 * R)], nfill)
            my = nose_y - 0.1 * R
        else:
            ell(c, 0, nose_y - 0.02 * R, 0.13 * R, 0.09 * R, nfill)
            my = nose_y - 0.11 * R
        c.line(0, my, 0, my - 0.08 * R)
        smile(c, -0.14 * R, my - 0.08 * R, 0.14 * R, 0.11 * R)
        smile(c, 0.14 * R, my - 0.08 * R, 0.14 * R, 0.11 * R)
        if tongue or kind == "dog":
            p = c.beginPath()
            p.moveTo(-0.08 * R, my - 0.17 * R)
            p.curveTo(-0.1 * R, my - 0.42 * R, 0.1 * R, my - 0.42 * R, 0.08 * R, my - 0.17 * R)
            c.setFillColor(PINK if color else white)
            c.drawPath(p, fill=1)
        if kind in ("bunny", "mouse"):
            c.setFillColor(white)
            c.rect(-0.07 * R, my - 0.3 * R, 0.07 * R, 0.13 * R, fill=1)
            c.rect(0, my - 0.3 * R, 0.07 * R, 0.13 * R, fill=1)
        if kind in ("cat", "mouse"):
            c.setLineWidth(lw * 0.6)
            for s in (-1, 1):
                c.line(s * 0.5 * R, -0.26 * R, s * 1.05 * R, -0.18 * R)
                c.line(s * 0.5 * R, -0.36 * R, s * 1.05 * R, -0.44 * R)
    c.restoreState()


def item(c, kind, cx, cy, s, color=False):
    """Draw a snack or prop roughly inside a box of half-size s."""
    c.saveState()
    c.translate(cx, cy)
    c.setLineWidth(max(1.0, s * 0.09))
    c.setLineJoin(1)
    c.setLineCap(1)
    c.setStrokeColor(black)
    if kind == "carrot":
        for rot in (-28, 0, 28):
            ell(c, 0.3 * s * math.sin(math.radians(-rot)), 0.78 * s, 0.11 * s, 0.3 * s, _f(color, "#5DBB63"), rot=rot)
        p = c.beginPath()
        p.moveTo(-0.38 * s, 0.5 * s)
        p.curveTo(-0.38 * s, 0.75 * s, 0.38 * s, 0.75 * s, 0.38 * s, 0.5 * s)
        p.lineTo(0, -1.0 * s)
        p.close()
        c.setFillColor(_f(color, "#FF8A2A"))
        c.drawPath(p, fill=1)
        c.line(-0.2 * s, 0.25 * s, 0.0, 0.2 * s)
        c.line(0.02 * s, -0.15 * s, 0.17 * s, -0.1 * s)
    elif kind == "honey":
        c.setFillColor(_f(color, "#FFC93C"))
        c.roundRect(-0.7 * s, -0.9 * s, 1.4 * s, 1.45 * s, 0.35 * s, fill=1)
        c.setFillColor(_f(color, "#C98F5E"))
        c.roundRect(-0.8 * s, 0.5 * s, 1.6 * s, 0.32 * s, 0.1 * s, fill=1)
        c.setFillColor(white)
        c.roundRect(-0.42 * s, -0.5 * s, 0.84 * s, 0.6 * s, 0.1 * s, fill=1)
        heart(c, 0, -0.2 * s, 0.2 * s, PINK if color else white)
    elif kind == "fish":
        poly(c, [(0.45 * s, 0), (1.0 * s, 0.5 * s), (1.0 * s, -0.5 * s)], _f(color, "#FFDB4D"))
        ell(c, -0.15 * s, 0, 0.8 * s, 0.52 * s, _f(color, "#5BB8F5"))
        ell(c, -0.55 * s, 0.12 * s, 0.09 * s, 0.09 * s, black)
        c.arc(-0.35 * s, -0.4 * s, 0.25 * s, 0.4 * s, -60, 120)
    elif kind == "bug":
        for sx in (-1, 1):
            ell(c, sx * 0.42 * s, 0.38 * s, 0.4 * s, 0.26 * s, _f(color, "#BFE9FF"), rot=sx * 25)
        ell(c, 0, -0.1 * s, 0.45 * s, 0.62 * s, _f(color, "#FF5C5C"))
        c.line(-0.4 * s, 0, 0.4 * s, 0)
        c.line(-0.44 * s, -0.25 * s, 0.44 * s, -0.25 * s)
        ell(c, 0, 0.5 * s, 0.26 * s, 0.2 * s, black)
    elif kind == "apple":
        ell(c, 0, -0.1 * s, 0.8 * s, 0.75 * s, _f(color, "#F0483E"))
        c.line(0, 0.5 * s, 0.08 * s, 0.95 * s)
        ell(c, 0.4 * s, 0.82 * s, 0.3 * s, 0.14 * s, _f(color, "#5DBB63"), rot=25)
    elif kind == "bamboo":
        for i in range(3):
            c.setFillColor(_f(color, "#7ED37A"))
            c.roundRect(-0.2 * s, -1.0 * s + i * 0.62 * s, 0.4 * s, 0.6 * s, 0.08 * s, fill=1)
        ell(c, 0.5 * s, 0.5 * s, 0.34 * s, 0.13 * s, _f(color, "#4FB04C"), rot=30)
        ell(c, -0.5 * s, 0.05 * s, 0.34 * s, 0.13 * s, _f(color, "#4FB04C"), rot=150)
    elif kind == "worm":
        for i in range(5):
            ell(c, (-0.75 + i * 0.36) * s, (0.16 if i % 2 else -0.1) * s, 0.26 * s, 0.26 * s, _f(color, "#F7A1B5"))
        ell(c, 0.72 * s, -0.02 * s, 0.05 * s, 0.05 * s, black)
    elif kind == "cheese":
        poly(c, [(-0.9 * s, -0.55 * s), (0.9 * s, -0.55 * s), (0.9 * s, 0.1 * s), (-0.2 * s, 0.7 * s), (-0.9 * s, 0.1 * s)],
             _f(color, "#FFD23F"))
        c.line(-0.9 * s, 0.1 * s, 0.9 * s, 0.1 * s)
        for hx, hy, hr in ((-0.45, -0.25, 0.14), (0.25, -0.2, 0.18), (0.6, -0.4, 0.08), (-0.1, 0.35, 0.1)):
            ell(c, hx * s, hy * s, hr * s, hr * s, _f(color, "#F2B705"))
    elif kind == "crown":
        poly(c, [(-0.85 * s, -0.55 * s), (-0.95 * s, 0.5 * s), (-0.45 * s, 0.0), (0, 0.75 * s), (0.45 * s, 0.0),
                 (0.95 * s, 0.5 * s), (0.85 * s, -0.55 * s)], _f(color, "#FFD23F"))
        for dx in (-0.45, 0, 0.45):
            ell(c, dx * s, -0.3 * s, 0.1 * s, 0.1 * s, _f(color, "#F0483E"))
    elif kind == "bone":
        c.setFillColor(white)
        for sx in (-1, 1):
            for sy in (-1, 1):
                ell(c, sx * 0.7 * s, sy * 0.2 * s, 0.25 * s, 0.25 * s, white)
        c.rect(-0.7 * s, -0.2 * s, 1.4 * s, 0.4 * s, stroke=0, fill=1)
        c.line(-0.62 * s, 0.2 * s, 0.62 * s, 0.2 * s)
        c.line(-0.62 * s, -0.2 * s, 0.62 * s, -0.2 * s)
    c.restoreState()


def star(c, cx, cy, r, fill=white, lw=None):
    pts = []
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.46
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    if lw:
        c.setLineWidth(lw)
    c.setLineJoin(1)
    poly(c, pts, fill)


def heart(c, cx, cy, r, fill=white):
    p = c.beginPath()
    p.moveTo(cx, cy - r)
    p.curveTo(cx - 1.7 * r, cy + 0.1 * r, cx - 0.9 * r, cy + 1.35 * r, cx, cy + 0.5 * r)
    p.curveTo(cx + 0.9 * r, cy + 1.35 * r, cx + 1.7 * r, cy + 0.1 * r, cx, cy - r)
    p.close()
    c.setFillColor(fill)
    c.setLineJoin(1)
    c.drawPath(p, fill=1)


def shape(c, kind, cx, cy, r, fill=white):
    if kind == "star":
        star(c, cx, cy, r * 1.1, fill)
    elif kind == "heart":
        heart(c, cx, cy - 0.05 * r, r * 0.85, fill)
    elif kind == "circle":
        ell(c, cx, cy, r * 0.9, r * 0.9, fill)
    elif kind == "triangle":
        poly(c, [(cx - r, cy - 0.8 * r), (cx + r, cy - 0.8 * r), (cx, cy + 0.95 * r)], fill)
    elif kind == "square":
        c.setFillColor(fill)
        c.rect(cx - 0.85 * r, cy - 0.85 * r, 1.7 * r, 1.7 * r, fill=1)


def sun(c, cx, cy, r, color=False):
    c.setLineCap(1)
    for k in range(10):
        a = k * math.pi / 5
        c.line(cx + 1.25 * r * math.cos(a), cy + 1.25 * r * math.sin(a), cx + 1.7 * r * math.cos(a), cy + 1.7 * r * math.sin(a))
    ell(c, cx, cy, r, r, _f(color, "#FFD23F"))
    for s in (-1, 1):
        ell(c, cx + s * 0.35 * r, cy + 0.15 * r, 0.09 * r, 0.09 * r, black)
    smile(c, cx, cy - 0.2 * r, 0.35 * r, 0.25 * r)


def cloud(c, cx, cy, r):
    parts = ((-0.9, 0, 0.6), (-0.2, 0.35, 0.8), (0.7, 0.1, 0.65), (0, -0.2, 0.7))
    c.setFillColor(white)
    for dx, dy, rr in parts:
        c.circle(cx + dx * r, cy + dy * r, rr * r, stroke=1, fill=0)
    for dx, dy, rr in parts:
        c.circle(cx + dx * r, cy + dy * r, rr * r - c._lineWidth / 2, stroke=0, fill=1)


def flower(c, cx, cy, r, color=False):
    c.line(cx, cy, cx, cy - 2.6 * r)
    ell(c, cx + 0.5 * r, cy - 1.7 * r, 0.5 * r, 0.2 * r, _f(color, "#5DBB63"), rot=30)
    for k in range(6):
        a = k * math.pi / 3
        ell(c, cx + 0.75 * r * math.cos(a), cy + 0.75 * r * math.sin(a), 0.45 * r, 0.45 * r, _f(color, "#FF9DB5"))
    ell(c, cx, cy, 0.42 * r, 0.42 * r, _f(color, "#FFD23F"))
