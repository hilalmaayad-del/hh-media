#!/usr/bin/env python3
"""Schermopname-stijl: echte rekentool van hhservices.nl in een telefoon, met tikjes, typen en zoom op de uitkomst.
Gebruik: python3 schermopname.py <script.json> <uit.mp4>   (site lokaal op http://localhost:8765)"""
import json, sys, io, math, os, subprocess, wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_video import mix, SR
from playwright.sync_api import sync_playwright
W,H,FPS=1080,1920,30
FD=os.path.join(os.path.dirname(os.path.abspath(__file__)),"fonts")
F=lambda n,s:ImageFont.truetype(os.path.join(FD,n),s)
INK=(18,18,18);OK=(227,160,42);CR=(243,235,221);RED=(214,64,52)
fH=F("archivo-900.ttf",84);fC=F("archivo-900.ttf",70);fM=F("jbmono-700.ttf",36);fL=F("archivo-900.ttf",58);fS=F("jbmono-700.ttf",30)
S=json.load(open(sys.argv[1],encoding="utf-8"));out=sys.argv[2]
VW,VH,DPR=390,780,2
SX,SY,SW=270,700,540; SH=int(SW*VH/VW)   # schermpositie in video
ease=lambda x:(lambda x:1-(1-x)**3)(max(0,min(1,x)))
# ---------- 1. opnemen
states=[]  # dict(img, dur, cap, tap, zoom, sfx)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={"width":VW,"height":VH},device_scale_factor=DPR)
    pg.goto("http://localhost:8765"+S["pad"]);pg.wait_for_timeout(900)
    pg.add_style_tag(content="html{scroll-behavior:auto!important}")
    snap=lambda:Image.open(io.BytesIO(pg.screenshot())).convert("RGB")
    sy=lambda:pg.evaluate("window.scrollY")
    def scroll_to(y,cap,dur=0.6,zoom=None):
        y0=sy()
        n=max(2,int(dur*FPS/2))
        for i in range(1,n+1):
            pg.evaluate(f"window.scrollTo(0,{y0+(y-y0)*ease(i/n)})");pg.wait_for_timeout(30)
            states.append(dict(img=snap(),dur=2/FPS,cap=cap,zoom=zoom))
    def box(sel):
        bb=pg.locator(sel).first.bounding_box();return bb
    states.append(dict(img=snap(),dur=S.get("intro",2.6),cap=None,zoom=None,sfx="pop"))
    for st in S["stappen"]:
        cap=st.get("cap")
        if "scroll" in st:
            bb=pg.locator(st["scroll"]).first.bounding_box();target=max(0,sy()+bb["y"]-st.get("marge",120))
            scroll_to(target,cap)
        if st.get("type"):
            sel=st["sel"];bb=box(sel);tap=(bb["x"]+bb["width"]/2,bb["y"]+bb["height"]/2)
            pg.click(sel);pg.keyboard.press("Control+A");pg.keyboard.press("Backspace");pg.wait_for_timeout(60)
            zt=(tap[0],tap[1],1.7);states.append(dict(img=snap(),dur=0.45,cap=cap,tap=tap,zoom=zt,sfx="pop"))
            for ch in st["type"]:
                pg.keyboard.type(ch);pg.wait_for_timeout(40);states.append(dict(img=snap(),dur=0.13,cap=cap,zoom=zt,sfx="key"))
            pg.keyboard.press("Tab");pg.wait_for_timeout(80);states.append(dict(img=snap(),dur=st.get("hold",0.7),cap=cap,zoom=zt))
        if st.get("klik"):
            bb=box(st["klik"]);tap=(bb["x"]+bb["width"]/2,bb["y"]+bb["height"]/2);pg.click(st["klik"]);pg.wait_for_timeout(80)
            states.append(dict(img=snap(),dur=st.get("hold",0.9),cap=cap,tap=tap,sfx="pop"))
        if st.get("zoom"):
            bb=box(st["zoom"]);z=(bb["x"]+bb["width"]/2,bb["y"]+bb["height"]/2,st.get("z",2.0))
            fb=box(st.get("focus",st["zoom"]))
            states.append(dict(img=snap(),dur=st.get("hold",2.5),cap=cap,zoom=z,sfx="ching",focus=fb))
        if st.get("wacht"):
            states.append(dict(img=snap(),dur=st["wacht"],cap=cap,zoom=states[-1].get("zoom")))
    b.close()
# ---------- 2. samenstellen
bgimg=Image.new("RGB",(W,H),CR);gd=ImageDraw.Draw(bgimg)
for i in range(0,W,60): gd.line([(i,0),(i,H)],fill=(234,224,206),width=2)
for j in range(0,H,60): gd.line([(0,j),(W,j)],fill=(234,224,206),width=2)
def wrap(d,t,f,mw):
    o=[];c=""
    for w in t.split(" "):
        x=(c+" "+w).strip()
        if d.textlength(x,font=f)<=mw:c=x
        else:o.append(c);c=w
    if c:o.append(c)
    return o
def head(d,t,dark=False):
    d.text((72,96),"HH",font=fL,fill=CR if dark else INK);x=72+d.textlength("HH ",font=fL);bb=d.textbbox((x,96),"Services",font=fL)
    d.rounded_rectangle([bb[0]-10,bb[1]-8,bb[2]+10,bb[3]+10],8,fill=INK);d.text((x,96),"Services",font=fL,fill=OK)
    lab=S["label"];tw=d.textlength(lab,font=fM);d.rounded_rectangle([72,200,72+tw+56,268],34,fill=RED);d.text((100,212),lab,font=fM,fill=(255,255,255))
def phone(base,img,zoom,tap,tapage,ring):
    scr=img;x0,y0,w,h=0,0,img.width,img.height
    if zoom:
        cx,cy,z=zoom;cx*=DPR;cy*=DPR;w=img.width/z;h=img.height/z
        x0=min(max(0,cx-w/2),img.width-w);y0=min(max(0,cy-h/2),img.height-h)
        scr=img.crop((int(x0),int(y0),int(x0+w),int(y0+h)))
    scr=scr.resize((SW,SH),Image.LANCZOS)
    sh=Image.new("RGBA",(W,H),(0,0,0,0));sd=ImageDraw.Draw(sh);sd.rounded_rectangle([SX-26,SY-26+18,SX+SW+26,SY+SH+26+18],70,fill=(0,0,0,90))
    sh=sh.filter(ImageFilter.GaussianBlur(22));base.paste(sh,(0,0),sh)
    d=ImageDraw.Draw(base);d.rounded_rectangle([SX-26,SY-26,SX+SW+26,SY+SH+26],70,fill=(20,20,20))
    m=Image.new("L",(SW,SH),0);ImageDraw.Draw(m).rounded_rectangle([0,0,SW,SH],48,fill=255);base.paste(scr,(SX,SY),m)
    d.rounded_rectangle([SX+SW//2-70,SY+14,SX+SW//2+70,SY+44],15,fill=(20,20,20))
    if tap and tapage<0.6:
        tx=SX+(tap[0]*DPR-x0)/w*SW;ty=SY+(tap[1]*DPR-y0)/h*SH;r=30+tapage*90;a=int(200*(1-tapage/0.6))
        ov=Image.new("RGBA",(W,H),(0,0,0,0));od=ImageDraw.Draw(ov)
        od.ellipse([tx-34,ty-34,tx+34,ty+34],fill=(227,160,42,min(200,a+60)));od.ellipse([tx-r,ty-r,tx+r,ty+r],outline=(227,160,42,a),width=8)
        base.paste(ov,(0,0),ov)
    if ring:
        d.rounded_rectangle([SX-10,SY+SH//2-ring,SX+SW+10,SY+SH//2+ring],30,outline=RED,width=10)
ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",out+".wav",
  "-c:v","libx264","-pix_fmt","yuv420p","-crf","18","-preset","medium","-af","loudnorm=I=-14:TP=-1.5:LRA=11","-ar","44100","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",out],stdin=subprocess.PIPE)
# tijdlijn
t=0;ev=[];tl=[]
for s in states:
    tl.append((t,s));
    if s.get("sfx"):ev.append([round(t,2),s["sfx"]])
    t+=s["dur"]
t_end=t;punch=S["punch"];tP=t_end;tC=tP+S.get("punchduur",3.0);total=tC+3.2
ev+= [[tP,"lever"],[tC,"lever"],[tC+0.4,"ching"]]
with wave.open(out+".wav","wb") as w: w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(mix(total,sorted(ev)))
prevzoom=None;zoomcur=None;si=0
n=int(total*FPS)
for i in range(n):
    tt=i/FPS
    if tt<tP:
        while si+1<len(tl) and tl[si+1][0]<=tt: si+=1
        t0,s=tl[si];age=tt-t0
        base=bgimg.copy();d=ImageDraw.Draw(base);head(d,tt)
        # zoom interpolatie
        z=s.get("zoom")
        if z:
            pz=None
            for j in range(si-1,-1,-1):
                if tl[j][1].get("zoom")!=z: pz=tl[j][1].get("zoom");break
            # start van deze zoom
            js=si
            while js>0 and tl[js-1][1].get("zoom")==z: js-=1
            a=ease((tt-tl[js][0])/0.5)
            zz=(z[0],z[1],1+(z[2]-1)*a)
        else: zz=None
        cap=s.get("cap") or S["haak"]
        f=fH if s.get("cap") is None else fC
        lines=wrap(d,cap,f,W-150);y=310
        for ln in lines:
            x=72
            for wd in ln.split(" "):
                red=wd.lower().strip("?!.,") in S.get("rood",[])
                d.text((x,y),wd,font=f,fill=RED if red else INK);x+=d.textlength(wd+" ",font=f)
            y+=int(f.size*1.08)
        phone(base,s["img"],zz,s.get("tap"),age,None)
    elif tt<tC:
        pt=tt-tP;base=Image.new("RGB",(W,H),INK);d=ImageDraw.Draw(base);head(d,tt,True)
        last=tl[-1][1];img=last["img"];fb=last.get("focus")
        if fb:
            pd=14;crop=img.crop((int((fb["x"]-pd)*DPR),int((fb["y"]-pd)*DPR),int((fb["x"]+fb["width"]+pd)*DPR),int((fb["y"]+fb["height"]+pd+S.get("focus_extra",0))*DPR)))
        else: crop=img
        cw=W-144;ch=int(crop.height*cw/crop.width);ch=min(ch,900);sc=0.85+0.15*ease(pt/0.5);crop=crop.resize((int(cw*sc),int(ch*sc)),Image.LANCZOS);cw,ch=crop.size
        m=Image.new("L",crop.size,0);ImageDraw.Draw(m).rounded_rectangle([0,0,cw,ch],36,fill=255);base.paste(crop,(W//2-cw//2,1150-ch//2),m)
        a=ease(pt/0.4);lines=wrap(d,punch,fC,W-150);y=330+int((1-a)*60)
        for ln in lines: d.text((72,y),ln,font=fC,fill=tuple(int(INK[c]+(CR[c]-INK[c])*a) for c in range(3)));y+=78
        d.text((72,1800),S.get("disc",""),font=fS,fill=(150,140,120))
    else:
        ct=tt-tC;base=Image.new("RGB",(W,H),OK);d=ImageDraw.Draw(base)
        d.text((72,96),"HH",font=fL,fill=INK);x=72+d.textlength("HH ",font=fL);bb=d.textbbox((x,96),"Services",font=fL)
        d.rounded_rectangle([bb[0]-10,bb[1]-8,bb[2]+10,bb[3]+10],8,fill=INK);d.text((x,96),"Services",font=fL,fill=OK)
        a=ease(ct/0.4);d.text((72,700+int((1-a)*80)),"Reken het zelf uit",font=F("archivo-900.ttf",104),fill=INK)
        sc=0.9+0.1*ease((ct-0.3)/0.4)+0.03*math.sin(ct*6);k="hhservices.nl/tools";fb=F("archivo-900.ttf",int(64*sc))
        bw=d.textlength(k,font=fb)+96;d.rounded_rectangle([72,900,72+bw,900+int(124*sc)],int(62*sc),fill=INK);d.text((120,900+int(28*sc)),k,font=fb,fill=OK)
        d.text((72,1090),"Gratis · zonder inloggen",font=F("jbmono-700.ttf",44),fill=INK)
        d.text((72,1160),"Reken mee · elke ma, wo en vr",font=fS,fill=(90,61,8))
    ff.stdin.write(base.tobytes())
ff.stdin.close();ff.wait();os.remove(out+".wav");print(out,round(total,1),"s")
