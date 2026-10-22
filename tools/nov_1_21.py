#!/usr/bin/env python3
"""Datafiles voor 1 t/m 21 november 2026 (30 posts). Reken mee-cijfers uit de echte tools van hhservices.nl (22-10-2026).
Gebruik: python3 tools/nov_1_21.py build  -> build/<slug>.json + build/planning.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "week_20_31okt.py"), encoding="utf-8").read()
ns = {"__name__": "x"}; exec(src.split("CTA_DEADLINE")[0].replace("out = sys.argv[1]; os.makedirs(out, exist_ok=True)", ""), ns)
quote, quotes, quiz, kies, aftel, vraag = (ns[k] for k in ("quote", "quotes", "quiz", "kies", "aftel", "vraag"))
NB = " "
CTA_CHECK = ("Gratis jaareinde-check", "App 'CHECK' naar 085 109 1274. Wij kijken gratis mee.")
CTA_UIT = ("Uitbesteden? Link in bio", "Administratie, btw en belasting. Vanaf €" + NB + "50 per maand excl. btw.")
CTA_VRAAG = ("Vragen? App ons: 085 109 1274", "Wij leggen het uit in gewone taal.")

def jaareinde(slug, nr, lijst):
    v = aftel(slug, "JAAREINDE 2026", nr, "om je belasting over 2026 nog te verlagen", lijst, *CTA_CHECK)
    v["van"] = 99; return v

def fout(slug, nr, haak, rood, kop, bedrag, stop, tips):
    T = dict(stop=3.0, b=5.8, tip=2.4); T["c"] = round(T["b"] + len(tips) * T["tip"], 2); total = round(T["c"] + 3.2, 2)
    w = len(haak.split()); ev = [[round(0.15 + i * 0.2, 2), "key"] for i in range(w)] + [[0.7, "whoosh"], [2.2, "lever"], [3.0, "tick"], [3.05, "key"], [3.9, "lever"]]
    for i in range(len(tips)):
        s = T["b"] + i * T["tip"]; ev += [[round(s + .05, 2), "key"], [round(s + .15, 2), "print"], [round(s + 1.85, 2), "tick"]]
    ev += [[T["c"], "whoosh"], [round(T["c"] + .25, 2), "ching"]]
    return dict(type="fout", slug=slug, haak=haak, rood=rood, label=f"DE FOUT VAN DE WEEK #{nr}", stop=stop, tips=tips, bonKop=kop, bonBedrag=bedrag,
                cta="Gratis check: app 'CHECK'", serie="De fout van de week · elke maandag", T=T, total=total, events=sorted(ev))

def rm(slug, nr, haak, rood, vraag_, titel, rijen, uit, punch, disc):
    v = dict(slug=slug, label=f"REKEN MEE #{nr}", haak=haak, rood=rood, vraag=vraag_.replace("€ ", "€" + NB), titel=titel, rijen=rijen,
             uitkomst=uit, punch=punch.replace("€ ", "€" + NB), disc=disc)
    T = {"in": 3.2, "rij": 0.85}; T["res"] = T["in"] + 0.45 + 5 * T["rij"] + 0.4; T["punch"] = T["res"] + 2.8; T["cta"] = T["punch"] + 4.2
    total = round(T["cta"] + 3.4, 2); ev = [[0.05, "pop"], [0.6, "pop"], [T["in"], "lever"]]
    for i in range(5):
        st = T["in"] + 0.45 + i * T["rij"]; ev += [[round(st + .1 + k * .1, 2), "key"] for k in range(4)]
    ev += [[round(T["res"] + .2 + k * .14, 2), "tick"] for k in range(8)]
    ev += [[T["res"], "print"], [T["res"] + 1.3, "ching"], [T["punch"] + .3, "pop"], [T["cta"], "lever"], [T["cta"] + .4, "ching"]]
    v.update(type="rekenmee", cta="Reken het zelf uit", T=T, total=total, events=sorted(ev)); return v

UUR = "UURTARIEF BEREKENEN"; BEL = "BELASTING OPZIJZETTEN"; AUTO = "AUTO ZAAK OF PRIVÉ"
VB = "Voorbeeld 2026 · met urencriterium, geen starter"; VU = "Voorbeeldberekening 2026 · indicatie"
TAGS_RM = " Reken het zelf uit: hhservices.nl/tools (gratis) #zzp #ondernemen #zzpnederland #rekenmee"
H = "#zzp #zzptips #administratie #ondernemen"
P = [
 ("01", "17:45", vraag("vraag-van-de-week-2", "VRAAG VAN DE WEEK", "Btw-aangifte gelukt? Wat was het lastigst?", "De meest gestelde vraag beantwoorden we in een eigen video.", "Reageer hieronder ↓", ["lastigst?"], *CTA_VRAAG),
  "Btw-aangifte Q3 gelukt? Wat vond jij het lastigst? 👇 #btwaangifte #vraagvandeweek " + H),
 ("02", "12:15", rm("rm9-omzet50k", 9, "Bouw-zzp'er met veel materiaal?", ["materiaal?"], "€ 50.000 omzet, € 10.000 kosten? Reken mee!", BEL,
   [["Omzet dit jaar", "€ 50.000"], ["Zakelijke kosten", "€ 10.000"], ["Winst", "€ 40.000", 1], ["Na aftrekposten", "€ 33.872", 1], ["Belasting + Zvw", "€ 5.349", 1]],
   dict(label="ZET OPZIJ", num=11, pre="", post="%", sub="van elke betaling · € 446 per maand"),
   "Je kosten drukken je winst. Elk bonnetje dat je bewaart, telt mee!", VB),
  "Bouw-zzp'er met veel materiaal? Bij € 50.000 omzet en € 10.000 kosten zet je 11% van elke betaling opzij, zo'n € 446 per maand." + TAGS_RM + " #zzpbouw"),
 ("02", "17:45", fout("fout3-factuur-btwid", 3, "Deze factuur kost je geld", ["geld"], "FACTUUR", "€ 349,00", "STOP! Eerst checken!",
   ["Staat het btw-id van je leverancier erop?", "Zonder juiste factuur geen btw terug", "Vraag direct een nieuwe factuur", "Check het bij elke inkoop"]),
  "De fout van de week #3: een inkoopfactuur zonder btw-id van je leverancier. Dan krijg je de btw niet terug 👇 #factuur #btw #zzpbouw " + H),
 ("03", "17:45", quote("q3-in-januari", "HERKENBAAR?", "Ik ga in januari echt alles bijwerken.", "— elke zzp'er, elk jaar weer", "Wie herkent dit? ↓", ["januari"], *CTA_CHECK),
  "Ik ga in januari echt alles bijwerken… 🙃 Wie herkent dit? 👇 #zzplife #uitstelgedrag " + H),
 ("04", "12:15", rm("rm10-netto3500", 10, "€ 3.500 netto per maand?", ["netto"], "€ 3.500 netto overhouden? Reken mee!", UUR,
   [["Netto per maand", "€ 3.500"], ["Kosten per jaar", "€ 8.000"], ["Verzekering + pensioen", "€ 550 p/m"], ["Werkuren per week", "40"], ["Deel factureerbaar", "70%"]],
   dict(label="MINIMAAL PER UUR", num=56, pre="€ ", post="", sub="excl. btw · 1.232 factureerbare uren"),
   "Voor € 3.000 netto is het € 46. € 500 per maand méér = € 10 per uur méér vragen!", VU),
  "€ 3.500 netto per maand overhouden? Met € 8.000 kosten per jaar vraag je minimaal € 56 per uur." + TAGS_RM + " #uurtarief"),
 ("04", "17:45", quiz("quiz2-voor-31-december", "MYTHE OF FEIT?", "Alles wat je vóór 31 december koopt, levert belastingvoordeel op.", "MYTHE",
   ["Investeringsaftrek pas boven € 2.900 totaal", "Per aankoop minimaal € 450", "Koop alleen wat je echt nodig hebt"], ["Alles"], *CTA_CHECK),
  "Mythe of feit? Alles wat je vóór 31 december koopt, levert belastingvoordeel op 👇 #mytheoffeit #investeringsaftrek #jaareinde " + H),
 ("05", "17:45", kies("kies3-wanneer-administratie", "WAT DOE JIJ?", "Wanneer doe jij je administratie?", "Elke week een uurtje", "Eens per kwartaal, in paniek", "Reageer A of B ↓", ["jij"], *CTA_UIT),
  "A of B? Eerlijk antwoorden 😏 👇 #boekhouding " + H),
 ("06", "12:15", rm("rm11-auto35k", 11, "Veel zakelijke km én privé rijden?", ["én"], "Auto van € 35.000? Reken mee!", AUTO,
   [["Cataloguswaarde", "€ 35.000"], ["Autokosten per jaar", "€ 7.000"], ["Zakelijke km", "20.000"], ["Privé km", "5.000"], ["Winst zonder auto", "€ 60.000"]],
   dict(label="PRIVÉ RIJDEN", num=2000, pre="€ ", post="", sub="voordeliger per jaar"),
   "Op de zaak kost hij je € 6.741 per jaar, privé € 4.741. De bijtelling maakt het verschil!", "Voorbeeld 2026 · benzineauto · indicatie"),
  "Auto op de zaak? Bij € 35.000, 20.000 zakelijke en 5.000 privé-km is privé rijden € 2.000 per jaar voordeliger." + TAGS_RM + " #autovandezaak #bijtelling"),
 ("06", "17:45", jaareinde("jaareinde-55", 55, ["Meer dan € 2.900 investeren?", "Dan 28% investeringsaftrek", "Koop alleen wat je nodig hebt"]),
  "Nog 55 dagen in 2026. Investeren vóór 31 december? Lees dit eerst 👇 #jaareinde #investeringsaftrek #belastingtips " + H),
 ("07", "17:45", quotes("qs2-boekhouder", "ZZP-HUMOR", "Dingen die je boekhouder nooit wil horen",
   ["Alle bonnetjes liggen in mijn bus.", "Btw? Die heb ik al uitgegeven.", "Mijn privérekening is ook zakelijk.", "Alles zit in een schoenendoos."], ["nooit"],
   "Welke mist er nog? Reageer ↓", "Of geef die schoenendoos gewoon aan ons."),
  "Dingen die je boekhouder nooit wil horen 😅 Welke mist er nog? 👇 #zzphumor #zzplife " + H),
 ("08", "17:45", vraag("vraag-van-de-week-3", "VRAAG VAN DE WEEK", "Wat wil jij in 2027 eindelijk goed geregeld hebben?", "Wij maken er een stappenplan van.", "Reageer hieronder ↓", ["2027"], *CTA_VRAAG),
  "Vraag van de week: wat wil jij in 2027 eindelijk goed geregeld hebben? 👇 #vraagvandeweek #2027 " + H),
 ("09", "12:15", rm("rm12-starter", 12, "Net gestart? Dan scheelt dit flink", ["gestart?"], "Starter met € 45.000 omzet? Reken mee!", BEL,
   [["Omzet dit jaar", "€ 45.000"], ["Zakelijke kosten", "€ 6.000"], ["Winst", "€ 39.000", 1], ["Na aftrekposten", "€ 31.146", 1], ["Belasting + Zvw", "€ 4.129", 1]],
   dict(label="ZET OPZIJ", num=10, pre="", post="%", sub="van elke betaling · € 344 per maand"),
   "Startersaftrek scheelt hier € 829 per jaar. Maximaal 3 keer in je eerste 5 jaar!", "Voorbeeld 2026 · starter, met urencriterium"),
  "Net gestart? Met startersaftrek zet je bij € 45.000 omzet 10% opzij in plaats van 12%. Dat scheelt € 829 per jaar." + TAGS_RM + " #starter #startersaftrek"),
 ("09", "17:45", fout("fout4-prive-zakelijk", 4, "Deze pinbetaling hoort hier niet", ["niet"], "SUPERMARKT", "€ 62,40", "STOP! Dit is privé!",
   ["Houd zakelijk en privé gescheiden", "Twee rekeningen geven overzicht", "Toch privé betaald? Boek het als privé", "Dan klopt je administratie bij controle"]),
  "De fout van de week #4: privé boodschappen met de zakelijke pas. Zo los je het op 👇 #zakelijkerekening #boekhouding " + H),
 ("10", "17:45", quote("q4-overhouden", "MISTER ZEGT", "Omzet is leuk. Wat je overhoudt is belangrijker.", "— Mister Rekenmachine", "Eens of oneens? ↓", ["overhoudt"], *CTA_UIT, dark=True),
  "Omzet is leuk. Wat je overhoudt is belangrijker. Eens of oneens? 👇 #ondernemen #geldtips " + H),
 ("11", "12:15", rm("rm13-reistijd", 13, "Veel reistijd en offertes?", ["reistijd"], "Maar 60% van je uren factureerbaar? Reken mee!", UUR,
   [["Netto per maand", "€ 3.000"], ["Kosten per jaar", "€ 6.000"], ["Verzekering + pensioen", "€ 550 p/m"], ["Werkuren per week", "40"], ["Deel factureerbaar", "60%"]],
   dict(label="MINIMAAL PER UUR", num=52, pre="€ ", post="", sub="excl. btw · 1.056 factureerbare uren"),
   "Bij 70% factureerbaar is het € 44. Reistijd kost je € 8 per uur!", VU),
  "Veel reistijd en offertes? Factureer je maar 60% van je uren, dan heb je voor € 3.000 netto € 52 per uur nodig in plaats van € 44." + TAGS_RM + " #uurtarief #zzpbouw"),
 ("11", "17:45", quiz("quiz3-zelfstandigenaftrek", "MYTHE OF FEIT?", "De zelfstandigenaftrek wordt in 2027 nog lager.", "FEIT",
   ["2025: € 2.470", "2026: € 1.200", "2027: € 900"], ["lager."], *CTA_CHECK),
  "Mythe of feit? De zelfstandigenaftrek wordt in 2027 nog lager 👇 #zelfstandigenaftrek #mytheoffeit #belasting " + H),
 ("12", "17:45", kies("kies4-factuur", "WAT DOE JIJ?", "Klus af. Wanneer stuur jij de factuur?", "Dezelfde dag nog", "Als ik eraan denk", "Reageer A of B ↓", ["factuur?"], *CTA_UIT),
  "Klus af. Wanneer stuur jij de factuur? A of B 👇 #factuur #zzpbouw " + H),
 ("13", "12:15", rm("rm14-auto-zaak", 14, "Rij je bijna nooit privé?", ["nooit"], "Auto van € 25.000, 400 privé-km? Reken mee!", AUTO,
   [["Cataloguswaarde", "€ 25.000"], ["Autokosten per jaar", "€ 9.000"], ["Zakelijke km", "30.000"], ["Privé km", "400"], ["Winst zonder auto", "€ 60.000"]],
   dict(label="ZAKELIJK RIJDEN", num=1324, pre="€ ", post="", sub="voordeliger per jaar"),
   "Met 3.000 privé-km is privé ineens € 887 voordeliger. Die 500 km-grens maakt het verschil!", "Voorbeeld 2026 · benzineauto · met rittenregistratie"),
  "Rij je bijna nooit privé? Dan kan een auto op de zaak juist voordeliger zijn: hier € 1.324 per jaar. Let op de 500 km-grens en houd een rittenregistratie bij." + TAGS_RM + " #autovandezaak #bijtelling"),
 ("13", "17:45", jaareinde("jaareinde-48", 48, ["Haal je 1.225 uur dit jaar?", "Ook administratie telt mee", "Dan krijg je zelfstandigenaftrek"]),
  "Nog 48 dagen in 2026. Haal jij het urencriterium? 👇 #urencriterium #jaareinde " + H),
 ("14", "17:45", quotes("qs3-december", "ZZP-HUMOR", "Zo herken je een zzp'er in december",
   ["Is dit zakelijk? Dan koop ik het nu.", "Factuur sturen? Na de feestdagen.", "Wat is een voorlopige aanslag?", "Volgend jaar doe ik het anders."], ["december"],
   "Herkenbaar? Tag een collega ↓", "Wil je 2027 wél goed beginnen? App ons."),
  "Zo herken je een zzp'er in december 😅 Tag een collega 👇 #zzphumor #december " + H),
 ("15", "17:45", vraag("vraag-van-de-week-4", "VRAAG VAN DE WEEK", "Welke vraag over belasting durf je niet te stellen?", "Anoniem mag ook: app hem naar 085 109 1274.", "Reageer hieronder ↓", ["durf"], *CTA_VRAAG),
  "Vraag van de week: welke vraag over belasting durf je niet te stellen? Anoniem mag ook 👇 #vraagvandeweek #belasting " + H),
 ("16", "12:15", rm("rm15-vakantie", 15, "Acht weken vrij per jaar?", ["vrij"], "€ 3.000 netto én 8 weken vakantie? Reken mee!", UUR,
   [["Netto per maand", "€ 3.000"], ["Kosten per jaar", "€ 6.000"], ["Verzekering + pensioen", "€ 550 p/m"], ["Vakantieweken", "8"], ["Deel factureerbaar", "70%"]],
   dict(label="MINIMAAL PER UUR", num=48, pre="€ ", post="", sub="excl. btw · 1.148 factureerbare uren"),
   "Met 5 weken vakantie is het € 44. Vrije tijd moet je zelf verdienen!", VU),
  "Acht weken vakantie per jaar? Dan vraag je voor € 3.000 netto minimaal € 48 per uur in plaats van € 44." + TAGS_RM + " #uurtarief #vakantie"),
 ("16", "17:45", fout("fout5-uren", 5, "Zonder dit briefje mis je aftrek", ["aftrek"], "WEEKSTAAT", "38 uur", "STOP! Bewaar je uren!",
   ["Zelfstandigenaftrek: 1.225 uur per jaar", "Administratie en acquisitie tellen mee", "Houd het bij in je agenda of een app", "Bij controle moet je het aantonen"]),
  "De fout van de week #5: geen urenregistratie. Zo houd je je aftrek 👇 #urencriterium #zelfstandigenaftrek " + H),
 ("17", "17:45", quote("q5-november", "MISTER ZEGT", "Wie in november opruimt, heeft in maart rust.", "— Mister Rekenmachine", "Bewaar dit ↓", ["rust."], *CTA_CHECK),
  "Wie in november opruimt, heeft in maart rust. Bewaar dit 👇 #aangifte #jaareinde " + H),
 ("18", "12:15", rm("rm16-omzet120k", 16, "Groeit je bedrijf hard?", ["hard?"], "€ 120.000 omzet dit jaar? Reken mee!", BEL,
   [["Omzet dit jaar", "€ 120.000"], ["Zakelijke kosten", "€ 25.000"], ["Winst", "€ 95.000", 1], ["Na aftrekposten", "€ 81.887", 1], ["Belasting + Zvw", "€ 33.337", 1]],
   dict(label="ZET OPZIJ", num=28, pre="", post="%", sub="van elke betaling · € 2.778 per maand"),
   "Bij deze winst loont het om te laten doorrekenen of een bv slimmer is!", VB),
  "Groeit je bedrijf hard? Bij € 120.000 omzet en € 25.000 kosten zet je 28% van elke betaling opzij, zo'n € 2.778 per maand." + TAGS_RM + " #belasting #bv"),
 ("18", "17:45", quiz("quiz4-zorgverzekering", "MYTHE OF FEIT?", "Je zorgverzekering is aftrekbaar van je winst.", "MYTHE",
   ["Je premie is niet aftrekbaar", "Je betaalt wél Zvw-bijdrage over je winst", "Zet die dus ook opzij"], ["aftrekbaar"], *CTA_CHECK),
  "Mythe of feit? Als zzp'er is je zorgverzekering aftrekbaar 👇 #zvw #mytheoffeit #belasting " + H),
 ("19", "17:45", kies("kies5-goede-maand", "WAT DOE JIJ?", "Goede maand gedraaid. Wat doe je eerst?", "Nieuw gereedschap kopen", "Geld opzij voor de belasting", "Reageer A of B ↓", ["eerst?"], *CTA_CHECK),
  "Goede maand gedraaid. Wat doe jij eerst? A of B 👇 #geldtips #zzpbouw " + H),
 ("20", "12:15", rm("rm17-urencriterium", 17, "Haal je de 1.225 uur niet?", ["niet?"], "€ 60.000 omzet, zonder urencriterium? Reken mee!", BEL,
   [["Omzet dit jaar", "€ 60.000"], ["Zakelijke kosten", "€ 8.000"], ["Winst", "€ 52.000", 1], ["Na aftrekposten", "€ 45.396", 1], ["Belasting + Zvw", "€ 11.168", 1]],
   dict(label="ZET OPZIJ", num=19, pre="", post="%", sub="van elke betaling · € 931 per maand"),
   "Mét urencriterium is het € 10.578. Zonder betaal je hier € 590 per jaar méér!", "Voorbeeld 2026 · zonder urencriterium, geen starter"),
  "Haal je de 1.225 uur niet? Bij € 60.000 omzet betaal je dan € 590 per jaar méér belasting. Houd je uren bij!" + TAGS_RM + " #urencriterium"),
 ("20", "17:45", jaareinde("jaareinde-41", 41, ["Zelfstandigenaftrek 2027: € 900", "Lijfrente kan aftrek opleveren", "Laat je jaar nu doorrekenen"]),
  "Nog 41 dagen in 2026. Dit kun je nu nog regelen 👇 #jaareinde #belastingtips " + H),
 ("21", "17:45", quote("q6-vak", "HH SERVICES", "Jij bent goed in je vak. Wij in de rest.", "— administratie · btw · belasting", "Link in bio ↓", ["rest."], *CTA_UIT, dark=True),
  "Jij bent goed in je vak. Wij in de rest. Administratie, btw en belasting vanaf € 50 per maand 👇 #uitbesteden #zzpbouw " + H),
]
plan = []
for d, tijd, v, cap in P:
    json.dump(v, open(os.path.join(out, v["slug"] + ".json"), "w"), ensure_ascii=False)
    eng = {"rekenmee": "rekenmee", "fout": "fout"}.get(v.get("type"), "interactie")
    plan.append(dict(datum="2026-11-" + d, tijd=tijd, slug=v["slug"], engine=eng, caption=cap))
json.dump(plan, open(os.path.join(out, "planning.json"), "w"), ensure_ascii=False, indent=1)
print(len(plan), "posts")
