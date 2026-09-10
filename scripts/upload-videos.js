// Upload the 15s product videos to each active listing (one video per listing on Etsy).
const fs = require('fs');
const { auth, call, SHOP_ID } = require('./_client');

const VID = '/home/ubuntu/drafts/etsy/video';
const MATCH = [
  [/compatib/i, 'compat'],
  [/year|forecast/i, 'yearly'],
  [/career|wealth|vocation/i, 'career'],
  [/birth chart/i, 'birthchart'],
];

(async () => {
  const h = await auth();
  const { results } = await call(h, 'GET', `/shops/${SHOP_ID}/listings/active?limit=50`);
  for (const l of results) {
    const key = (MATCH.find(([re]) => re.test(l.title)) || [])[1];
    if (!key) { console.log('skip', l.listing_id, l.title); continue; }
    const existing = await call(h, 'GET', `/listings/${l.listing_id}/videos`).catch(() => ({ results: [] }));
    for (const v of existing.results || []) {
      await call(h, 'DELETE', `/shops/${SHOP_ID}/listings/${l.listing_id}/videos/${v.video_id}`);
      console.log('deleted old video', v.video_id);
    }
    const file = `${VID}/etsy-${key}-15s.mp4`;
    const fd = new FormData();
    fd.append('video', new Blob([fs.readFileSync(file)], { type: 'video/mp4' }), `etsy-${key}-15s.mp4`);
    fd.append('name', `etsy-${key}-15s.mp4`);
    const r = await call(h, 'POST', `/shops/${SHOP_ID}/listings/${l.listing_id}/videos`, fd);
    console.log('uploaded', l.listing_id, key, '->', r.video_id, r.video_state);
  }
})().catch((e) => { console.error(e.message); process.exit(1); });
