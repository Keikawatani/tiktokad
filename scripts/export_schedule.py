#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""投稿スケジュールをCSVとMarkdownで書き出す（内容の一言プレビュー付き）。

例:
  python scripts/export_schedule.py --date 2026-08-01 --days 182 \
      --csv docs/schedule.csv --md docs/schedule_preview.md
"""
import argparse
import csv
import datetime as dt
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from fortune import build_post, iter_schedule, date_label  # noqa: E402


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date")
    p.add_argument("--days", type=int, default=182)  # 約半年
    p.add_argument("--csv", default=os.path.join(ROOT, "docs", "schedule.csv"))
    p.add_argument("--md", default=os.path.join(ROOT, "docs", "schedule_preview.md"))
    a = p.parse_args()

    start = dt.date.fromisoformat(a.date) if a.date else dt.date.today()
    rows = []
    for d, theme_key, spec in iter_schedule(start, a.days):
        post = build_post(d, theme_key, spec)
        first = post["rows"][0]
        top = f"1位 {first['name']}（{first['comment']}）" if post["mode"] == "rank" else "星座別カラー"
        rows.append({
            "date": d.isoformat(),
            "label": date_label(d),
            "theme": theme_key,
            "title": post["title"],
            "subtitle": post["subtitle"],
            "highlight": top,
        })

    os.makedirs(os.path.dirname(a.csv), exist_ok=True)
    with open(a.csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date", "label", "theme", "title", "subtitle", "highlight"])
        w.writeheader()
        w.writerows(rows)

    with open(a.md, "w", encoding="utf-8") as f:
        f.write(f"# 投稿スケジュール プレビュー（{start.isoformat()} から {a.days}日）\n\n")
        f.write("自動生成。`scripts/export_schedule.py` で再生成できます。\n\n")
        f.write("| 日付 | テーマ | タイトル | ハイライト |\n|---|---|---|---|\n")
        for r in rows[:35]:  # 最初の5週間だけ表に（全量はCSV参照）
            f.write(f"| {r['label']} | {r['theme']} | {r['title']} | {r['highlight']} |\n")
        f.write(f"\n※全{len(rows)}日分は `docs/schedule.csv` を参照。\n")

    print(f"wrote {a.csv} and {a.md} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
