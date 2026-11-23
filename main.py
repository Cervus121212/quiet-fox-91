#!/usr/bin/env python3
"""THE WORLD TODAY - front page for Monday 23 November 2026.

Draws a newspaper front page (1024x1024 PNG) with 9 verified news
stories of 23 November 2026: 1 hero + 8 secondary stories.
Pure Python 3.13 standard library only (os, sys, struct, zlib, math).
No network, no PIL. Deterministic output.
"""

import os
import struct
import sys
import zlib

W = 1024
H = 1024

PAPER = (253, 248, 232)
INK = (20, 20, 20)
RED = (158, 28, 28)
NAVY = (24, 48, 88)

# ---------------------------------------------------------------- font
# Hand-written 5x7 bitmap glyphs. '#' = ink, '.' = empty.
# Only capitals, digits and punctuation are needed: all copy is upper case.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01111", "10000", "10000", "10111", "10001", "10001", "01110"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "01010", "00100", "00100", "00100", "01010", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    '3': ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00010", "00100", "00100", "00100"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "01100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "01100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '-': ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '/': ("00001", "00001", "00010", "00100", "01000", "10000", "10000"),
    '&': ("01100", "10010", "10010", "01000", "10101", "10010", "01101"),
    '%': ("10001", "10010", "00010", "00100", "01000", "01001", "10001"),
    '$': ("00100", "01111", "10101", "01110", "00101", "11110", "00100"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
}

# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def rect(self, x0, y0, x1, y1, color):
        for y in range(max(0, y0), min(self.h, y1)):
            base = (y * self.w + max(0, x0)) * 3
            for x in range(max(0, x0), min(self.w, x1)):
                self.px[base], self.px[base + 1], self.px[base + 2] = color
                base += 3

    def hline(self, x0, x1, y, color, thick=1):
        self.rect(x0, y, x1, y + thick, color)

    def circle(self, cx, cy, r, color):
        for y in range(cy - r, cy + r + 1):
            dy = y - cy
            dx = int((r * r - dy * dy) ** 0.5)
            self.rect(cx - dx, y, cx + dx + 1, y + 1, color)

    def polygon(self, points, color):
        # Scanline fill of a simple polygon.
        ys = [p[1] for p in points]
        for y in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            n = len(points)
            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for j in range(0, len(xs) - 1, 2):
                self.rect(int(xs[j]), y, int(xs[j + 1]) + 1, y + 1, color)

    def text(self, x, y, s, scale, color):
        s = s.upper()
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT[' '])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == '1':
                        self.rect(cx + col * scale, y + row * scale,
                                  cx + (col + 1) * scale,
                                  y + (row + 1) * scale, color)
            cx += 6 * scale
        return cx

    def text_width(self, s, scale):
        return len(s) * 6 * scale

    def text_centred(self, y, s, scale, color):
        w = self.text_width(s, scale)
        self.text((W - w) // 2, y, s, scale, color)


def write_png(path, canvas):
    raw = bytearray()
    stride = W * 3
    for y in range(H):
        raw.append(0)
        raw.extend(canvas.px[y * stride:(y + 1) * stride])
    comp = zlib.compress(bytes(raw), 9)

    def chunk(kind, data):
        out = struct.pack('>I', len(data)) + kind + data
        out += struct.pack('>I', zlib.crc32(kind + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', ihdr)
    png += chunk(b'IDAT', comp)
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)


# ---------------------------------------------------------------- page
def build():
    c = Canvas(W, H, PAPER)
    MX = 36            # side margin
    RX = W - MX        # right edge of text block

    # ---- nameplate -------------------------------------------------
    c.text_centred(28, "THE WORLD TODAY", 9, INK)
    c.text_centred(106, "MONDAY 23 NOVEMBER 2026 - EDITION NO. 327 - PRICE $2.50",
                   2, INK)
    c.hline(MX, RX, 130, INK, 6)
    c.hline(MX, RX, 142, INK, 2)

    # ---- hero ------------------------------------------------------
    c.text(MX, 160, "01 - CLIMATE", 2, RED)
    c.text(MX, 184, "CLIMATE TALKS", 7, INK)
    c.text(MX, 241, "COLLAPSE IN ANTALYA", 7, INK)

    # Flat illustration: summit hall under a red sun, navy sky.
    c.rect(MX, 302, RX, 464, NAVY)
    c.circle(872, 356, 44, RED)
    # mountain ridge
    c.polygon([(MX, 464), (MX, 428), (180, 396), (300, 436), (430, 402),
               (560, 440), (700, 404), (830, 438), (RX, 410), (RX, 464)],
              INK)
    # conference hall: roof + block + columns + flag
    c.polygon([(150, 392), (330, 344), (510, 392)], INK)
    c.rect(150, 392, 510, 464, INK)
    for wx in (180, 250, 320, 390, 460):
        c.rect(wx, 408, wx + 22, 446, PAPER)
    c.rect(328, 300, 332, 344, INK)
    c.rect(332, 300, 372, 322, RED)
    # birds
    for bx, by in ((620, 330), (680, 352), (740, 326)):
        c.polygon([(bx, by), (bx + 12, by - 8), (bx + 24, by)], INK)

    c.text(MX, 472, "ANTALYA: DELEGATES LEAVE AFTER THE FINAL PLENARY FAILS.",
           2, INK)

    # Standfirst with drop cap (4x = 28px tall, exactly two text lines,
    # so the third line clears it with no overlap).
    c.text(MX, 496, "T", 4, RED)
    c.text(68, 496, "WO WEEKS OF TALKS END WITH NO DEAL AS MORE THAN 190 NATIONS",
           2, INK)
    c.text(68, 514, "SPLIT OVER FOSSIL FUELS. THE LONGEST CLIMATE SUMMIT ON",
           2, INK)
    c.text(MX, 532, "RECORD CLOSES WITHOUT A PACT.", 2, INK)
    c.text(MX, 556, "BY STAFF WRITER", 2, INK)
    c.text(MX, 574, "SOURCE: REUTERS AND UN NEWS - CONFIRMED - CONTINUED ON PAGE A7",
           2, INK)

    # ---- secondary grid: 2 cols x 4 rows, stories 02-09 ------------
    stories = [
        ("02 - WASHINGTON", "DEMOCRATS WIN 258", "SEATS IN THE HOUSE",
         "LARGEST US MAJORITY SINCE 1992.", "SOURCE: AP - CONFIRMED"),
        ("03 - MEXICO", "MEXICO SEIZES", "EL CHAPO ISIDRO",
         "FBI TOP-10 FUGITIVE HELD; 11 DEAD.", "SOURCE: AP - CONFIRMED"),
        ("04 - WAR AT SEA", "RUSSIAN WARSHIP", "SUNK OFF LIBYA",
         "DRONES HIT TWO SHIPS IN 24 HOURS.", "SOURCE: WSJ - REPORTED"),
        ("05 - INDONESIA", "FACTORY FIRE IN", "INDONESIA: 3 DEAD",
         "DOZENS MISSING AFTER BANTEN BLAZE.", "SOURCE: AP - CONFIRMED"),
        ("06 - SEOUL", "SEOUL MINISTER", "QUITS OVER AI EXAMS",
         "CHEATING SCANDAL FORCES RESIGNATION.", "SOURCE: GUARDIAN - CONFIRMED"),
        ("07 - DELHI", "NEPAL PM MEETS", "MODI IN DELHI",
         "FIRST BILATERAL TRIP; FLOODS ON AGENDA.", "SOURCE: DW - CONFIRMED"),
        ("08 - SPORT", "INDIA DECLARE", "720-9 IN WELLINGTON",
         "RECORD TEST TOTAL IN NEW ZEALAND.", "SOURCE: DW - CONFIRMED"),
        ("09 - UNITED NATIONS", "NATIONS KEEP", "AI WEAPONS TALKS",
         "UN TO CONTINUE CURBS NEGOTIATIONS.", "SOURCE: UN - REPORTED"),
    ]
    col_w = (RX - MX - 24) // 2
    top = 610
    cell_h = 86
    gap = 6
    for i, (tag, h1, h2, body, src) in enumerate(stories):
        col = i % 2
        row = i // 2
        x = MX + col * (col_w + 24)
        y = top + row * (cell_h + gap)
        c.text(x, y, tag, 2, RED)
        c.text(x, y + 16, h1, 3, INK)
        c.text(x, y + 36, h2, 3, INK)
        c.text(x, y + 56, body, 2, INK)
        c.text(x, y + 71, src, 2, INK)
        if col == 0:
            c.rect(x + col_w + 12, y, x + col_w + 13, y + cell_h - 4, INK)

    # ---- markets strip ----------------------------------------------
    c.hline(MX, RX, 980, INK, 2)
    c.text(MX, 988, "MARKETS:", 2, RED)
    c.text(MX + 108, 988, "S&P 500 6,910.39 -3.7% - NASDAQ 22,617.73 -5.3% - BRENT $92.57",
           2, NAVY)
    c.text(MX, 1006, "BITCOIN $60,900 - FUTURES REBOUND AS ASIA OPENS: S&P FUTURES +1.3%",
           2, NAVY)

    return c


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    canvas = build()
    write_png(path, canvas)
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    sys.exit(main())
