#!/usr/bin/env python3
"""Nanling Illustration Engine: procedural SVGs + image optimization + catalog."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, html, json, re, shutil
from PIL import Image, ImageOps

ROOT=Path(__file__).resolve().parent
INBOX=ROOT/"assets"/"inbox"
GENERATED=ROOT/"generated"
SITE=ROOT/"site"
OUT=SITE/"assets"
BG,PANEL,TEAL,GOLD,TEXT,MUTED="#0b1425","#14243a","#63c9c3","#d8b96e","#edf2f7","#a9b7c9"

def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-") or "illustration"

def svg(title,body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
<defs><radialGradient id="bg"><stop stop-color="{PANEL}"/><stop offset="1" stop-color="{BG}"/></radialGradient><linearGradient id="gold"><stop stop-color="{GOLD}"/><stop offset="1" stop-color="#94733c"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<rect width="100%" height="100%" fill="url(#bg)"/><g opacity=".18" fill="none" stroke="{TEAL}"><circle cx="1280" cy="150" r="230"/><circle cx="1280" cy="150" r="300"/><path d="M0 740 Q500 550 1000 760 T1600 620"/></g>
<text x="90" y="105" fill="{GOLD}" font-family="Georgia,serif" font-size="30" letter-spacing="7">NANLING DAOZANG · SCIENCE ATLAS</text><text x="90" y="190" fill="{TEXT}" font-family="Georgia,serif" font-size="58">{html.escape(title)}</text>{body}</svg>'''

def generate_all():
    GENERATED.mkdir(parents=True,exist_ok=True)
    planet=f'''<g transform="translate(800 520)"><circle r="245" fill="#245d78" stroke="{TEAL}" stroke-width="8" filter="url(#glow)"/><path d="M-220 -30 Q-90 -160 20 -70 T220 -110 L220 20 Q80 90 -30 30 T-220 100Z" fill="#4d9a86" opacity=".9"/><path d="M-220 70 Q-80 10 30 90 T220 60" fill="none" stroke="#d9e8ee" stroke-width="22" opacity=".5"/><ellipse rx="340" ry="90" fill="none" stroke="url(#gold)" stroke-width="5" transform="rotate(-18)"/></g><text x="90" y="820" fill="{MUTED}" font-size="28">Concept illustration · not observational data</text>'''
    (GENERATED/"earth-like-planet.svg").write_text(svg("Earth-like Planet",planet),encoding="utf-8")
    cards=""
    for i,(roman,label) in enumerate([("I","Planetary"),("II","Stellar"),("III","Galactic")]):
        x=180+i*430
        cards+=f'<rect x="{x}" y="300" width="340" height="330" rx="26" fill="{PANEL}" stroke="{GOLD}" stroke-width="3"/><text x="{x+170}" y="450" text-anchor="middle" fill="{GOLD}" font-size="90">{roman}</text><text x="{x+170}" y="535" text-anchor="middle" fill="{TEXT}" font-size="30">{label}</text>'
    (GENERATED/"kardashev-scale.svg").write_text(svg("Kardashev Civilization Scale",cards+f'<text x="180" y="760" fill="{MUTED}" font-size="27">Conceptual scale · boundaries depend on convention</text>'),encoding="utf-8")
    flow=f'''<g fill="none" stroke="{TEAL}" stroke-width="5"><rect x="150" y="340" width="320" height="210" rx="24"/><rect x="640" y="340" width="320" height="210" rx="24"/><rect x="1130" y="340" width="320" height="210" rx="24"/><path d="M470 445 H640 M960 445 H1130" stroke="{GOLD}"/><path d="M615 420 L640 445 L615 470 M1105 420 L1130 445 L1105 470"/></g><g fill="{TEXT}" font-size="34" text-anchor="middle"><text x="310" y="460">Input</text><text x="800" y="460">Process</text><text x="1290" y="460">Output</text></g><text x="150" y="760" fill="{MUTED}" font-size="27">Conceptual technology flow · verify technical details separately</text>'''
    (GENERATED/"technology-flow.svg").write_text(svg("Technology Evolution",flow),encoding="utf-8")
    return "Generated 3 procedural SVG illustrations."

def build():
    OUT.mkdir(parents=True,exist_ok=True); records=[]
    for src in sorted(GENERATED.glob("*.svg")):
        shutil.copy2(src,OUT/src.name)
        title=src.stem.replace("-"," ").title()
        records.append({"title":title,"category":"generated","file":src.name,"thumbnail":src.name,"alt":title,"description":"Procedural concept illustration; not observational data.","source":"Nanling Illustration Engine"})
    for src in sorted(INBOX.iterdir()):
        if src.suffix.lower() not in {".png",".jpg",".jpeg",".webp"}: continue
        side=src.with_suffix(".json"); meta=json.loads(side.read_text(encoding="utf-8")) if side.exists() else {}
        name=slug(meta.get("title",src.stem)); im=ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        im.thumbnail((2400,2400),Image.Resampling.LANCZOS)
        full=f"{name}.webp"; thumb=f"{name}-thumb.webp"
        im.save(OUT/full,"WEBP",quality=88,method=6)
        small=im.copy(); small.thumbnail((720,720),Image.Resampling.LANCZOS); small.save(OUT/thumb,"WEBP",quality=82,method=6)
        records.append({"title":meta.get("title",src.stem),"category":meta.get("category","artwork"),"file":full,"thumbnail":thumb,"alt":meta.get("alt",meta.get("title",src.stem)),"description":meta.get("description",""),"creator":meta.get("creator",""),"license":meta.get("license","Not specified"),"tags":meta.get("tags",[]),"source":"Imported artwork"})
    SITE.mkdir(exist_ok=True)
    (SITE/"catalog.json").write_text(json.dumps({"name":"Nanling Daozang","updated":datetime.now(timezone.utc).isoformat(),"illustrations":records},ensure_ascii=False,indent=2),encoding="utf-8")
    return f"Catalog built with {len(records)} illustrations."

def main():
    p=argparse.ArgumentParser(); p.add_argument("command",choices=["generate-all","build","all"]); cmd=p.parse_args().command
    if cmd in ("generate-all","all"): print(generate_all())
    if cmd in ("build","all"): print(build())
if __name__=="__main__": main()
