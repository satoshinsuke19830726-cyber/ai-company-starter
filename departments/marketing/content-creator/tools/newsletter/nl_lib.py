"""ほっとニュースレター 2026年11月号（カラー・イラスト入り）を3パターンの .docx で書き出す。"""
import sys
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

OUT_DIR, A = (sys.argv[1], sys.argv[2]) if __name__ == "__main__" else (None, "assets")
IMG_SCALE = 1.0  # ページに収めるための縮小率（自動調整）
FIXED = ("masthead", "telbanner", "card", "yawaragi", "megumi")
BODY_FONT = "BIZ UDPゴシック"
POP_FONT = "HG丸ｺﾞｼｯｸM-PRO"  # 10月号の見出しに近い丸ゴシック（Office付属）
BODY = 10.5

# ---------------------------------------------------------------- 原稿
SHIMO = [
    ("h", "１１月は「霜月（しもつき）」"),
    ("p", "11月の和風月名は「霜月」。文字どおり「霜が降りる月」という意味の「霜降月（しもふりづき）」が短くなった、という説がよく知られています。ほかにも、収穫を終えた実りを神様に感謝する月だから……など、いくつかの説があるそうです。"),
    ("p", "暦の上では、11月上旬に冬の始まりを告げる「立冬（りっとう）」を迎えます。朝、庭の草木や車の窓がうっすら白くなっているのを見ると、「ああ、霜月だなぁ」と季節の移ろいを感じますね。"),
]
SHIMO2 = [
    ("p", "この時期は、日中は過ごしやすくても、朝晩はぐっと冷え込みます。寒さで体がこわばると、肩や腰、ひざの痛みをいつもより強く感じる方も少なくありません。首・手首・足首の「3つの首」を冷やさない服装や、ひざ掛け・湯たんぽなど、ひと足早い冬じたくを始めておきましょう。"),
]
SHICHIGOSAN = [
    ("h", "１１月１５日は「七五三」"),
    ("p", "子どもの健やかな成長を願い、神社にお参りする七五三。一般的には、男の子は3歳と5歳、女の子は3歳と7歳でお祝いします（地域やご家庭によって異なります）。"),
    ("p", "七五三に欠かせないのが「千歳飴（ちとせあめ）」。細く長い形には「長く元気に生きてほしい」という願いが、紅白の色や、鶴亀・松竹梅が描かれた袋にも縁起の良い意味が込められています。最近は11月15日にこだわらず、ご家族の都合の良い秋の休日にお参りするご家庭も多いようです。"),
]
SHICHIGOSAN2 = [
    ("p", "お孫さんやひ孫さんの晴れ着姿を見るのは、祖父母世代にとっても格別の喜び。一緒に写真を撮ったり、昔のお宮参りの思い出話をしたり……。遠くに住んでいて会えない場合は、写真を送ってもらい、それを見ながら電話でお祝いを伝えるのも素敵ですね。"),
]
TOC = ("toc", [
    ("P.2", "これだけは知っておこう！しておこう！", "～ヒートショック予防～", "ic_person-taking-bath.png"),
    ("P.3", "今さら聞けない！", "～フレイル～", "ic_flexed-biceps.png"),
    ("P.4", "おいしいのおと", "～柿（かき）～", "kaki.png"),
])

def p1_top(shimo_w, chitose_w):
    return [
    ("theme", "purple"),
    ("size", 11),
    ("img", ("masthead_hot.png", 180, "c")),
    ("date", "２０２６年１１月発行"),
    ("img", ("telbanner.png", 175, "c")),
    ("imgtext", ("shimotsuki.png", shimo_w, "l", SHIMO)),
    ("imgtext", ("fuyujitaku.png", 38, "r", SHIMO2)),
    ("theme", "red"),
    ("imgtext", ("shichigosan.png", chitose_w, "r", SHICHIGOSAN)),
    ("imgtext", ("photo.png", 38, "l", SHICHIGOSAN2)),
]

def heat(size, img_w):
    return [
    ("theme", "orange"),
    ("size", size),
    ("pagetitle", ("これだけは知っておこう！\nしておこう！", "～ヒートショック予防～", "letters_heat.png", 88)),
    ("lead", "これからの寒い季節に、特に気をつけたいのが「ヒートショック」。暖かい部屋から寒い脱衣所・浴室への移動など、急な温度の変化で血圧が大きく上下し、体に負担がかかる現象です。ご本人はもちろん、ご家族や介護に関わる皆さまにも知っておいていただきたいポイントをまとめました。"),
    ("img", ("heat.png", img_w, "c")),
    ("cols", (
        [
            ("h", "ヒートショックとは？"),
            ("p", "暖かい居間から寒い脱衣所に移って服を脱ぐと、体は熱を逃がさないように血管を縮め、血圧が上がります。そのあと熱いお湯につかると、今度は血管が一気に広がり、血圧が急に下がります。"),
            ("p", "この急な上がり下がりが、めまいや失神、さらには心筋梗塞や脳卒中などを引き起こすことがあります。浴槽の中で意識を失うと、溺れてしまう危険もあります。"),
            ("h", "こんな方は特に注意"),
            ("imgtext", ("ic_older-person.png", 16, "r", [("check", [
                "65歳以上の方",
                "高血圧・糖尿病・脂質異常症などの持病がある方",
                "「一番風呂」や「熱いお湯」が好きな方",
                "お酒を飲んだあとに入浴する習慣がある方",
                "脱衣所や浴室に暖房がないお住まいの方",
            ])])),
        ],
        [
            ("h", "今日からできる５つの対策"),
            ("img", ("bathrule.png", 52, "c")),
            ("bi", ("ic_fire.png", "① 入浴前に脱衣所と浴室を暖める")),
            ("p", "小型の暖房器具や、シャワーでお湯をためて浴室を蒸気で暖めましょう。"),
            ("bi", ("ic_thermometer.png", "② お湯は41℃以下、つかるのは10分まで")),
            ("bi", ("ic_chair.png", "③ 浴槽から急に立ち上がらない")),
            ("bi", ("ic_sake.png", "④ 食後すぐ・飲酒後・服薬直後は避ける")),
            ("bi", ("ic_speech-balloon.png", "⑤ 入浴前に、家族にひと声かける")),
            ("p", "※消費者庁などでも呼びかけられている対策です。"),
            ("boxi", ("ic_woman-health-worker.png", "【ご家族・介護に関わる皆さまへ】\nいつもより入浴が長いと感じたら、迷わず声をかけてください。返事がない時は、すぐに様子を確認しましょう。")),
        ],
    )),
]

FRAIL = [
    ("theme", "green"),
    ("size", 11),
    ("pagetitle", ("今さら聞けない！？", "～フレイル～", "letters_frail.png", 80)),
    ("lead", "最近よく耳にする「フレイル」。英語の「Frailty（虚弱）」が語源で、年齢とともに筋力や心身の活力が低下し、介護が必要になる一歩手前の状態を指します。大切なのは、早く気づいて対策すれば、元気な状態に戻れる可能性があるということです。"),
    ("cols", (
        [
            ("h", "フレイルの３つの側面"),
            ("img", ("frail3.png", 66, "c")),
            ("p", "3つは互いに影響し合います。たとえば「ひざが痛い → 外出が減る → 筋力が落ちる → さらに動きにくくなる」という悪循環に陥りやすいのです。"),
            ("h", "１分でできるセルフチェック"),
            ("imgtext", ("check.png", 18, "r", [("check", [
                "半年で2kg以上、体重が減った",
                "ここ2週間、わけもなく疲れたような感じがする",
                "歩く速さが遅くなったと感じる",
                "ペットボトルのふたが開けにくくなった",
                "軽い体操や運動を、ふだんしていない",
            ])])),
            ("p", "3つ以上なら「フレイル」、1～2つなら「プレフレイル（予備群）」の可能性があります。※国の研究班の基準をわかりやすく言い換えた目安で、診断ではありません。気になる方は、かかりつけ医にご相談ください。"),
        ],
        [
            ("h", "ふくらはぎで分かる「指輪っかテスト」"),
            ("p", "両手の親指と人さし指で輪っかをつくり、ふくらはぎの一番太いところを軽く囲んでみましょう。すき間ができる場合は、筋肉の量が減っている可能性があります。"),
            ("img", ("ring.png", 84, "c")),
            ("h", "予防の３本柱"),
            ("img", ("pillars.png", 84, "c")),
            ("b", "① 栄養：たんぱく質を毎食"),
            ("p", "肉・魚・卵・大豆製品・乳製品を、朝・昼・晩に少しずつ。"),
            ("b", "② 運動：座ったままでもOK"),
            ("p", "いすに座ってひざを伸ばし3秒止める、かかとの上げ下げなど。痛みがある時は無理をしないでください。"),
            ("b", "③ 社会参加：人と話す・出かける"),
            ("p", "趣味の集まり、デイサービス、ご近所とのおしゃべりも立派な予防です。"),
            ("boxi", ("ic_woman-health-worker.png", "「痛みがあるから動けない」が、フレイルの入り口になることもあります。通院が難しい方には、ご自宅で施術を受けられる訪問鍼灸マッサージという選択肢もあります。")),
        ],
    )),
]

KAKI_LEAD = [
    ("lead", "秋の味覚・柿。「柿が赤くなると医者が青くなる」ということわざがあるほど、昔から栄養豊富な果物として親しまれてきました。甘い柿の秘密に迫りましょう。"),
]
KAKI_INTRO = [
    ("b", "● 柿の歴史"),
    ("p", "原産は中国などの東アジアとされ、日本には奈良時代ごろに伝わったといわれています（諸説あり）。干し柿は、砂糖が貴重だった時代の大切な甘味でした。学名は「Diospyros kaki」。日本語の「カキ」がそのまま使われ、海外でも「KAKI」の名で知られています。主な産地は和歌山県・奈良県・福岡県などです。"),
    ("b", "● 柿に含まれる栄養素は？"),
    ("p", "果物の中でもビタミンCが多く、体内でビタミンAに変わるβ-カロテン、食物繊維、カリウムなども含まれています。※カリウムが多い果物なので、腎臓の病気などで食事制限のある方は、主治医にご相談ください。"),
]
RECIPE = ("recipe", {
    "name": "● 柿と大根のなます ●",
    "ing": [("柿", "1/2個"), ("大根", "約5cm（150g）"), ("塩", "小さじ1/4"),
            ("酢", "大さじ2"), ("砂糖", "大さじ1"), ("ゆずの皮（あれば）", "少々")],
    "steps": [
        "大根は皮をむいて細切りにし、塩をふって10分ほどおき、水気をしぼります。",
        "柿は皮と種を取り、大根と同じくらいの細切りにします。",
        "ボウルで酢と砂糖を混ぜ、大根と柿を加えてあえます。",
        "冷蔵庫で15分ほどなじませたら完成。ゆずの皮を散らすと香りよく仕上がります。",
    ],
    "tip": "柿の甘みがあるので、砂糖は控えめでもおいしくいただけます。",
    "img": "namasu.png",
})
AFTERWORD = [
    ("theme", "brown"),
    ("imgtext", ("kotatsu.png", 36, "r", [
        ("h", "編集後記　冬じたく"),
        ("p", "先月号で「関東以南の紅葉はもうしばらく先」とお話ししましたが、11月は、いよいよ各地で見頃を迎える季節です。皆さまの近くでは、木々は色づいてきましたか？"),
        ("p", "そろそろ「冬じたく」の季節です。こたつや暖房器具を出したり、厚手の靴下やひざ掛けを用意したり……。今月号でご紹介したヒートショック対策も、冬じたくのひとつ。脱衣所の暖房器具の準備は、寒さが本格的になる前に済ませておきたいですね。どうぞ温かくしてお過ごしください。"),
    ])),
]
FOOTER = ("footer", [
    "発行：アトラス合同会社　担当：佐藤 信助",
    "住所：〒193-0801",
    "　　　東京都八王子市川口町1373-14",
    "TEL：070-1524-0101　FAX：042-633-2783",
])
KAKI_PAGE = [
    ("theme", "orange"),
    ("size", 10.5),
    ("pagetitle", ("♪おいしいのおと♪", "～柿（かき）～", "letters_kaki.png", 36)),
] + KAKI_LEAD + [
    ("imgtext", ("kaki.png", 34, "r", KAKI_INTRO)),
    RECIPE,
    ("b", "● おいしい柿はどう選ぶ？"),
    ("chips", ["ヘタが緑色で実に張りついている", "皮にハリとツヤがある", "色ムラがなく濃いオレンジ色", "持つとずっしり重い"]),
] + AFTERWORD + [FOOTER]

RUN = lambda n: ("runner", f"ほっとニュースレター　２０２６年１１月号　　P.{n}")

CHOKO_P1 = [
    ("theme", "green"),
    ("img", ("masthead_choko.png", 180, "c")),
    ("logo_date", ("yawaragi_logo.png", "２０２６年１１月発行")),
] + heat(10.5, 80)
CHOKO_P2 = [
    ("theme", "green"),
    ("greentitle", "今月のやわらぎ"),
    ("photo", "（写真スペース：今月の行事・施術の様子などの写真を貼ってください）"),
    ("megumi", "（ここに今月のひとことを入れてください）"),
] + AFTERWORD + [FOOTER]

EDITIONS = [
    ("01_ほっとニュースレター_2026-11_A4-4枚", [p1_top(40, 36) + [TOC], [RUN(2)] + heat(11, 114), [RUN(3)] + FRAIL, [RUN(4)] + KAKI_PAGE]),
    ("02_ちょこっとニュース_2026-11_A4-2枚", [CHOKO_P1, CHOKO_P2]),
    ("03_ほっとニュースレター_2026-11_A4-2枚", [p1_top(50, 46), KAKI_PAGE]),
]

# ---------------------------------------------------------------- 色
THEMES = {  # 見出し帯, 淡い背景, 文字色
    "purple": ("7B5EA7", "F1ECF8", "5A3E8A"),
    "red": ("D9433F", "FDEDEC", "B02A2A"),
    "orange": ("E8772E", "FFF3E6", "C25E00"),
    "green": ("3E9B4F", "EAF6EC", "2C7A3B"),
    "brown": ("8B5A2B", "F8F0E6", "6E4520"),
}
T = THEMES["orange"]


def rgb(h):
    return RGBColor.from_string(h)


# ---------------------------------------------------------------- docx helpers
def set_font(run, size, bold=False, color=None, font=BODY_FONT):
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = rgb(color)
    rpr = run._element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rpr.insert(0, fonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        fonts.set(qn(attr), font)


def para(c, text="", size=BODY, bold=False, align=None, before=0, after=2, indent=None, color=None, font=BODY_FONT, line=1.15):
    p = c.add_paragraph()
    pf = p.paragraph_format
    pf.space_before, pf.space_after = Pt(before), Pt(after)
    pf.line_spacing = line
    if align is not None:
        p.alignment = align
    if indent is not None:
        pf.first_line_indent = Pt(indent)
    lines = text.split("\n")
    for i, line_ in enumerate(lines):
        r = p.add_run(line_)
        set_font(r, size, bold, color, font)
        if i < len(lines) - 1:
            r.add_break()
    return p


def shade(el_pr, fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    el_pr.append(shd)


def cell_style(cell, border=None, size=8, val="single", fill=None, margin=None):
    tcpr = cell._element.get_or_add_tcPr()
    b = OxmlElement("w:tcBorders")
    for side in ("top", "left", "bottom", "right"):
        e = OxmlElement(f"w:{side}")
        if border:
            e.set(qn("w:val"), val)
            e.set(qn("w:sz"), str(size))
            e.set(qn("w:color"), border)
        else:
            e.set(qn("w:val"), "nil")
        b.append(e)
    tcpr.append(b)
    if fill:
        shade(tcpr, fill)
    if margin is not None:
        m = OxmlElement("w:tcMar")
        for side in ("top", "left", "bottom", "right"):
            e = OxmlElement(f"w:{side}")
            e.set(qn("w:w"), str(int(margin * 56.7)))
            e.set(qn("w:type"), "dxa")
            m.append(e)
        tcpr.append(m)


def row_height(row, mm):
    h = OxmlElement("w:trHeight")
    h.set(qn("w:val"), str(int(mm * 56.7)))
    h.set(qn("w:hRule"), "exact")
    row._tr.get_or_add_trPr().append(h)


def set_grid(t, widths):
    grid = t._tbl.tblGrid
    for gc, w in zip(grid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(int(w * 56.7)))
    tblpr = t._tbl.tblPr
    tw = OxmlElement("w:tblW")
    tw.set(qn("w:w"), str(int(sum(widths) * 56.7)))
    tw.set(qn("w:type"), "dxa")
    old = tblpr.find(qn("w:tblW"))
    if old is not None:
        tblpr.remove(old)
    tblpr.append(tw)
    lay = OxmlElement("w:tblLayout")
    lay.set(qn("w:type"), "fixed")
    tblpr.append(lay)
    mar = OxmlElement("w:tblCellMar")
    for side in ("left", "right"):
        e = OxmlElement(f"w:{side}")
        e.set(qn("w:w"), "57")
        e.set(qn("w:type"), "dxa")
        mar.append(e)
    tblpr.append(mar)


def table(c, rows, cols, widths):
    t = c.add_table(rows=rows, cols=cols)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for row in t.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Mm(w)
    set_grid(t, widths)
    for row in t.rows:
        for cell in row.cells:
            for p in list(cell.paragraphs):
                p._element.getparent().remove(p._element)
    return t


def picture(c, name, width, align="c", before=1, after=1):
    al = {"c": WD_ALIGN_PARAGRAPH.CENTER, "l": WD_ALIGN_PARAGRAPH.LEFT, "r": WD_ALIGN_PARAGRAPH.RIGHT}[align]
    p = para(c, "", 4, align=al, before=before, after=after, line=1.0)
    if not any(k in name for k in FIXED):
        width = width * IMG_SCALE
    p.add_run().add_picture(f"{A}/{name}", width=Mm(width))
    return p


def heading(c, text):
    # 10月号の茶色い帯見出しにならい、色帯に白抜き文字
    p = para(c, " " + text, 12, True, before=5, after=3, color="FFFFFF", font=POP_FONT)
    shade(p._element.get_or_add_pPr(), T[0])


def render(c, items, width=180):
    global T, BODY, IMG_SCALE
    for kind, body in items:
        if kind == "theme":
            T = THEMES[body]
        elif kind == "size":
            BODY = body
        elif kind == "scale":
            IMG_SCALE = body
        elif kind == "img":
            name, w, al = body
            picture(c, name, min(w, width - 2), al)
        elif kind == "date":
            para(c, body, 10, True, WD_ALIGN_PARAGRAPH.RIGHT, after=0, color="1D3557")
        elif kind == "logo_date":
            t = table(c, 1, 2, (110, 70))
            l, r = t.rows[0].cells
            cell_style(l), cell_style(r)
            para(l, body[1], 10, True, before=8, color="1D3557")
            picture(r, body[0], 60, "r")
        elif kind == "runner":
            para(c, body, 8.5, align=WD_ALIGN_PARAGRAPH.RIGHT, after=1, color="777777")
        elif kind == "pagetitle":
            title, sub, img, iw = body
            t = table(c, 1, 2, (180 - iw - 2, iw + 2))
            l, r = t.rows[0].cells
            cell_style(l), cell_style(r)
            l.vertical_alignment = r.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            para(l, title, 20, True, color="1F6FD1", font=POP_FONT, after=0, line=1.05)
            para(l, sub, 13, True, color=T[2], font=POP_FONT, before=2, after=0)
            picture(r, img, iw, "r")
        elif kind == "greentitle":
            para(c, body, 18, True, color=T[2], font=POP_FONT, before=2, after=2)
        elif kind == "lead":
            t = table(c, 1, 1, (width,))
            cell = t.rows[0].cells[0]
            cell_style(cell, T[0], 6, "single", T[1], margin=2)
            para(cell, body, BODY, before=1, after=1, indent=BODY)
            para(c, "", 3, after=0, line=1.0)
        elif kind == "h":
            heading(c, body)
        elif kind == "b":
            para(c, body, BODY + 0.5, True, before=3, after=1, color=T[2])
        elif kind == "p":
            para(c, body, BODY, indent=BODY, after=2)
        elif kind == "check":
            for line_ in body:
                p = para(c, "", BODY, after=1)
                set_font(p.add_run("✔ "), BODY, True, T[0])
                set_font(p.add_run(line_), BODY)
        elif kind == "chips":
            p = para(c, "", BODY, before=1, after=3)
            for i, chip in enumerate(body):
                set_font(p.add_run(f"「{chip}」"), BODY, True, ["D9433F", "E8772E", "3E9B4F", "1F6FD1"][i % 4])
        elif kind == "bi":
            ic, text = body
            p = para(c, "", BODY + 0.5, before=2, after=1)
            p.add_run().add_picture(f"{A}/{ic}", height=Mm(4.2))
            set_font(p.add_run(" " + text), BODY + 0.5, True, T[2])
        elif kind == "boxi":
            ic, text = body
            para(c, "", 3, after=0, line=1.0)
            t = table(c, 1, 2, (13, width - 15))
            a_, b_ = t.rows[0].cells
            for cell in (a_, b_):
                cell_style(cell, "E0A21B", 12, "dashed", "FFF8DC", margin=1)
            a_.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            picture(a_, ic, 11, "c")
            para(b_, text, BODY, before=1, after=1)
        elif kind == "box":
            para(c, "", 3, after=0, line=1.0)
            t = table(c, 1, 1, (width - 2,))
            cell = t.rows[0].cells[0]
            cell_style(cell, "E0A21B", 12, "dashed", "FFF8DC", margin=1.5)
            para(cell, body, BODY, before=1, after=1)
        elif kind == "imgtext":
            name, iw, side, sub = body
            tw = width - iw - 2
            ws = (iw + 2, tw) if side == "l" else (tw, iw + 2)
            t = table(c, 1, 2, ws)
            a, b = t.rows[0].cells
            cell_style(a), cell_style(b)
            img_cell, txt_cell = (a, b) if side == "l" else (b, a)
            img_cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            picture(img_cell, name, iw, "c")
            render(txt_cell, sub, tw)
        elif kind == "cols":
            t = table(c, 1, 2, (89, 89))
            for i, col in enumerate(body):
                cell = t.rows[0].cells[i]
                cell_style(cell)
                render(cell, col, 87)
        elif kind == "toc":
            para(c, "", 4, after=0, line=1.0)
            t = table(c, 1, 1, (180,))
            cell = t.rows[0].cells[0]
            cell_style(cell, "E87AA0", 12, "single", "FDEEF4", margin=1.5)
            para(cell, "もくじ", 13, True, WD_ALIGN_PARAGRAPH.CENTER, color="D6467A", font=POP_FONT, after=2)
            for pg, ttl, sub, ic in body:
                p = para(cell, "", 11, after=1)
                p.add_run().add_picture(f"{A}/{ic}", height=Mm(5.5))
                set_font(p.add_run(" "), 11)
                set_font(p.add_run(f"{pg}　"), 11, True, "D6467A")
                set_font(p.add_run(f"{ttl}　"), 11, True, "333333")
                set_font(p.add_run(sub), 11, True, "1F6FD1")
        elif kind == "photo":
            t = table(c, 1, 1, (width,))
            row_height(t.rows[0], 119)
            cell = t.rows[0].cells[0]
            cell_style(cell, "3E9B4F", 12, "single", "FAFFFA")
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            para(cell, body, 10, align=WD_ALIGN_PARAGRAPH.CENTER, color="888888")
            para(c, "", 6, after=0, line=1.0)
        elif kind == "megumi":
            t = table(c, 1, 2, (66, 114))
            l, r = t.rows[0].cells
            cell_style(l)
            cell_style(r, "E8956A", 12, "dotted", "FFF6EF", margin=2)
            r.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            picture(l, "megumi.png", 64, "c")
            para(r, body, 11, align=WD_ALIGN_PARAGRAPH.CENTER, color="888888")
        elif kind == "recipe":
            para(c, "", 3, after=0, line=1.0)
            t = c.add_table(rows=2, cols=3)
            t.alignment = WD_TABLE_ALIGNMENT.CENTER
            t.autofit = False
            for row in t.rows:
                for i, w in enumerate((50, 88, 42)):
                    row.cells[i].width = Mm(w)
            set_grid(t, (50, 88, 42))
            top = t.rows[0].cells[0].merge(t.rows[0].cells[2])
            for row in t.rows:
                for cell in row.cells:
                    for p in list(cell.paragraphs):
                        p._element.getparent().remove(p._element)
            cell_style(top, T[0], 8, "single", T[0])
            para(top, body["name"], 12, True, WD_ALIGN_PARAGRAPH.CENTER, color="FFFFFF", font=POP_FONT, before=1, after=1)
            l, m, r = t.rows[1].cells
            for cell in (l, m, r):
                cell_style(cell, T[0], 8, "single", T[1], margin=1.2)
            para(l, "【材料】2人分", BODY, True, color=T[2], after=1)
            for n, amt in body["ing"]:
                para(l, f"・{n}　{amt}", 10, after=0)
            para(m, "【作り方】", BODY, True, color=T[2], after=1)
            for i, s in enumerate(body["steps"], 1):
                para(m, f"{i}. {s}", 10, after=0)
            para(m, "★ " + body["tip"], 10, True, before=2, after=1, color="B02A2A")
            r.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            picture(r, body["img"], 39, "c")
        elif kind == "footer":
            para(c, "", 4, after=0, line=1.0)
            t = table(c, 1, 2, (114, 66))
            l, r = t.rows[0].cells
            cell_style(l, "3E9B4F", 12, "single", "F4FBF4", margin=2)
            cell_style(r, "3E9B4F", 12, "single", "FFFFFF")
            l.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            para(l, "\n".join(body), 10.5, True, after=0, color="1E5A2B")
            picture(r, "card.png", 54, "c")
        else:
            raise ValueError(kind)


def page_border(sec):
    pg = OxmlElement("w:pgBorders")
    pg.set(qn("w:offsetFrom"), "page")
    for side in ("top", "left", "bottom", "right"):
        e = OxmlElement(f"w:{side}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "6")
        e.set(qn("w:space"), "20")
        e.set(qn("w:color"), "9FB8C8")
        pg.append(e)
    sec._sectPr.append(pg)


def build(pages, path):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(15)
    sec.top_margin, sec.bottom_margin = Mm(11), Mm(9)
    page_border(sec)
    st = doc.styles["Normal"]
    st.font.name = BODY_FONT
    st.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
    body = doc.element.body
    if body[0].tag == qn("w:p"):
        body.remove(body[0])
    for i, page in enumerate(pages):
        if i:
            p = doc.add_paragraph()
            p.paragraph_format.page_break_before = True
            p.paragraph_format.space_after = Pt(0)
            set_font(p.add_run(""), 2)
        render(doc, page)
    doc.save(path)


if __name__ == "__main__":
    for fname, pages in EDITIONS:
        build(pages, f"{OUT_DIR}/{fname}.docx")
    print("ok")
