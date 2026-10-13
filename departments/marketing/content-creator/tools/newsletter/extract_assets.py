"""合格版の11月号Word（経営者手直し版）から、公開リポジトリに置けない画像を取り出して assets/ に置く。

使い方: python extract_assets.py <01_..._経営者手直し版.docx> <02_ちょこっとニュース_..._経営者手直し版.docx>
（名刺・やわらぎロゴ・めぐみさん・タイトル帯は個人情報や他社ロゴを含むため git には入れない）"""
import hashlib, os, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
WANT = {  # 画像のmd5先頭12桁 -> ファイル名
    "0fd323c32c7e": "card.png", "4051e000ec57": "yawaragi_logo.png", "db95a259381e": "megumi.png",
    "4f4a67da9431": "masthead_hot.png", "c6e755649461": "masthead_choko.png", "d1f4f7c87b66": "telbanner.png",
}
found = set()
for path in sys.argv[1:]:
    z = zipfile.ZipFile(path)
    for n in z.namelist():
        if n.startswith("word/media/"):
            data = z.read(n)
            h = hashlib.md5(data).hexdigest()[:12]
            if h in WANT and WANT[h] not in found:
                open(os.path.join(HERE, "assets", WANT[h]), "wb").write(data)
                found.add(WANT[h])
missing = sorted(set(WANT.values()) - found)
print("取り出した:", sorted(found))
print("見つからない:", missing or "なし")
