# -*- coding: utf-8 -*-
"""夜投稿用の「診断系」コンテンツ（運勢とは別テーマ）。

例:「12星座の〇〇度」「MBTI別の〇〇率」「12星座が〇〇なとき」など。
視覚インパクト重視のポップなレイアウト（templates/diagnosis.html）で描画する。

※ 参考にした人気アカウントのキャラクターは各社の独自イラストなので複製しない。
   ここで作るのは「フォーマット・数値・文言」まで。キャラは assets/mascots/ に
   各自の素材を置けば差し込まれる（無ければ簡易バッジ表示）。
"""
import os
import hashlib
import random

from . import data

_MASCOT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "mascots")
HANDLE = "@uranai_daily"

# スタイル（鮮やかめの配色 + タイトルの袋文字色）
STYLES = {
    "gold":   {"bg1": "#FBF2DD", "bg2": "#F0DFBB", "fill": "#FFE27A", "stroke": "#6E5214", "num": "#C8951C", "ink": "#5A4A22"},
    "orange": {"bg1": "#FFF4D6", "bg2": "#FFE29A", "fill": "#FFFFFF", "stroke": "#E1600C", "num": "#F0600C", "ink": "#7A3E12"},
    "pink":   {"bg1": "#FFE7F1", "bg2": "#FFC6DD", "fill": "#FFFFFF", "stroke": "#E24C86", "num": "#E24C86", "ink": "#7A3352"},
    "green":  {"bg1": "#E4F6D2", "bg2": "#C2E89C", "fill": "#FFFFFF", "stroke": "#3F8E2C", "num": "#3F8E2C", "ink": "#33551F"},
    "blue":   {"bg1": "#E1EEFF", "bg2": "#BCD8FF", "fill": "#FFFFFF", "stroke": "#2E6ED0", "num": "#2E6ED0", "ink": "#2C466E"},
    "purple": {"bg1": "#ECE4FF", "bg2": "#D2C1FF", "fill": "#FFFFFF", "stroke": "#6A4FD0", "num": "#6A4FD0", "ink": "#3F3070"},
}

_Z = {z["key"]: z for z in data.ZODIAC}
_M = {m["key"]: m for m in data.MBTI}


def _mascot(key):
    if key and os.path.exists(os.path.join(_MASCOT_DIR, f"{key}.png")):
        return f"../assets/mascots/{key}.png"
    return None


# ---------------------------------------------------------------------------
# トピック定義
#   percent(12星座/MBTI): items = {key: (値, ラベル, 説明)}
#   groups            : groups = [(見出し, サブ, [key,...]), ...]
# ---------------------------------------------------------------------------
TOPICS = [
    # ===== 12星座 %（グリッド） =====
    {
        "id": "mental", "kind": "zodiac_percent", "style": "orange", "unit": "%",
        "title": "12星座のメンタル強度", "subtitle": "打たれ強いのは？",
        "items": {
            "aries": (92, "鋼のハート", "立ち直り0秒"),
            "taurus": (88, "動じない", "常にマイペース"),
            "gemini": (60, "切り替え上手", "寝たら復活"),
            "cancer": (40, "豆腐メンタル", "気にして眠れない"),
            "leo": (95, "無敵の自信", "プライドが盾"),
            "virgo": (55, "反省会常連", "脳内反省エンドレス"),
            "libra": (70, "平和第一", "揉め事は回避"),
            "scorpio": (99, "執念の塊", "根に持つが折れない"),
            "sagittarius": (85, "楽観マスター", "なんとかなる精神"),
            "capricorn": (90, "我慢の鬼", "顔に出さず耐える"),
            "aquarius": (75, "マイワールド", "他人の評価は別世界"),
            "pisces": (30, "共感しすぎ", "もらい泣きで消耗"),
        },
    },
    {
        "id": "numaraseru", "kind": "zodiac_percent", "style": "pink", "unit": "%",
        "title": "12星座の沼らせ度", "subtitle": "気づけばハマってるのは？",
        "items": {
            "aries": (70, "猪突猛進", "まっすぐな好意"),
            "taurus": (65, "居心地系", "手放せなくなる"),
            "gemini": (88, "飽きさせない", "会話が中毒に"),
            "cancer": (80, "尽くし系", "甘やかされ沼"),
            "leo": (92, "主役オーラ", "一緒が楽しい"),
            "virgo": (55, "ギャップ", "隙に落ちる"),
            "libra": (85, "上品タラシ", "特別扱い上手"),
            "scorpio": (99, "独占魔性", "深く刺さる"),
            "sagittarius": (60, "自由人", "追いたくなる"),
            "capricorn": (50, "塩対応", "たまの優しさが効く"),
            "aquarius": (78, "謎多き人", "掴めず気になる"),
            "pisces": (90, "甘え上手", "守りたくなる"),
        },
    },
    {
        "id": "tennen", "kind": "zodiac_percent", "style": "green", "unit": "%",
        "title": "12星座の天然度", "subtitle": "実は無自覚なのは？",
        "items": {
            "aries": (80, "勢い天然", "考える前に動く"),
            "taurus": (45, "実は計算", "天然のフリ上手"),
            "gemini": (70, "話し天然", "話がよく飛ぶ"),
            "cancer": (60, "情緒天然", "気分屋さん"),
            "leo": (85, "堂々天然", "間違えても自信満々"),
            "virgo": (20, "しっかり者", "天然とは無縁…？"),
            "libra": (55, "上品天然", "ふわっと発言"),
            "scorpio": (30, "計算派", "隙を見せない"),
            "sagittarius": (95, "自由天然", "思いつきで生きる"),
            "capricorn": (25, "現実派", "天然ゼロ"),
            "aquarius": (99, "宇宙人", "発想が斜め上"),
            "pisces": (90, "メルヘン", "夢の中で生きてる"),
        },
    },
    # ===== MBTI %（グリッド16） =====
    {
        "id": "mbti_numa", "kind": "mbti_percent", "style": "purple", "unit": "%",
        "title": "MBTI別の恋愛沼らせ率", "subtitle": "本気にさせたら抜け出せない",
        "items": {
            "INTJ": (88, "戦略沼", "狙ったら逃さない"),
            "INTP": (60, "論破沼", "議論が楽しい"),
            "ENTJ": (90, "俺様沼", "頼れるリード"),
            "ENTP": (85, "トーク沼", "飽きさせない"),
            "INFJ": (92, "理解沼", "見透かされる"),
            "INFP": (80, "世界観沼", "独特の魅力"),
            "ENFJ": (95, "王子沼", "気遣いで骨抜き"),
            "ENFP": (88, "太陽沼", "一緒が楽しい"),
            "ISTJ": (50, "安定沼", "誠実さがじわる"),
            "ISFJ": (78, "尽くし沼", "甘やかし上手"),
            "ESTJ": (65, "リード沼", "頼りがい抜群"),
            "ESFJ": (82, "愛され沼", "面倒見の良さ"),
            "ISTP": (70, "ミステリ沼", "掴めない魅力"),
            "ISFP": (85, "アート沼", "感性にやられる"),
            "ESTP": (80, "刺激沼", "スリルで夢中"),
            "ESFP": (90, "エンタメ沼", "楽しすぎ注意"),
        },
    },
    # ===== 12星座 グループ分け =====
    {
        "id": "angry", "kind": "zodiac_groups", "style": "blue",
        "title": "12星座が怒ったとき", "subtitle": "タイプ別・怒りの出し方",
        "groups": [
            ("その場で即爆発", "感情をストレートにぶつける", ["aries", "leo", "sagittarius", "gemini"]),
            ("正論で冷静に詰める", "ロジックで追い込むタイプ", ["taurus", "virgo", "libra", "aquarius"]),
            ("静かに氷点下", "無言で距離を置き根に持つ", ["cancer", "scorpio", "capricorn", "pisces"]),
        ],
    },
    {
        "id": "line", "kind": "zodiac_groups", "style": "green",
        "title": "12星座のLINE返信速度", "subtitle": "既読つけたら…？",
        "groups": [
            ("秒で既読・即レス", "通知が来たら即反応", ["aries", "gemini", "leo", "sagittarius"]),
            ("気が向いたら返す", "マイペースに返信", ["taurus", "cancer", "scorpio", "pisces"]),
            ("未読が溜まりがち", "悪気なく放置しがち", ["virgo", "libra", "capricorn", "aquarius"]),
        ],
    },
]

TOPICS_BY_ID = {t["id"]: t for t in TOPICS}


def _rng(*parts):
    seed = hashlib.sha256("::".join(str(p) for p in parts).encode()).hexdigest()
    return random.Random(int(seed[:16], 16))


def build_diagnosis(topic_id, d=None) -> dict:
    """トピックIDから描画用データを組み立てる。"""
    t = TOPICS_BY_ID[topic_id]
    st = STYLES[t["style"]]
    out = {
        "format": "groups" if t["kind"].endswith("groups") else "grid",
        "kind": t["kind"],
        "title": t["title"], "subtitle": t["subtitle"],
        "unit": t.get("unit", ""), "style": st, "handle": HANDLE,
        "topic_id": topic_id,
    }
    lookup = _M if t["kind"].startswith("mbti") else _Z

    if out["format"] == "grid":
        cells = []
        for key, (val, label, desc) in t["items"].items():
            meta = lookup[key]
            cells.append({
                "key": key, "name": meta["name"], "sub": meta.get("sub", ""),
                "grad": list(meta["grad"]), "value": val, "label": label, "desc": desc,
                "mascot": _mascot(key),
            })
        out["cells"] = cells
    else:
        groups = []
        for head, sub, keys in t["groups"]:
            gcells = [{
                "key": k, "name": lookup[k]["name"], "grad": list(lookup[k]["grad"]),
                "mascot": _mascot(k),
            } for k in keys]
            groups.append({"head": head, "sub": sub, "cells": gcells})
        out["groups"] = groups

    # 簡潔キャプション
    q = "あなたのMBTIは何%？" if t["kind"].startswith("mbti") else "あなたの星座は何%？"
    if out["format"] == "groups":
        q = "あなたは何タイプ？"
    tags = "#占い #星座 #12星座 #性格診断 #あるある #fyp"
    if t["kind"].startswith("mbti"):
        tags = "#MBTI #性格診断 #mbti診断 #あるある #fyp"
    out["caption"] = f"🦊{t['title']}\n{q} コメントで教えてね👇\n{tags}"
    return out
