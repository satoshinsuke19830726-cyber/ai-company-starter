"""ニュースレターを3パターンずつ組み、各ページが1枚に収まるよう挿絵を自動で縮める。

使い方（このフォルダで）:
  python build.py <出力先の output フォルダ> <日付の接頭辞 YYYY-MM-DD> [作る号 YYYY-MM ...]
  例: python build.py ../../output 2027-03-10 2027-04
号を省略すると content.py にある全号を作る。"""
import os, re, subprocess, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nl_lib as L
from content import MONTHS, FOOTER

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
PREFIX = sys.argv[2] if len(sys.argv) > 2 else "draft"
ONLY = set(sys.argv[3:])
L.A = os.path.join(HERE, "assets")
WORK = os.path.join(HERE, "fit")


def res(folder, name):
    if name.startswith("ic_") or name.startswith("masthead") or name in ("telbanner.png", "card.png", "kaki.png"):
        return name
    return f"{folder}/{name if name.endswith('.png') else name + '.png'}"


def conv(folder, items):
    """原稿の独自要素（badge, ichk など）を nl_lib の要素に変換する"""
    out = []
    for kind, body in items:
        if kind == "badge":
            title, ps = body
            out.append(("imgtext", (f"{folder}/badge.png", 40, "l", [("h", title)] + ps)))
        elif kind == "c1":
            img, ps = body
            out.append(("imgtext", (f"{folder}/{img}.png", 38, "r", ps)))
        elif kind == "event":
            title, img, ps = body
            out.append(("theme", "red"))
            out.append(("imgtext", (f"{folder}/{img}.png", 40, "r", [("h", title)] + ps)))
        elif kind == "ichk":
            img, lines = body
            w = 16 if img.startswith("ic_") else 20
            out.append(("imgtext", (res(folder, img), w, "r", [("check", lines)])))
        elif kind == "img":
            n, w, al = body
            out.append(("img", (res(folder, n), w, al)))
        elif kind in ("bi", "boxi"):
            ic, text = body
            out.append((kind, (res(folder, ic), text)))
        else:
            out.append((kind, body))
    return out


def food_name(sub):
    return re.sub(r"[～（].*", "", sub.strip("～")) if sub else ""


def pages_for(m):
    F = m["folder"]
    run = lambda n: ("runner", f"ほっとニュースレター　{m['runner']}　　P.{n}")
    p1 = [("theme", "purple"), ("size", 11),
          ("img", ("masthead_hot.png", 180, "c")), ("date", m["date"]), ("img", ("telbanner.png", 175, "c"))] + conv(F, m["p1"])
    toc = ("toc", [(a, b, c, (f"{F}/p4food.png" if a == "P.4" else d)) for a, b, c, d in m["toc"]])
    q = m["p2"]
    p2 = [("theme", "orange"), ("size", 11),
          ("pagetitle", ("これだけは知っておこう！\nしておこう！", q["sub"], f"{F}/{q['L']}", q["Lw"])),
          ("lead", q["lead"]), ("img", (f"{F}/{q['panel']}.png", 168, "c")),
          ("cols", (conv(F, q["left"]), conv(F, q["right"])))]
    r = m["p3"]
    p3 = [("theme", "green"), ("size", 11),
          ("pagetitle", ("今さら聞けない！？", r["sub"], f"{F}/{r['L']}", r["Lw"])), ("lead", r["lead"])]
    if r["signs"]:
        p3 += [("h", "こんなサインに気づいたら注意"), ("img", (f"{F}/{r['signs']}.png", 168, "c"))]
    p3 += [("cols", (conv(F, r["left"]), conv(F, r["right"])))]
    f = m["p4"]
    rec = dict(f["recipe"], img=f"{F}/p4dish.png")
    rec["ing"] = rec["ing"]
    after_title, after_ps = f["after"]
    p4 = [("theme", "orange"), ("size", 10.5),
          ("pagetitle", ("♪おいしいのおと♪", f["sub"], f"{F}/{f['L']}", f["Lw"])), ("lead", f["lead"]),
          ("imgtext", (f"{F}/p4food.png", 34, "r", f["intro"])),
          ("recipe", rec),
          ("b", f"● おいしい{food_name(f['sub'])}はどう選ぶ？"), ("chips", f["choose"]),
          ("theme", "brown"), ("imgtext", (f"{F}/after.png", 36, "r", [("h", after_title)] + after_ps)), FOOTER]
    choko1 = [("theme", "green"), ("img", ("masthead_choko.png", 180, "c")),
              ("logo_date", ("yawaragi_logo.png", m["date"]))] + p2
    choko2 = [("theme", "green"), ("greentitle", "今月のやわらぎ"), ("photo", ""), ("megumi", ""),
              ("theme", "brown"), ("imgtext", (f"{F}/after.png", 36, "r", [("h", after_title)] + after_ps)), FOOTER]
    return {
        "01_ほっとニュースレター_{ym}_A4-4枚": [p1 + [toc], [run(2)] + p2, [run(3)] + p3, [run(4)] + p4],
        "02_ちょこっとニュース_{ym}_A4-2枚": [choko1, choko2],
        "03_ほっとニュースレター_{ym}_A4-2枚": [p1, p4],
    }


def page_count(paths):
    """LibreOffice でまとめてPDF化し、各ファイルのページ数を返す"""
    out = os.path.join(WORK, "pdf")
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    subprocess.run(["soffice", "--headless", "--norestore", "--convert-to", "pdf", "--outdir", out] + paths,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=900)
    counts = {}
    for p in paths:
        pdf = os.path.join(out, os.path.basename(p)[:-5] + ".pdf")
        info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
        counts[p] = int(re.search(r"Pages:\s+(\d+)", info).group(1)) if "Pages" in info else 99
    return counts


SCALES = [1.0, 0.92, 0.85, 0.78, 0.72, 0.66, 0.6]


def build_page(page, scale, path):
    L.IMG_SCALE = scale
    L.build([page], path)


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK)
    jobs = {}  # (month, edition, idx) -> page
    plan = {}
    for ym, m in MONTHS.items():
        if ONLY and ym not in ONLY:
            continue
        for ed, pages in pages_for(m).items():
            for i, pg in enumerate(pages):
                jobs[(ym, ed, i)] = pg
    level = {k: 0 for k in jobs}
    pending = set(jobs)
    while pending:
        paths = {}
        for k in pending:
            p = os.path.join(WORK, f"{k[0]}_{k[1].split('_')[0]}_{k[2]}.docx")
            build_page(jobs[k], SCALES[level[k]], p)
            paths[k] = p
        counts = page_count(list(paths.values()))
        nxt = set()
        for k, p in paths.items():
            if counts[p] > 1 and level[k] < len(SCALES) - 1:
                level[k] += 1
                nxt.add(k)
            elif counts[p] > 1:
                print("WARN still overflowing", k)
        pending = nxt
        print("round done; refit", len(nxt))
    # 本番：ページごとに決まった縮小率で1ファイルに組む
    for ym, m in MONTHS.items():
        if ONLY and ym not in ONLY:
            continue
        out_dir = os.path.join(OUT_ROOT, f"{PREFIX}_ニュースレター{ym[:4]}年{int(ym[5:])}月号")
        os.makedirs(out_dir, exist_ok=True)
        for ed, pages in pages_for(m).items():
            scaled = [[("scale", SCALES[level[(ym, ed, i)]])] + pg for i, pg in enumerate(pages)]
            L.build(scaled, os.path.join(out_dir, ed.format(ym=ym) + ".docx"))
        print(ym, {ed.split('_')[0]: [SCALES[level[(ym, ed, i)]] for i in range(len(p))] for ed, p in pages_for(m).items()})


if __name__ == "__main__":
    main()
