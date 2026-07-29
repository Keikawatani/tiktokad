#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""可愛い丸ゴシックフォント(Zen Maru Gothic / M PLUS Rounded 1c)を
Google Fonts から取得し、assets/fonts/ にローカル化する。

同梱の assets/fonts/ が壊れた・消えた場合の再取得用。
Google Fonts の CSS を取得し、参照される woff2 サブセットを全てDLして
url() をローカル相対パスに書き換えた fonts.css を作る。
"""
import hashlib
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "fonts")
FILES = os.path.join(OUT, "files")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

FAMILIES = [
    ("Zen Maru Gothic", "Zen+Maru+Gothic:wght@500;700;900"),
    ("M PLUS Rounded 1c", "M+PLUS+Rounded+1c:wght@700;800"),
]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=60).read()


def main():
    os.makedirs(FILES, exist_ok=True)
    css_parts = []
    for label, q in FAMILIES:
        css = get(f"https://fonts.googleapis.com/css2?family={q}&display=swap").decode()
        urls = sorted(set(re.findall(r"https://fonts\.gstatic\.com/[^)]+\.woff2", css)))
        print(f"{label}: {len(urls)} subsets")
        for u in urls:
            fn = os.path.join("files", hashlib.md5(u.encode()).hexdigest()[:10] + ".woff2")
            full = os.path.join(OUT, fn)
            if not os.path.exists(full) or os.path.getsize(full) < 100:
                try:
                    open(full, "wb").write(get(u))
                except Exception as e:  # noqa: BLE001
                    print("  FAIL", u, e, file=sys.stderr)
            css = css.replace(u, fn)
        css_parts.append(css)
    open(os.path.join(OUT, "fonts.css"), "w").write("\n".join(css_parts))
    print("wrote", os.path.join(OUT, "fonts.css"))


if __name__ == "__main__":
    main()
