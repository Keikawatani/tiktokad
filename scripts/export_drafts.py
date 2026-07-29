#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""1ヶ月分などの「初稿画像＋簡潔な投稿文」を一括で書き出してZIPにまとめる。

デザインはこの初稿の上から作り替える前提なので、装飾控えめの plain テンプレを既定にしている。

例:
  # 8/1 から30日分の初稿を出力してZIP化
  python scripts/export_drafts.py --date 2026-08-01 --days 30

  # 可愛い装飾版で出したい場合
  python scripts/export_drafts.py --date 2026-08-01 --days 30 --template templates/ranking.html

出力: drafts/<開始日>_<日数>days/
  001_2026-08-01_blood_pair.png     … 初稿画像
  001_2026-08-01_blood_pair.txt     … その画像の投稿文（簡潔）
  ...
  captions.md / captions.csv        … 全日分の投稿文まとめ
  そして drafts/<...>.zip           … 上記をまとめたZIP
"""
import argparse
import csv
import datetime as dt
import json
import os
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from fortune import build_post, iter_schedule  # noqa: E402

RENDER = os.path.join(ROOT, "scripts", "render.mjs")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", help="開始日 YYYY-MM-DD（省略で今日）")
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--template", default=os.path.join(ROOT, "templates", "plain.html"))
    p.add_argument("--out", default=os.path.join(ROOT, "drafts"))
    a = p.parse_args()

    start = dt.date.fromisoformat(a.date) if a.date else dt.date.today()
    folder_name = f"{start.isoformat()}_{a.days}days"
    out_dir = os.path.join(a.out, folder_name)
    os.makedirs(out_dir, exist_ok=True)

    index = []
    for i, (d, theme_key, spec) in enumerate(iter_schedule(start, a.days), 1):
        post = build_post(d, theme_key, spec)
        base = f"{i:03d}_{d.isoformat()}_{theme_key}"
        data_path = os.path.join(out_dir, base + ".json")
        png_path = os.path.join(out_dir, base + ".png")
        txt_path = os.path.join(out_dir, base + ".txt")

        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(post, f, ensure_ascii=False)
        subprocess.run(["node", RENDER, a.template, data_path, png_path],
                       cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(post["caption"] + "\n")
        os.remove(data_path)  # 中間ファイルは残さない

        index.append({"no": i, "date": d.isoformat(), "label": post["date_label"],
                      "theme": theme_key, "title": post["title"],
                      "file": base + ".png", "caption": post["caption"].replace("\n", " / ")})
        print(f"[{i}/{a.days}] {base}")

    # captions.csv
    with open(os.path.join(out_dir, "captions.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["no", "date", "label", "theme", "title", "file", "caption"])
        w.writeheader()
        w.writerows(index)
    # captions.md（画像ファイル名の下に投稿文をそのまま貼れる形）
    with open(os.path.join(out_dir, "captions.md"), "w", encoding="utf-8") as f:
        f.write(f"# 投稿文まとめ（{start.isoformat()} から {a.days}日）\n\n")
        for r in index:
            f.write(f"## {r['no']:03d}. {r['label']}　{r['title']}\n")
            f.write(f"`{r['file']}`\n\n```\n")
            # 投稿文は元の改行のまま
            post_caption = r["caption"].replace(" / ", "\n")
            f.write(post_caption + "\n```\n\n")

    # ZIP
    zip_path = os.path.join(a.out, folder_name + ".zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(os.listdir(out_dir)):
            z.write(os.path.join(out_dir, name), arcname=os.path.join(folder_name, name))
    print(f"\n完了: {len(index)}件\nフォルダ: {out_dir}\nZIP: {zip_path}")


if __name__ == "__main__":
    main()
