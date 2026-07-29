# -*- coding: utf-8 -*-
"""日付から1投稿分のコンテンツ(JSON)を決定論的に生成する。

同じ日付・同じテーマなら常に同じ結果になる（seed = 日付+テーマ）。
これにより「作り直しても内容がブレない」「事前に全期間を確認できる」を両立する。
"""

import hashlib
import os
import random

from . import data, schedule

_MASCOT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "mascots")


def _mascot_rel(key):
    """assets/mascots/<key>.png があれば、テンプレートから見た相対パスを返す。無ければ None。"""
    if key and os.path.exists(os.path.join(_MASCOT_DIR, f"{key}.png")):
        return f"../assets/mascots/{key}.png"
    return None

# 投稿者ハンドル・CTA はここを書き換えるだけで全動画に反映される。
HANDLE = "@uranai_daily"
CTA = "フォローして毎日チェック♡"

_BASE_HASHTAGS = ["#占い", "#今日の運勢", "#星座占い", "#占いランキング", "#開運", "#fyp", "#おすすめにのりたい"]


def _rng(*parts) -> random.Random:
    seed = hashlib.sha256("::".join(str(p) for p in parts).encode()).hexdigest()
    return random.Random(int(seed[:16], 16))


def _tier_for_rank(rank: int, total: int) -> str:
    if rank == 1:
        return "top"
    if rank <= max(2, total * 0.30):
        return "high"
    if rank <= max(3, total * 0.75):
        return "mid"
    return "low"


def _stars(tier: str) -> int:
    return {"top": 5, "high": 4, "mid": 3, "low": 2}[tier]


def _pick(rng: random.Random, seq):
    return seq[rng.randrange(len(seq))]


def _picker(rng, seq):
    """同じ投稿内で同じ値をなるべく繰り返さないピッカーを返す。"""
    used = set()

    def pick():
        candidates = [x for x in seq if (x if isinstance(x, str) else x[0]) not in used]
        if not candidates:
            used.clear()
            candidates = list(seq)
        x = candidates[rng.randrange(len(candidates))]
        used.add(x if isinstance(x, str) else x[0])
        return x
    return pick


def _message(rng, msg_key, tier):
    return _pick(rng, data.MESSAGES[msg_key][tier])


def _msg_stream(rng, msg_key):
    """tier を渡すと、投稿内でなるべく重複しないメッセージを返す関数。"""
    used = set()

    def get(tier):
        for _ in range(8):
            m = _message(rng, msg_key, tier)
            if m not in used:
                used.add(m)
                return m
        return m
    return get


def _zodiac_rows(rng, msg_key):
    order = data.ZODIAC[:]
    rng.shuffle(order)
    msg = _msg_stream(rng, msg_key)
    item = _picker(rng, data.LUCKY_ITEMS)
    rows = []
    total = len(order)
    for i, z in enumerate(order):
        rank = i + 1
        tier = _tier_for_rank(rank, total)
        it = item()
        rows.append({
            "rank": rank, "key": z["key"], "name": z["name"], "sub": z["dates"], "grad": list(z["grad"]),
            "comment": msg(tier), "item": it, "note": f"ラッキー: {it}",
            "stars": _stars(tier), "swatch": None,
        })
    return rows


def _blood_rows(rng, msg_key):
    order = data.BLOOD[:]
    rng.shuffle(order)
    msg = _msg_stream(rng, msg_key)
    color = _picker(rng, data.LUCKY_COLORS)
    item = _picker(rng, data.LUCKY_ITEMS)
    rows = []
    total = len(order)
    for i, b in enumerate(order):
        rank = i + 1
        tier = _tier_for_rank(rank, total)
        c = color(); it = item()
        rows.append({
            "rank": rank, "key": b["key"], "name": b["name"], "sub": "", "grad": list(b["grad"]),
            "comment": msg(tier), "item": it, "note": f"ラッキーカラー: {c[0]}／{it}",
            "stars": _stars(tier), "swatch": c[1],
        })
    return rows


def _blood_compat_rows(rng, msg_key):
    order = data.BLOOD[:]
    rng.shuffle(order)
    msg = _msg_stream(rng, msg_key)
    rows = []
    total = len(order)
    for i, b in enumerate(order):
        rank = i + 1
        tier = _tier_for_rank(rank, total)
        partner = _pick(rng, [x for x in data.BLOOD if x["key"] != b["key"]])
        rows.append({
            "rank": rank, "key": b["key"], "name": b["name"], "sub": "", "grad": list(b["grad"]),
            "comment": msg(tier), "item": f"相性◎ {partner['name']}", "note": f"今日の相性◎は {partner['name']}",
            "stars": _stars(tier), "swatch": None,
        })
    return rows


def _lucky_color_rows(rng, _msg_key):
    # 星座順（固定）で、その日の各星座のラッキーカラー＆アイテムを出す。
    color = _picker(rng, data.LUCKY_COLORS)
    item = _picker(rng, data.LUCKY_ITEMS)
    rows = []
    for z in data.ZODIAC:
        c = color(); it = item()
        rows.append({
            "rank": None, "key": z["key"], "name": z["name"], "sub": z["dates"], "grad": list(z["grad"]),
            "comment": c[0], "item": it, "note": f"ラッキー: {it}",
            "stars": None, "swatch": c[1],
        })
    return rows


def _mbti_rows(rng, msg_key):
    order = data.MBTI[:]
    rng.shuffle(order)
    msg = _msg_stream(rng, msg_key)
    item = _picker(rng, data.LUCKY_ITEMS)
    rows = []
    total = len(order)
    for i, m in enumerate(order):
        rank = i + 1
        tier = _tier_for_rank(rank, total)
        it = item()
        rows.append({
            "rank": rank, "key": m["key"], "name": m["name"], "sub": m["sub"], "grad": list(m["grad"]),
            "comment": msg(tier), "item": it, "note": f"ラッキー: {it}",
            "stars": _stars(tier), "swatch": None,
        })
    return rows


def _pairs_from(seq, include_same):
    out = []
    for i, a in enumerate(seq):
        for j, b in enumerate(seq):
            if j < i:
                continue
            if j == i and not include_same:
                continue
            out.append((a, b))
    return out


def _pair_rows(rng, msg_key, seq, include_same, top_n):
    pairs = _pairs_from(seq, include_same)
    rng.shuffle(pairs)
    pairs = pairs[:top_n]
    msg = _msg_stream(rng, msg_key)
    rows = []
    total = len(pairs)
    for i, (a, b) in enumerate(pairs):
        rank = i + 1
        tier = _tier_for_rank(rank, total)
        rows.append({
            "rank": rank,
            "name": f"{a['name']} × {b['name']}",
            "sub": "",
            "grad": list(a["grad"]),
            "pair": [
                {"name": a["name"], "grad": list(a["grad"])},
                {"name": b["name"], "grad": list(b["grad"])},
            ],
            "comment": msg(tier),
            "item": "相性◎",
            "note": "今日の相性◎",
            "stars": _stars(tier), "swatch": None,
        })
    return rows


def _blood_pair_rows(rng, msg_key):
    # 4型 -> 同型含む10ペア。上位8を出す。
    return _pair_rows(rng, msg_key, data.BLOOD, include_same=True, top_n=8)


def _zodiac_pair_rows(rng, msg_key):
    # 12星座 -> 66ペア。上位10を出す。
    return _pair_rows(rng, msg_key, data.ZODIAC, include_same=False, top_n=10)


_BUILDERS = {
    "zodiac": _zodiac_rows,
    "blood": _blood_rows,
    "blood_compat": _blood_compat_rows,
    "lucky_color": _lucky_color_rows,
    "mbti": _mbti_rows,
    "blood_pair": _blood_pair_rows,
    "zodiac_pair": _zodiac_pair_rows,
}


def build_post(d, theme_key=None, spec=None) -> dict:
    """date d の投稿データを1件生成して dict で返す。"""
    if theme_key is None:
        theme_key = schedule.theme_for(d)
    if spec is None:
        spec = schedule.THEME_SPECS[theme_key]

    rng = _rng(d.isoformat(), theme_key)
    rows = _BUILDERS[spec["kind"]](rng, spec["msg"])
    mode = "color" if spec["kind"] == "lucky_color" else "rank"

    # キャラ画像(assets/mascots/<key>.png)があれば自動でひも付け（無ければ None のまま）
    for row in rows:
        row["mascot"] = _mascot_rel(row.get("key"))

    kind = spec["kind"]
    tag = spec["emoji_tag"]
    first = rows[0]["name"]
    # 簡潔な投稿文（1行フック＋ハッシュタグ4つ）
    hooks = {
        "zodiac": f"1位は{first}✨ あなたは何位？",
        "blood": f"1位は{first}✨ あなたは何型？",
        "blood_compat": f"1位は{first}✨ 気になる相手は？",
        "mbti": f"1位は{first}✨ あなたのMBTIは？",
        "lucky_color": "あなたのラッキーカラーは？保存してね",
        "blood_pair": f"今日のベストペアは{first}💞",
        "zodiac_pair": f"今日の運命ペアは{first}💞",
    }
    hashtags = {
        "zodiac": ["#占い", "#星座占い", "#今日の運勢", "#fyp"],
        "blood": ["#占い", "#血液型占い", "#今日の運勢", "#fyp"],
        "blood_compat": ["#占い", "#血液型占い", "#相性占い", "#fyp"],
        "mbti": ["#占い", "#MBTI", "#性格診断", "#fyp"],
        "lucky_color": ["#占い", "#星座占い", "#ラッキーカラー", "#fyp"],
        "blood_pair": ["#占い", "#血液型占い", "#相性占い", "#fyp"],
        "zodiac_pair": ["#占い", "#星座占い", "#相性占い", "#fyp"],
    }
    tags = hashtags.get(kind, ["#占い", "#今日の運勢", "#fyp", "#おすすめ"])
    hook = hooks.get(kind, f"1位は{first}✨")
    caption = f"{tag}{spec['title']}｜{schedule.date_label(d)}\n{hook}\n" + " ".join(tags)

    return {
        "date": d.isoformat(),
        "date_label": schedule.date_label(d),
        "theme": theme_key,
        "kind": spec["kind"],
        "mode": mode,
        "title": spec["title"],
        "subtitle": spec["subtitle"],
        "palette_key": spec["palette"],
        "palette": data.PALETTES[spec["palette"]],
        "handle": HANDLE,
        "cta": CTA,
        "rows": rows,
        "hashtags": tags,
        "caption": caption,
    }
