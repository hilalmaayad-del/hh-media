#!/usr/bin/env python3
"""HH Services - TikTok-videomaker v3: Mister Rekenmachine (telmachine), kassabon, eigen geluid.
Gebruik: python3 make_video2.py <plan.json> <item-id> <uit.mp4> <fonts-map>
"""
import json, os, sys, math, random, subprocess, wave, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ===== Mister Rekenmachine (telmachine + geluid) =====

BODY = (30, 29, 27); BODY_HI = (44, 42, 39); KEY = (236, 232, 222); KEY_OP = (64, 60, 55); LCD = (26, 18, 6)
KEYS = ["7", "8", "9", "÷", "4", "5", "6", "×", "1", "2", "3", "−", "0", ",", "=", "+"]

def _f(fd, n, s):
    import os
    return ImageFont.truetype(os.path.join(fd, n), s)

def draw_machine(d, fd, x, y, w, display="0,00", label="TOTAAL\nVERWERKT", pressed=None, lever=0.0):
    """Tekent de telmachine met linkerbovenhoek (x, y) en breedte w. Geeft (hoogte, slot_y) terug.
    pressed: index 0-15 van ingedrukte toets. lever: 0 (omhoog) .. 1 (omlaag)."""
    s = w / 900.0
    pad = int(54 * s); r = int(54 * s)
    gap = int(22 * s); kw = (w - 2 * pad - 3 * gap) // 4; kh = int(kw * 0.62)
    brand_h = int(60 * s); scr_h = int(150 * s)
    h = pad + brand_h + scr_h + int(34 * s) + 4 * kh + 3 * gap + pad
    # hendel (rechts)
    lx = x + w - int(6 * s); ly = y + int(150 * s)
    ang = math.radians(70 - 120 * lever)
    L = int(190 * s); ex = lx + int(math.cos(ang) * L * 0.35) + int(30 * s); ey = ly - int(math.sin(ang) * L)
    d.rounded_rectangle([lx - int(8 * s), ly - int(26 * s), lx + int(36 * s), ly + int(26 * s)], int(10 * s), fill=BODY_HI)
    d.line([lx + int(14 * s), ly, ex, ey], fill=(150, 146, 138), width=max(4, int(16 * s)))
    d.ellipse([ex - int(30 * s), ey - int(30 * s), ex + int(30 * s), ey + int(30 * s)], fill=OK)
    # body
    d.rounded_rectangle([x, y, x + w, y + h], r, fill=BODY)
    d.rounded_rectangle([x + int(6 * s), y + int(6 * s), x + w - int(6 * s), y + int(40 * s)], r, fill=BODY_HI)
    d.rounded_rectangle([x, y + int(26 * s), x + w, y + h], r, fill=BODY)
    # papiergleuf
    d.rounded_rectangle([x + int(90 * s), y - int(10 * s), x + w - int(90 * s), y + int(16 * s)], int(8 * s), fill=(8, 8, 8))
    # merkregel
    by = y + pad
    d.text((x + pad, by), "HH-TELMACHINE", font=_f(fd, "archivo-900.ttf", max(12, int(40 * s))), fill=(255, 255, 255))
    m = _f(fd, "jbmono-700.ttf", max(10, int(28 * s))); t = "MOD. 2026"
    d.text((x + w - pad - d.textlength(t, font=m), by + int(8 * s)), t, font=m, fill=(130, 126, 118))
    # scherm
    sy = by + brand_h
    d.rounded_rectangle([x + pad, sy, x + w - pad, sy + scr_h], int(22 * s), fill=LCD)
    sm = _f(fd, "jbmono-700.ttf", max(9, int(26 * s)))
    for i, ln in enumerate(label.split("\n")):
        d.text((x + pad + int(28 * s), sy + int(30 * s) + i * int(32 * s)), ln, font=sm, fill=(140, 98, 30))
    big = _f(fd, "jbmono-700.ttf", max(14, int(84 * s)))
    tw = d.textlength(display, font=big)
    gx = x + w - pad - int(30 * s) - tw; gy = sy + scr_h // 2 - int(50 * s)
    d.text((gx, gy), display, font=big, fill=OK)
    # toetsen
    ky0 = sy + scr_h + int(34 * s)
    kf = _f(fd, "archivo-900.ttf", max(12, int(54 * s)))
    for i, k in enumerate(KEYS):
        c, rr = i % 4, i // 4
        kx = x + pad + c * (kw + gap); ky = ky0 + rr * (kh + gap)
        down = (pressed == i)
        col = OK if k == "=" else (KEY_OP if c == 3 or k == "," else KEY)
        txtc = INK if col in (OK, KEY) else (235, 230, 220)
        off = int(6 * s) if down else 0
        if not down:
            d.rounded_rectangle([kx, ky + int(8 * s), kx + kw, ky + kh + int(8 * s)], int(16 * s), fill=(10, 10, 10))
        d.rounded_rectangle([kx, ky + off, kx + kw, ky + kh + off], int(16 * s), fill=col)
        bb = d.textbbox((0, 0), k, font=kf)
        d.text((kx + (kw - (bb[2] - bb[0])) // 2 - bb[0], ky + off + (kh - (bb[3] - bb[1])) // 2 - bb[1]), k, font=kf, fill=txtc)
    return h, y


# ---------------------------------------------------------------- geluid
SR = 44100

def _env(n, a=0.004, dcy=8.0):
    t = np.arange(n) / SR
    e = np.exp(-t * dcy)
    na = max(1, int(a * SR)); e[:na] *= np.linspace(0, 1, na)
    return e

def _lowpass(x, cutoff):
    a = math.exp(-2 * math.pi * cutoff / SR)
    try:
        from scipy.signal import lfilter
        return lfilter([1 - a], [1, -a], x).astype(np.float32)
    except ImportError:
        y = np.empty_like(x); acc = 0.0
        for i, v in enumerate(x):
            acc = (1 - a) * v + a * acc; y[i] = acc
        return y

def sfx_key(rng):
    n = int(0.07 * SR); t = np.arange(n) / SR
    click = rng.normal(0, 1, n) * np.exp(-t * 400) * 0.25
    beep = np.sin(2 * np.pi * 2350 * t) * _env(n, 0.002, 45) * 0.22
    return (click + beep).astype(np.float32)

def sfx_print(rng, dur=0.42):
    n = int(dur * SR); t = np.arange(n) / SR
    # naaldprinter: korte tikjes in snel ritme + zachte motorbrom
    out = np.zeros(n, np.float32)
    step = int(SR / 46)
    for i in range(0, n - 600, step):
        m = int(0.006 * SR); tt = np.arange(m) / SR
        out[i:i + m] += (rng.normal(0, 1, m) * np.exp(-tt * 900) * 0.32).astype(np.float32)
    motor = (np.sin(2 * np.pi * 120 * t) * 0.5 + np.sin(2 * np.pi * 240 * t) * 0.25) * 0.05
    fade = np.minimum(1, np.minimum(t / 0.03, (dur - t) / 0.06))
    out = (out + motor) * fade
    return _lowpass(out.astype(np.float32), 5000).astype(np.float32)

def sfx_lever(rng):
    n = int(0.25 * SR); t = np.arange(n) / SR
    thunk = np.sin(2 * np.pi * (140 * np.exp(-t * 18) + 60) * t) * np.exp(-t * 22) * 0.55
    rattle = rng.normal(0, 1, n) * np.exp(-t * 60) * 0.12
    return _lowpass((thunk + rattle).astype(np.float32), 2500).astype(np.float32)

def sfx_ching(rng):
    n = int(1.3 * SR); t = np.arange(n) / SR; out = np.zeros(n)
    for start, f0 in ((0.0, 2093.0), (0.09, 2637.0)):
        i = int(start * SR); tt = t[: n - i]
        tone = sum(amp * np.sin(2 * np.pi * f0 * ratio * tt) * np.exp(-tt * dec)
                   for ratio, amp, dec in ((1, 0.5, 3.2), (2.76, 0.18, 6), (5.4, 0.08, 10)))
        out[i:] += tone * 0.32
    drawer = rng.normal(0, 1, n) * np.exp(-t * 30) * 0.05
    return (out + drawer).astype(np.float32)

def sfx_whoosh(rng):
    n = int(0.4 * SR); t = np.arange(n) / SR
    w = rng.normal(0, 1, n) * np.sin(np.pi * t / 0.4) ** 2 * 0.18
    return _lowpass(w.astype(np.float32), 1800).astype(np.float32)

def music_bed(total, bpm=96):
    """Warme, rustige marimba-achtige loop (C - G - Am - F) met zacht ritme."""
    n = int(total * SR); out = np.zeros(n, np.float32)
    beat = 60.0 / bpm
    chords = [(261.6, 329.6, 392.0), (246.9, 293.7, 392.0), (220.0, 261.6, 329.6), (220.0, 261.6, 349.2)]
    bass = [130.8, 98.0, 110.0, 87.3]
    rng = np.random.default_rng(3)
    def pluck(f, dur, amp):
        m = int(dur * SR); tt = np.arange(m) / SR
        s = (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * f * 4 * tt) * np.exp(-tt * 18)) * np.exp(-tt * 5.5)
        na = int(0.003 * SR); s[:na] *= np.linspace(0, 1, na)
        return (s * amp).astype(np.float32)
    nb = int(total / beat) + 1
    for b in range(nb):
        t0 = b * beat; bar = (b // 4) % 4; ch = chords[bar]
        i = int(t0 * SR)
        if b % 4 == 0:
            s = pluck(bass[bar], beat * 4, 0.20); e = min(n, i + len(s))
            if i < n: out[i:e] += s[: e - i]
        # arpeggio op achtsten
        for k in range(2):
            j = int((t0 + k * beat / 2) * SR)
            f = ch[(b * 2 + k) % 3] * (2 if (b + k) % 4 == 3 else 1)
            s = pluck(f, 0.6, 0.075); e = min(n, j + len(s))
            if j < n: out[j:e] += s[: e - j]
        # zachte shaker op de offbeat
        j = int((t0 + beat / 2) * SR); m = int(0.04 * SR)
        if j + m < n:
            tt = np.arange(m) / SR
            out[j:j + m] += (rng.normal(0, 1, m) * np.exp(-tt * 120) * 0.025).astype(np.float32)
    out = _lowpass(out, 3800)
    fade = np.ones(n, np.float32); fl = int(0.6 * SR)
    fade[:int(0.15 * SR)] = np.linspace(0, 1, int(0.15 * SR)); fade[-fl:] = np.linspace(1, 0, fl)
    return out * fade

def mix(total, events, bpm=96):
    """events: lijst van (tijd, soort) met soort in key/print/lever/ching/whoosh/tick/pop."""
    rng = np.random.default_rng(11)
    a = music_bed(total, bpm) * 0.9
    n = len(a)
    for ts, kind in events:
        if kind in ("key", "tick", "pop"): s = sfx_key(rng) * (0.8 if kind == "tick" else 1.0)
        elif kind == "print": s = sfx_print(rng)
        elif kind == "lever": s = sfx_lever(rng)
        elif kind == "ching": s = sfx_ching(rng)
        else: s = sfx_whoosh(rng)
        i = int(ts * SR); e = min(n, i + len(s))
        if i < n: a[i:e] += s[: e - i]
    # zachte limiter
    a = np.tanh(a * 1.6) / np.tanh(1.6)
    a = a / max(1e-6, np.abs(a).max()) * 0.89
    pcm = (a * 32767).astype(np.int16)
    return np.stack([pcm, pcm], 1).tobytes()

# ===== Video =====

W, H, FPS, SR = 1080, 1920, 30, 44100
OK = (227, 160, 42); INK = (18, 18, 18); CR = (250, 245, 234); PAPER = (251, 250, 244); DIM = (60, 56, 50)

def F(d, n, s): return ImageFont.truetype(os.path.join(d, n), s)
def ease_out(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def ease_back(t):
    t = max(0, min(1, t)); c = 1.70158; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2

def wrap(d, text, font, maxw):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out

class Video:
    def __init__(self, fdir, item):
        self.fd = fdir; self.item = item
        self.f = {k: F(fdir, n, s) for k, (n, s) in {
            "mega": ("archivo-900.ttf", 420), "hook": ("archivo-900.ttf", 118), "sub": ("jbmono-700.ttf", 44),
            "word": ("archivo-900.ttf", 150), "logo": ("archivo-900.ttf", 60), "rc": ("jbmono-700.ttf", 48),
            "rch": ("archivo-900.ttf", 62), "cta": ("archivo-900.ttf", 104), "small": ("jbmono-700.ttf", 38)}.items()}
        self.frames = []; self.sfx = []  # (time, kind)
        rng = np.random.default_rng(7)
        g = rng.normal(0, 1, (H // 4, W // 4)).astype(np.float32)
        self.grain = Image.fromarray(np.clip(128 + g * 22, 0, 255).astype(np.uint8)).resize((W, H)).convert("L")

    # ---------- helpers
    def bg(self, color, t, shake=0):
        im = Image.new("RGB", (W, H), color)
        d = ImageDraw.Draw(im)
        # drifting oker glow
        if color == INK:
            gx = int(W * (0.7 + 0.15 * math.sin(t * 0.7))); gy = int(H * (0.3 + 0.1 * math.cos(t * 0.5)))
            glow = Image.new("RGB", (W, H), INK); gd = ImageDraw.Draw(glow)
            gd.ellipse([gx - 520, gy - 520, gx + 520, gy + 520], fill=(70, 48, 14))
            glow = glow.filter(ImageFilter.GaussianBlur(160))
            im = Image.blend(im, glow, 0.9)
        im = Image.composite(im, Image.new("RGB", (W, H), tuple(min(255, c + 10) for c in color)), self.grain.point(lambda p: 255 if p < 150 else 235))
        return im

    def logo(self, d, x, y, dark=True):
        f = self.f["logo"]
        d.text((x, y), "HH", font=f, fill=CR if dark else INK)
        w = d.textlength("HH ", font=f); bb = d.textbbox((x + w, y), "Services", font=f)
        d.rounded_rectangle([bb[0] - 10, bb[1] - 8, bb[2] + 10, bb[3] + 10], 8, fill=OK if dark else INK)
        d.text((x + w, y), "Services", font=f, fill=INK if dark else OK)

    def chrome(self, im, t, total, dark=True):
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, int(W * t / total), 12], fill=OK if dark else INK)
        self.logo(d, 72, 96, dark)
        return im

    def push(self, im): self.frames.append(im)

    # ---------- scenes
    def scene_hook(self, t0, dur, total):
        it = self.item; hook = it["haak"]
        m = re.search(r"(?<![\d.,])(\d+)(?![\d.,])", hook)
        n = int(m.group(1)) if m and len(m.group(1)) <= 4 and int(m.group(1)) < 2000 else None
        label = it.get("rubriek", "")
        N = int(dur * FPS)
        if n is not None and n <= 60:
            start = min(n + 9, 99)
            for i in range(N):
                t = i / FPS; p = min(1, t / (dur * 0.55))
                val = round(start - (start - n) * ease_out(p))
                if i > 0 and val != getattr(self, "_lv", None): self.sfx.append((t0 + t, "tick"))
                self._lv = val
                im = self.bg(INK, t0 + t); d = ImageDraw.Draw(im)
                s = 1 + 0.06 * math.sin(t * 30) * max(0, 1 - t * 2)
                txt = str(val); f = self.f["mega"]
                bb = d.textbbox((0, 0), txt, font=f); tw = bb[2] - bb[0]
                d.text(((W - tw) // 2 - bb[0], 480), txt, font=f, fill=OK)
                if re.match(r"^\s*(Nog\s+|nog\s+)?\d+", hook):
                    rest = hook.replace(m.group(1), "", 1).strip(" :-")
                    rest = re.sub(r"^(Nog|nog)\s*", "", rest).strip(" :")
                else:
                    rest = hook  # getal staat midden in de zin: zin compleet laten
                lines = wrap(d, rest, self.f["hook"], W - 160)
                a = ease_out((t - 0.35) / 0.4)
                for k, ln in enumerate(lines):
                    yy = 1010 + k * 128 + int((1 - a) * 80)
                    col = tuple(int(INK[c] + (CR[c] - INK[c]) * a) for c in range(3))
                    d.text((80, yy), ln, font=self.f["hook"], fill=col)
                d.text((80, 380), label.upper() if label else "", font=self.f["sub"], fill=OK)
                self.push(self.chrome(im, t0 + t, total))
        else:
            words = hook.split()
            for i in range(N):
                t = i / FPS
                im = self.bg(INK, t0 + t); d = ImageDraw.Draw(im)
                shown = len(words) if it.get('volle_haak') else min(len(words), int(t / 0.18) + 1)
                if i == 0 or int(t / 0.18) != int((t - 1 / FPS) / 0.18):
                    if shown <= len(words): self.sfx.append((t0 + t, "pop"))
                lines = wrap(d, " ".join(words), self.f["hook"], W - 160)
                cnt = 0; y = 620
                for ln in lines:
                    x = 80
                    for w in ln.split():
                        cnt += 1
                        if cnt > shown: break
                        age = 1 if it.get('volle_haak') else t - (cnt - 1) * 0.18
                        sc = ease_back(age / 0.25)
                        col = OK if cnt == len(words) else CR
                        d.text((x, y + int((1 - sc) * 40)), w, font=self.f["hook"], fill=col)
                        x += d.textlength(w + " ", font=self.f["hook"])
                    y += 132
                if label: d.text((80, 470), label.upper(), font=self.f["sub"], fill=OK)
                self.push(self.chrome(im, t0 + t, total))

    def scene_receipt(self, t0, dur, total):
        lines = self.item["slides"]; N = int(dur * FPS)
        per = (dur - 0.8) / len(lines)
        self.sfx.append((t0, "whoosh")); self.sfx.append((t0 + 0.12, "lever"))
        mx, my, mw = 130, 1100, 820
        px0, px1 = mx + 82, mx + mw - 82
        # lettergrootte zo kiezen dat de hele bon past
        probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        for size in (60, 56, 52, 48, 44):
            f = F(self.fd, "archivo-900.ttf", size); blocks = []
            for txt in lines:
                wl = wrap(probe, txt, f, px1 - px0 - 64)
                blocks.append((f, wl, len(wl) * (f.size + 10) + 30))
            if 150 + sum(b[2] for b in blocks) <= my - 250: break
        for i in range(N):
            t = i / FPS
            im = self.bg(INK, t0 + t); d = ImageDraw.Draw(im)
            shown = min(len(lines), int(max(0, t - 0.4) / per) + 1) if t > 0.4 else 0
            prog = 0 if t < 0.4 else min(1, ((t - 0.4) - (shown - 1) * per) / 0.35)
            if t > 0.4 and int((t - 1 / FPS - 0.4) / per) != int((t - 0.4) / per) or (t >= 0.4 and t - 1 / FPS < 0.4):
                self.sfx.append((t0 + t, "key")); self.sfx.append((t0 + t + 0.08, "print"))
            lever = math.sin(min(1, t / 0.4) * math.pi) if t < 0.4 else 0
            pressed = 14 if (shown and prog < 0.35) else None
            draw_machine(d, self.fd, mx, my, mw, display=f"{shown}/{len(lines)}" if shown else "0/" + str(len(lines)),
                         label="BON\nREGEL", pressed=pressed, lever=lever)
            if shown:
                ph = 150 + sum(b[2] for b in blocks[:shown - 1]) + ease_out(prog) * blocks[shown - 1][2]
            else:
                ph = 110
            top = my - ph
            d.rectangle([px0, top, px1, my + 4], fill=PAPER)
            for z in range(px0, px1, 30):
                d.polygon([(z, top), (z + 15, top - 16), (z + 30, top)], fill=PAPER)
            d.text((px0 + 30, top + 24), "HH SERVICES", font=self.f["rc"], fill=(90, 90, 90))
            d.line([px0 + 30, top + 86, px1 - 30, top + 86], fill=(190, 190, 190), width=3)
            y = top + 110
            for k in range(shown):
                f, wl, bh = blocks[k]
                col = (138, 85, 0) if k == len(lines) - 1 else INK
                for j, ln in enumerate(wl):
                    d.text((px0 + 32, y + j * (f.size + 10)), ln, font=f, fill=col)
                y += bh
            # papier opnieuw over de gleuf
            d.rounded_rectangle([mx + 82, my - 10, mx + mw - 82, my + 14], 8, fill=(8, 8, 8))
            d.rectangle([px0 + 6, my - 4, px1 - 6, my + 2], fill=PAPER)
            z = 1 + 0.05 * ease_out(t / dur)
            if z > 1.001:
                cw, ch = int(W / z), int(H / z); cx, cy = (W - cw) // 2, int((H - ch) * 0.5)
                im = im.crop((cx, cy, cx + cw, cy + ch)).resize((W, H))
            self.push(self.chrome(im, t0 + t, total))

    def scene_punch(self, t0, dur, total):
        words = ["Geen", "tijd?", "Wij", "regelen", "het."]
        N = int(dur * FPS); step = dur * 0.7 / len(words)
        for i in range(N):
            t = i / FPS; k = min(len(words) - 1, int(t / step))
            if i == 0 or int((t - 1 / FPS) / step) != int(t / step):
                if t / step < len(words): self.sfx.append((t0 + t, "key"))
                if k == 2: self.sfx.append((t0 + t, "ching"))
            im = self.bg(INK, t0 + t); d = ImageDraw.Draw(im)
            age = t - k * step; sc = ease_back(age / 0.22)
            w = words[k]; f = self.f["word"]
            size = int(150 * (0.6 + 0.4 * sc)); f = F(self.fd, "archivo-900.ttf", max(40, size))
            bb = d.textbbox((0, 0), w, font=f); tw = bb[2] - bb[0]; th = bb[3] - bb[1]
            x = (W - tw) // 2 - bb[0]; y = (H - th) // 2 - bb[1]
            if k >= 2:
                d.rectangle([x - 26, y + bb[1] - 18, x + tw + 26, y + bb[1] + th + 22], fill=OK)
                d.text((x, y), w, font=f, fill=INK)
            else:
                d.text((x, y), w, font=f, fill=CR)
            self.push(self.chrome(im, t0 + t, total))

    def scene_cta(self, t0, dur, total):
        N = int(dur * FPS); self.sfx.append((t0, "whoosh"))
        cta = self.item["cta"]
        lay = Image.new("RGBA", (560, 560), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        draw_machine(ld, self.fd, 40, 60, 420, display="KLAAR", label="STATUS")
        self.mini = lay.rotate(6, resample=Image.BICUBIC, expand=False)
        for i in range(N):
            t = i / FPS
            im = self.bg(OK, t0 + t); d = ImageDraw.Draw(im)
            a = ease_out(t / 0.4)
            lines = wrap(d, cta, self.f["cta"], W - 160)
            for k, ln in enumerate(lines):
                d.text((80, 760 + k * 116 + int((1 - a) * 90)), ln, font=self.f["cta"], fill=INK)
            pulse = 1 + 0.04 * math.sin(t * 6)
            knop = self.item.get("knop", "hhservices.nl")
            bw, bh = int((d.textlength(knop, font=self.f["rch"]) + 96) * pulse), int(120 * pulse); bx = 80; by = 1160
            d.rounded_rectangle([bx, by, bx + bw, by + bh], bh // 2, fill=INK)
            d.text((bx + 48, by + bh // 2 - 26), knop, font=self.f["rch"], fill=OK)
            d.text((80, 1360), "085 109 1274", font=self.f["sub"], fill=INK)
            d.text((80, 1420), self.item.get("onderregel", "Administratie · btw · belasting · loon · HR"), font=self.f["small"], fill=(70, 50, 10))
            im.paste(self.mini, (W - self.mini.width + 40, 1510 + int(8 * math.sin(t * 3))), self.mini)
            self.push(self.chrome(im, t0 + t, total, dark=False))

    # ---------- audio
    def audio(self, total):
        return mix(total, self.sfx)

    def render(self, out):
        plan = [("hook", 2.6), ("receipt", 1.2 + 1.25 * len(self.item["slides"])), ("punch", 2.2), ("cta", 2.6)]
        total = sum(d for _, d in plan); t0 = 0
        for name, d in plan:
            getattr(self, "scene_" + name)(t0, d, total); t0 += d
        wav = out + ".wav"
        with wave.open(wav, "wb") as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(self.audio(total))
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                              "-r", str(FPS), "-i", "-", "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19",
                              "-preset", "medium", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out],
                             stdin=subprocess.PIPE)
        for im in self.frames: p.stdin.write(im.tobytes())
        p.stdin.close(); p.wait(); os.remove(wav)
        if p.returncode: sys.exit("ffmpeg mislukt")
        print(out, round(total, 1), "s")

if __name__ == "__main__":
    plan, iid, out, fd = sys.argv[1:5]
    item = next(i for i in json.load(open(plan, encoding="utf-8"))["items"] if i["id"] == iid)
    Video(fd, item).render(out)
