#!/usr/bin/env python3
"""Losse quote-kaarten (PNG 1080x1920) in de interactie-stijl. quote_cards.py <uitmap>"""
import json,sys,os,io,importlib.util
from playwright.sync_api import sync_playwright
out=sys.argv[1];os.makedirs(out,exist_ok=True)
spec=importlib.util.spec_from_file_location("w",os.path.join(os.path.dirname(__file__),"week_20_31okt.py"))
# hergebruik quote() zonder het hele plan te draaien
src=open(os.path.join(os.path.dirname(__file__),"week_20_31okt.py"),encoding="utf-8").read().split("CTA_DEADLINE =")[0]
ns={};exec(src.replace("out = sys.argv[1]; os.makedirs(out, exist_ok=True)","out=None"),ns)
Q=ns["quote"]
K=[("kaart-1-belastingdienst","HERKENBAAR?","Mijn administratie begint pas als de Belastingdienst belt.","— elke zzp'er, minstens één keer","Tag die collega ↓",["Belastingdienst"],False),
 ("kaart-2-morgen","HERKENBAAR?","Ik doe het morgen wel.","— ik, 4 dagen voor de btw-deadline","Wie herkent dit? ↓",["morgen"],True),
 ("kaart-3-btw-geleend","MISTER ZEGT","Btw is geen omzet. Het is geld dat je even vasthoudt voor de Belastingdienst.","— Mister Rekenmachine","Bewaar dit ↓",["geen"],True),
 ("kaart-4-bonnetje","MISTER ZEGT","Een bonnetje van vijf euro is óók een bonnetje.","— Mister Rekenmachine","Tag je collega ↓",["óók"],False),
 ("kaart-5-overzicht","MISTER ZEGT","Je bent niet slecht met geld. Je hebt alleen geen overzicht.","— Mister Rekenmachine","Herkenbaar? ↓",["overzicht."],True),
 ("kaart-6-oktober","MISTER ZEGT","Wie in oktober opruimt, heeft in maart rust.","— Mister Rekenmachine","Bewaar dit ↓",["rust."],False),
 ("kaart-7-vakman","HH SERVICES","Jij bent goed in je vak. Wij in de rest.","— administratie · btw · loon · HR","Link in bio ↓",["rest."],True),
 ("kaart-8-omzet","MISTER ZEGT","Omzet is leuk. Wat je overhoudt is belangrijker.","— Mister Rekenmachine","Eens of oneens? ↓",["overhoudt"],False)]
with sync_playwright() as p:
    b=p.chromium.launch()
    for slug,lab,q,wie,trig,rood,dark in K:
        d=Q(slug,lab,q,wie,trig,rood,"","",dark=dark)
        pg=b.new_page(viewport={"width":1080,"height":1920})
        pg.add_init_script("window.DATA="+json.dumps(d,ensure_ascii=False)+";")
        pg.goto("file://"+os.path.abspath("tools/interactie.html"))
        pg.evaluate("document.fonts.ready");pg.wait_for_timeout(200)
        pg.evaluate(f"render({d['T']['cta']+1.6})")
        pg.evaluate("document.getElementById('prog').setAttribute('width',0)")
        pg.screenshot(path=os.path.join(out,slug+".png"));pg.close();print(slug)
    b.close()
