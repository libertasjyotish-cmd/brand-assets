import sys
sys.argv = ['x']
src = open('/home/ubuntu/drafts/etsy/make_images.py').read()
head = src[:src.index('# 1 hero')]
exec(head)
PAGES = '/home/ubuntu/drafts/etsy/pages2'
import shutil


def out(name, im):
    im.save(f'{OUT}/{name}', quality=92)


def hero(prefix, lines, bullets, cover):
    im, d = start()
    mock = page_mock(cover, 760, tilt=-4)
    im.paste(mock, (W - mock.width - 40, 420), mock)
    y = 430
    for i, (t, col) in enumerate(lines):
        shadow(d, (100, y + i * 115), t, F(EN, 88), col)
    for i, t in enumerate(bullets):
        d.text((100, y + 420 + i * 58), '◆  ' + t, font=F(EN_R, 36), fill=WHITE)
    footer(d)
    out(f'{prefix}-01-hero.jpg', im)


def contents(prefix, title, items, mockpage):
    im, d = start()
    mock = page_mock(mockpage, 960)
    im.paste(mock, (80, 300), mock)
    x = 80 + mock.width + 40
    shadow(d, (x, 350), title, F(EN, 90), GOLD)
    for i, t in enumerate(items):
        for j, l in enumerate(wrap(d, t, F(EN_R, 36), W - x - 100)):
            d.text((x, 470 + i * 80 + j * 40), ('◆  ' if j == 0 else '     ') + l, font=F(EN_R, 36), fill=WHITE)
    footer(d)
    out(f'{prefix}-02-contents.jpg', im)


def feature(prefix, n, big, sub, paras):
    im, d = start()
    shadow(d, (100, 380), big, F(EN, 100), GOLD)
    d.text((100, 520), sub, font=F(EN_R, 46), fill=WHITE)
    y = 660
    for p in paras:
        for l in wrap(d, p, F(EN_R, 40), W - 200):
            d.text((100, y), l, font=F(EN_R, 40), fill=WHITE if p == paras[0] else DIM); y += 54
        y += 40
    footer(d)
    out(f'{prefix}-0{n}-feature.jpg', im)


def steps(prefix, n, rows):
    im, d = start()
    shadow(d, (100, 340), 'How it works', F(EN, 96), GOLD)
    for i, (num, t, body) in enumerate(rows):
        x = 100 + i * 620
        d.ellipse((x, 480, x + 130, 610), outline=GOLD, width=4)
        d.text((x + 65 - d.textlength(num, font=F(EN, 72)) / 2, 500), num, font=F(EN, 72), fill=GOLD)
        d.text((x, 660), t, font=F(EN, 48), fill=WHITE)
        for j, l in enumerate(wrap(d, body, F(EN_R, 36), 560)):
            d.text((x, 750 + j * 50), l, font=F(EN_R, 36), fill=DIM)
    footer(d)
    out(f'{prefix}-0{n}-how.jpg', im)


# ---------- Compatibility ----------
hero('compat', [('Why did you', WHITE), ('two meet?', WHITE), ('Vedic Compatibility Report', GOLD)],
     ['Two birth charts compared  ·  10 chapters PDF', 'Love · marriage · friendship · business — any two people',
      'When your relationship moves: 12-month timeline'], 'compat-00')
contents('compat', "What's inside",
         ['The map of your relationship (one page)', 'Two blueprints: Moon, ascendant, nakshatra', 'Hearts: how your Moons fit together', 'What each of you brings to the other',
          'Words & values (Mercury, Sun, Jupiter)', 'Action & passion (Mars & Venus)', 'Staying power (Saturn)',
          'The meaning of this bond — why you met', 'When the relationship moves: next 12 months', 'How to nurture it',
          'Traditional 36-point score (love & marriage only)'], 'compat-13')
feature('compat', 3, 'Why did you two meet?', 'The destiny chapter',
        ['Where your partner\'s Moon, Sun and Venus fall in your chart — and where the Rahu–Ketu axis of one touches the other — tells a story about why this bond exists and what it is here to teach each of you.',
         'Calculated from both birth charts. Written as a story you can read again on hard days.'])
feature('compat', 4, 'When does it move?', 'A 12-month relationship timeline',
        ['Month by month: when Jupiter, Saturn and Venus pass through the relationship houses of both charts, and when either person\'s planetary period (dasha) changes.',
         'Named phases — a time to draw closer, a time that tests you, a time to decide — with the best month to take the next step and the month to slow down and talk.'])
steps('compat', 5, [('1', 'Enter two people', 'Date, time and place of birth for Person A and Person B, the type of relationship (love / friends / business), and your language.'),
                    ('2', 'We calculate', 'Both sidereal charts, synastry overlays, dashas and 12 months of transits — with a professional calculation engine.'),
                    ('3', 'PDF within 24h', 'Your report arrives by email (or Etsy message) in English, Español, Português, Bahasa Indonesia, Japanese or Arabic.')])
feature('compat', 6, 'Any two people', 'No gender required',
        ['Couples of any gender, best friends, business partners, parent and child. Choose the relationship type and the report adapts its chapters.',
         'The traditional 36-point marriage score is included only for love & marriage; other relationships focus on how you feel, talk, act and share responsibility.'])

# ---------- Year ahead ----------
hero('yearly', [('Is this your year', WHITE), ('to make the move?', WHITE), ('Year-Ahead Forecast', GOLD)],
     ['Next 12 months from your order  ·  9 chapters PDF', 'Dasha periods + Jupiter, Saturn, Rahu & Ketu transits',
      'A year to move, or to prepare — and which months'], 'yearly-00')
contents('yearly', "What's inside",
         ['The theme of your year (one page)', 'Your planetary period (dasha) and what changes this year', 'Jupiter, Saturn, Rahu & Ketu over your chart',
          'Four quarters — the seasons of your year', 'Work & money · relationships · mind & body',
          'A year to move, or to prepare? — decision windows by month', 'Best months, care months, action plan'],
         'yearly-12')
feature('yearly', 3, 'Move — or prepare?', 'The turning-point chapter',
        ['A job change, going independent, a move, going back to study, a relationship to commit to. Your chart says whether this is the year — and in which months — from dasha changes and Jupiter, Saturn, Rahu & Ketu over your Moon.',
         'Every verdict names the placement behind it. If the sky is quiet, we say so and show you what to build instead. No invented events, no promises.'])
steps('yearly', 4, [('1', 'Order & personalize', 'Enter your date, time and place of birth and your report language in the personalization box.'),
                    ('2', 'We calculate', 'Your birth chart, current dasha, Sade Sati and twelve months of transits with a professional engine.'),
                    ('3', 'PDF within 24h', 'Your report arrives by email (or Etsy message) in English, Español, Português, Bahasa Indonesia, Japanese or Arabic.')])
feature('yearly', 5, 'Not a calendar year', 'Best months. Care months.',
        ['Order in any month and the forecast covers the coming twelve — from next month to the same month next year. No waiting for January.',
         'Which months carry a tailwind for work, money and relationships, and which ask you to slow down and build. Calm, practical voice — seasons to use, never omens.'])

# ---------- Career ----------
hero('career', [('What is your', WHITE), ('true calling?', WHITE), ('Career & Wealth Report', GOLD)],
     ['Work style · talents · money  ·  8 chapters PDF', '10th, 2nd & 11th houses, D10 chart, dasha, Ashtakavarga',
      'Employed or independent? When your career moves'], 'career-00')
contents('career', "What's inside",
         ['Your calling at a glance — type, gifts, stance', 'The shape of your calling (10th house & its lord)', 'Talents & skills — and one you have not used yet',
          'Employed, independent or in partnership?', 'Your money pattern — how income arrives, how it stays', 'The cycles of your working life (dasha)',
          'When your career moves — next 12 months', 'Action plan: next 3 months and this year'], 'career-10')
feature('career', 3, 'Employed or independent?', 'Not a job title — how you are built to work',
        ['The 6th, 7th and 10th houses, Saturn and Rahu show whether your strengths compound inside an organisation, on your own, or with a partner — and the conditions to have in place before you change.',
         'We describe the nature of work that suits you and the roles where you carry authority. We never declare a single "destined" job.'])
steps('career', 4, [('1', 'Order & personalize', 'Enter your date, time and place of birth and your report language in the personalization box.'),
                    ('2', 'We calculate', 'Your birth chart, D10 career chart, dasha periods and twelve months of transits with a professional engine.'),
                    ('3', 'PDF within 24h', 'Your report arrives by email (or Etsy message) in English, Español, Português, Bahasa Indonesia, Japanese or Arabic.')])
feature('career', 5, 'Money & timing', 'Your pattern, your months',
        ['2nd & 11th houses, Venus and Jupiter, Ashtakavarga scores: how income tends to come to you, how you keep it, where spending swells. Understanding, not investment advice.',
         'Then the next 12 months: months suited to a job change, to preparing independence, to promotion and recognition, to re-training — and the months not to rush.'])
print('ok')
