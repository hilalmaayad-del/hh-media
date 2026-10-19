#!/usr/bin/env python3
"""Maakt de datafiles (JSON) voor de video's van 20 t/m 31 oktober 2026.
Gebruik: python3 week_20_31okt.py <uitmap>  -> schrijft <slug>.json + planning.json"""
import json, os, sys
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
NB = " "

def ev_words(t0, n, step):
    return [[round(t0 + i * step, 2), "pop"] for i in range(n)]

def end(ev, T, total):
    ev += [[T["end"], "whoosh"], [T["end"] + 0.25, "ching"]]
    return sorted(ev)

V = []
# ---------- QUOTE
def quote(slug, label, quote, wie, trigger, rood, eind, eind2, dark=False):
    n = len(quote.split())
    T = dict(attr=round(0.9 + n * 0.17 + 0.5, 2))
    T["mister"] = T["attr"] + 0.9; T["cta"] = T["mister"] + 1.0; T["end"] = T["cta"] + 3.4
    total = round(T["end"] + 3.6, 2)
    ev = [[0.2, "whoosh"]] + ev_words(0.7, n, 0.17) + [[T["attr"], "print"], [T["mister"] + 0.2, "pop"], [T["cta"], "lever"], [T["cta"] + 0.15, "ching"]]
    return dict(type="quote", slug=slug, label=label, quote=quote, wie=wie, trigger=trigger, rood=rood, eind=eind, eind2=eind2, dark=dark, T=T, total=total, events=end(ev, T, total))

def quotes(slug, label, haak, qs, rood, eind, eind2, q=3.0):
    T = dict(hook=2.8, q=q); T["end"] = T["hook"] + len(qs) * q
    total = round(T["end"] + 3.6, 2)
    ev = ev_words(0.1, len(haak.split()), 0.25)
    for i in range(len(qs)):
        s = T["hook"] + i * q; ev += [[s, "whoosh"], [s + 0.95, "lever"], [s + 1.0, "print"]]
    return dict(type="quotes", slug=slug, label=label, haak=haak, quotes=qs, rood=rood, eind=eind, eind2=eind2, T=T, total=total, events=end(ev, T, total))

def quiz(slug, label, stelling, antwoord, uitleg, rood, eind, eind2):
    n = len(stelling.split())
    T = dict(keuze=2.8, reveal=6.0, regel=1.5); T["end"] = T["reveal"] + 1.0 + len(uitleg) * T["regel"] + 2.2
    total = round(T["end"] + 3.6, 2)
    ev = [[0.15, "whoosh"]] + [[round(0.5 + i * 1.8 / n, 2), "key"] for i in range(n)] + [[T["keuze"], "pop"], [T["keuze"] + 0.2, "pop"]]
    ev += [[T["reveal"] - 3, "tick"], [T["reveal"] - 2, "tick"], [T["reveal"] - 1, "tick"], [T["reveal"], "lever"], [T["reveal"] + 0.05, "ching"]]
    ev += [[round(T["reveal"] + 0.9 + i * T["regel"], 2), "print"] for i in range(len(uitleg))]
    return dict(type="quiz", slug=slug, label=label, stelling=stelling, antwoord=antwoord, uitleg=uitleg, rood=rood, eind=eind, eind2=eind2, T=T, total=total, events=end(ev, T, total))

def kies(slug, label, vraag, a, b, trigger, rood, eind, eind2):
    T = dict(ab=2.6, timer=4.2); T["end"] = 10.5
    total = round(T["end"] + 3.6, 2)
    ev = ev_words(0.05, len(vraag.split()), 1.4 / len(vraag.split())) + [[T["ab"] + 0.25, "whoosh"], [T["ab"] + 0.55, "whoosh"]]
    ev += [[round(T["timer"] + i, 2), "tick"] for i in range(6)] + [[T["timer"], "lever"]]
    return dict(type="kies", slug=slug, label=label, vraag=vraag, a=a, b=b, trigger=trigger, rood=rood, eind=eind, eind2=eind2, T=T, total=total, events=end(ev, T, total))

def aftel(slug, label, nr, sub, lijst, eind, eind2, vandaag=False):
    T = dict(tel=0.01 if vandaag else 2.2, regel=0.9); T["lijst"] = T["tel"] + 1.2; T["end"] = T["lijst"] + len(lijst) * T["regel"] + 2.6
    total = round(T["end"] + 3.6, 2)
    ev = [] if vandaag else [[round(i * 0.11, 2), "tick"] for i in range(int(T["tel"] / 0.11))]
    ev += [[T["tel"], "lever"], [T["tel"] + 0.05, "ching"]] + [[round(T["lijst"] + i * T["regel"], 2), "key"] for i in range(len(lijst))]
    return dict(type="aftellen", slug=slug, label=label, nr=nr, van=31, sub=sub, lijst=lijst, vandaag=vandaag, rood=[], eind=eind, eind2=eind2, T=T, total=total, events=end(ev, T, total))

def vraag(slug, label, vr, belofte, trigger, rood, eind, eind2):
    T = dict(vraag=1.6); T["belofte"] = T["vraag"] + 2.6; T["cta"] = T["belofte"] + 1.8; T["end"] = T["cta"] + 3.4
    total = round(T["end"] + 3.6, 2)
    ev = [[0.3, "whoosh"], [1.25, "pop"]] + ev_words(T["vraag"], len(vr.split()), 1.8 / len(vr.split())) + [[T["belofte"], "print"], [T["cta"], "lever"], [T["cta"] + 0.1, "ching"]]
    return dict(type="vraag", slug=slug, label=label, vraag=vr, belofte=belofte, trigger=trigger, rood=rood, eind=eind, eind2=eind2, T=T, total=total, events=end(ev, T, total))

CTA_DEADLINE = ("Btw nog niet geregeld?", "Stuur ons een bericht. Wij doen hem nog vóór 31 oktober.")
CTA_UIT = ("Uitbesteden? Link in bio", "Administratie, btw en belasting. Vanaf €" + NB + "50 per maand excl. btw.")
CTA_VRAAG = ("Vragen? Stuur ons een bericht", "Wij leggen het uit in gewone taal.")

PLAN = [
 ("2026-10-20", "17:45", quote("q1-belastingdienst-belt", "HERKENBAAR?",
   "Mijn administratie begint pas als de Belastingdienst belt.", "— elke zzp'er, minstens één keer",
   "Tag die collega ↓", ["Belastingdienst"], *CTA_UIT),
   "Herkenbaar? 😅 Tag de collega die dit is 👇 #zzp #zzptips #administratie #zzplife #ondernemen"),
 ("2026-10-21", "12:15", "rm4-netto4000",
   "Wil jij € 4.000 netto per maand? Dan moet je minimaal € 63 per uur vragen. Dat is € 19 per uur méér dan voor € 3.000 netto. Reken het zelf uit: hhservices.nl/tools (gratis) #zzp #uurtarief #ondernemen #zzpnederland #rekenmee"),
 ("2026-10-21", "17:45", quiz("quiz1-bewaarplicht", "MYTHE OF FEIT?",
   "Na 5 jaar mag je je administratie weggooien.", "MYTHE",
   ["Je bewaart je administratie 7 jaar", "Bonnen, facturen én bankafschriften", "Digitaal bewaren mag ook"], ["5"], *CTA_VRAAG),
   "Mythe of feit? Zeg het eerlijk: wist jij dit? 👇 #bewaarplicht #administratie #zzp #zzptips #mytheoffeit"),
 ("2026-10-22", "17:45", aftel("aftel-9", "BTW-DEADLINE Q3", 9, "tot je btw-aangifte Q3 binnen moet zijn",
   ["Aangifte over juli t/m september", "Én betaald op 31 oktober", "Te laat? Dan riskeer je een boete"], *CTA_DEADLINE),
   "Nog 9 dagen voor de btw-aangifte Q3. Al gedaan? 👇 #btwaangifte #zzp #deadline #ondernemen #zzptips"),
 ("2026-10-23", "12:15", "rm5-omzet40k",
   "Minder omzet? Dan zet je ook minder opzij. Bij € 40.000 omzet en € 5.000 kosten: 9% van elke betaling, zo'n € 284 per maand. De btw zet je daar nog bovenop apart! Reken het zelf uit: hhservices.nl/tools (gratis) #zzp #belasting #ondernemen #zzpnederland #rekenmee"),
 ("2026-10-23", "17:45", kies("kies1-btw-potje", "WAT DOE JIJ?",
   "Hoe zet jij de btw apart?", "Elke betaling direct apart", "Ik kijk wel als de aangifte komt",
   "Reageer A of B ↓", ["btw"], *CTA_VRAAG),
   "A of B? Eerlijk antwoorden 😏 👇 #btw #zzp #geldtips #zzptips #ondernemen"),
 ("2026-10-24", "17:45", quotes("qs-nooit-gezegd", "ZZP-HUMOR",
   "Dingen die een zzp'er nooit zegt",
   ["Mijn bonnetjes liggen netjes op volgorde.", "Ik kijk echt uit naar de btw-aangifte.", "Ik weet precies wat ik aan belasting moet betalen.", "Mijn administratie is altijd bij."],
   ["nooit"], "Welke mist er nog? Reageer ↓", "Of laat de administratie gewoon aan ons over."),
   "Welke zin mist er nog? Reageer 👇 #zzp #zzplife #zzphumor #administratie #ondernemen"),
 ("2026-10-25", "17:45", vraag("vraag-van-de-week-1", "VRAAG VAN DE WEEK",
   "Waar loop jij vast in je administratie?", "De beste vraag beantwoorden we in een eigen video.",
   "Stel hem hieronder ↓", ["vast"], "Stel je vraag in de reacties", "Of stuur ons een bericht via de link in bio."),
   "Vraag van de week: waar loop jij vast in je administratie? De beste vraag krijgt een eigen video 👇 #zzp #administratie #vraagvandeweek #zzptips #ondernemen"),
 ("2026-10-26", "12:15", "rm6-vier-dagen",
   "Vier dagen per week werken? Voor € 3.000 netto per maand heb je dan minimaal € 56 per uur nodig. Bij vijf dagen is dat € 44. Reken het zelf uit: hhservices.nl/tools (gratis) #zzp #uurtarief #vierdagen #ondernemen #rekenmee"),
 ("2026-10-26", "17:45", "fout2-inkoopfactuur",
   "De fout van de week #2: inkoopfacturen weggooien. Zonder factuur geen btw terug. Bewaar ze 7 jaar 👇 #factuur #btw #administratie #zzpbouw #zzp"),
 ("2026-10-27", "17:45", quote("q2-doe-het-morgen", "HERKENBAAR?",
   "Ik doe het morgen wel.", "— ik, 4 dagen voor de btw-deadline",
   "Wie herkent dit? ↓", ["morgen"], *CTA_DEADLINE, dark=True),
   "Ik doe het morgen wel… 🙃 Wie herkent dit? 👇 #btwaangifte #zzp #uitstelgedrag #zzplife #deadline"),
 ("2026-10-28", "12:15", "rm7-goed-jaar",
   "Goed jaar gedraaid? Schrik niet. Bij € 85.000 omzet en € 15.000 kosten zet je 23% van elke betaling opzij, zo'n € 1.618 per maand. Reken het zelf uit: hhservices.nl/tools (gratis) #zzp #belasting #ondernemen #zzpnederland #rekenmee"),
 ("2026-10-28", "17:45", "achterstand",
   "Maanden achter met je administratie? Zo begin je. Of je geeft het uit handen. Bewaar dit 👇 #achterstand #administratie #zzp #zzptips #ondernemen"),
 ("2026-10-29", "17:45", aftel("aftel-2", "BTW-DEADLINE Q3", 2, "tot je btw-aangifte Q3 binnen moet zijn",
   ["Pak je facturen en bonnen erbij", "Check je bankafschriften", "Doe aangifte én betaal"], *CTA_DEADLINE),
   "Nog 2 dagen. Btw-aangifte Q3 al gedaan? Ja of nee 👇 #btwaangifte #zzp #deadline #ondernemen #zzptips"),
 ("2026-10-30", "12:15", "rm8-veel-zakelijk",
   "Veel zakelijke kilometers = auto op de zaak? Niet per se. Auto van € 28.000, 25.000 zakelijke km en 2.000 privé-km: privé rijden is hier nog € 1.190 per jaar voordeliger. Reken het zelf uit: hhservices.nl/tools (gratis) #zzp #autovandezaak #bijtelling #ondernemen #rekenmee"),
 ("2026-10-30", "17:45", kies("kies2-zelf-of-uitbesteden", "WAT DOE JIJ?",
   "Je administratie: hoe doe jij het?", "Ik doe alles zelf", "Ik besteed het uit",
   "Reageer A of B ↓", ["jij"], *CTA_UIT),
   "Zelf doen of uitbesteden? Waarom? 👇 #administratie #zzp #boekhouding #zzptips #ondernemen"),
 ("2026-10-31", "09:00", aftel("aftel-vandaag", "BTW-DEADLINE Q3", 0, "moet je btw-aangifte Q3 binnen én betaald zijn",
   ["Aangifte over juli t/m september", "Betaling op tijd bij de Belastingdienst", "Lukt het niet? Stuur ons een bericht"], *CTA_DEADLINE, vandaag=True),
   "Vandaag is de deadline voor je btw-aangifte Q3. Gelukt? 👇 #btwaangifte #zzp #deadline #ondernemen #zzptips"),
]
plan = []
for datum, tijd, v, caption in PLAN:
    if isinstance(v, dict):
        json.dump(v, open(os.path.join(out, v["slug"] + ".json"), "w"), ensure_ascii=False)
        slug, engine = v["slug"], "interactie"
    else:
        slug, engine = v, ("rekenmee" if v.startswith("rm") else "fout" if v.startswith("fout") else "telmachine")
    plan.append(dict(datum=datum, tijd=tijd, slug=slug, engine=engine, caption=caption))
json.dump(plan, open(os.path.join(out, "planning.json"), "w"), ensure_ascii=False, indent=1)
print(len(plan), "posts")
