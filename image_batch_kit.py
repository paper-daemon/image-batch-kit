#!/usr/bin/env python3
import argparse, json, math
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

SUFFIXES={'.jpg','.jpeg','.png','.webp'}

def iter_images(root):
    root=Path(root)
    if root.is_file():
        if root.suffix.lower() in SUFFIXES: yield root
        return
    for p in sorted(root.iterdir()):
        if p.is_file() and p.suffix.lower() in SUFFIXES: yield p

def process_one(src,dst,max_px=1600,fmt='webp',quality=88):
    with Image.open(src) as im:
        im=ImageOps.exif_transpose(im)
        before=im.size
        im.thumbnail((max_px,max_px),Image.Resampling.LANCZOS)
        if fmt.lower() in {'jpg','jpeg'}:
            if im.mode not in {'RGB','L'}: im=im.convert('RGB')
        elif fmt.lower()=='webp' and im.mode not in {'RGB','RGBA'}:
            im=im.convert('RGBA' if 'A' in im.getbands() else 'RGB')
        dst.parent.mkdir(parents=True,exist_ok=True)
        savefmt='JPEG' if fmt.lower() in {'jpg','jpeg'} else fmt.upper()
        kwargs={'quality':quality} if savefmt in {'JPEG','WEBP'} else {}
        im.save(dst,format=savefmt,**kwargs)
        return {'source':str(src),'output':str(dst),'before':list(before),'after':list(im.size),'bytes':dst.stat().st_size}
def contact_sheet(records,path,thumb=260,cols=4):
    if not records: return None
    cells=[]
    for r in records:
        with Image.open(r['output']) as im:
            im=ImageOps.exif_transpose(im).convert('RGB')
            im.thumbnail((thumb,thumb),Image.Resampling.LANCZOS)
            cell=Image.new('RGB',(thumb,thumb+34),'white')
            x=(thumb-im.width)//2; y=(thumb-im.height)//2
            cell.paste(im,(x,y)); ImageDraw.Draw(cell).text((8,thumb+8),Path(r['output']).name,fill='black')
            cells.append(cell)
    rows=math.ceil(len(cells)/cols)
    sheet=Image.new('RGB',(cols*thumb,rows*(thumb+34)),(238,233,226))
    for i,c in enumerate(cells): sheet.paste(c,((i%cols)*thumb,(i//cols)*(thumb+34)))
    Path(path).parent.mkdir(parents=True,exist_ok=True); sheet.save(path,quality=90)
    return str(path)

def run(root,outdir,max_px=1600,fmt='webp',quality=88,sheet=None):
    records=[]; outdir=Path(outdir)
    for src in iter_images(root):
        dst=outdir/(src.stem+'.'+('jpg' if fmt.lower() in {'jpg','jpeg'} else fmt.lower()))
        records.append(process_one(src,dst,max_px,fmt,quality))
    sheet_path=contact_sheet(records,sheet) if sheet else None
    return {'count':len(records),'items':records,'contact_sheet':sheet_path}
def main():
    ap=argparse.ArgumentParser(description='Resize, convert and make contact sheets from image folders.')
    ap.add_argument('input'); ap.add_argument('--outdir',default='output')
    ap.add_argument('--max-px',type=int,default=1600); ap.add_argument('--format',choices=['webp','jpg','png'],default='webp')
    ap.add_argument('--quality',type=int,default=88); ap.add_argument('--contact-sheet'); ap.add_argument('--json')
    a=ap.parse_args(); report=run(a.input,a.outdir,a.max_px,a.format,a.quality,a.contact_sheet)
    if a.json: Path(a.json).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f"images={report['count']} format={a.format} max_px={a.max_px} outdir={a.outdir}")

if __name__=='__main__':
    main()
