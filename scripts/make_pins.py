import sys, os, json
sys.argv = ['x']
src = open('/home/ubuntu/drafts/etsy/make_images.py').read()
exec(src[:src.index('# 1 hero')])

OUT = '/home/ubuntu/drafts/pinterest/pins'
os.makedirs(OUT, exist_ok=True)
PW, PH = 1000, 1500
PAGES2 = '/home/ubuntu/drafts/etsy/pages2'
PAGES1 = '/home/ubuntu/drafts/etsy/pages'

URL = {
    'natal': 'https://www.etsy.com/listing/4570455921',
    'compat': 'https://www.etsy.com/listing/4572458099',
    'yearly': 'https://www.etsy.com/listing/4572470899',
    'career': 'https://www.etsy.com/listing/4572487096',
    'shop': 'https://www.etsy.com/shop/LibertasJyotish',
}
PRICE = {'natal': '$59', 'compat': '$69', 'yearly': '$49', 'career': '$49'}


def pbase():
    im = base(PW, PH)
    d = ImageDraw.Draw(im)
    logo = Image.open(f'{IMG}/libertas-logo.png').convert('RGBA').resize((90, 90), Image.LANCZOS)
    im.paste(logo, (60, 60), logo)
    d.text((170, 74), 'LIBERTAS JYOTISH', font=F(EN, 34), fill=GOLD)
    d.text((170, 116), 'Vedic Astrology  /  Jyotisha', font=F(EN_R, 22), fill=WHITE)
    return im, d


def pfooter(d, text):
    d.line((60, PH - 120, PW - 60, PH - 120), fill=GOLD, width=1)
    f = F(EN_R, 26)
    d.text(((PW - d.textlength(text, font=f)) / 2, PH - 100), text, font=f, fill=DIM)


def mock(name, height, tilt=0, folder=PAGES2):
    global PAGES
    PAGES = folder
    return page_mock(name, height, tilt)


def headline(d, y, lines, size=76):
    for i, (t, col) in enumerate(lines):
        for l in wrap(d, t, F(EN, size), PW - 120):
            shadow(d, (60, y), l, F(EN, size), col); y += int(size * 1.2)
    return y


def pin_product(name, prod, lines, sub, bullets, page, folder=PAGES2, tilt=-3):
    im, d = pbase()
    y = headline(d, 200, lines)
    d.text((60, y + 10), sub, font=F(EN_R, 32), fill=WHITE)
    y += 80
    for b in bullets:
        for j, l in enumerate(wrap(d, b, F(EN_R, 28), PW - 140)):
            d.text((60, y), ('◆  ' if j == 0 else '     ') + l, font=F(EN_R, 28), fill=DIM); y += 38
        y += 8
    m = mock(page, 640, tilt, folder)
    im.paste(m, (PW - m.width + 40, PH - m.height - 90), m)
    d = ImageDraw.Draw(im)
    tag = f'{PRICE[prod]} launch price · PDF within 24h'
    pfooter(d, tag)
    im.save(f'{OUT}/{name}.jpg', quality=92)


def pin_text(name, big, paras, cta, small_mock=None, folder=PAGES2):
    im, d = pbase()
    y = headline(d, 200, [(big, GOLD)], 72)
    y += 30
    for p in paras:
        for l in wrap(d, p, F(EN_R, 34), PW - 120):
            d.text((60, y), l, font=F(EN_R, 34), fill=WHITE if p == paras[0] else DIM); y += 46
        y += 30
    if small_mock:
        m = mock(small_mock, 420, -3, folder)
        im.paste(m, (PW - m.width + 40, PH - m.height - 90), m)
        d = ImageDraw.Draw(im)
    pfooter(d, cta)
    im.save(f'{OUT}/{name}.jpg', quality=92)


def pin_list(name, big, items, cta, prod):
    im, d = pbase()
    y = headline(d, 200, [(big, GOLD)], 72) + 30
    for i, (h, body) in enumerate(items):
        d.text((60, y), h, font=F(EN, 36), fill=WHITE); y += 48
        for l in wrap(d, body, F(EN_R, 28), PW - 120):
            d.text((60, y), l, font=F(EN_R, 28), fill=DIM); y += 38
        y += 26
    pfooter(d, cta)
    im.save(f'{OUT}/{name}.jpg', quality=92)


pins = []


def reg(name, prod, title, desc, board):
    pins.append({'file': f'{name}.jpg', 'link': URL[prod], 'board': board, 'title': title, 'description': desc})


# ---------- Natal ----------
pin_product('natal-01', 'natal', [('Your birth chart,', WHITE), ('read the Vedic way', WHITE)],
            'Personalized Vedic birth chart report · 10 chapters PDF',
            ['Sidereal zodiac, Lahiri ayanamsa — your real Moon sign & nakshatra', 'Personality, love, career, wealth, health, dasha timeline',
             'Written for you, in English, Spanish, Portuguese, Indonesian, Japanese or Arabic'], 'p00', PAGES1)
reg('natal-01', 'natal', 'Vedic Birth Chart Report — personalized PDF',
    'A personalized Vedic (Indian) astrology birth chart reading: sidereal Moon sign, nakshatra, ascendant, dasha timeline, love, career, wealth. 10-chapter PDF delivered within 24h. #vedicastrology #birthchart #jyotish #kundli #natalchart', 'Vedic Birth Chart Reports')

pin_text('natal-02', 'Why is your Vedic Sun sign different?',
         ['Western astrology uses the tropical zodiac; Vedic astrology uses the sidereal zodiac — about 24° apart. Roughly 3 in 4 people move one sign back.',
          'The Moon sign and nakshatra (lunar mansion) matter more than the Sun in Jyotish. Discover yours in a personalized report.'],
         'Personalized Vedic birth chart report · from $59', 'p00', PAGES1)
reg('natal-02', 'natal', 'Vedic vs Western astrology: why your sign changes',
    'Sidereal vs tropical zodiac explained — and why your Vedic Moon sign and nakshatra matter more than your Sun sign. Get your personalized Vedic birth chart report (PDF). #vedicastrology #siderealastrology #moonsign #nakshatra', 'Vedic Astrology Basics')

pin_list('natal-03', 'What a Vedic birth chart reveals',
         [('Your nature', 'Ascendant, Moon sign and nakshatra — the three pillars of who you are.'),
          ('Your timing', 'Vimshottari dasha: which planetary period you are in now and what it asks of you.'),
          ('Your houses', 'Love (7th), career (10th), wealth (2nd & 11th), health (6th) — read from your actual chart.'),
          ('Your remedies', 'Gentle, practical suggestions — never fear, never fixed fate.')],
         'Personalized 10-chapter PDF report · $59', 'natal')
reg('natal-03', 'natal', 'What a Vedic birth chart reading reveals',
    'Ascendant, Moon sign, nakshatra, dasha periods and the houses of love, career and wealth — what a personalized Vedic astrology report covers. PDF within 24h. #vedicastrology #birthchartreading #jyotish #dasha', 'Vedic Birth Chart Reports')

pin_text('natal-04', 'Do you need your exact birth time?',
         ['For a Vedic chart, yes — the ascendant changes every two hours and the houses move with it.',
          'Do not know it? Check your birth certificate or hospital record. If it is unknown we use noon and mark which chapters are time-sensitive.'],
         'Vedic birth chart report · personalized PDF', None)
reg('natal-04', 'natal', 'Why your birth time matters in Vedic astrology',
    'The ascendant changes every two hours — here is why the exact birth time matters for a Vedic chart and what to do if you do not know it. #vedicastrology #birthtime #ascendant #kundli', 'Vedic Astrology Basics')

# ---------- Compatibility ----------
pin_product('compat-01', 'compat', [('Why did you', WHITE), ('two meet?', WHITE)],
            'Vedic compatibility report for any two people',
            ['Two birth charts compared · love, marriage, friendship or business', 'The meaning of this bond — and when it moves in the next 12 months',
             'Traditional 36-point score for love & marriage'], 'compat-00')
reg('compat-01', 'compat', 'Why did you two meet? — Vedic compatibility report',
    'A personalized Vedic astrology compatibility reading for two people — couples, friends or business partners. Why this bond exists, how your Moons fit, and when your relationship moves in the coming 12 months. PDF within 24h. #compatibility #synastry #vedicastrology #kundlimatching #soulmate', 'Compatibility & Relationships')

pin_list('compat-02', 'Signs the bond is karmic (Vedic view)',
         [('Rahu–Ketu axis', 'One person\'s nodes falling on the other\'s Moon or Sun: a bond with something to complete.'),
          ('Moon in the 7th', 'Their Moon in your 7th house — a partnership feeling from the first meeting.'),
          ('Same nakshatra lord', 'Shared lunar mansion rulers: instant familiarity.'),
          ('Saturn contacts', 'Duty, patience, staying power — the glue of long relationships.')],
         'Two-chart compatibility report · $69', 'compat')
reg('compat-02', 'compat', 'Karmic connection signs in Vedic astrology',
    'Rahu-Ketu on the Moon, Moon in the 7th house, shared nakshatra lords, Saturn contacts — what Vedic synastry looks for in a fated bond. Personalized two-chart report. #karmicrelationship #vedicastrology #synastry #twinflame #compatibility', 'Compatibility & Relationships')

pin_text('compat-03', 'Not just for couples',
         ['Best friends. Business partners. Parent and child. The report adapts its chapters to the relationship you choose — no gender required.',
          'The traditional 36-point marriage score appears only for love & marriage; other bonds focus on how you feel, talk, act and share responsibility.'],
         'Compatibility report for any two people · $69', 'compat-00')
reg('compat-03', 'compat', 'Vedic compatibility for friends, business partners & couples',
    'A Vedic astrology compatibility report that adapts to love, friendship or business — any two people, no gender required. Moon, Venus, Mars and Saturn overlays plus a 12-month relationship timeline. #compatibility #businesspartner #friendship #vedicastrology', 'Compatibility & Relationships')

pin_text('compat-04', 'When will your relationship move?',
         ['Month by month: when Jupiter, Saturn and Venus cross the relationship houses of both charts, and when either person\'s dasha changes.',
          'A time to draw closer, a time that tests you, a time to decide — with the best month to take the next step.'],
         'Compatibility report with 12-month timeline · $69', 'compat-00')
reg('compat-04', 'compat', 'When will your relationship move? 12-month Vedic timeline',
    'Personalized 12-month relationship timeline from two Vedic birth charts: the months to draw closer, the months that test you, the month to decide. #relationshiptiming #vedicastrology #compatibility #synastry', 'Compatibility & Relationships')

# ---------- Year ahead ----------
pin_product('yearly-01', 'yearly', [('Is this your year', WHITE), ('to make the move?', WHITE)],
            'Vedic year-ahead forecast · the 12 months after you order',
            ['Career change, independence, relocation, study, relationships', 'Dasha changes + Jupiter, Saturn, Rahu & Ketu over your Moon',
             'A year to move, or a year to prepare — and which months'], 'yearly-00')
reg('yearly-01', 'yearly', 'Is this your year to make the big move? — Vedic 12-month forecast',
    'A personalized Vedic astrology forecast for the next 12 months (starting the month after you order — not January). Whether this is a year to move or to prepare, and in which months. Dasha, Sade Sati, Jupiter & Saturn transits. #yearahead #vedicastrology #forecast #careerchange #dasha', 'Year Ahead Forecasts')

pin_text('yearly-02', 'Not a calendar year',
         ['Order in any month and your forecast covers the coming twelve — from next month to the same month next year.',
          'No waiting for January, no waiting for your birthday. Best months, care months, and a turning-point verdict with the placements behind it.'],
         'Year-ahead forecast · $49 · PDF within 24h', 'yearly-00')
reg('yearly-02', 'yearly', 'A 12-month Vedic forecast that starts when you order',
    'Not a January-to-December horoscope: a personalized Vedic forecast covering the twelve months after your order, with best months, care months and decision windows. #12monthforecast #vedicastrology #yearahead #transits', 'Year Ahead Forecasts')

pin_list('yearly-03', 'Signs of a turning-point year',
         [('Mahadasha change', 'Your major planetary period ends and a new one begins — the biggest shift Jyotish knows.'),
          ('Jupiter over your 10th or 1st', 'Expansion in work and identity.'),
          ('Saturn leaving Sade Sati', 'Seven and a half years of pressure lift.'),
          ('Rahu–Ketu axis moves', 'Ambition and release change houses.')],
         'See which apply to you · year-ahead forecast $49', 'yearly')
reg('yearly-03', 'yearly', 'Signs of a turning-point year in Vedic astrology',
    'Mahadasha change, Jupiter over the 10th house, Saturn leaving Sade Sati, Rahu-Ketu moving — the placements Vedic astrology reads as a turning-point year. Personalized 12-month forecast PDF. #dasha #sadesati #vedicastrology #turningpoint #forecast', 'Vedic Astrology Basics')

pin_text('yearly-04', 'What is Sade Sati?',
         ['The seven-and-a-half years when Saturn passes over the sign before, on, and after your Moon. Pressure, responsibility, pruning.',
          'Knowing where you are in it — start, peak, or ending — changes how you plan the year. Your forecast tells you.'],
         'Year-ahead forecast with Sade Sati · $49', None)
reg('yearly-04', 'yearly', 'What is Sade Sati? Saturn over your Moon explained',
    'Sade Sati: the 7.5-year Saturn transit over your Moon sign in Vedic astrology — what it means and how to plan around it. Personalized year-ahead forecast. #sadesati #saturntransit #vedicastrology #shani', 'Vedic Astrology Basics')

# ---------- Career ----------
pin_product('career-01', 'career', [('What is your', WHITE), ('true calling?', WHITE)],
            'Vedic career, vocation & wealth report · 8 chapters PDF',
            ['How you are built to work — not a job title', 'Employed, independent or in partnership?',
             'Your money pattern and when your career moves (next 12 months)'], 'career-00')
reg('career-01', 'career', 'What is your true calling? — Vedic career & wealth report',
    'A personalized Vedic astrology career reading: 10th house, D10 chart, dasha and transits — the kind of work where your strengths compound, employed vs independent, your money pattern, and when your career moves. PDF within 24h. #careerastrology #vedicastrology #truecalling #vocation #d10chart', 'Career & Wealth')

pin_list('career-02', 'Employed or independent? Ask your chart',
         [('Saturn strong', 'Structure, long games, institutions — you compound inside organisations.'),
          ('Rahu in the 10th', 'Unconventional paths, new industries, being first.'),
          ('7th-house emphasis', 'Partnership: you do your best work with one other person.'),
          ('Strong 3rd & 6th', 'Self-made effort, freelancing, consulting.')],
         'Career & wealth report · $49', 'career')
reg('career-02', 'career', 'Employed or self-employed? What Vedic astrology says',
    'Saturn, Rahu in the 10th, the 7th house, the 3rd and 6th — how a Vedic chart hints whether you thrive employed, independent or in partnership. Personalized career report PDF. #careerastrology #selfemployed #vedicastrology #10thhouse', 'Career & Wealth')

pin_text('career-03', 'How money comes to you',
         ['The 2nd house is what you earn and keep; the 11th is what flows in from others. Venus and Jupiter show ease; Saturn shows slow, steady accumulation.',
          'Understanding your pattern — not investment advice — so you stop fighting your own nature.'],
         'Career & wealth report · $49 · PDF within 24h', 'career-00')
reg('career-03', 'career', 'Your money pattern in Vedic astrology (2nd & 11th house)',
    'How income arrives and how it stays: the 2nd and 11th houses, Venus, Jupiter and Saturn in your Vedic chart. Part of a personalized career & wealth report. #moneyastrology #vedicastrology #wealth #11thhouse', 'Career & Wealth')

pin_text('career-04', 'Best months to change jobs',
         ['Jupiter over your 10th or 6th, a dasha change, Saturn leaving a tense house — the months when a career move is supported by your chart.',
          'And the months not to rush. Your report names them for the next 12 months.'],
         'Career timing in your report · $49', 'career-00')
reg('career-04', 'career', 'Best months for a career change — Vedic timing',
    'When does your chart support a job change, going independent or a promotion? Jupiter, Saturn and dasha timing for the next 12 months, in a personalized Vedic career report. #careerchange #careertiming #vedicastrology #jupitertransit', 'Career & Wealth')

# ---------- Shop / general ----------
pin_text('shop-01', 'Four Vedic readings, one chart',
         ['Birth chart · Compatibility · Year ahead · Career & wealth. Every report is calculated from your real birth data with a professional engine and written for you.',
          'Delivered as a PDF within 24 hours in English, Spanish, Portuguese, Indonesian, Japanese or Arabic.'],
         'Launch sale: 25% off every report', 'p00', PAGES1)
reg('shop-01', 'shop', 'Personalized Vedic astrology reports — birth chart, compatibility, year ahead, career',
    'Libertas Jyotish: personalized Vedic (Indian) astrology PDF reports — birth chart, compatibility, 12-month forecast, career & wealth. Calculated from your birth data, delivered within 24h. Launch sale 25% off. #vedicastrology #jyotish #astrologyreport #kundli', 'Vedic Birth Chart Reports')

pin_list('shop-02', 'What is a nakshatra?',
         [('27 lunar mansions', 'The sky divided into 27 parts of 13°20\' — older than the 12 signs.'),
          ('Your birth star', 'The nakshatra your Moon was in at birth — your emotional signature.'),
          ('Deity, symbol, animal', 'Each carries a story that describes you better than a Sun sign.'),
          ('Used for timing', 'Dasha periods are counted from your birth nakshatra.')],
         'Find your nakshatra · Vedic birth chart report $59', 'natal')
reg('shop-02', 'natal', 'What is a nakshatra? Your Vedic birth star explained',
    'Nakshatras — the 27 lunar mansions of Vedic astrology. What your birth star says about you and why dasha timing starts from it. Personalized birth chart report. #nakshatra #vedicastrology #birthstar #moonsign', 'Vedic Astrology Basics')

json.dump(pins, open('/home/ubuntu/drafts/pinterest/pins.json', 'w'), indent=1, ensure_ascii=False)
print(len(pins), 'pins')
