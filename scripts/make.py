#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""占い動画を生成する司令塔。

例:
  # 今日1日分（画像＋無音動画＋キャプション）を作る
  python scripts/make.py

  # 2026-08-01 から30日分を一括生成（BGM付き）
  python scripts/make.py --date 2026-08-01 --days 30 --bgm assets/bgm/loop.mp3

  # 画像とキャプションだけ（動画は作らない）＝内容の事前チェック用
  python scripts/make.py --days 7 --no-video

出力:
  output/<date>_<theme>/
    data.json      … 生成データ
    frame.png      … 完成画像（サムネにもなる）
    video.mp4      … 投稿用動画（--no-video 指定時は作らない）
    caption.txt    … 投稿文（コピペ用・ハッシュタグ入り）
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from fortune import build_post, iter_schedule  # noqa: E402
from fortune.schedule import THEME_SPECS  # noqa: E402

TEMPLATE = os.path.join(ROOT, "templates", "ranking.html")
RENDER = os.path.join(ROOT, "scripts", "render.mjs")
BUILD = os.path.join(ROOT, "scripts", "build_video.sh")


def parse_args():
    p = argparse.ArgumentParser(description="占い動画ジェネレーター")
    p.add_argument("--date", help="開始日 YYYY-MM-DD（省略時は今日）")
    p.add_argument("--days", type=int, default=1, help="生成する日数（デフォルト1）")
    p.add_argument("--outdir", default=os.path.join(ROOT, "output"))
    p.add_argument("--bgm", default="", help="BGMファイル（省略で無音）")
    p.add_argument("--duration", type=int, default=10, help="動画の長さ(秒)")
    p.add_argument("--no-video", action="store_true", help="画像とキャプションのみ")
    p.add_argument("--template", default=TEMPLATE)
    return p.parse_args()


def run(cmd):
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        raise SystemExit(f"command failed: {' '.join(cmd)}")


def main():
    a = parse_args()
    start = dt.date.fromisoformat(a.date) if a.date else dt.date.today()
    os.makedirs(a.outdir, exist_ok=True)

    made = 0
    for d, theme_key, spec in iter_schedule(start, a.days):
        post = build_post(d, theme_key, spec)
        slug = f"{d.isoformat()}_{theme_key}"
        day_dir = os.path.join(a.outdir, slug)
        os.makedirs(day_dir, exist_ok=True)

        data_path = os.path.join(day_dir, "data.json")
        png_path = os.path.join(day_dir, "frame.png")
        mp4_path = os.path.join(day_dir, "video.mp4")
        cap_path = os.path.join(day_dir, "caption.txt")

        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(post, f, ensure_ascii=False, indent=2)
        with open(cap_path, "w", encoding="utf-8") as f:
            f.write(post["caption"] + "\n")

        run(["node", RENDER, a.template, data_path, png_path])
        if not a.no_video:
            cmd = ["bash", BUILD, png_path, mp4_path]
            if a.bgm:
                cmd += [a.bgm, str(a.duration)]
            else:
                cmd += ["", str(a.duration)]
            run(cmd)

        made += 1
        print(f"[{made}/{a.days}] {slug}  ({THEME_SPECS[theme_key]['title']})")

    print(f"\n完了: {made}件 -> {a.outdir}")


if __name__ == "__main__":
    main()
