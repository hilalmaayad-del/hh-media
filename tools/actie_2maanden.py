#!/usr/bin/env python3
"""Actievideo's 'eerste 2 maanden gratis' (1 nov 2026 t/m 31 jan 2027).
Gebruik: python3 tools/actie_2maanden.py build  -> build/<slug>.json + build/planning-actie.json"""
import json, os, sys
bron = open(os.path.join(os.path.dirname(__file__), "week_20_31okt.py")).read()
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
exec(bron[bron.index("NB = "):bron.index("CTA_DEADLINE")])  # hergebruik de video-sjablonen

CTA = ("2 maanden gratis? Link in bio", "Start vóór 1 februari. Daarna vanaf €" + NB + "50 per maand excl. btw.")
PLAN = [
 ("2026-11-01", "17:45", quiz("actie1-mythe-duur", "MYTHE OF FEIT?",
   "Je administratie uitbesteden is duur.", "MYTHE",
   ["Vanaf €" + NB + "50 p/m excl. btw", "Nu 2 maanden gratis", "Alleen t/m 31 januari"], ["duur."], *CTA),
   "Mythe of feit? 👀 Tot en met 31 januari zijn je eerste 2 maanden administratie gratis (bij een jaarabonnement). Alles op hhservices.nl/actie #zzp #administratie #actie #ondernemen #zzptips"),
 ("2026-11-15", "17:45", kies("actie2-2027", "WAT DOE JIJ?",
   "Je administratie in 2027:", "Weer alles zelf doen", "Uitbesteden, 2 maanden gratis",
   "Reageer A of B ↓", ["2027:"], *CTA),
   "A of B? Eerlijk zijn 😏 Kies je B: de eerste 2 maanden zijn gratis t/m 31 januari. hhservices.nl/actie #zzp #administratie #goedevoornemens #ondernemen #zzptips"),
 ("2026-12-28", "17:45", quote("actie3-schone-lei", "HERKENBAAR?",
   "In januari begin ik met een schone lei.", "— elke zzp'er, elk jaar",
   "Wie herkent dit? ↓", ["januari"], *CTA),
   "Dit jaar écht een schone lei? 😅 Laat je administratie aan ons over: de eerste 2 maanden zijn gratis t/m 31 januari. hhservices.nl/actie #zzp #goedevoornemens #administratie #ondernemen"),
 ("2027-01-24", "17:45", aftel("actie4-nog-7", "ACTIE LOOPT AF", 7, "tot de actie '2 maanden gratis' stopt",
   ["2 maanden gratis", "Bij een jaarabonnement", "Plan je kennismaking"], *CTA),
   "Nog 7 dagen: tot en met 31 januari zijn je eerste 2 maanden administratie gratis. hhservices.nl/actie #zzp #administratie #actie #ondernemen"),
 ("2027-01-31", "09:00", aftel("actie5-laatste-dag", "LAATSTE DAG", 0, "loopt de actie '2 maanden gratis' af",
   ["2 maanden gratis", "Bij een jaarabonnement", "Plan vandaag je kennismaking"],
   "Laatste kans: link in bio", "Vanaf morgen betaal je gewoon vanaf maand 1.", vandaag=True),
   "Laatste dag! Vandaag is je kans: eerste 2 maanden administratie gratis. hhservices.nl/actie #zzp #administratie #laatstekans #ondernemen"),
]
plan = []
for datum, tijd, v, caption in PLAN:
    json.dump(v, open(os.path.join(out, v["slug"] + ".json"), "w"), ensure_ascii=False)
    plan.append(dict(datum=datum, tijd=tijd, slug=v["slug"], engine="interactie", caption=caption))
json.dump(plan, open(os.path.join(out, "planning-actie.json"), "w"), ensure_ascii=False, indent=1)
print(len(plan), "actievideo's")
