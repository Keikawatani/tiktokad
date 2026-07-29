# -*- coding: utf-8 -*-
"""投稿ローテーション（曜日ごとのテーマ）と、期間分のスケジュール生成。

曜日ごとに「テーマの系統」を固定しつつ、週替わり（隔週）でバリエーションを持たせる
2週間ローテーションを採用。フォロワーの習慣（例:月曜はランキング）を保ちつつ飽きを防ぐ。
"""

from datetime import date, timedelta

# テーマ定義。kind がコンテンツの作り方（generator の builder）を決める。
THEME_SPECS = {
    # --- 星座 ---
    "zodiac_overall": {
        "kind": "zodiac", "msg": "general", "palette": "pink",
        "title": "今日の運勢ランキング", "subtitle": "12星座 総合運 TOP12", "emoji_tag": "⭐️",
    },
    "zodiac_love": {
        "kind": "zodiac", "msg": "love", "palette": "lav",
        "title": "恋愛運ランキング", "subtitle": "12星座 LOVE運 TOP12", "emoji_tag": "💗",
    },
    "zodiac_money": {
        "kind": "zodiac", "msg": "money", "palette": "lemon",
        "title": "金運ランキング", "subtitle": "12星座 MONEY運 TOP12", "emoji_tag": "💰",
    },
    "zodiac_weekly": {
        "kind": "zodiac", "msg": "general", "palette": "sky",
        "title": "今週の運勢ランキング", "subtitle": "12星座 総合運まとめ", "emoji_tag": "🌈",
    },
    # --- 血液型 ---
    "blood_overall": {
        "kind": "blood", "msg": "general", "palette": "mint",
        "title": "血液型占い", "subtitle": "今日のごきげん運ランキング", "emoji_tag": "🩸",
    },
    "blood_compat": {
        "kind": "blood_compat", "msg": "compat", "palette": "pink",
        "title": "血液型 相性ランキング", "subtitle": "今日ハッピーになれる相手", "emoji_tag": "💞",
    },
    # --- ラッキーカラー ---
    "lucky_color": {
        "kind": "lucky_color", "msg": "general", "palette": "sky",
        "title": "今日のラッキーカラー", "subtitle": "12星座別・開運カラー診断", "emoji_tag": "🎨",
    },
    # --- MBTI ---
    "mbti_overall": {
        "kind": "mbti", "msg": "general", "palette": "lav",
        "title": "MBTI運勢ランキング", "subtitle": "16タイプ 今日の運勢 TOP16", "emoji_tag": "🔮",
    },
    "mbti_love": {
        "kind": "mbti", "msg": "love", "palette": "pink",
        "title": "MBTI恋愛運ランキング", "subtitle": "16タイプ LOVE運 TOP16", "emoji_tag": "💘",
    },
    # --- 掛け合わせペア ---
    "blood_pair": {
        "kind": "blood_pair", "msg": "pair", "palette": "mint",
        "title": "血液型ペア相性ランキング", "subtitle": "今日の最強カップル血液型", "emoji_tag": "💑",
    },
    "zodiac_pair": {
        "kind": "zodiac_pair", "msg": "pair", "palette": "lav",
        "title": "星座ペア相性ランキング", "subtitle": "今日の運命ペア TOP10", "emoji_tag": "👯",
    },
}

# 2週間ローテーション。曜日(0=月..6=日) -> [第A週テーマ, 第B週テーマ]。
# A/B は ISO週番号の偶奇で切り替わる（隔週）。
WEEKLY_ROTATION = {
    0: ["zodiac_overall", "mbti_overall"],   # 月：総合運の日
    1: ["blood_overall",  "blood_pair"],     # 火：血液型の日
    2: ["zodiac_love",    "zodiac_pair"],    # 水：恋愛・相性の日
    3: ["lucky_color",    "mbti_love"],      # 木：診断の日
    4: ["zodiac_money",   "mbti_overall"],   # 金：金運/性格の日
    5: ["blood_compat",   "zodiac_pair"],    # 土：相性の日
    6: ["zodiac_weekly",  "zodiac_weekly"],  # 日：今週のまとめ
}

_WEEKDAY_JP = ["月", "火", "水", "木", "金", "土", "日"]


def theme_for(d: date) -> str:
    """その日のテーマキーを返す（曜日 × 隔週）。"""
    variants = WEEKLY_ROTATION[d.weekday()]
    week_parity = d.isocalendar()[1] % 2  # ISO週番号の偶奇
    return variants[week_parity % len(variants)]


def date_label(d: date) -> str:
    return f"{d.month}月{d.day}日({_WEEKDAY_JP[d.weekday()]})"


def iter_schedule(start: date, days: int):
    """start から days 日分の (date, theme_key, spec) を返すジェネレータ。"""
    for i in range(days):
        d = start + timedelta(days=i)
        key = theme_for(d)
        yield d, key, THEME_SPECS[key]
