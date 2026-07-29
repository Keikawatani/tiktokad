#!/usr/bin/env bash
# 静止画(PNG) + BGM(任意) -> TikTok用 縦型MP4 (1080x1920 / H.264)
#
# 使い方:
#   scripts/build_video.sh <img.png> <out.mp4> [bgm.(mp3|m4a|wav)] [duration_sec]
#
# BGM を省略すると無音動画になります（テスト用）。本番は必ず利用OKな音源を指定するか、
# TikTokアプリ内の「商用楽曲ライブラリ / トレンド音源」を後から付けてください（推奨・下記docs参照）。
set -euo pipefail

IMG="${1:?img path required}"
OUT="${2:?out path required}"
BGM="${3:-}"
DUR="${4:-10}"

command -v ffmpeg >/dev/null || { echo "ffmpeg が見つかりません"; exit 1; }

VF="scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=white,format=yuv420p"

if [[ -n "$BGM" && -f "$BGM" ]]; then
  # BGMをDUR秒でトリム、終端1秒フェードアウト
  ffmpeg -y -loglevel error \
    -loop 1 -i "$IMG" \
    -stream_loop -1 -i "$BGM" \
    -t "$DUR" -r 30 \
    -vf "$VF" \
    -c:v libx264 -preset medium -crf 20 \
    -c:a aac -b:a 192k -ar 44100 \
    -af "afade=t=out:st=$((DUR-1)):d=1" \
    -shortest -movflags +faststart \
    "$OUT"
else
  # 無音（テスト用フォールバック）
  ffmpeg -y -loglevel error \
    -loop 1 -i "$IMG" \
    -f lavfi -i anullsrc=r=44100:cl=stereo \
    -t "$DUR" -r 30 \
    -vf "$VF" \
    -c:v libx264 -preset medium -crf 20 \
    -c:a aac -b:a 128k \
    -shortest -movflags +faststart \
    "$OUT"
fi

echo "built: $OUT ($(du -h "$OUT" | cut -f1), ${DUR}s)"
