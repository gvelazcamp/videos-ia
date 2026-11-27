#!/usr/bin/env bash
# mezclar.sh — video sin audio + voz (ya a 1,2x) + música con ducking -> MP4 final
# Uso: bash mezclar.sh sin-audio.mp4 voz.mp3 musica.wav salida.mp4
set -euo pipefail
V=$1; VOZ=$2; MUS=$3; OUT=$4
T=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
FADE=$(python3 -c "print(round($T-0.7,3))")
ffmpeg -y -v error -i "$V" -i "$VOZ" -i "$MUS" -filter_complex "\
[1:a]aresample=44100,aformat=channel_layouts=mono,apad=whole_dur=$T,asplit[v1][v2];\
[2:a]aresample=44100,aformat=channel_layouts=mono,volume=0.55[m];\
[m][v2]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=300[md];\
[v1][md]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95,afade=t=out:st=$FADE:d=0.7,aformat=channel_layouts=stereo[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -t "$T" -movflags +faststart "$OUT"
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height:format=duration -of compact "$OUT"
