"""Publish a pin via the Pinterest pin builder already open in Chrome (CDP).
Usage: post_pin.py <file> <title> <desc> <link> <board> [topic]"""
import sys, time
from playwright.sync_api import sync_playwright

f, title, desc, link, board = sys.argv[1:6]
topic = sys.argv[6] if len(sys.argv) > 6 else '星座'
with sync_playwright() as p:
    b = p.chromium.connect_over_cdp('http://localhost:29229')
    pg = [x for c in b.contexts for x in c.pages if 'pinterest.com/pin-creation-tool' in x.url][0]
    pg.bring_to_front()
    pg.reload(); time.sleep(4)
    pg.set_input_files('input[type=file]', f)
    time.sleep(12 if f.endswith('.mp4') else 4)
    pg.fill('input[placeholder="ピンのタイトルを追加する"]', title)
    pg.click('div[aria-label="ピンを説明する"]')
    pg.keyboard.type(desc)
    pg.fill('input[placeholder="リンクを追加する"]', link)
    # board
    pg.get_by_text('ボード', exact=True).click(); time.sleep(1)
    pg.locator('input[aria-label="自分のボードを検索する"]').fill(board); time.sleep(1)
    pg.locator('section[aria-label="ボードフィルター"]').get_by_text(board, exact=True).first.click(); time.sleep(1)
    # topic
    i = pg.locator('input[placeholder="タグを検索する"]'); i.click(); i.fill(topic); time.sleep(2)
    pg.locator('div[aria-selected="false"]').filter(has_text=topic).first.click(); time.sleep(1)
    print('tags:', pg.locator('label:has-text("タグ付けされたトピック")').inner_text())
    print('board ok:', pg.get_by_text(board, exact=True).count() > 0)
    time.sleep(2)
    pg.get_by_role('button', name='公開する').click()
    for _ in range(30):
        time.sleep(1)
        a = pg.locator('a[aria-label="作成したピンに移動する"]')
        if a.count():
            print('published', a.first.get_attribute('href')); break
    else:
        print('no toast')
