"""Educational 'wait, what?' infographic pins (white/cream, 1000x1500)."""
from PIL import Image, ImageDraw, ImageFont
import math, os, json

OUT = '/home/ubuntu/drafts/pinterest/pins'
IMG = '/home/ubuntu/repos/libertas-jyotish/img'
os.makedirs(OUT, exist_ok=True)
W, H = 1000, 1500

B = '/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf'
R = '/usr/share/fonts/truetype/freefont/FreeSerif.ttf'
I = '/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf'
SB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
S = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

CREAM = (249, 245, 236)
INK = (28, 36, 46)
TEAL = (12, 78, 86)
GOLD = (176, 132, 52)
RED = (170, 52, 44)
GREY = (120, 120, 118)
LINE = (215, 208, 194)
LIGHT = (236, 229, 214)

URL = {
    'natal': 'https://www.etsy.com/listing/4570455921',
    'compat': 'https://www.etsy.com/listing/4572458099',
    'yearly': 'https://www.etsy.com/listing/4572470899',
    'career': 'https://www.etsy.com/listing/4572487096',
}


def F(p, s):
    return ImageFont.truetype(p, s)


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


def para(d, x, y, text, f, fill, maxw, lh=None):
    lh = lh or int(f.size * 1.3)
    for l in wrap(d, text, f, maxw):
        d.text((x, y), l, font=f, fill=fill); y += lh
    return y


def center(d, y, text, f, fill):
    d.text(((W - d.textlength(text, font=f)) / 2, y), text, font=f, fill=fill)


def start(kicker):
    im = Image.new('RGB', (W, H), CREAM)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 14), fill=TEAL)
    d.text((60, 44), kicker.upper(), font=F(SB, 20), fill=GOLD)
    return im, d


def hook(d, y, lines, size=80, fill=INK):
    f = F(B, size)
    for l in lines:
        d.text((60, y), l, font=f, fill=fill); y += int(size * 1.08)
    return y + 10


def footer(im, d, cta):
    y = H - 170
    d.line((60, y, W - 60, y), fill=LINE, width=2)
    logo = Image.open(f'{IMG}/libertas-logo.png').convert('RGBA').resize((72, 72), Image.LANCZOS)
    im.paste(logo, (60, y + 32), logo)
    d.text((150, y + 34), 'LIBERTAS JYOTISH', font=F(SB, 24), fill=TEAL)
    d.text((150, y + 68), 'Personalized Vedic astrology reports · PDF within 24h', font=F(S, 18), fill=GREY)
    f = F(SB, 20)
    tw = d.textlength(cta, font=f)
    d.rounded_rectangle((W - 60 - tw - 44, y + 38, W - 60, y + 90), radius=26, fill=TEAL)
    d.text((W - 60 - tw - 22, y + 51), cta, font=f, fill=CREAM)


pins = []


def reg(name, prod, title, desc, board):
    pins.append({'file': f'{name}.jpg', 'link': URL[prod], 'board': board, 'title': title, 'description': desc})


SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

# ---------------- 1. Your zodiac sign is probably wrong ----------------
im, d = start('Vedic vs Western astrology')
y = hook(d, 90, ['Your zodiac', 'sign is probably', 'wrong.'], 92)
y = para(d, 60, y + 6, 'Western horoscopes use the tropical zodiac. Vedic astrology uses the sidereal zodiac — the actual stars. They have drifted ~24° apart. Most people move one sign back.', F(R, 30), GREY, W - 120)

# two-band diagram
by = y + 40
bw = (W - 120) / 12
d.text((60, by), 'WESTERN (tropical)', font=F(SB, 18), fill=GREY)
d.text((60, by + 150), 'VEDIC (sidereal)', font=F(SB, 18), fill=TEAL)
for i, s in enumerate(SIGNS):
    x0 = 60 + i * bw
    d.rectangle((x0, by + 30, x0 + bw - 3, by + 110), fill=LIGHT)
    d.text((x0 + 8, by + 40), s[:3].upper(), font=F(SB, 18), fill=INK)
    # shift 24 degrees = 0.8 of a sign
    sx = x0 + bw * 0.8
    d.rectangle((sx, by + 180, min(W - 60, sx + bw - 3), by + 260), fill=(206, 226, 226))
    if sx + 40 < W - 60:
        d.text((sx + 8, by + 190), s[:3].upper(), font=F(SB, 18), fill=TEAL)
# leading partial Pisces box
d.rectangle((60, by + 180, 60 + bw * 0.8 - 3, by + 260), fill=(206, 226, 226))
d.text((68, by + 190), 'PIS', font=F(SB, 18), fill=TEAL)
# arrow: same birthday, one sign back
ax = 60 + 4 * bw + bw / 2
d.line((ax, by + 115, ax, by + 175), fill=RED, width=4)
d.polygon([(ax, by + 180), (ax - 10, by + 162), (ax + 10, by + 162)], fill=RED)
d.text((ax + 16, by + 128), 'same birthday, one sign back', font=F(SB, 20), fill=RED)
d.text((60, by + 270), 'Sidereal signs start ~24 days later in the year (ayanamsa ≈ 24°).', font=F(I, 20), fill=GREY)

# example rows
ey = by + 330
d.text((60, ey), 'Example', font=F(SB, 20), fill=GOLD); ey += 36
rows = [('Born Aug 10', 'Leo', 'Cancer'), ('Born Nov 30', 'Sagittarius', 'Scorpio'), ('Born Mar 25', 'Aries', 'Pisces')]
d.text((360, ey), 'Western', font=F(SB, 22), fill=GREY)
d.text((680, ey), 'Vedic', font=F(SB, 22), fill=TEAL); ey += 40
for a, b, c in rows:
    d.line((60, ey - 8, W - 60, ey - 8), fill=LINE)
    d.text((60, ey), a, font=F(R, 30), fill=INK)
    d.text((360, ey), b, font=F(R, 30), fill=GREY)
    d.text((620, ey + 4), '→', font=F(S, 26), fill=RED)
    d.text((680, ey), c, font=F(B, 30), fill=TEAL); ey += 56
yy = para(d, 60, ey + 14, 'And in Vedic astrology the Sun sign is only a supporting role: the Moon sign and your nakshatra come first.', F(I, 28), INK, W - 120)
d.rounded_rectangle((60, yy + 24, W - 60, yy + 104), radius=12, fill=LIGHT)
d.text((84, yy + 40), 'Born in the last ~6 days of your sign? You keep it. Everyone else moves one back.', font=F(R, 23), fill=INK)
footer(im, d, 'Find your real sign →')
im.save(f'{OUT}/edu-01.jpg', quality=92)
reg('edu-01', 'natal', 'Your zodiac sign is probably wrong (Vedic vs Western astrology)',
    'Western horoscopes use the tropical zodiac, Vedic astrology uses the sidereal zodiac - about 24 degrees apart, so most people shift one sign back. Find your real Vedic Moon sign, Sun sign and nakshatra in a personalized birth chart report (PDF). #vedicastrology #zodiacsigns #siderealastrology #astrologyfacts #birthchart', 'Vedic Astrology Basics')

# ---------------- 2. 27 signs, not 12 ----------------
im, d = start('Nakshatras · the lunar zodiac')
y = hook(d, 90, ['There are 27', 'signs. Not 12.'], 92)
y = para(d, 60, y + 6, 'Before the 12 signs, India divided the sky by the Moon: 27 nakshatras of 13°20′ each. The one your Moon was in at birth is your birth star — and it says more about you than any Sun sign.', F(R, 30), GREY, W - 120)
NAK = ['Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra', 'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'P.Phalguni', 'U.Phalguni', 'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha', 'Mula', 'P.Ashadha', 'U.Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha', 'P.Bhadra', 'U.Bhadra', 'Revati']
cx, cy, r1, r2, r3 = W / 2, y + 330, 300, 225, 150
d.ellipse((cx - r1, cy - r1, cx + r1, cy + r1), outline=TEAL, width=3)
d.ellipse((cx - r2, cy - r2, cx + r2, cy + r2), outline=GOLD, width=2)
d.ellipse((cx - r3, cy - r3, cx + r3, cy + r3), outline=LINE, width=2)
for i in range(27):
    a = math.radians(-90 + i * 360 / 27)
    d.line((cx + r2 * math.cos(a), cy + r2 * math.sin(a), cx + r1 * math.cos(a), cy + r1 * math.sin(a)), fill=TEAL, width=1)
    am = math.radians(-90 + (i + 0.5) * 360 / 27)
    f = F(S, 13)
    t = NAK[i]
    tw = d.textlength(t, font=f)
    tx, ty = cx + 262 * math.cos(am), cy + 262 * math.sin(am)
    d.text((tx - tw / 2, ty - 8), t, font=f, fill=TEAL)
for i in range(12):
    a = math.radians(-90 + i * 30)
    d.line((cx + r3 * math.cos(a), cy + r3 * math.sin(a), cx + r2 * math.cos(a), cy + r2 * math.sin(a)), fill=GOLD, width=2)
    am = math.radians(-90 + (i + 0.5) * 30)
    f = F(SB, 15)
    t = SIGNS[i][:3].upper()
    tw = d.textlength(t, font=f)
    d.text((cx + 188 * math.cos(am) - tw / 2, cy + 188 * math.sin(am) - 8), t, font=f, fill=GOLD)
d.text((cx - d.textlength('27 nakshatras', font=F(SB, 22)) / 2, cy - 40), '27 nakshatras', font=F(SB, 22), fill=TEAL)
d.text((cx - d.textlength('12 signs', font=F(SB, 22)) / 2, cy - 8), '12 signs', font=F(SB, 22), fill=GOLD)
d.text((cx - d.textlength('one Moon', font=F(I, 22)) / 2, cy + 24), 'one Moon', font=F(I, 22), fill=GREY)
yy = cy + r1 + 40
para(d, 60, yy, 'Each nakshatra has a ruling planet, a symbol, a deity and an animal. Two people with the same Sun sign can have completely different birth stars — and completely different lives.', F(I, 27), INK, W - 120)
footer(im, d, 'Find your birth star →')
im.save(f'{OUT}/edu-02.jpg', quality=92)
reg('edu-02', 'natal', 'There are 27 signs, not 12 - the nakshatras of Vedic astrology',
    'Vedic astrology divides the sky into 27 nakshatras (lunar mansions) of 13 degrees 20 minutes. The nakshatra your Moon occupied at birth is your birth star - more personal than a Sun sign. Personalized Vedic birth chart report (PDF) shows yours. #nakshatra #vedicastrology #moonsign #birthstar #astrologyfacts', 'Vedic Astrology Basics')

# ---------------- 3. Life runs on a planetary timetable ----------------
im, d = start('Vimshottari dasha · planetary periods')
y = hook(d, 90, ['Your life runs', 'on a planetary', 'timetable.'], 88)
y = para(d, 60, y + 6, 'Vedic astrology says your life is divided into planetary periods (dashas) — a 120-year cycle where each planet rules for a fixed number of years. Where you start depends on your birth nakshatra.', F(R, 30), GREY, W - 120)
DASHA = [('Ketu', 7, (150, 150, 150)), ('Venus', 20, (200, 150, 170)), ('Sun', 6, (222, 160, 70)), ('Moon', 10, (190, 200, 215)), ('Mars', 7, (190, 80, 70)), ('Rahu', 18, (90, 90, 110)), ('Jupiter', 16, (210, 175, 90)), ('Saturn', 19, (60, 80, 110)), ('Mercury', 17, (110, 170, 130))]
ty = y + 40
x = 60
tot = W - 120
d.text((60, ty), 'THE 120-YEAR CYCLE', font=F(SB, 18), fill=GOLD); ty += 34
for name, yrs, col in DASHA:
    wdt = tot * yrs / 120
    d.rectangle((x, ty, x + wdt - 2, ty + 90), fill=col)
    if wdt > 60:
        d.text((x + 8, ty + 8), name, font=F(SB, 16), fill=CREAM)
        d.text((x + 8, ty + 50), f'{yrs}y', font=F(S, 22), fill=CREAM)
    else:
        d.text((x + 4, ty + 30), f'{yrs}', font=F(S, 18), fill=CREAM)
    x += wdt
ty += 110
d.text((60, ty), 'Ketu 7 · Venus 20 · Sun 6 · Moon 10 · Mars 7 · Rahu 18 · Jupiter 16 · Saturn 19 · Mercury 17', font=F(S, 15), fill=GREY)
ty += 50
# example person
d.text((60, ty), 'Example: born in Venus period, age 0–14 remaining', font=F(SB, 20), fill=TEAL); ty += 34
seq = [('Venus', 14, 'childhood ease'), ('Sun', 6, 'identity, father, career start'), ('Moon', 10, 'emotion, home, public'), ('Mars', 7, 'drive, conflict, property'), ('Rahu', 18, 'ambition, foreign, upheaval')]
age = 0
for name, yrs, note in seq:
    d.line((60, ty - 6, W - 60, ty - 6), fill=LINE)
    d.text((60, ty), f'{age}–{age + yrs}', font=F(SB, 26), fill=INK)
    d.text((200, ty), name, font=F(B, 26), fill=TEAL)
    d.text((380, ty + 2), note, font=F(I, 24), fill=GREY)
    age += yrs; ty += 46
para(d, 60, ty + 16, 'Big life changes cluster around the switch from one period to the next. Knowing your next switch date changes how you plan.', F(I, 27), INK, W - 120)
footer(im, d, 'See your periods →')
im.save(f'{OUT}/edu-03.jpg', quality=92)
reg('edu-03', 'natal', 'Your life runs on a planetary timetable - Vedic dasha periods explained',
    'Vimshottari dasha: Vedic astrology divides life into planetary periods - Ketu 7, Venus 20, Sun 6, Moon 10, Mars 7, Rahu 18, Jupiter 16, Saturn 19, Mercury 17 years. Big changes cluster at the switch. A personalized birth chart report shows your current and next period. #dasha #vedicastrology #lifecycle #astrologyfacts #jyotish', 'Vedic Astrology Basics')

# ---------------- 4. Moon over Sun ----------------
im, d = start('Moon sign vs Sun sign')
y = hook(d, 90, ['Vedic astrology', 'barely looks at', 'your Sun sign.'], 84)
y = para(d, 60, y + 6, '"What\'s your sign?" in India means your Moon sign (rashi). The Sun shows the outer role; the Moon shows the mind — how you feel, react, bond and decide.', F(R, 30), GREY, W - 120)
cy = y + 60
# sun
d.ellipse((150, cy, 410, cy + 260), fill=(240, 200, 110))
d.text((280 - d.textlength('SUN', font=F(SB, 34)) / 2, cy + 110), 'SUN', font=F(SB, 34), fill=CREAM)
# moon
d.ellipse((590, cy, 850, cy + 260), fill=(200, 210, 225))
d.ellipse((650, cy - 10, 890, cy + 230), fill=CREAM)
d.text((720 - d.textlength('MOON', font=F(SB, 34)) / 2, cy + 110), 'MOON', font=F(SB, 34), fill=TEAL)
ry = cy + 300
pairs = [('Western focus', 'Vedic focus'), ('Ego, vitality', 'Mind, emotions'), ('Public face', 'Private self'), ('Same for ~30 days', 'Changes every 2.5 days'), ('12 signs', '12 signs × 27 nakshatras'), ('Yearly horoscopes', 'Timing (dasha, Sade Sati)')]
for i, (a, b) in enumerate(pairs):
    fa = F(SB, 22) if i == 0 else F(R, 27)
    fb = F(SB, 22) if i == 0 else F(B, 27)
    ca = GREY if i == 0 else INK
    cb = GREY if i == 0 else TEAL
    d.line((60, ry - 8, W - 60, ry - 8), fill=LINE)
    d.text((280 - d.textlength(a, font=fa) / 2, ry), a, font=fa, fill=ca)
    d.text((720 - d.textlength(b, font=fb) / 2, ry), b, font=fb, fill=cb)
    ry += 52
d.line((W / 2, cy + 290, W / 2, ry - 10), fill=LINE, width=2)
yy = para(d, 60, ry + 16, 'So a "Leo" who reads Leo horoscopes may actually be a Vedic Cancer Moon in Pushya — a completely different story. Your birth time and place decide it.', F(I, 27), INK, W - 120)
d.rounded_rectangle((60, yy + 24, W - 60, yy + 104), radius=12, fill=LIGHT)
d.text((84, yy + 40), 'The Moon moves ~13° a day — two people born the same week can have different Moon signs.', font=F(R, 22), fill=INK)
footer(im, d, 'Get your Moon sign →')
im.save(f'{OUT}/edu-04.jpg', quality=92)
reg('edu-04', 'natal', 'Vedic astrology barely looks at your Sun sign - here is why',
    'In Vedic astrology your sign means your Moon sign (rashi): the Moon shows the mind, emotions and timing, and changes every 2.5 days. Why Jyotish reads the Moon and nakshatra before the Sun. Personalized Vedic birth chart report (PDF). #moonsign #vedicastrology #sunsign #astrologyfacts #rashi', 'Vedic Astrology Basics')

# ---------------- 5. Sade Sati ----------------
im, d = start('Sade Sati · Saturn over the Moon')
y = hook(d, 90, ['Saturn tests', 'everyone for', '7½ years.'], 90)
y = para(d, 60, y + 6, 'Sade Sati: the seven and a half years Saturn spends crossing the sign before your Moon, your Moon sign, and the sign after. It comes around roughly every 30 years — and most people go through it two or three times in a life.', F(R, 30), GREY, W - 120)
ty = y + 40
# three-phase bar
tw3 = (W - 120) / 3
labels = [('PHASE 1', '12th from Moon', 'Losses, expenses, endings. Pruning begins.'), ('PHASE 2', 'Saturn on Moon', 'Peak pressure. Health, mind, responsibility.'), ('PHASE 3', '2nd from Moon', 'Rebuilding, money, family. The lesson lands.')]
cols = [(180, 190, 200), (60, 80, 110), (140, 165, 170)]
for i, (p, h, body) in enumerate(labels):
    x0 = 60 + i * tw3
    d.rectangle((x0, ty, x0 + tw3 - 4, ty + 70), fill=cols[i])
    d.text((x0 + 14, ty + 10), p, font=F(SB, 18), fill=CREAM)
    d.text((x0 + 14, ty + 38), '2.5 years', font=F(S, 18), fill=CREAM)
    d.text((x0 + 4, ty + 84), h, font=F(SB, 20), fill=TEAL)
    para(d, x0 + 4, ty + 112, body, F(R, 21), GREY, tw3 - 20, 27)
ty += 220
d.text((60, ty), 'WHEN IT HAPPENS (typical ages)', font=F(SB, 18), fill=GOLD); ty += 34
ly = ty + 30
d.line((60, ly, W - 60, ly), fill=INK, width=3)
for age in (0, 30, 60, 90):
    x = 60 + (W - 120) * age / 90
    d.line((x, ly - 8, x, ly + 8), fill=INK, width=3)
    d.text((x - 14, ly + 16), str(age), font=F(S, 20), fill=GREY)
for start_ in (7, 37, 67):
    x0 = 60 + (W - 120) * start_ / 90
    x1 = 60 + (W - 120) * (start_ + 7.5) / 90
    d.rectangle((x0, ly - 22, x1, ly - 4), fill=(60, 80, 110))
d.text((60, ly + 50), 'e.g. ages 7–14, 37–44, 67–74 (depends on your Moon sign)', font=F(I, 22), fill=GREY)
ty = ly + 100
para(d, 60, ty, 'It is not a curse — it is Saturn\'s audit. The people who know where they are in it (start, peak or ending) plan the year very differently from those who don\'t.', F(I, 27), INK, W - 120)
footer(im, d, 'Am I in Sade Sati? →')
im.save(f'{OUT}/edu-05.jpg', quality=92)
reg('edu-05', 'yearly', 'Saturn tests everyone for 7.5 years - Sade Sati explained',
    'Sade Sati: Saturn crossing the sign before, on and after your Moon - 7.5 years in three phases, roughly every 30 years. What each phase brings and how to plan around it. A personalized Vedic year-ahead forecast tells you where you are in it. #sadesati #saturntransit #vedicastrology #shani #astrologyfacts', 'Year Ahead Forecasts')

json.dump(pins, open('/home/ubuntu/drafts/pinterest/edu-pins.json', 'w'), indent=1, ensure_ascii=False)
print(len(pins))
