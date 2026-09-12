"""Hook-first Pinterest pins (v2): big one-line hook, large drawn visual, one line of copy, save CTA.
Output: pins/hook-*.jpg + hook-pins.json"""
import sys, os, json, math
sys.argv = ['x']
src = open('/home/ubuntu/drafts/etsy/make_images.py').read()
exec(src[:src.index('# 1 hero')])

OUT = '/home/ubuntu/drafts/pinterest/pins'
PW, PH = 1000, 1500
MANDALA = '/home/ubuntu/repos/brand-assets/illustrations/mandala-zodiac-gold.png'
URL = {
    'natal': 'https://www.etsy.com/listing/4570455921',
    'compat': 'https://www.etsy.com/listing/4572458099',
    'yearly': 'https://www.etsy.com/listing/4572470899',
    'career': 'https://www.etsy.com/listing/4572487096',
}
PRICE = {'natal': '$59', 'compat': '$69', 'yearly': '$49', 'career': '$49'}
GOLD2 = (255, 225, 150)
RED = (214, 92, 92)


def pbase():
    im = base(PW, PH)
    m = Image.open(MANDALA).convert('RGBA')
    m = m.resize((1300, 1300), Image.LANCZOS)
    a = m.split()[3].point(lambda v: int(v * 0.18))
    m.putalpha(a)
    im.paste(m, ((PW - 1300) // 2, 380), m)
    d = ImageDraw.Draw(im)
    logo = Image.open(f'{IMG}/libertas-logo.png').convert('RGBA').resize((70, 70), Image.LANCZOS)
    im.paste(logo, (60, 50), logo)
    d.text((145, 58), 'LIBERTAS JYOTISH', font=F(EN, 28), fill=GOLD)
    d.text((145, 92), 'Vedic Astrology', font=F(EN_R, 20), fill=DIM)
    return im, d


def hook(d, y, lines, size=92, col=WHITE):
    for t in lines:
        f = F(EN, size)
        x = (PW - d.textlength(t, font=f)) / 2
        shadow(d, (x, y), t, f, col); y += int(size * 1.15)
    return y


def center(d, y, t, f, col):
    d.text(((PW - d.textlength(t, font=f)) / 2, y), t, font=f, fill=col)


def cta(im, d, prod, label):
    # save band
    y = PH - 250
    d.rounded_rectangle((70, y, PW - 70, y + 78), radius=39, fill=GOLD)
    f = F(EN, 32)
    t = f'SAVE THIS PIN  \u2022  {label}'
    d.text(((PW - d.textlength(t, font=f)) / 2, y + 18), t, font=f, fill=(20, 30, 40))
    center(d, y + 100, f'Tap the pin \u2192 personalized PDF report  \u00b7  {PRICE[prod]}  \u00b7  in 24h', F(EN_R, 26), WHITE)
    center(d, y + 140, 'Etsy shop: LibertasJyotish', F(EN_R, 22), DIM)


# ---------- visuals ----------
def kundli(size, planets, lw=3):
    """North-Indian chart on transparent canvas. planets: {house:[abbr,...]}"""
    c = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    s = size - 8; o = 4
    d.rectangle((o, o, o + s, o + s), outline=GOLD, width=lw, fill=(8, 24, 34, 200))
    d.line((o, o, o + s, o + s), fill=GOLD, width=lw)
    d.line((o + s, o, o, o + s), fill=GOLD, width=lw)
    mid = o + s / 2
    d.polygon([(mid, o), (o + s, mid), (mid, o + s), (o, mid)], outline=GOLD, width=lw)
    q = s / 4
    pos = {1: (mid, o + q), 2: (o + q, o + q / 2), 3: (o + q / 2, o + q), 4: (o + q, mid),
           5: (o + q / 2, o + 3 * q), 6: (o + q, o + s - q / 2), 7: (mid, o + 3 * q), 8: (o + 3 * q, o + s - q / 2),
           9: (o + s - q / 2, o + 3 * q), 10: (o + 3 * q, mid), 11: (o + s - q / 2, o + q), 12: (o + 3 * q, o + q / 2)}
    fn = F(EN_R, int(size * 0.045)); fp = F(EN, int(size * 0.07))
    for h, (x, y) in pos.items():
        d.text((x - 8, y - size * 0.135), str(h), font=fn, fill=DIM)
        ps = planets.get(h, [])
        for i, p in enumerate(ps):
            t = p; w = d.textlength(t, font=fp)
            d.text((x - w / 2, y - size * 0.02 + i * size * 0.075 - (len(ps) - 1) * size * 0.03), t, font=fp,
                   fill=RED if p in ('Sa', 'Ra', 'Ke') else GOLD2)
    return c


def timeline(w, h, months, marks):
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    y = h // 2
    d.line((20, y, w - 20, y), fill=GOLD, width=4)
    step = (w - 40) / 11
    f = F(EN_R, 22)
    for i, m in enumerate(months):
        x = 20 + i * step
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(8, 24, 34), outline=GOLD, width=3)
        d.text((x - d.textlength(m, font=f) / 2, y + 22), m, font=f, fill=DIM)
    fb = F(EN, 26)
    for i, (label, col) in marks.items():
        x = 20 + i * step
        d.ellipse((x - 20, y - 20, x + 20, y + 20), fill=col)
        d.text((x - d.textlength(label, font=fb) / 2, y - 80), label, font=fb, fill=col)
        d.line((x, y - 44, x, y - 24), fill=col, width=3)
    return c


def save(im, name):
    im.save(f'{OUT}/{name}.jpg', quality=92)


pins = []


def reg(name, prod, title, desc, board):
    pins.append({'file': f'{name}.jpg', 'link': URL[prod], 'board': board, 'title': title, 'description': desc})


# 1 NATAL — birth time hook
im, d = pbase()
y = hook(d, 170, ['3 in 4 people', 'have the WRONG', 'zodiac sign'], 88)
center(d, y + 10, 'Vedic (sidereal) astrology moves you ~24° back', F(EN_R, 30), GOLD)
k = kundli(560, {1: ['Mo'], 4: ['Ju'], 7: ['Sa'], 9: ['Su', 'Me'], 10: ['Ve'], 11: ['Ma'], 2: ['Ra'], 8: ['Ke']})
im.paste(k, ((PW - 560) // 2, 600), k)
d = ImageDraw.Draw(im)
center(d, 1180, 'Your real Moon sign, nakshatra & dasha \u2014 read for you', F(EN_R, 28), WHITE)
cta(im, d, 'natal', 'FIND YOUR REAL SIGN')
save(im, 'hook-natal')
reg('hook-natal', 'natal', '3 in 4 people have the wrong zodiac sign (Vedic astrology)',
    'Vedic astrology uses the sidereal zodiac, ~24° behind the Western one — so most people shift one sign back. Find your real Moon sign, nakshatra and dasha in a personalized 10-chapter Vedic birth chart PDF, delivered within 24h. Save this pin for later. #vedicastrology #birthchart #moonsign #nakshatra #kundli #jyotish',
    'Vedic Birth Chart Reports')

# 2 COMPAT — two charts
im, d = pbase()
y = hook(d, 170, ['Why did', 'you two meet?'], 96)
center(d, y + 10, 'Two birth charts. One answer.', F(EN_R, 32), GOLD)
k1 = kundli(400, {1: ['Mo'], 7: ['Ve'], 5: ['Ju'], 10: ['Sa']})
k2 = kundli(400, {7: ['Mo'], 1: ['Ve'], 9: ['Ju'], 4: ['Ra']})
im.paste(k1, (40, 600), k1)
im.paste(k2, (PW - 440, 720), k2)
d = ImageDraw.Draw(im)
fh = F(EN, 120)
d.text(((PW - d.textlength('\u2661', font=fh)) / 2, 960), '\u2661', font=fh, fill=RED)
center(d, 1160, 'Couples \u00b7 friends \u00b7 business partners', F(EN_R, 28), WHITE)
center(d, 1198, 'When your bond moves in the next 12 months', F(EN_R, 26), DIM)
cta(im, d, 'compat', 'CHECK YOUR MATCH')
save(im, 'hook-compat')
reg('hook-compat', 'compat', 'Why did you two meet? Vedic compatibility from two birth charts',
    'A personalized Vedic astrology compatibility PDF for any two people — couples, friends or business partners. Why this bond exists, how your Moons fit, and the months your relationship moves in the coming year. Delivered within 24h. Save for later. #compatibility #synastry #vedicastrology #kundlimatching #soulmate #relationshipastrology',
    'Compatibility & Relationships')

# 3 YEARLY — timeline
im, d = pbase()
y = hook(d, 170, ['Is 2026', 'your year', 'to move?'], 96)
center(d, y + 10, 'Or a year to prepare? Your chart already knows.', F(EN_R, 30), GOLD)
months = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']
tl = timeline(PW - 120, 200, months, {2: ('Care', RED), 5: ('Jupiter \u2192 10th', GOLD2), 9: ('Dasha shift', GOLD2)})
im.paste(tl, (60, 640), tl)
d = ImageDraw.Draw(im)
k = kundli(300, {10: ['Ju'], 1: ['Mo'], 7: ['Sa']})
im.paste(k, ((PW - 300) // 2, 860), k)
d = ImageDraw.Draw(im)
center(d, 1180, 'Career change \u00b7 relocation \u00b7 independence \u00b7 love', F(EN_R, 28), WHITE)
center(d, 1218, '12 months from the day you order \u2014 not a calendar year', F(EN_R, 24), DIM)
cta(im, d, 'yearly', 'PLAN YOUR YEAR')
save(im, 'hook-yearly')
reg('hook-yearly', 'yearly', 'Is 2026 your year to move? Personalized 12-month Vedic forecast',
    'A Vedic astrology forecast for the 12 months after you order: is this a year to make the move or to prepare — and in which months? Dasha shifts, Jupiter & Saturn over your Moon, Sade Sati. Personalized PDF within 24h. Save this pin. #yearahead #2026astrology #vedicastrology #forecast #dasha #careerchange',
    'Year Ahead Forecasts')

# 4 CAREER — 10th house highlight
im, d = pbase()
y = hook(d, 170, ['Employee,', 'founder or', 'partner?'], 96)
center(d, y + 10, 'Your 10th house has an opinion.', F(EN_R, 32), GOLD)
k = kundli(560, {10: ['Su', 'Sa'], 1: ['Ma'], 2: ['Ju'], 11: ['Ve'], 7: ['Mo'], 6: ['Me']})
# highlight house 10
hl = Image.new('RGBA', k.size, (0, 0, 0, 0))
hd = ImageDraw.Draw(hl)
s = 560 - 8; o = 4; q = s / 4; mid = o + s / 2
hd.polygon([(mid, mid), (o + s, mid), (o + s, o + s), (mid, o + s)][:0] or [(o + s, mid), (o + 3 * q, o + q), (mid, mid), (o + 3 * q, o + 3 * q)], fill=(232, 205, 130, 70))
k.alpha_composite(hl)
im.paste(k, ((PW - 560) // 2, 600), k)
d = ImageDraw.Draw(im)
center(d, 1180, 'How you are built to work \u00b7 your money pattern \u00b7 timing', F(EN_R, 27), WHITE)
cta(im, d, 'career', 'FIND YOUR CALLING')
save(im, 'hook-career')
reg('hook-career', 'career', 'Employee, founder or partner? Your Vedic 10th house knows',
    'A personalized Vedic career, vocation & wealth PDF: how you are built to work, whether you thrive employed, independent or in partnership, your money pattern and when your career moves in the next 12 months. Delivered within 24h. Save for later. #careerastrology #vedicastrology #10thhouse #vocation #wealth #jyotish',
    'Career & Wealth')

json.dump(pins, open('/home/ubuntu/drafts/pinterest/hook-pins.json', 'w'), indent=1, ensure_ascii=False)
print('ok', [p['file'] for p in pins])
