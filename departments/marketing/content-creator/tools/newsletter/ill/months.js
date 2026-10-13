// 12月〜3月号のイラスト（Fluent Emoji・MIT）を月ごとに書き出す
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const path = require('path');
const fs = require('fs');

const ASSETS = path.resolve(__dirname, '../assets');
const ICONS = require('@iconify-json/fluent-emoji/icons.json');
const FONT = path.resolve(__dirname, 'node_modules/@fontsource/m-plus-rounded-1c');
const head = `<meta charset="utf-8"><link rel="stylesheet" href="file://${FONT}/800.css">
<style>html,body{margin:0;background:transparent}svg{display:block}text{font-family:'M PLUS Rounded 1c',sans-serif;font-weight:800}</style>`;

let uid = 0;
function place(name, x, y, size, rot = 0) {
  const ic = ICONS.icons[name];
  if (!ic) throw new Error('no icon ' + name);
  const w = ic.width || ICONS.width || 32, h = ic.height || ICONS.height || 32;
  const p = `m${uid++}_`;
  const b = ic.body.replace(/id="([^"]+)"/g, `id="${p}$1"`).replace(/url\(#([^)]+)\)/g, `url(#${p}$1)`).replace(/href="#([^"]+)"/g, `href="#${p}$1"`);
  return `<svg x="${x}" y="${y}" width="${size}" height="${size}" viewBox="0 0 ${w} ${h}" overflow="visible"><g transform="rotate(${rot} ${w / 2} ${h / 2})">${b}</g></svg>`;
}
const svg = (w, h, inner) => `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${inner}</svg>`;

// 月名バッジ（11月号の霜月バッジと同じ作り）
function badge({ kanji, kana, label, ring, bg = '#dcecfb', bd = '#a9cdee', ink = '#23466e', sub = '#4f7fb1', accent = '#c9372c' }) {
  let r = '';
  for (let i = 0; i < 18; i++) {
    const a = (i / 18) * Math.PI * 2 - Math.PI / 2, s = 76;
    r += place(ring[i % ring.length], 300 + Math.cos(a) * 236 - s / 2, 300 + Math.sin(a) * 236 - s / 2, s, (i * 37) % 50 - 25);
  }
  const [k1, k2] = [...kanji];
  return svg(600, 600, `<defs><radialGradient id="g" cx=".45" cy=".4"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="${bg}"/></radialGradient></defs>
    <circle cx="300" cy="300" r="215" fill="url(#g)" stroke="${bd}" stroke-width="6"/>${r}
    <text x="290" y="282" font-size="180" text-anchor="middle" fill="${ink}">${k1}</text>
    <text x="290" y="455" font-size="180" text-anchor="middle" fill="${ink}">${k2}</text>
    ${[...kana].map((c, i) => `<text x="440" y="${236 + i * 44}" font-size="40" text-anchor="middle" fill="${sub}">${c}</text>`).join('')}
    <text x="150" y="420" font-size="44" text-anchor="middle" fill="${accent}">${label}</text>`);
}

// アイコンを横に並べた挿絵
function cluster(names, size = 210) {
  const step = size * 0.86, w = Math.round(step * (names.length - 1) + size);
  return svg(w, size + 20, names.map((n, i) => place(n, i * step, (i % 2) * 20, size)).join(''));
}

// 説明パネル（11月号の「予防の3本柱」と同じ作り）
function panels(items, { w = 316, h = 330, cols = 0 } = {}) {
  const gap = 20, nc = cols || items.length, nr = Math.ceil(items.length / nc);
  const W = nc * w + (nc - 1) * gap, H = nr * h + (nr - 1) * gap;
  let s = '';
  items.forEach((it, i) => {
    const x = (i % nc) * (w + gap), y0 = Math.floor(i / nc) * (h + gap);
    s += `<g transform="translate(0 ${y0})">`;
    s += `<rect x="${x + 4}" y="4" width="${w - 8}" height="${h - 8}" rx="26" fill="${it.bg}" stroke="${it.bd}" stroke-width="6"/>`;
    const n = it.icons.length, top = 24, area = h - (it.sub ? 128 : 100);
    if (n === 1) s += place(it.icons[0], x + w / 2 - 85, top, 170);
    else if (n === 2) { s += place(it.icons[0], x + 20, top + 20, 140); s += place(it.icons[1], x + w - 160, top + 20, 140); }
    else { s += place(it.icons[0], x + 18, top + 4, 112); s += place(it.icons[1], x + w - 130, top + 4, 112); s += place(it.icons[2], x + w / 2 - 56, top + area - 118, 112); }
    const fs_ = Math.min(44, Math.floor((w - 28) / it.label.length));
    s += `<text x="${x + w / 2}" y="${h - (it.sub ? 62 : 34)}" font-size="${fs_}" text-anchor="middle" fill="${it.col}">${it.label}</text>`;
    if (it.sub) s += `<text x="${x + w / 2}" y="${h - 24}" font-size="${Math.min(26, Math.floor((w - 24) / it.sub.length))}" text-anchor="middle" fill="#555">${it.sub}</text>`;
    s += '</g>';
  });
  return svg(W, H, s);
}

function letters(chars, palette, size = 160) {
  const gap = 14, w = chars.length * (size + gap);
  let s = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${size + 20}" viewBox="0 0 ${w} ${size + 20}"><defs>`;
  palette.forEach((c, i) => {
    s += `<pattern id="p${i}" width="36" height="36" patternUnits="userSpaceOnUse" patternTransform="rotate(${i % 2 ? 45 : 0})">
      <rect width="36" height="36" fill="${c[0]}"/><rect width="18" height="36" fill="${c[1]}" opacity=".55"/><rect width="36" height="18" fill="${c[1]}" opacity=".35"/></pattern>`;
  });
  s += `</defs>`;
  [...chars].forEach((ch, i) => {
    const cx = i * (size + gap) + size / 2 + gap / 2, cy = size / 2 + 8 + (i % 2 ? 10 : 0), c = palette[i % palette.length];
    s += `<circle cx="${cx}" cy="${cy}" r="${size / 2 - 4}" fill="url(#p${i % palette.length})" stroke="#fff" stroke-width="6"/>
      <text x="${cx}" y="${cy + size * 0.22}" font-size="${size * 0.62}" text-anchor="middle" fill="#fff" stroke="${c[2]}" stroke-width="10" paint-order="stroke" stroke-linejoin="round">${ch}</text>`;
  });
  return s + '</svg>';
}

const PAL = {
  warm: [['#ff9f43', '#ffd28a', '#c25e00'], ['#ff6b6b', '#ffb3b3', '#b02a2a'], ['#54a0ff', '#a9cfff', '#1e5aa8']],
  green: [['#2ecc71', '#a3e8bf', '#1b7a43'], ['#f6b93b', '#fde2a3', '#a86a00'], ['#4a90d9', '#b3d4f5', '#1f5a99'], ['#e66767', '#f7b8b8', '#9e2e2e']],
  food: [['#f27a12', '#ffc27a', '#9a4300'], ['#5aa04a', '#b5dea8', '#2f6326'], ['#e8403f', '#ffb0b0', '#9a1d1d']],
  blue: [['#4a90d9', '#b3d4f5', '#1f5a99'], ['#7b5ea7', '#cdbbe8', '#4a2f78'], ['#2ecc71', '#a3e8bf', '#1b7a43']],
  pink: [['#ff7fa3', '#ffc4d4', '#a8355b'], ['#f6b93b', '#fde2a3', '#a86a00'], ['#5aa04a', '#b5dea8', '#2f6326']],
};
const C = { // パネルの色
  o: { bg: '#fff4e3', bd: '#f0a43a', col: '#d9821a' }, g: { bg: '#eaf7ec', bd: '#4fb062', col: '#2f8a43' },
  p: { bg: '#fdeef4', bd: '#e87aa0', col: '#d6467a' }, b: { bg: '#ebf6ff', bd: '#3d8fd6', col: '#2f6fb0' },
  r: { bg: '#fff0ec', bd: '#f07b5a', col: '#d9433f' }, y: { bg: '#fffbe9', bd: '#e8c45a', col: '#a87a00' },
};
const P = (c, label, icons, sub) => ({ ...C[c], label, icons, sub });

const MONTHS = {
  m12: {
    badge: badge({ kanji: '師走', kana: 'しわす', label: '12月', ring: ['snowflake', 'christmas-tree', 'snowman', 'snowflake', 'bell', 'wrapped-gift'] }),
    toji: cluster(['sun-behind-cloud', 'hot-springs', 'lemon'], 200),
    winter: cluster(['snowman', 'scarf', 'hot-beverage'], 200),
    p2a: panels([P('o', '手洗い', ['soap', 'droplet'], '指の間・爪・手首まで'), P('b', '換気', ['window', 'wind-face'], 'こまめに空気を入れかえ'), P('g', '加湿', ['droplet', 'potted-plant'], '湿度40〜60％が目安'), P('p', '口のケア', ['toothbrush', 'tooth'], '歯みがき・入れ歯の手入れ')]),
    p2b: cluster(['face-with-medical-mask', 'microbe', 'syringe'], 200),
    p3a: panels([P('r', 'むせる・せきこむ', ['face-exhaling'], '食事中や飲み物で'), P('o', '声がガラガラ', ['speaking-head'], '食後に声が変わる'), P('y', '微熱が続く', ['face-with-thermometer'], 'なんとなく元気がない'), P('b', '食事に時間がかかる', ['stopwatch'], '食べる量が減る')]),
    p3b: panels([P('g', '口のケア', ['toothbrush'], '毎食後と寝る前'), P('o', '食べる姿勢', ['chair'], 'あごを軽く引く'), P('p', 'お口の体操', ['mouth'], 'パ・タ・カ・ラ'), P('b', '食後すぐ横にならない', ['bed'], '30分ほど体を起こす')], { cols: 2 }),
    p3c: cluster(['older-person', 'stethoscope'], 200),
    p4food: cluster(['leafy-green'], 260),
    p4dish: cluster(['pot-of-food'], 260),
    after: cluster(['broom', 'calendar', 'sparkles'], 200),
    L2: letters('かぜよぼう', PAL.warm, 150), L3: letters('ごえん', PAL.green, 170), L4: letters('はくさい', PAL.food, 160),
  },
  m01: {
    badge: badge({ kanji: '睦月', kana: 'むつき', label: '1月', ring: ['pine-decoration', 'sunrise', 'sparkles', 'pine-decoration', 'red-envelope', 'sunrise-over-mountains'], bg: '#fde8e8', bd: '#f2a7a7', ink: '#8a1f1f', sub: '#c9372c', accent: '#b8892b' }),
    newyear: cluster(['sunrise-over-mountains', 'pine-decoration', 'sparkles'], 200),
    nanakusa: cluster(['steaming-bowl', 'herb', 'seedling'], 200),
    p2a: panels([P('o', '足ぶみ', ['chair', 'foot'], '座ったまま30秒'), P('g', 'かかと上げ', ['leg'], 'いすにつかまって'), P('b', 'ひざ伸ばし', ['chair'], '3秒止めて、ゆっくり'), P('p', '肩まわし', ['flexed-biceps'], '前に5回・後ろに5回')]),
    p2b: cluster(['person-in-lotus-position', 'person-walking'], 200),
    p3a: panels([P('r', '口や唇が乾く', ['mouth'], ''), P('o', '皮膚がカサカサ', ['raised-back-of-hand'], ''), P('y', 'おしっこの色が濃い', ['toilet'], ''), P('b', 'だるい・ふらつく', ['face-with-spiral-eyes'], '')], { h: 300 }),
    p3b: panels([P('o', '起きたとき', ['sunrise'], ''), P('g', '食事のとき', ['bowl-with-spoon'], ''), P('b', 'お風呂の前後', ['bathtub'], ''), P('p', '寝る前', ['crescent-moon'], '')], { h: 300, cols: 2 }),
    p3c: cluster(['teacup-without-handle', 'cup-with-straw', 'glass-of-milk'], 200),
    p4food: cluster(['tangerine', 'tangerine'], 230),
    p4dish: cluster(['custard', 'tangerine'], 230),
    after: cluster(['sunrise', 'pine-decoration'], 200),
    L2: letters('たいそう', PAL.green, 160), L3: letters('だっすい', PAL.blue, 160), L4: letters('みかん', PAL.food, 170),
  },
  m02: {
    badge: badge({ kanji: '如月', kana: 'きさらぎ', label: '2月', ring: ['cherry-blossom', 'snowflake', 'blossom', 'cherry-blossom', 'snowflake', 'white-flower'], bg: '#fdebf2', bd: '#f3a9c4', ink: '#7a2550', sub: '#c2457a', accent: '#2f6fb0' }),
    setsubun: cluster(['ogre', 'beans', 'sushi'], 200),
    kisaragi: cluster(['coat', 'scarf', 'gloves'], 200),
    p2a: panels([P('b', 'ぬるめのお湯', ['bathtub', 'thermometer'], '38〜40℃くらい'), P('o', 'やさしく洗う', ['soap'], 'ゴシゴシこすらない'), P('g', 'すぐに保湿', ['lotion-bottle'], 'お風呂上がりすぐ'), P('p', '肌着は綿', ['t-shirt'], 'チクチクを避ける')]),
    p2b: cluster(['droplet', 'lotion-bottle', 'potted-plant'], 200),
    p3a: panels([P('r', '朝', ['alarm-clock'], '起きて1時間以内'), P('b', '夜', ['crescent-moon'], '寝る前')], { w: 300, h: 300 }),
    p3b: panels([P('o', '減塩', ['salt'], '1日6g未満が目標'), P('g', '野菜・果物', ['broccoli', 'banana'], 'カリウムをとる'), P('b', '体を温める', ['scarf'], '急な寒さを避ける'), P('p', '適度な運動', ['person-walking'], '散歩など無理なく')], { cols: 2 }),
    p3c: cluster(['anatomical-heart', 'stethoscope'], 200),
    p4food: cluster(['broccoli'], 260),
    p4dish: cluster(['broccoli', 'bowl-with-spoon'], 230),
    after: cluster(['cherry-blossom', 'blossom'], 200),
    L2: letters('ほしつ', PAL.blue, 170), L3: letters('けつあつ', PAL.warm, 160), L4: letters('ブロッコリー', PAL.food, 130),
  },
  m03: {
    badge: badge({ kanji: '弥生', kana: 'やよい', label: '3月', ring: ['cherry-blossom', 'tulip', 'seedling', 'blossom', 'cherry-blossom', 'peach'], bg: '#eef7e6', bd: '#a9d68b', ink: '#2f5d1e', sub: '#4f8a33', accent: '#d6467a' }),
    hina: cluster(['japanese-dolls', 'peach', 'cherry-blossom'], 200),
    spring: cluster(['tulip', 'seedling', 'sun'], 200),
    p2a: panels([P('b', 'マスク・メガネ', ['face-with-medical-mask', 'glasses'], '外出するとき'), P('o', '玄関で払う', ['coat'], '家に持ちこまない'), P('g', '洗濯物は部屋干し', ['t-shirt', 'window'], '飛ぶ日は特に'), P('p', '花粉情報を確認', ['sun-behind-cloud'], '晴れ・風の日は多い')]),
    p2b: cluster(['sneezing-face', 'evergreen-tree'], 200),
    p3a: panels([P('r', '立ち上がるとき', ['chair'], ''), P('o', '歩きはじめ', ['person-walking'], ''), P('y', '階段の上り下り', ['leg'], '特に下り'), P('b', '正座がつらい', ['older-person'], '')], { h: 300 }),
    p3b: panels([P('g', '太ももの体操', ['chair', 'leg'], 'ひざ伸ばし'), P('o', '体重管理', ['balance-scale'], 'ひざの負担を減らす'), P('b', '冷やさない', ['scarf'], 'ひざ掛け・サポーター'), P('p', '早めに受診', ['hospital'], '整形外科へ')], { cols: 2 }),
    p3c: cluster(['older-person', 'woman-health-worker'], 200),
    p4food: cluster(['strawberry', 'strawberry'], 230),
    p4dish: cluster(['strawberry', 'glass-of-milk'], 230),
    after: cluster(['cherry-blossom', 'tulip'], 200),
    L2: letters('かふんしょう', PAL.pink, 130), L3: letters('ひざ', PAL.green, 180), L4: letters('いちご', PAL.food, 170),
  },
};

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const page = await browser.newPage({ deviceScaleFactor: 2 });
  await page.setViewportSize({ width: 1500, height: 1000 });
  for (const [m, arts] of Object.entries(MONTHS)) {
    fs.mkdirSync(`${ASSETS}/${m}`, { recursive: true });
    for (const [name, s] of Object.entries(arts)) {
      await page.setContent(`<html><head>${head}</head><body>${s}</body></html>`);
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(80);
      await page.locator('body > svg').first().screenshot({ path: `${ASSETS}/${m}/${name}.png`, omitBackground: true });
    }
  }
  await browser.close();
  console.log('done');
})();
