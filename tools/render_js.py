#!/usr/bin/env python3
"""Rendert een HTML/JS-animatie (window.render(t)) frame voor frame met Playwright naar MP4 met Mister Rekenmachine-geluid.
Gebruik: python3 render_js.py <pagina.html> <data.json> <uit.mp4> [--sheet sheet.png]
data.json bevat window.DATA voor de pagina plus "total" en "events" [[t, soort], ...].
"""
import json, os, sys, subprocess, wave
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from make_video import mix, SR
from playwright.sync_api import sync_playwright

FPS = 30
page_path, data_path, out = sys.argv[1:4]
data = json.load(open(data_path, encoding="utf-8"))
total = data["total"]; events = [tuple(e) for e in data["events"]]
wav = out + ".wav"
with wave.open(wav, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(mix(total, events))
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
                       "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
                       "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "aac", "-b:a", "160k", "-shortest",
                       "-movflags", "+faststart", out], stdin=subprocess.PIPE)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    pg.add_init_script("window.DATA = " + json.dumps(data, ensure_ascii=False) + ";")
    pg.goto("file://" + os.path.abspath(page_path))
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(300)
    n = int(total * FPS)
    for i in range(n):
        pg.evaluate(f"render({i / FPS})")
        ff.stdin.write(pg.screenshot(type="png"))
    b.close()
ff.stdin.close(); ff.wait(); os.remove(wav)
if ff.returncode: sys.exit("ffmpeg mislukt")
print(out, total, "s")
if "--sheet" in sys.argv:
    sheet = sys.argv[sys.argv.index("--sheet") + 1]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-vf", f"fps=1/{max(1, total / 12):.2f},scale=216:-1,tile=6x2", "-frames:v", "1", sheet])
    print(sheet)
