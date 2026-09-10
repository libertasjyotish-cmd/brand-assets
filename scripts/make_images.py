from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, sys
sys.path.insert(0, '/home/ubuntu/drafts')

IMG = '/home/ubuntu/repos/libertas-jyotish/img'
OUT = '/home/ubuntu/drafts/etsy/images'
PAGES = '/home/ubuntu/drafts/etsy/pages'
EN = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
EN_R = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
JP = '/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf'
GOLD = (232, 205, 130)
WHITE = (240, 236, 226)
DIM = (190, 186, 176)
W, H = 2000, 1500
os.makedirs(OUT, exist_ok=True)


def F(p, s):
    return ImageFont.truetype(p, s)


def base(w=W, h=H):
    bg = Image.open(f'{IMG}/bg-jyotish.jpg').convert('RGB')
    s = max(w / bg.width, h / bg.height)
    bg = bg.resize((int(bg.width * s) + 1, int(bg.height * s) + 1), Image.LANCZOS)
    x = (bg.width - w) // 2
    y = int((bg.height - h) * 0.35)
    bg = bg.crop((x, y, x + w, y + h))
    grad = Image.new('L', (1, h))
    for i in range(h):
        grad.putpixel((0, i), int(110 + 90 * (i / h)))
    grad = grad.resize((w, h))
    dark = Image.new('RGB', (w, h), (6, 22, 30))
    bg = Image.composite(dark, bg, grad)
    return Image.blend(bg, dark, 0.2)


def brand(im, d, m):
    logo = Image.open(f'{IMG}/libertas-logo.png').convert('RGBA')
    ls = 150
    logo = logo.resize((ls, ls), Image.LANCZOS)
    im.paste(logo, (m, m), logo)
    d.text((m + ls + 24, m + 30), 'LIBERTAS JYOTISH', font=F(EN, 54), fill=GOLD)
    d.text((m + ls + 24, m + 96), 'Vedic Astrology  /  Jyotisha', font=F(EN_R, 32), fill=WHITE)


def shadow(d, xy, t, f, fill):
    x, y = xy
    d.text((x + 3, y + 4), t, font=f, fill=(0, 0, 0))
    d.text(xy, t, font=f, fill=fill)


def page_mock(name, height, tilt=0):
    p = Image.open(f'{PAGES}/{name}.png').convert('RGB')
    w = int(p.width * height / p.height)
    p = p.resize((w, height), Image.LANCZOS)
    pad = 60
    canvas = Image.new('RGBA', (w + pad * 2, height + pad * 2), (0, 0, 0, 0))
    sh = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((pad + 10, pad + 18, pad + w + 10, pad + height + 18), fill=(0, 0, 0, 170))
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    canvas.alpha_composite(sh)
    canvas.paste(p, (pad, pad))
    ImageDraw.Draw(canvas).rectangle((pad, pad, pad + w - 1, pad + height - 1), outline=GOLD, width=2)
    if tilt:
        canvas = canvas.rotate(tilt, resample=Image.BICUBIC, expand=True)
    return canvas


def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w_
    lines.append(cur)
    return lines


def footer(d, text='Personalized · Made to order · PDF by email within 24 hours'):
    d.line((100, H - 110, W - 100, H - 110), fill=GOLD, width=1)
    f = F(EN_R, 34)
    d.text(((W - d.textlength(text, font=f)) / 2, H - 92), text, font=f, fill=DIM)


def start():
    im = base(); d = ImageDraw.Draw(im); brand(im, d, 100); return im, d


# 1 hero
im, d = start()
mock = page_mock('p00', 880, tilt=-4)
im.paste(mock, (W - mock.width - 60, 330), mock)
y = 430
shadow(d, (100, y), 'Personalized', F(EN, 104), WHITE)
shadow(d, (100, y + 125), 'Vedic Astrology', F(EN, 104), WHITE)
shadow(d, (100, y + 250), 'Birth Chart Report', F(EN, 104), GOLD)
for i, t in enumerate(['13 chapters  ·  30–40 page PDF', '6 languages', 'Calculated from your exact birth time & place']):
    d.text((100, y + 430 + i * 60), '◆  ' + t, font=F(EN_R, 40), fill=WHITE)
footer(d)
im.save(f'{OUT}/01-hero.jpg', quality=92)

# 2 contents
im, d = start()
mock = page_mock('p01', 1080)
im.paste(mock, (80, 300), mock)
x = 80 + mock.width + 40
shadow(d, (x, 380), "What's inside", F(EN, 96), GOLD)
items = ['Your one-page owner\'s manual', 'Ascendant, Moon, Sun & nakshatra', 'Your strongest planet and yogas',
         'Stones, colours, habits, places', 'Career (D10) and wealth', 'Lifetime dasha timeline',
         'Current & upcoming golden periods', 'Turning trials into foundations', 'Appendix: chart data']
for i, t in enumerate(items):
    d.text((x, 530 + i * 78), '◆  ' + t, font=F(EN_R, 44), fill=WHITE)
footer(d)
im.save(f'{OUT}/02-contents.jpg', quality=92)

# 3 chapters
im, d = start()
shadow(d, (100, 300), '13 chapters, one person: you', F(EN, 88), GOLD)
ch = ['At a glance — your owner\'s manual', '1  The blueprint that is you', '2  The strongest planet within you',
      '3  The good fortune you were born with', '4  Things — stones and colours', '5  Practices — habits & ways of working',
      '6  Places — directions & environments', '7  Your calling and talents (D10)', '8  Your route to abundance',
      '9  The map of your destiny — dasha timeline', '10  Where you stand now', '11  The golden period ahead',
      '12  Turning trials into foundations']
for i, t in enumerate(ch):
    col, row = divmod(i, 7)
    d.text((100 + col * 950, 450 + row * 105), t, font=F(EN_R, 42), fill=WHITE if i else GOLD)
footer(d)
im.save(f'{OUT}/03-chapters.jpg', quality=92)

# 4 how it works
im, d = start()
shadow(d, (100, 300), 'How it works', F(EN, 96), GOLD)
steps = [('1', 'Order & personalize', 'Enter date, time and place of birth, plus your report language, in the personalization box.'),
         ('2', 'We calculate', 'Sidereal zodiac, Lahiri ayanamsa, Vimshottari dasha, D9, D10 and ashtakavarga from your exact data.'),
         ('3', 'Receive your PDF', 'Your report is emailed to your Etsy address — normally within 24 hours, often faster.')]
for i, (n, t, s) in enumerate(steps):
    x = 100 + i * 610
    d.ellipse((x, 480, x + 130, 610), outline=GOLD, width=4)
    d.text((x + 65 - d.textlength(n, font=F(EN, 72)) / 2, 500), n, font=F(EN, 72), fill=GOLD)
    d.text((x, 660), t, font=F(EN, 50), fill=WHITE)
    for j, l in enumerate(wrap(d, s, F(EN_R, 36), 560)):
        d.text((x, 750 + j * 50), l, font=F(EN_R, 36), fill=DIM)
footer(d)
im.save(f'{OUT}/04-how-it-works.jpg', quality=92)

# 5 vedic vs western
im, d = start()
shadow(d, (100, 300), 'Not a sun-sign horoscope', F(EN, 96), GOLD)
d.text((100, 440), 'Western astrology', font=F(EN, 52), fill=DIM)
d.text((1050, 440), 'Vedic astrology (Jyotish)', font=F(EN, 52), fill=WHITE)
rows = [('Tropical zodiac (seasons)', 'Sidereal zodiac (actual stars)'),
        ('12 signs', '12 signs + 27 nakshatras'),
        ('Sun sign is central', 'Moon & ascendant are central'),
        ('Describes personality', 'Times your life: 120-year dasha cycle'),
        ('One chart', 'Divisional charts (D9 marriage, D10 career)')]
for i, (a, b) in enumerate(rows):
    y = 560 + i * 120
    d.line((100, y - 20, W - 100, y - 20), fill=(60, 80, 90), width=1)
    d.text((100, y), a, font=F(EN_R, 40), fill=DIM)
    d.text((1050, y), '◆  ' + b, font=F(EN_R, 40), fill=WHITE)
footer(d)
im.save(f'{OUT}/05-vedic-vs-western.jpg', quality=92)

# 6 languages
im, d = start()
shadow(d, (100, 300), 'Your report, in your language', F(EN, 88), GOLD)
langs = ['English', 'Español', 'Português', 'Bahasa Indonesia', '日本語', 'العربية']
for i, t in enumerate(langs):
    col, row = divmod(i, 3)
    x, y = 100 + col * 920, 480 + row * 220
    d.rounded_rectangle((x, y, x + 860, y + 170), radius=30, outline=GOLD, width=3)
    f = F(JP, 64) if t in ('日本語', 'العربية') else F(EN, 60)
    if t == 'العربية':
        f = F('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 60)
    d.text((x + 430 - d.textlength(t, font=f) / 2, y + 50), t, font=f, fill=WHITE)
for j, l in enumerate(wrap(d, 'Choose one language per report in the personalization box. Every Sanskrit term is explained in plain words.', F(EN_R, 38), W - 200)):
    d.text((100, 1170 + j * 52), l, font=F(EN_R, 38), fill=DIM)
footer(d)
im.save(f'{OUT}/06-languages.jpg', quality=92)

# 7 birth time
im, d = start()
shadow(d, (100, 300), 'Why your birth time matters', F(EN, 88), GOLD)
para = ['The ascendant changes roughly every two hours, and your dasha timeline depends on the Moon\'s exact position.',
        'Please check a birth certificate or hospital record if you can.',
        'Time unknown? Write "unknown" and we use noon. Your Moon sign, nakshatra and dasha are usually still reliable; house-based sections are noted as approximate.']
y = 470
for p in para:
    for l in wrap(d, p, F(EN_R, 44), W - 200):
        d.text((100, y), l, font=F(EN_R, 44), fill=WHITE); y += 62
    y += 40
footer(d)
im.save(f'{OUT}/07-birth-time.jpg', quality=92)

# 8 delivery
im, d = start()
m1 = page_mock('p00', 950, tilt=-5)
im.paste(m1, (120, 330), m1)
x = 1000
shadow(d, (x, 460), 'Delivered', F(EN, 96), WHITE)
shadow(d, (x, 580), 'within 24h', F(EN, 96), GOLD)
for i, t in enumerate(['Made to order from your data', 'Emailed as a PDF to your Etsy address', 'Wrong data? Regenerated once, free', 'For self-understanding & entertainment']):
    for j, l in enumerate(wrap(d, t, F(EN_R, 40), 880)):
        d.text((x, 760 + i * 120 + j * 48), ('◆  ' if j == 0 else '     ') + l, font=F(EN_R, 38), fill=WHITE)
footer(d)
im.save(f'{OUT}/08-delivery.jpg', quality=92)

# shop icon 500x500
ic = Image.new('RGB', (500, 500), (6, 22, 30))
logo = Image.open(f'{IMG}/libertas-logo.png').convert('RGBA').resize((360, 360), Image.LANCZOS)
ic.paste(logo, (70, 40), logo)
d = ImageDraw.Draw(ic)
f = F(EN, 34); t = 'LIBERTAS JYOTISH'
d.text(((500 - d.textlength(t, font=f)) / 2, 420), t, font=f, fill=GOLD)
ic.save(f'{OUT}/shop-icon-500.png')

# banners
for name, bw, bh in [('shop-banner-mini-1200x300', 1200, 300), ('shop-banner-big-3360x840', 3360, 840)]:
    b = base(bw, bh); d = ImageDraw.Draw(b)
    ls = int(bh * 0.6)
    logo = Image.open(f'{IMG}/libertas-logo.png').convert('RGBA').resize((ls, ls), Image.LANCZOS)
    m = int(bh * 0.2)
    b.paste(logo, (m, m), logo)
    x = m + ls + int(bh * 0.12)
    d.text((x, int(bh * 0.22)), 'LIBERTAS JYOTISH', font=F(EN, int(bh * 0.2)), fill=GOLD)
    d.text((x, int(bh * 0.5)), 'Personalized Vedic Astrology Reports  ·  6 languages  ·  PDF within 24 hours', font=F(EN_R, int(bh * 0.1)), fill=WHITE)
    b.save(f'{OUT}/{name}.jpg', quality=92)
print('done')
