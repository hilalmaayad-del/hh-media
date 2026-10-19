#!/usr/bin/env python3
"""Reken mee #4-#8 (20-31 okt 2026). Cijfers uitgerekend met de echte tools op hhservices.nl/tools (20-10-2026)."""
import json,os,sys
out=sys.argv[1]
V=[
 dict(slug="rm4-netto4000",label="REKEN MEE #4",haak="Wil jij € 4.000 netto per maand?",rood=["netto"],
  vraag="€ 4.000 netto per maand overhouden? Reken mee!",titel="UURTARIEF BEREKENEN",
  rijen=[["Netto per maand","€ 4.000"],["Kosten per jaar","€ 6.000"],["Verzekering + pensioen","€ 550 p/m"],["Werkuren per week","40"],["Deel factureerbaar","70%"]],
  uitkomst=dict(label="MINIMAAL PER UUR",num=63,pre="€ ",post="",sub="excl. btw · 1.232 factureerbare uren"),
  punch="Voor € 3.000 netto was het € 44. Elke € 1.000 netto extra kost je € 19 per uur méér!",
  disc="Voorbeeldberekening 2026 · indicatie"),
 dict(slug="rm5-omzet40k",label="REKEN MEE #5",haak="Minder omzet? Dan zet je minder opzij",rood=["minder"],
  vraag="€ 40.000 omzet dit jaar? Reken mee!",titel="BELASTING OPZIJZETTEN",
  rijen=[["Omzet dit jaar","€ 40.000"],["Zakelijke kosten","€ 5.000"],["Winst","€ 35.000",1],["Na aftrekposten","€ 29.507",1],["Belasting + Zvw","€ 3.410",1]],
  uitkomst=dict(label="ZET OPZIJ",num=9,pre="",post="%",sub="van elke betaling · € 284 per maand"),
  punch="Bij € 60.000 omzet was het 18%. Je percentage groeit mee met je winst!",
  disc="Voorbeeld 2026 · met urencriterium, geen starter"),
 dict(slug="rm6-vier-dagen",label="REKEN MEE #6",haak="Vier dagen werken? Reken even mee",rood=["Vier"],
  vraag="€ 3.000 netto, maar 32 uur per week? Reken mee!",titel="UURTARIEF BEREKENEN",
  rijen=[["Netto per maand","€ 3.000"],["Kosten per jaar","€ 6.000"],["Verzekering + pensioen","€ 550 p/m"],["Werkuren per week","32"],["Deel factureerbaar","70%"]],
  uitkomst=dict(label="MINIMAAL PER UUR",num=56,pre="€ ",post="",sub="excl. btw · 986 factureerbare uren"),
  punch="Bij vijf dagen is het € 44. Een dag minder werken = € 12 per uur méér vragen!",
  disc="Voorbeeldberekening 2026 · indicatie"),
 dict(slug="rm7-goed-jaar",label="REKEN MEE #7",haak="Goed jaar gedraaid? Schrik niet",rood=["Schrik"],
  vraag="€ 85.000 omzet dit jaar? Reken mee!",titel="BELASTING OPZIJZETTEN",
  rijen=[["Omzet dit jaar","€ 85.000"],["Zakelijke kosten","€ 15.000"],["Winst","€ 70.000",1],["Na aftrekposten","€ 60.062",1],["Belasting + Zvw","€ 19.420",1]],
  uitkomst=dict(label="ZET OPZIJ",num=23,pre="",post="%",sub="van elke betaling · € 1.618 per maand"),
  punch="Bijna een kwart van elke betaling is niet van jou. En de btw komt er nog bovenop!",
  disc="Voorbeeld 2026 · met urencriterium, geen starter"),
 dict(slug="rm8-veel-zakelijk",label="REKEN MEE #8",haak="Veel zakelijke km? Toch geen zaakauto",rood=["geen"],
  vraag="25.000 zakelijke km per jaar? Reken mee!",titel="AUTO ZAAK OF PRIVÉ",
  rijen=[["Cataloguswaarde","€ 28.000"],["Autokosten per jaar","€ 8.000"],["Zakelijke km","25.000"],["Privé km","2.000"],["Winst zonder auto","€ 60.000"]],
  uitkomst=dict(label="PRIVÉ RIJDEN",num=1190,pre="€ ",post="",sub="voordeliger per jaar"),
  punch="Op de zaak kost hij je € 6.366 per jaar, privé € 5.176. Reken het altijd even na!",
  disc="Voorbeeld 2026 · benzineauto · indicatie"),
]
for v in V:
    for k in ('vraag','punch'): v[k]=v[k].replace('€ ','€ ')
    T=dict(**{"in":3.2,"rij":0.85}); T["res"]=T["in"]+0.45+5*T["rij"]+0.4; T["punch"]=T["res"]+2.8; T["cta"]=T["punch"]+4.2
    total=round(T["cta"]+3.4,2)
    ev=[[0.05,"pop"],[0.6,"pop"],[T["in"],"lever"]]
    for i in range(5):
        st=T["in"]+0.45+i*T["rij"]
        for k in range(4): ev.append([round(st+0.1+k*0.1,2),"key"])
    for k in range(8): ev.append([round(T["res"]+0.2+k*0.14,2),"tick"])
    ev+=[[T["res"],"print"],[T["res"]+1.3,"ching"],[T["punch"]+0.3,"pop"],[T["cta"],"lever"],[T["cta"]+0.4,"ching"]]
    v.update(cta="Reken het zelf uit",T=T,total=total,events=sorted(ev))
    json.dump(v,open(os.path.join(out,v["slug"]+".json"),"w"),ensure_ascii=False)
print(len(V))
