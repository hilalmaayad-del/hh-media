import json
V=[
 dict(slug="rm1-uurtarief",label="REKEN MEE #1",haak="Vraag jij genoeg per uur?",rood=["genoeg"],
  vraag="Je wilt € 3.000 netto per maand. Reken mee!",titel="UURTARIEF BEREKENEN",
  rijen=[["Netto per maand","€ 3.000"],["Kosten per jaar","€ 6.000"],["Verzekering + pensioen","€ 550 p/m"],["Werkuren per week","40"],["Deel factureerbaar","70%"]],
  uitkomst=dict(label="MINIMAAL PER UUR",num=44,pre="€ ",post="",sub="excl. btw · 1.232 factureerbare uren"),
  punch="Reken je met álle uren, dan kom je op € 31. Dat is € 13 per uur te weinig!",
  disc="Voorbeeldberekening 2026 · indicatie"),
 dict(slug="rm2-belasting",label="REKEN MEE #2",haak="Hoeveel belasting moet jij opzijzetten?",rood=["belasting"],
  vraag="€ 60.000 omzet dit jaar? Reken mee!",titel="BELASTING OPZIJZETTEN",
  rijen=[["Omzet dit jaar","€ 60.000"],["Zakelijke kosten","€ 8.000"],["Winst","€ 52.000",1],["Na aftrekposten","€ 44.348",1],["Belasting + Zvw","€ 10.578",1]],
  uitkomst=dict(label="ZET OPZIJ",num=18,pre="",post="%",sub="van elke betaling · € 882 per maand"),
  punch="Zet 18% van elke betaling apart. En de btw zet je daar nog bovenop apart!",
  disc="Voorbeeld 2026 · met urencriterium, geen starter"),
 dict(slug="rm3-auto",label="REKEN MEE #3",haak="Auto op de zaak? Niet altijd slimmer",rood=["niet"],
  vraag="Auto van € 40.000 en veel privé rijden? Reken mee!",titel="AUTO ZAAK OF PRIVÉ",
  rijen=[["Cataloguswaarde","€ 40.000"],["Autokosten per jaar","€ 9.000"],["Zakelijke km","15.000"],["Privé km","8.000"],["Winst zonder auto","€ 60.000"]],
  uitkomst=dict(label="PRIVÉ RIJDEN",num=921,pre="€ ",post="",sub="voordeliger per jaar"),
  punch="Op de zaak kost hij je € 8.226 per jaar, privé € 7.305. Die bijtelling hakt erin!",
  disc="Voorbeeld 2026 · benzineauto · indicatie"),
]
for v in V:
    for k in ('vraag','punch'): v[k]=v[k].replace('€ ','€\u00a0')
    T=dict(**{"in":3.2,"rij":0.85}); T["res"]=T["in"]+0.45+5*T["rij"]+0.4; T["punch"]=T["res"]+2.8; T["cta"]=T["punch"]+4.2
    total=round(T["cta"]+3.4,2)
    ev=[[0.05,"pop"],[0.6,"pop"],[T["in"],"lever"]]
    for i in range(5):
        st=T["in"]+0.45+i*T["rij"]
        for k in range(4): ev.append([round(st+0.1+k*0.1,2),"key"])
    for k in range(8): ev.append([round(T["res"]+0.2+k*0.14,2),"tick"])
    ev+= [[T["res"],"print"],[T["res"]+1.3,"ching"],[T["punch"]+0.3,"pop"],[T["cta"],"lever"],[T["cta"]+0.4,"ching"]]
    v.update(cta="Reken het zelf uit",T=T,total=total,events=sorted(ev))
    json.dump(v,open(v["slug"]+".json","w"),ensure_ascii=False)
    print(v["slug"],total)
