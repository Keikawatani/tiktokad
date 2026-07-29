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
    # ===== 追加：人気の%グリッド =====
    {
        "id": "sukibare", "kind": "zodiac_percent", "style": "pink", "unit": "%",
        "title": "12星座の好きバレ率", "subtitle": "好きな人にバレやすいのは？",
        "items": {
            "aries": (95, "全身で好き", "態度に全部出る"), "taurus": (30, "隠し上手", "顔に出さない"),
            "gemini": (88, "話しかけ増", "つい目で追う"), "cancer": (80, "挙動不審", "わかりやすい"),
            "leo": (92, "グイグイ", "独占欲だだ漏れ"), "virgo": (40, "平静を装う", "陰でソワソワ"),
            "libra": (55, "全員に優しい", "撹乱して隠す"), "scorpio": (20, "完全ポーカー", "絶対バレない"),
            "sagittarius": (85, "ストレート", "好意まっすぐ"), "capricorn": (35, "塩対応化", "逆に冷たく"),
            "aquarius": (60, "読めない", "態度が謎"), "pisces": (90, "うるうる", "目が物語る"),
        },
    },
    {
        "id": "terekakushi", "kind": "zodiac_percent", "style": "purple", "unit": "%",
        "title": "12星座の照れ隠し度", "subtitle": "素直になれないのは？",
        "items": {
            "aries": (70, "つい強気", "照れて強がる"), "taurus": (50, "無言照れ", "黙り込む"),
            "gemini": (65, "茶化す", "冗談でごまかす"), "cancer": (80, "拗ねる", "素直じゃない"),
            "leo": (60, "咳払い", "威厳を保つ"), "virgo": (75, "早口否定", "「別に」連発"),
            "libra": (45, "笑顔で流す", "スマートに逃げる"), "scorpio": (90, "塩対応化", "好きほど冷たく"),
            "sagittarius": (40, "笑ってごまかす", "ノリで隠す"), "capricorn": (85, "真顔防御", "感情を出さない"),
            "aquarius": (95, "話題変える", "急に別の話"), "pisces": (55, "顔真っ赤", "隠しきれない"),
        },
    },
    {
        "id": "iikaeshi", "kind": "zodiac_percent", "style": "gold", "unit": "%",
        "title": "12星座の言い返す度", "subtitle": "売られた喧嘩を買うのは？",
        "items": {
            "aries": (99, "秒で応戦", "即買い"), "taurus": (60, "溜めて反撃", "限界で一撃"),
            "gemini": (85, "口が達者", "言葉で圧倒"), "cancer": (30, "泣き寝入り", "後で凹む"),
            "leo": (90, "プライド戦", "負けを認めない"), "virgo": (80, "正論ラッシュ", "理詰めで詰める"),
            "libra": (40, "穏便に回避", "荒立てない"), "scorpio": (95, "執念の反撃", "倍返し"),
            "sagittarius": (55, "笑って流す", "気にしない"), "capricorn": (70, "冷静に論破", "感情抜き"),
            "aquarius": (65, "論点ずらし", "煙に巻く"), "pisces": (20, "言い返せない", "飲み込む"),
        },
    },
    {
        "id": "atodeyaru", "kind": "zodiac_percent", "style": "blue", "unit": "%",
        "title": "12星座の後でやる率", "subtitle": "後回しにしがちなのは？",
        "items": {
            "aries": (78, "熱で動く", "気分次第"), "taurus": (85, "腰が重い", "動くまで長い"),
            "gemini": (80, "目移り", "別のこと開始"), "cancer": (55, "気分屋", "ノると早い"),
            "leo": (60, "直前本気", "追込まれ覚醒"), "virgo": (20, "即着手", "計画的"),
            "libra": (65, "迷って停滞", "決められない"), "scorpio": (40, "一点集中", "決めたら早い"),
            "sagittarius": (88, "明日やる", "楽観先延ばし"), "capricorn": (15, "前倒し", "早めに片付け"),
            "aquarius": (82, "気分次第", "興味が全て"), "pisces": (90, "夢の中", "気づけば締切"),
        },
    },
    {
        "id": "sewayaki", "kind": "zodiac_percent", "style": "green", "unit": "%",
        "title": "12星座の世話焼き度", "subtitle": "面倒見がいいのは？",
        "items": {
            "aries": (70, "兄貴肌", "ほっとけない"), "taurus": (75, "陰で支える", "黙って助ける"),
            "gemini": (55, "情報係", "役立つ話"), "cancer": (95, "ママ気質", "尽くしすぎ"),
            "leo": (85, "親分肌", "頼られたい"), "virgo": (90, "気配りの鬼", "先回りケア"),
            "libra": (65, "バランス係", "場を整える"), "scorpio": (60, "身内限定", "選んだ人に全力"),
            "sagittarius": (50, "放任型", "自由にさせる"), "capricorn": (72, "現実支援", "具体的に助ける"),
            "aquarius": (40, "見守り型", "干渉しない"), "pisces": (88, "共感係", "寄り添い上手"),
        },
    },
    {
        "id": "sokubaku", "kind": "zodiac_percent", "style": "pink", "unit": "%",
        "title": "12星座の束縛強め度", "subtitle": "恋人を独占したいのは？",
        "items": {
            "aries": (75, "まっすぐ独占", "好きを隠さず"), "taurus": (88, "手放さない", "安定を求める"),
            "gemini": (40, "自由派", "束縛は苦手"), "cancer": (90, "甘え独占", "そばにいたい"),
            "leo": (85, "一番でいたい", "注目を独占"), "virgo": (60, "心配性", "つい確認"),
            "libra": (45, "スマート", "束縛を嫌う"), "scorpio": (99, "完全独占", "深く一途"),
            "sagittarius": (20, "超自由", "束縛ゼロ"), "capricorn": (70, "静かに独占", "態度に出さず"),
            "aquarius": (25, "個人主義", "距離を保つ"), "pisces": (80, "依存型", "尽くして囲う"),
        },
    },
    {
        "id": "mbti_tensai", "kind": "mbti_percent", "style": "purple", "unit": "%",
        "title": "MBTI別の天才率", "subtitle": "発想がぶっ飛んでるのは？",
        "items": {
            "INTJ": (92, "戦略天才", "数手先を読む"), "INTP": (95, "理論天才", "独自理論"),
            "ENTJ": (85, "統率天才", "人を動かす"), "ENTP": (90, "発想天才", "アイデア無限"),
            "INFJ": (80, "洞察天才", "本質を見抜く"), "INFP": (78, "空想天才", "独自の世界"),
            "ENFJ": (75, "共感天才", "人心掌握"), "ENFP": (82, "ひらめき", "思いつき爆発"),
            "ISTJ": (50, "堅実型", "コツコツ派"), "ISFJ": (45, "サポート型", "縁の下の力"),
            "ESTJ": (60, "実務天才", "段取り最強"), "ESFJ": (48, "調整型", "空気を読む"),
            "ISTP": (88, "職人天才", "手が動く"), "ISFP": (70, "感性天才", "センスの塊"),
            "ESTP": (72, "瞬発天才", "行動が速い"), "ESFP": (68, "エンタメ天才", "場を沸かす"),
        },
    },
    # ===== 追加：グループ分け =====
    {
        "id": "tachinaori", "kind": "zodiac_groups", "style": "blue",
        "title": "12星座の立ち直り方", "subtitle": "落ち込んだ時どうする？",
        "groups": [
            ("寝て忘れる", "睡眠でリセット", ["aries", "sagittarius", "leo", "gemini"]),
            ("人に話す", "話してスッキリ", ["cancer", "libra", "pisces", "taurus"]),
            ("一人でこもる", "静かに回復", ["virgo", "scorpio", "capricorn", "aquarius"]),
        ],
    },
    {
        "id": "honshou", "kind": "zodiac_groups", "style": "orange",
        "title": "親しい人にだけ出る本性", "subtitle": "心を許すとこうなる",
        "groups": [
            ("急に甘えん坊", "実はデレる", ["cancer", "pisces", "leo", "taurus"]),
            ("毒舌全開", "本音ダダ漏れ", ["gemini", "virgo", "sagittarius", "aquarius"]),
            ("無言で安心", "一緒にいるだけ", ["scorpio", "capricorn", "libra", "aries"]),
        ],
    },
]

TOPICS_BY_ID = {t["id"]: t for t in TOPICS}

# 夜投稿のローテーション順（このリストを日付順に消化していく）
NIGHT_ORDER = [t["id"] for t in TOPICS]


def night_topic_for(d):
    """日付から夜投稿のトピックIDを返す（NIGHT_ORDER を巡回）。"""
    return NIGHT_ORDER[d.toordinal() % len(NIGHT_ORDER)]


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
