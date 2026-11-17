#!/usr/bin/env python3
"""Batch 3: video's voor 22 november t/m 13 december 2026 (TikTok, en de reels voor Facebook/Instagram).
Reken mee-cijfers uit de echte rekentools van hhservices.nl (12-11-2026).
Alle eindkaarten sturen naar de actiepagina (geen 'CHECK' meer in nieuwe posts).
KOR-datum gecheckt bij de Belastingdienst: aanmelding uiterlijk 3 december binnen voor 1 januari.
Gebruik: python3 tools/nov22_dec13.py build  -> build/<slug>.json + build/planning-b3.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "nov_1_21.py"), encoding="utf-8").read()
ns = {"__name__": "x", "sys": sys, "__file__": os.path.join(os.path.dirname(os.path.abspath(__file__)), "nov_1_21.py")}
sys_argv = sys.argv; sys.argv = [sys.argv[0], "/tmp/_b3_dummy"]
exec(src.split("P = [")[0], ns)
sys.argv = sys_argv
quote, quotes, quiz, kies, aftel, vraag, fout, rm = (ns[k] for k in ("quote", "quotes", "quiz", "kies", "aftel", "vraag", "fout", "rm"))
UUR, BEL, AUTO, VB, VU, TAGS_RM, H, NB = (ns[k] for k in ("UUR", "BEL", "AUTO", "VB", "VU", "TAGS_RM", "H", "NB"))

CTA = ("2 maanden gratis!", "Administratie vanaf €" + NB + "50 per maand excl. btw. hhservices.nl/actie")
CTA_VRAAG = ("Vragen? Stuur ons een bericht", "Of kijk op hhservices.nl/actie")

def jaareinde(slug, nr, lijst):
    v = aftel(slug, "JAAREINDE 2026", nr, "om je belasting over 2026 nog te verlagen", lijst, *CTA); v["van"] = 99; return v

def fouta(*a):
    v = fout(*a); v["cta"] = "2 maanden gratis!"; v["serie"] = "De fout van de week · elke maandag"; return v

P = [
 ("2026-11-22", "17:45", vraag("vraag-van-de-week-5", "VRAAG VAN DE WEEK", "Waar erger jij je het meest aan in je administratie?", "De meest genoemde ergernis lossen we op in een video.", "Reageer hieronder ↓", ["erger"], *CTA_VRAAG),
  "Vraag van de week: waar erger jij je het meest aan in je administratie? 👇 #vraagvandeweek #boekhouding " + H),
 ("2026-11-23", "12:15", rm("rm18-lage-winst", 18, "Lage winst dit jaar?", ["Lage"], "€ 40.000 omzet, € 12.000 kosten? Reken mee!", BEL,
   [["Omzet dit jaar", "€ 40.000"], ["Zakelijke kosten", "€ 12.000"], ["Winst", "€ 28.000", 1], ["Na aftrekposten", "€ 23.396", 1], ["Belasting + Zvw", "€ 1.135", 1]],
   dict(label="ZET OPZIJ", num=3, pre="", post="%", sub="van elke betaling · € 95 per maand"),
   "Lage winst? Dan valt de belasting mee. De btw zet je wél volledig apart!", VB),
  "Lage winst dit jaar? Bij € 40.000 omzet en € 12.000 kosten zet je maar 3% opzij voor de inkomstenbelasting. Maar de btw is nooit van jou: die zet je volledig apart." + TAGS_RM + " #btw #zzpbouw"),
 ("2026-11-23", "17:45", fouta("fout6-te-laat-factureren", 6, "Deze factuur ligt al 3 weken klaar", ["3", "weken"], "FACTUUR", "€ 1.850,00", "STOP! Verstuur hem nu!",
   ["Klus af? Factuur dezelfde week", "Later factureren = later betaald", "Zet een vaste factuurdag in je agenda", "Betaaltermijn verlopen? Stuur een herinnering"]),
  "De fout van de week #6: te laat factureren. Je werk is klaar, maar je geld nog niet binnen 👇 #factuur #cashflow #zzpbouw " + H),
 ("2026-11-24", "17:45", quote("q7-factuur", "MISTER ZEGT", "Een factuur die je niet stuurt, wordt nooit betaald.", "— Mister Rekenmachine", "Eens? ↓", ["nooit"], *CTA, dark=True),
  "Een factuur die je niet stuurt, wordt nooit betaald. Hoe snel factureer jij? 👇 #factuur #cashflow " + H),
 ("2026-11-25", "12:15", rm("rm19-netto4000", 19, "€ 4.000 netto per maand?", ["4.000"], "€ 4.000 netto overhouden? Reken mee!", UUR,
   [["Netto per maand", "€ 4.000"], ["Kosten per jaar", "€ 6.000"], ["Verzekering + pensioen", "€ 550 p/m"], ["Werkuren per week", "40"], ["Deel factureerbaar", "70%"]],
   dict(label="MINIMAAL PER UUR", num=63, pre="€ ", post="", sub="excl. btw · 1.232 factureerbare uren"),
   "Voor € 3.000 netto is het € 44. € 1.000 netto méér = € 19 per uur méér!", VU),
  "€ 4.000 netto per maand overhouden? Dan vraag je minimaal € 63 per uur. Voor € 3.000 netto is dat € 44." + TAGS_RM + " #uurtarief"),
 ("2026-11-25", "17:45", quiz("quiz5-kor", "MYTHE OF FEIT?", "Onder € 20.000 omzet hoef je nooit btw af te dragen.", "MYTHE",
   ["Alleen met de KOR", "Per 1 januari meedoen?", "Uiterlijk 3 december"], ["nooit"], *CTA),
  "Mythe of feit? Onder € 20.000 omzet hoef je nooit btw af te dragen 👇 Alleen met de KOR, en die vraag je zelf aan. Per 1 januari meedoen? Dan moet je aanmelding uiterlijk 3 december binnen zijn. #kor #btw #mytheoffeit " + H),
 ("2026-11-26", "17:45", kies("kies6-voorlopige-aanslag", "WAT DOE JIJ?", "Belasting betalen. Hoe doe jij het?", "Elke maand een vast bedrag", "Alles in één keer achteraf", "Reageer A of B ↓", ["jij"], *CTA),
  "Belasting betalen: elke maand een beetje via een voorlopige aanslag, of alles in één keer achteraf? A of B 👇 #voorlopigeaanslag #belasting " + H),
 ("2026-11-27", "12:15", rm("rm20-auto-elektrisch", 20, "Elektrische auto op de zaak?", ["Elektrische"], "Elektrisch, € 45.000, 6.000 privé-km? Reken mee!", AUTO,
   [["Cataloguswaarde", "€ 45.000"], ["Autokosten per jaar", "€ 8.000"], ["Zakelijke km", "25.000"], ["Privé km", "6.000"], ["Winst zonder auto", "€ 70.000"]],
   dict(label="PRIVÉ RIJDEN", num=2877, pre="€ ", post="", sub="voordeliger per jaar"),
   "Op de zaak kost hij je € 8.053 per jaar, privé € 5.176. Ook elektrisch telt de bijtelling!", "Voorbeeld 2026 · elektrische auto · indicatie"),
  "Elektrische auto op de zaak? Bij € 45.000 en 6.000 privé-km is privé rijden hier € 2.877 per jaar voordeliger." + TAGS_RM + " #autovandezaak #elektrischrijden #bijtelling"),
 ("2026-11-27", "17:45", jaareinde("jaareinde-34", 34, ["Klopt je voorlopige aanslag nog?", "Meer winst? Pas hem nu aan", "Zo voorkom je belastingrente"]),
  "Nog 34 dagen in 2026. Klopt jouw voorlopige aanslag nog? 👇 #voorlopigeaanslag #jaareinde " + H),
 ("2026-11-28", "17:45", quotes("qs4-black-friday", "ZZP-HUMOR", "Zzp'ers op Black Friday",
   ["Het is zakelijk, dus eigenlijk gratis.", "Ik koop het voor de aftrek.", "De bon? Die zit vast in mijn mail.", "Volgend jaar heb ik dit echt nodig."], ["Black", "Friday"],
   "Herkenbaar? Tag een collega ↓", "Twijfel je over een aankoop? hhservices.nl/actie"),
  "Zzp'ers op Black Friday 😅 Welke herken jij? Tag een collega 👇 #blackfriday #zzphumor " + H),
 ("2026-11-29", "17:45", vraag("vraag-van-de-week-6", "VRAAG VAN DE WEEK", "Hoeveel uur per week ben jij kwijt aan je administratie?", "Wij rekenen uit wat dat jou kost.", "Reageer hieronder ↓", ["uur"], *CTA_VRAAG),
  "Vraag van de week: hoeveel uur per week ben jij kwijt aan je administratie? 👇 #vraagvandeweek #tijd " + H),
 ("2026-11-30", "12:15", rm("rm21-vier-dagen", 21, "Vier dagen per week werken?", ["Vier"], "€ 3.000 netto in 32 uur per week? Reken mee!", UUR,
   [["Netto per maand", "€ 3.000"], ["Kosten per jaar", "€ 6.000"], ["Verzekering + pensioen", "€ 550 p/m"], ["Werkuren per week", "32"], ["Deel factureerbaar", "70%"]],
   dict(label="MINIMAAL PER UUR", num=56, pre="€ ", post="", sub="excl. btw · 986 factureerbare uren"),
   "Met 40 uur per week is het € 44. Minder uren = hoger tarief!", VU),
  "Vier dagen per week werken en toch € 3.000 netto? Dan vraag je minimaal € 56 per uur in plaats van € 44." + TAGS_RM + " #uurtarief #vierdaagsewerkweek"),
 ("2026-11-30", "17:45", fouta("fout7-voorlopige-aanslag", 7, "Deze brief negeren kost je geld", ["geld"], "VOORLOPIGE AANSLAG", "€ 2.400", "STOP! Klopt dit nog?",
   ["Meer winst dan geschat?", "Dan betaal je straks bij, plus rente", "Pas je voorlopige aanslag aan", "Dat kan online bij de Belastingdienst"]),
  "De fout van de week #7: je voorlopige aanslag niet aanpassen terwijl je meer verdient. Dan betaal je straks bij, plus rente 👇 #voorlopigeaanslag #belasting " + H),
 ("2026-12-01", "17:45", quote("q8-rust", "MISTER ZEGT", "Een goede administratie geeft rust in je hoofd.", "— Mister Rekenmachine", "Eens? ↓", ["rust"], *CTA),
  "Een goede administratie geeft rust in je hoofd. Eens? 👇 #rust #ondernemen " + H),
 ("2026-12-02", "12:15", rm("rm22-omzet90k", 22, "Goed jaar gedraaid?", ["Goed"], "€ 90.000 omzet, € 15.000 kosten? Reken mee!", BEL,
   [["Omzet dit jaar", "€ 90.000"], ["Zakelijke kosten", "€ 15.000"], ["Winst", "€ 75.000", 1], ["Na aftrekposten", "€ 64.427", 1], ["Belasting + Zvw", "€ 21.876", 1]],
   dict(label="ZET OPZIJ", num=25, pre="", post="%", sub="van elke betaling · € 1.823 per maand"),
   "Tip: vraag een voorlopige aanslag aan. Dan betaal je per maand!", VB),
  "Goed jaar gedraaid? Bij € 90.000 omzet en € 15.000 kosten zet je 25% van elke betaling opzij, zo'n € 1.823 per maand." + TAGS_RM + " #belasting #voorlopigeaanslag"),
 ("2026-12-02", "17:45", quiz("quiz6-lijfrente", "MYTHE OF FEIT?", "Als zzp'er kun je niets aan je pensioen doen.", "MYTHE",
   ["Je bouwt zelf pensioen op", "Lijfrente kan aftrekbaar zijn", "Binnen je jaarruimte"], ["niets"], *CTA),
  "Mythe of feit? Als zzp'er kun je niets aan je pensioen doen 👇 #lijfrente #pensioen #mytheoffeit " + H),
 ("2026-12-03", "17:45", kies("kies7-pakjesavond", "WAT DOE JIJ?", "Pakjesavond! Wat zit er in jouw schoen?", "Een nieuwe laptop (zakelijk)", "Een stapel bonnetjes", "Reageer A of B ↓", ["schoen?"], *CTA),
  "Pakjesavond! Wat zit er in jouw schoen? A of B 👇 #sinterklaas #zzphumor " + H),
 ("2026-12-04", "12:15", rm("rm23-factureerbaar", 23, "Veel uren die je niet kunt factureren?", ["niet"], "Maar de helft van je uren factureerbaar? Reken mee!", UUR,
   [["Netto per maand", "€ 3.000"], ["Kosten per jaar", "€ 6.000"], ["Verzekering + pensioen", "€ 550 p/m"], ["Werkuren per week", "40"], ["Deel factureerbaar", "50%"]],
   dict(label="MINIMAAL PER UUR", num=62, pre="€ ", post="", sub="excl. btw · 880 factureerbare uren"),
   "Bij 70% factureerbaar is het € 44. Onbetaalde uren tellen mee!", VU),
  "Maar de helft van je uren factureerbaar? Dan vraag je voor € 3.000 netto minimaal € 62 per uur in plaats van € 44." + TAGS_RM + " #uurtarief"),
 ("2026-12-04", "17:45", jaareinde("jaareinde-27", 27, ["Bonnen van 2026 compleet?", "Mis je een factuur? Vraag hem op", "Zet alles op één plek"]),
  "Nog 27 dagen in 2026. Zijn al je bonnen en facturen compleet? 👇 #bonnetjes #jaareinde " + H),
 ("2026-12-05", "17:45", quotes("qs5-sinterklaas", "ZZP-HUMOR", "Als Sinterklaas zzp'er was",
   ["Pakjes? Eerst een offerte.", "De stoomboot: zakelijk of privé?", "Pieten in dienst? Loonaangifte doen!", "Mag een gedicht ook als factuur?"], ["Sinterklaas"],
   "Welke mist er nog? ↓", "Fijne pakjesavond! hhservices.nl/actie"),
  "Als Sinterklaas zzp'er was 🎁 Welke mist er nog? 👇 #sinterklaas #zzphumor " + H),
 ("2026-12-06", "17:45", vraag("vraag-van-de-week-7", "VRAAG VAN DE WEEK", "Wat wil jij weten over de jaarafsluiting?", "Wij beantwoorden de vaakst gestelde vraag.", "Reageer hieronder ↓", ["jaarafsluiting?"], *CTA_VRAAG),
  "Vraag van de week: wat wil jij weten over de jaarafsluiting? 👇 #vraagvandeweek #jaareinde " + H),
 ("2026-12-07", "12:15", rm("rm24-starter35k", 24, "Dit jaar gestart?", ["gestart?"], "Starter met € 35.000 omzet? Reken mee!", BEL,
   [["Omzet dit jaar", "€ 35.000"], ["Zakelijke kosten", "€ 5.000"], ["Winst", "€ 30.000", 1], ["Na aftrekposten", "€ 23.289", 1], ["Belasting + Zvw", "€ 1.130", 1]],
   dict(label="ZET OPZIJ", num=4, pre="", post="%", sub="van elke betaling · € 94 per maand"),
   "Zonder startersaftrek betaal je € 1.735. Dat scheelt € 605 per jaar!", "Voorbeeld 2026 · starter, met urencriterium"),
  "Dit jaar gestart? Met startersaftrek zet je bij € 35.000 omzet 4% opzij. Dat scheelt hier € 605 per jaar." + TAGS_RM + " #starter #startersaftrek"),
 ("2026-12-07", "17:45", fouta("fout8-bonnetjes", 8, "Dit bonnetje is straks onleesbaar", ["onleesbaar"], "KASSABON", "€ 84,95", "STOP! Maak een foto!",
   ["Kassabonnen vervagen snel", "Maak direct een foto", "Bewaarplicht: 7 jaar", "Geen bon? Dan geen bewijs"]),
  "De fout van de week #8: bonnetjes in je bus laten liggen tot ze onleesbaar zijn. Zo voorkom je het 👇 #bonnetjes #administratie " + H),
 ("2026-12-08", "17:45", quote("q9-schone-start", "MISTER ZEGT", "Begin 2027 zonder achterstand.", "— Mister Rekenmachine", "Wie doet mee? ↓", ["zonder"], *CTA, dark=True),
  "Begin 2027 zonder achterstand. T/m 31 januari zijn je eerste 2 maanden administratie gratis (bij een jaarabonnement). hhservices.nl/actie #2027 " + H),
 ("2026-12-09", "12:15", rm("rm25-elektrisch-prive", 25, "Veel privé rijden met je EV?", ["privé"], "Elektrisch, € 40.000, 10.000 privé-km? Reken mee!", AUTO,
   [["Cataloguswaarde", "€ 40.000"], ["Autokosten per jaar", "€ 7.000"], ["Zakelijke km", "20.000"], ["Privé km", "10.000"], ["Winst zonder auto", "€ 60.000"]],
   dict(label="PRIVÉ RIJDEN", num=2314, pre="€ ", post="", sub="voordeliger per jaar"),
   "Op de zaak € 7.055 per jaar, privé € 4.741. Reken het altijd even door!", "Voorbeeld 2026 · elektrische auto · indicatie"),
  "Veel privé rijden met je elektrische auto? Bij € 40.000 en 10.000 privé-km is privé rijden hier € 2.314 per jaar voordeliger." + TAGS_RM + " #autovandezaak #elektrischrijden"),
 ("2026-12-09", "17:45", quiz("quiz7-bv", "MYTHE OF FEIT?", "Met een bv betaal je altijd minder belasting.", "MYTHE",
   ["Bv loont pas bij hoge winst", "Een bv kost extra geld", "Laat het doorrekenen"], ["altijd"], *CTA),
  "Mythe of feit? Met een bv betaal je altijd minder belasting 👇 #bv #mytheoffeit #belasting " + H),
 ("2026-12-10", "17:45", kies("kies8-kerstpakket", "WAT DOE JIJ?", "Personeel in dienst. Wat geef jij met kerst?", "Een kerstpakket", "Een cadeaubon", "Reageer A of B ↓", ["kerst?"], *CTA),
  "Personeel in dienst? Wat geef jij met kerst: A of B? 👇 Tip: het valt vaak in de vrije ruimte van de werkkostenregeling. #kerstpakket #werkgever #personeel " + H),
 ("2026-12-11", "12:15", rm("rm26-pensioen", 26, "Zelf pensioen opbouwen?", ["pensioen"], "€ 600 per maand pensioen? Reken mee!", UUR,
   [["Netto per maand", "€ 3.000"], ["Kosten per jaar", "€ 6.000"], ["Verzekering + pensioen", "€ 850 p/m"], ["Werkuren per week", "40"], ["Deel factureerbaar", "70%"]],
   dict(label="MINIMAAL PER UUR", num=48, pre="€ ", post="", sub="excl. btw · 1.232 factureerbare uren"),
   "Met € 300 pensioen is het € 44. Reken je pensioen mee in je tarief!", VU),
  "Zelf pensioen opbouwen? Met € 600 per maand pensioen vraag je voor € 3.000 netto minimaal € 48 per uur." + TAGS_RM + " #pensioen #uurtarief"),
 ("2026-12-11", "17:45", jaareinde("jaareinde-20", 20, ["Kerstpakket? Werkkostenregeling", "Investering nodig? Vóór 31 dec", "Uren van 2026 bijgewerkt?"]),
  "Nog 20 dagen in 2026. Dit regel je nog vóór de feestdagen 👇 #jaareinde #werkgever " + H),
 ("2026-12-12", "17:45", quotes("qs6-kerstborrel", "ZZP-HUMOR", "Zzp'ers op de kerstborrel",
   ["Druk? Vooral met mijn administratie.", "Wat ik doe? Eigenlijk alles.", "Vakantie? Wat is dat?", "Mijn beste collega is een rekenmachine."], ["kerstborrel"],
   "Herkenbaar? Tag een collega ↓", "Meer tijd in 2027? hhservices.nl/actie"),
  "Zzp'ers op de kerstborrel 🎄 Welke herken jij? 👇 #kerstborrel #zzphumor " + H),
 ("2026-12-13", "17:45", vraag("vraag-van-de-week-8", "VRAAG VAN DE WEEK", "Wat neem jij je voor in 2027 voor je bedrijf?", "Wij helpen je het waar te maken.", "Reageer hieronder ↓", ["2027"], *CTA_VRAAG),
  "Vraag van de week: wat neem jij je voor in 2027 voor je bedrijf? 👇 #vraagvandeweek #2027 " + H),
]
plan = []
for datum, tijd, v, cap in P:
    json.dump(v, open(os.path.join(out, v["slug"] + ".json"), "w"), ensure_ascii=False)
    eng = {"rekenmee": "rekenmee", "fout": "fout_actie"}.get(v.get("type"), "interactie")
    plan.append(dict(datum=datum, tijd=tijd, slug=v["slug"], engine=eng, caption=cap))
json.dump(plan, open(os.path.join(out, "planning-b3.json"), "w"), ensure_ascii=False, indent=1)
print(len(plan), "video's")
