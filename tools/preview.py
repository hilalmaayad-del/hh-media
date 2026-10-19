#!/usr/bin/env python3
"""Snelle preview: rendert N momenten van een JS-video naar één contactsheet. preview.py <pagina> <data.json> <uit.png> [n]"""
import json,sys,io,os
from PIL import Image
from playwright.sync_api import sync_playwright
page,dp,out=sys.argv[1:4];n=int(sys.argv[4]) if len(sys.argv)>4 else 12
d=json.load(open(dp,encoding="utf-8"));tot=d["total"]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={"width":1080,"height":1920})
    pg.add_init_script("window.DATA="+json.dumps(d,ensure_ascii=False)+";");pg.goto("file://"+os.path.abspath(page));pg.evaluate("document.fonts.ready");pg.wait_for_timeout(300)
    ims=[]
    for i in range(n):
        t=tot*(i+0.5)/n;pg.evaluate(f"render({t})");ims.append(Image.open(io.BytesIO(pg.screenshot())).resize((270,480)))
    b.close()
cols=6;rows=(n+cols-1)//cols;sh=Image.new("RGB",(270*cols,480*rows),"white")
for i,im in enumerate(ims):sh.paste(im,((i%cols)*270,(i//cols)*480))
sh.save(out);print(out)
