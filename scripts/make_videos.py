"""Etsy listing videos: 15 s, 1080x1080, silent. Background = brand-assets loop (dimmed),
overlay = title / sample PDF pages sliding / footer. Frames rendered with Pillow, muxed by ffmpeg."""
import os, math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ARGS = sys.argv[1:]; sys.argv = ['x']
src = open('/home/ubuntu/drafts/etsy/make_images.py').read()
exec(src[:src.index('# 1 hero')])  # F, EN, EN_R, GOLD, WHITE, DIM, IMG, shadow, page_mock

VID = '/home/ubuntu/repos/brand-assets/video/source'
OUT = '/home/ubuntu/drafts/etsy/video'
S = 1080
FPS = 24
DUR = 15
N = FPS * DUR
os.makedirs(OUT, exist_ok=True)

PRODUCTS = {
    'birthchart': dict(
        bg='grok_video_2026-08-14-17-24-08.mp4', pages='/home/ubuntu/drafts/etsy/pages-en',
        pgs=['birth-00', 'birth-01', 'birth-04', 'birth-11', 'birth-13'],
        title=['Vedic Birth Chart', 'Report'],
        hook='Your Moon sign, nakshatra & life periods — explained',
        stats=['30+ pages', 'Personalized PDF', '6 languages', 'Delivered in 24h']),
    'compat': dict(
        bg='grok_video_2026-08-30-00-48-03.mp4', pages='/home/ubuntu/drafts/etsy/pages-en',
        pgs=['compat-00', 'compat-13', 'compat-14'],
        title=['Vedic Compatibility', 'Report'],
        hook='Why did you two meet? Two charts, one story',
        stats=['For couples, friends & partners', 'Personalized PDF', '6 languages', 'Delivered in 24h']),
    'yearly': dict(
        bg='grok_video_2026-08-14-22-10-29.mp4', pages='/home/ubuntu/drafts/etsy/pages-en',
        pgs=['yearly-00', 'yearly-12', 'yearly-13'],
        title=['Year-Ahead', 'Vedic Forecast'],
        hook='Is this your year to move — or to prepare?',
        stats=['12 months, starts next month', 'Personalized PDF', '6 languages', 'Delivered in 24h']),
    'career': dict(
        bg='grok_video_2026-08-14-23-00-51.mp4', pages='/home/ubuntu/drafts/etsy/pages-en',
        pgs=['career-00', 'career-11', 'career-13'],
        title=['Career, Calling', '& Wealth Report'],
        hook='The work you were built for — and when it pays',
        stats=['D10 career chart included', 'Personalized PDF', '6 languages', 'Delivered in 24h']),
}


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * min(max(t, 0), 1))


def page_img(pages_dir, name, height):
    global PAGES
    PAGES = pages_dir
    return page_mock(name, height, tilt=0)


def make_overlay(p, i):
    t = i / FPS
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # gradient darken top/bottom for legibility
    grad = Image.new('L', (1, S))
    for y in range(S):
        v = 0
        if y < 400: v = int(200 * (1 - y / 400))
        if y > 800: v = int(170 * ((y - 800) / 280))
        grad.putpixel((0, y), v)
    im.alpha_composite(Image.merge('RGBA', (*Image.new('RGB', (S, S), (4, 14, 22)).split(), grad.resize((S, S)))))
    d = ImageDraw.Draw(im)

    # brand
    logo = Image.open(f'{IMG}/libertas-logo.png').convert('RGBA').resize((72, 72), Image.LANCZOS)
    im.paste(logo, (48, 40), logo)
    d.text((134, 50), 'LIBERTAS JYOTISH', font=F(EN, 30), fill=GOLD)
    d.text((134, 88), 'Vedic Astrology  /  Jyotisha', font=F(EN_R, 20), fill=WHITE)

    # title (fade in 0-0.8s)
    a = ease(t / 0.8)
    if a > 0:
        tl = Image.new('RGBA', (S, S), (0, 0, 0, 0)); td = ImageDraw.Draw(tl)
        y = 150
        for k, line in enumerate(p['title']):
            f = F(EN, 66)
            shadow(td, (48, y + k * 78), line, f, GOLD if k == 0 else WHITE)
        f2 = F(EN_R, 30)
        hy = y + 78 * len(p['title']) + 14
        tw = td.textlength(p['hook'], font=f2)
        td.rounded_rectangle((36, hy - 8, 36 + tw + 24, hy + 44), 10, fill=(4, 14, 22, 175))
        td.text((48, hy), p['hook'], font=f2, fill=GOLD)
        tl.putalpha(tl.getchannel('A').point(lambda v: int(v * a)))
        im.alpha_composite(tl)

    # pages carousel: one page per 2.6s, sliding right->center->left
    start = 0.9
    period = (DUR - start - 0.3) / len(p['pgs'])
    ph = 470
    cy = 380
    for k, name in enumerate(p['pgs']):
        t0 = start + k * period
        rel = (t - t0) / period
        if -0.3 < rel < 1.3:
            pg = page_img(p['pages'], name, ph)
            # position: enter from right, hold, exit left
            if rel < 0.25: x_off = (1 - ease(rel / 0.25)) * 700
            elif rel > 0.75: x_off = -ease((rel - 0.75) / 0.25) * 700
            else: x_off = 0
            alpha = 1.0
            if rel < 0.25: alpha = ease(rel / 0.25)
            if rel > 0.75: alpha = 1 - ease((rel - 0.75) / 0.25)
            x = int((S - pg.width) / 2 + x_off)
            pgc = pg.copy(); pgc.putalpha(pgc.getchannel('A').point(lambda v: int(v * alpha)))
            im.alpha_composite(pgc, (x, cy))
    # dots
    cur = int((t - start) // period) if t >= start else -1
    for k in range(len(p['pgs'])):
        cx = S // 2 - (len(p['pgs']) - 1) * 14 + k * 28
        d.ellipse((cx - 6, 912, cx + 6, 924), fill=GOLD if k == cur else (255, 255, 255, 110))

    # footer stats rotating every 3.5s with crossfade
    period2 = 3.5
    k = int(t // period2) % len(p['stats'])
    rel = (t % period2) / period2
    a2 = ease(rel / 0.15) * (1 - ease((rel - 0.85) / 0.15))
    f = F(EN, 40)
    txt = p['stats'][k]
    wtxt = d.textlength(txt, font=f)
    fl = Image.new('RGBA', (S, S), (0, 0, 0, 0)); fd = ImageDraw.Draw(fl)
    fd.rounded_rectangle(((S - wtxt) / 2 - 40, 940, (S + wtxt) / 2 + 40, 1012), 18, fill=(0, 0, 0, 150), outline=GOLD, width=2)
    fd.text(((S - wtxt) / 2, 952), txt, font=f, fill=WHITE)
    fl.putalpha(fl.getchannel('A').point(lambda v: int(v * a2)))
    im.alpha_composite(fl)
    d.text((S / 2 - d.textlength('etsy.com/shop/LibertasJyotish', font=F(EN_R, 22)) / 2, 1036),
           'etsy.com/shop/LibertasJyotish', font=F(EN_R, 22), fill=DIM)
    return im


def build(key):
    p = PRODUCTS[key]
    fdir = f'{OUT}/frames-{key}'
    os.makedirs(fdir, exist_ok=True)
    for i in range(N):
        make_overlay(p, i).save(f'{fdir}/{i:04d}.png')
    out = f'{OUT}/etsy-{key}-15s.mp4'
    # crop 1088x1920 -> center square 1080x1080, dim 30%, overlay frames
    cmd = ['ffmpeg', '-y', '-stream_loop', '-1', '-i', f"{VID}/{p['bg']}", '-framerate', str(FPS), '-i', f'{fdir}/%04d.png',
           '-filter_complex',
           f"[0:v]crop=1080:1080:4:(ih-1080)/2,fps={FPS},eq=brightness=-0.08:saturation=1.05,format=rgba[bg];"
           f"[bg][1:v]overlay=0:0:shortest=1,format=yuv420p[v]",
           '-map', '[v]', '-t', str(DUR), '-an', '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]
    subprocess.run(cmd, check=True, capture_output=True)
    print(out, os.path.getsize(out) // 1024, 'KB')


if __name__ == '__main__':
    for k in (ARGS or list(PRODUCTS)):
        build(k)
