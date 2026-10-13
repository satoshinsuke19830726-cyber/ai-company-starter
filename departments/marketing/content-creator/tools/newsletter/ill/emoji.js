// Fluent Emoji（Microsoft・MITライセンス）のイラストをPNGにし、組み合わせ画像を作る
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const path = require('path');
const fs = require('fs');

const OUT = path.resolve(__dirname, '../assets');
const ICONS = require('@iconify-json/fluent-emoji/icons.json');
const FONT = path.resolve(__dirname, 'node_modules/@fontsource/m-plus-rounded-1c');
const head = `<meta charset="utf-8"><link rel="stylesheet" href="file://${FONT}/800.css">
<style>html,body{margin:0;background:transparent}svg{display:block}text{font-family:'M PLUS Rounded 1c',sans-serif;font-weight:800}</style>`;

function iconSvg(name) {
  const ic = ICONS.icons[name];
  if (!ic) throw new Error('no icon ' + name);
  const w = ic.width || ICONS.width || 32, h = ic.height || ICONS.height || 32;
  return { body: ic.body, w, h };
}
// アイコンを任意の位置・大きさで置く（id衝突を避けるため接頭辞を付ける）
let uid = 0;
function place(name, x, y, size, rot = 0) {
  const { body, w, h } = iconSvg(name);
  const p = `i${uid++}_`;
  const b = body.replace(/id="([^"]+)"/g, `id="${p}$1"`).replace(/url\(#([^)]+)\)/g, `url(#${p}$1)`).replace(/href="#([^"]+)"/g, `href="#${p}$1"`);
  return `<svg x="${x}" y="${y}" width="${size}" height="${size}" viewBox="0 0 ${w} ${h}" overflow="visible"><g transform="rotate(${rot} ${w / 2} ${h / 2})">${b}</g></svg>`;
}
const svg = (w, h, inner) => `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${inner}</svg>`;

const ART = {};

// 単体アイコン（本文中の小さな挿絵用）
const SINGLES = ['person-taking-bath', 'flexed-biceps', 'fire', 'thermometer', 'chair', 'sake', 'speech-balloon',
  'older-person', 'old-woman', 'old-man', 'woman-health-worker', 'warning', 'clipboard', 'person-walking',
  'maple-leaf', 'fallen-leaf', 'tangerine', 'camera-with-flash', 'memo', 'telephone-receiver', 'pill',
  'droplet', 'window', 'potted-plant', 'toothbrush', 'syringe'];
for (const n of SINGLES) ART['ic_' + n] = svg(256, 256, place(n, 0, 0, 256));

// 霜月バッジ：落ち葉・もみじ・雪の結晶のリース
ART.shimotsuki = (() => {
  let ring = '';
  const names = ['maple-leaf', 'fallen-leaf', 'leaf-fluttering-in-wind', 'maple-leaf', 'fallen-leaf', 'snowflake'];
  for (let i = 0; i < 18; i++) {
    const a = (i / 18) * Math.PI * 2 - Math.PI / 2, r = 236, s = i % 6 === 5 ? 62 : 80;
    ring += place(names[i % 6], 300 + Math.cos(a) * r - s / 2, 300 + Math.sin(a) * r - s / 2, s, (i * 37) % 60 - 30);
  }
  return svg(600, 600, `<defs><radialGradient id="g" cx=".45" cy=".4"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#dcecfb"/></radialGradient></defs>
    <circle cx="300" cy="300" r="215" fill="url(#g)" stroke="#a9cdee" stroke-width="6"/>${ring}
    <text x="290" y="282" font-size="180" text-anchor="middle" fill="#23466e">霜</text>
    <text x="290" y="455" font-size="180" text-anchor="middle" fill="#23466e">月</text>
    ${[...'しもつき'].map((c, i) => `<text x="440" y="${236 + i * 44}" font-size="40" text-anchor="middle" fill="#4f7fb1">${c}</text>`).join('')}
    <text x="150" y="420" font-size="44" text-anchor="middle" fill="#c9372c">11月</text>`);
})();

// 七五三：神社・着物・千歳飴（ぺろぺろキャンディで代用）
ART.shichigosan = svg(560, 520, place('shinto-shrine', 150, 0, 300) + place('kimono', 20, 250, 250) + place('lollipop', 300, 260, 230, 15) + place('sparkles', 440, 40, 110));
// 冬じたく（3つの首を冷やさない）：マフラー・手袋・靴下
ART.fuyujitaku = svg(560, 300, place('scarf', 0, 20, 230) + place('gloves', 190, 60, 200) + place('socks', 360, 30, 210));
// お孫さんの写真
ART.photo = svg(560, 300, place('old-woman', 0, 20, 250) + place('camera-with-flash', 230, 90, 160) + place('framed-picture', 380, 40, 180));
// 編集後記：こたつのお供
ART.kotatsu = svg(560, 300, place('tangerine', 0, 70, 190) + place('hot-beverage', 180, 40, 200) + place('socks', 370, 60, 190));

// 温度差とヒートショックの図（アイコン版）
ART.heat = (() => {
  const room = (x, label, temp, bg, col, icons) => `
    <rect x="${x}" y="40" width="300" height="280" rx="22" fill="${bg}" stroke="${col}" stroke-width="5"/>
    <text x="${x + 150}" y="96" font-size="40" text-anchor="middle" fill="#333">${label}</text>
    <text x="${x + 150}" y="300" font-size="68" text-anchor="middle" fill="${col}">${temp}</text>${icons}`;
  return svg(1040, 590, `<defs><marker id="ar" markerWidth="10" markerHeight="10" refX="6" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#666"/></marker></defs>
    ${room(10, '居間', '20℃', '#fff1e6', '#f07b22', place('couch-and-lamp', 95, 108, 120))}
    ${room(370, '脱衣所', '10℃', '#e6f2ff', '#2f7fd1', place('cold-face', 410, 112, 105) + place('snowflake', 530, 118, 90))}
    ${room(730, '浴槽', '42℃', '#ffe9ea', '#e8403f', place('person-taking-bath', 815, 106, 125))}
    <line x1="315" y1="180" x2="362" y2="180" stroke="#666" stroke-width="6" marker-end="url(#ar)"/>
    <line x1="675" y1="180" x2="722" y2="180" stroke="#666" stroke-width="6" marker-end="url(#ar)"/>
    <rect x="10" y="345" width="1020" height="235" rx="22" fill="#fffbe9" stroke="#e8c45a" stroke-width="4"/>
    <text x="40" y="397" font-size="34" fill="#8a5a00">血圧</text>
    <polyline points="60,495 300,495 360,495 470,395 600,395 700,395 790,535 1000,535" fill="none" stroke="#e8403f" stroke-width="10" stroke-linejoin="round" stroke-linecap="round"/>
    <text x="160" y="480" font-size="32" text-anchor="middle" fill="#555">ふつう</text>
    <text x="530" y="380" font-size="38" text-anchor="middle" fill="#e8403f">急上昇 ↑</text>
    <text x="890" y="515" font-size="38" text-anchor="middle" fill="#2f7fd1">急降下 ↓</text>
    ${place('face-with-spiral-eyes', 935, 380, 80)}
    <text x="520" y="568" font-size="30" text-anchor="middle" fill="#8a5a00">この「急な上がり下がり」が体の負担に！</text>`);
})();

// 41℃・10分
ART.bathrule = svg(620, 300, `
  <rect x="6" y="6" width="290" height="288" rx="30" fill="#fff0ec" stroke="#f07b5a" stroke-width="6"/>${place('thermometer', 14, 90, 120)}
  <text x="210" y="150" font-size="64" text-anchor="middle" fill="#e8403f">41℃</text><text x="210" y="210" font-size="40" text-anchor="middle" fill="#555">以下</text>
  <rect x="324" y="6" width="290" height="288" rx="30" fill="#ebf6ff" stroke="#3d8fd6" stroke-width="6"/>${place('timer-clock', 334, 70, 140)}
  <text x="540" y="150" font-size="64" text-anchor="middle" fill="#3d8fd6">10分</text><text x="540" y="210" font-size="40" text-anchor="middle" fill="#555">まで</text>`);

// フレイルの3つの側面
ART.frail3 = svg(640, 600, `<defs><marker id="a" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#8aa"/></marker></defs>
  <g stroke="#9bb" stroke-width="7" fill="none" marker-end="url(#a)"><path d="M235 190 Q160 270 160 330"/><path d="M240 470 Q320 520 400 470"/><path d="M480 330 Q480 270 405 190"/></g>
  <circle cx="320" cy="125" r="110" fill="#ffe2b8" stroke="#ffb54c" stroke-width="6"/>${place('flexed-biceps', 262, 40, 116)}
  <text x="320" y="200" font-size="40" text-anchor="middle" fill="#d9821a">体</text>
  <circle cx="140" cy="440" r="110" fill="#ffd9e4" stroke="#ff7fa3" stroke-width="6"/>${place('red-heart', 85, 355, 110)}
  <text x="140" y="515" font-size="40" text-anchor="middle" fill="#d6467a">心</text>
  <circle cx="500" cy="440" r="110" fill="#d9f2dd" stroke="#5cbf6a" stroke-width="6"/>${place('people-hugging', 442, 352, 116)}
  <text x="500" y="515" font-size="40" text-anchor="middle" fill="#2f8a43">社会</text>
  <text x="320" y="340" font-size="34" text-anchor="middle" fill="#557">影響し合う</text>`);

// 予防の3本柱
const pillar = (x, bg, bd, label, col, icons) => `<rect x="${x}" y="6" width="316" height="318" rx="26" fill="${bg}" stroke="${bd}" stroke-width="6"/>${icons}
  <text x="${x + 158}" y="292" font-size="46" text-anchor="middle" fill="${col}">${label}</text>`;
ART.pillars = svg(1000, 330,
  pillar(6, '#fff4e3', '#f0a43a', '栄養', '#d9821a', place('egg', 26, 40, 110) + place('fish', 120, 30, 120) + place('glass-of-milk', 220, 50, 100) + place('cut-of-meat', 90, 130, 110)) +
  pillar(342, '#eaf7ec', '#4fb062', '運動', '#2f8a43', place('chair', 370, 50, 150) + place('person-walking', 510, 40, 160)) +
  pillar(678, '#fdeef4', '#e87aa0', '社会参加', '#d6467a', place('people-hugging', 700, 70, 160) + place('speech-balloon', 860, 30, 110)));

// 指輪っかテスト（説明図。手は「OKサイン」のアイコンを添える）
ART.ring = (() => {
  const panel = (x, calf, label, sub, col) => `
    <rect x="${x}" y="6" width="320" height="420" rx="24" fill="#fff" stroke="${col}" stroke-width="6"/>
    <path d="M${x + 160 - calf} 60 C ${x + 160 - calf - 18} 150, ${x + 160 - calf + 6} 250, ${x + 160 - 34} 320 L ${x + 160 + 34} 320 C ${x + 160 + calf - 6} 250, ${x + 160 + calf + 18} 150, ${x + 160 + calf} 60 Z" fill="#f7cfae" stroke="#d99a6c" stroke-width="4"/>
    <ellipse cx="${x + 160}" cy="165" rx="68" ry="20" fill="none" stroke="#e98c63" stroke-width="16"/>
    <text x="${x + 160}" y="368" font-size="36" text-anchor="middle" fill="${col}">${label}</text>
    <text x="${x + 160}" y="408" font-size="26" text-anchor="middle" fill="#555">${sub}</text>`;
  return svg(1000, 432, panel(6, 84, '囲めない', '筋肉がしっかり', '#3d9a4f') + panel(340, 68, 'ちょうど囲める', 'まずまず', '#e0a21b') +
    panel(674, 46, 'すき間ができる', '筋肉が減っているかも', '#e8403f') + place('ok-hand', 20, 230, 90) + place('ok-hand', 354, 230, 90) + place('ok-hand', 688, 230, 90));
})();

// セルフチェックの挿絵
ART.check = svg(300, 300, place('clipboard', 20, 20, 200) + place('older-person', 150, 120, 150));

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const page = await browser.newPage({ deviceScaleFactor: 2 });
  await page.setViewportSize({ width: 1400, height: 1000 });
  for (const [name, s] of Object.entries(ART)) {
    await page.setContent(`<html><head>${head}</head><body>${s}</body></html>`);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(100);
    await page.locator('body > svg').first().screenshot({ path: `${OUT}/${name}.png`, omitBackground: true });
  }
  await browser.close();
  console.log('done', Object.keys(ART).length);
})();
