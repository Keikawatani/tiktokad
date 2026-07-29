# -*- coding: utf-8 -*-
"""投稿ローテーション（曜日ごとのテーマ）と、期間分のスケジュール生成。"""

from datetime import date, timedelta

# テーマ定義。kind がコンテンツの作り方を決める。
THEME_SPECS = {
    "zodiac_overall": {
        "kind": "zodiac", "msg": "general", "palette": "pink",
        "title": "今日の運勢ランキング", "subtitle": "12星座 総合運 TOP12",
        "emoji_tag": "⭐️",
    },
    "blood_overall": {
        "kind": "blood", "msg": "general", "palette": "mint",
        "title": "血液型占い", "subtitle": "今日のごきげん運ランキング",
        "emoji_tag": "🩸",
    },
    "zodiac_love": {
        "kind": "zodiac", "msg": "love", "palette": "lav",
        "title": "恋愛運ランキング", "subtitle": "12星座 LOVE運 TOP12",
        "emoji_tag": "💗",
    },
    "lucky_color": {
        "kind": "lucky_color", "msg": "general", "palette": "sky",
        "title": "今日のラッキーカラー", "subtitle": "12星座別・開運カラー診断",
        "emoji_tag": "🎨",
    },
    "zodiac_money": {
        "kind": "zodiac", "msg": "money", "palette": "lemon",
        "title": "金運ランキング", "subtitle": "12星座 MONEY運 TOP12",
        "emoji_tag": "💰",
    },
    "blood_compat": {
        "kind": "blood_compat", "msg": "compat", "palette": "pink",
        "title": "血液型 相性ランキング", "subtitle": "今日ハッピーになれる相手",
        "emoji_tag": "💞",
    },
    "zodiac_weekly": {
        "kind": "zodiac", "msg": "general", "palette": "sky",
        "title": "今週の運勢ランキング", "subtitle": "12星座 総合運まとめ",
        "emoji_tag": "🌈",
    },
}

# 曜日ローテーション（0=月曜 ... 6=日曜）
WEEKLY_ROTATION = {
    0: "zodiac_overall",   # 月
    1: "blood_overall",    # 火
    2: "zodiac_love",      # 水
    3: "lucky_color",      # 木
    4: "zodiac_money",     # 金
    5: "blood_compat",     # 土
    6: "zodiac_weekly",    # 日
}

_WEEKDAY_JP = ["月", "火", "水", "木", "金", "土", "日"]


def theme_for(d: date) -> str:
    """その日のテーマキーを返す。"""
    return WEEKLY_ROTATION[d.weekday()]


def date_label(d: date) -> str:
    return f"{d.month}月{d.day}日({_WEEKDAY_JP[d.weekday()]})"


def iter_schedule(start: date, days: int):
    """start から days 日分の (date, theme_key, spec) を返すジェネレータ。"""
    for i in range(days):
        d = start + timedelta(days=i)
        key = theme_for(d)
        yield d, key, THEME_SPECS[key]
