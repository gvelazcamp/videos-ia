#!/usr/bin/env bash
# mezclar.sh — une video sin audio + voz (ya a 1,2×) + música con ducking + 2 efectos en palabras exactas.
# Uso: bash mezclar.sh sin-audio.mp4 voz.mp3 musica.wav puerta.wav alarma.wav <idx_palabra_puerta> <idx_palabra_alarma> final.mp4
# Todo se pasa a mono 44,1 kHz antes de mezclar (evita desfasajes mono/estéreo); salida AAC estéreo.
set -euo pipefail
V=$1; VOZ=$2; MUS=$3; FXP=$4; FXA=$5; IP=$6; IA=$7; OUT=$8
T=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")               # duración decimal del video
read P A <<<"$(python3 -c "import json;w=json.load(open('timing.json'))['wt'];print(int(w[$IP]*1000),int(w[$IA]*1000))")"
FADE=$(python3 -c "print(round($T-0.7,3))")                                          # el fundido empieza 0,7 s antes del final
ffmpeg -y -v error -i "$V" -i "$VOZ" -i "$MUS" -i "$FXP" -i "$FXA" -filter_complex "\
[1:a]aresample=44100,aformat=channel_layouts=mono,apad=whole_dur=$T,asplit[v1][v2];\
[2:a]aresample=44100,aformat=channel_layouts=mono,volume=0.55[m];\
[m][v2]sidechaincompress=threshold=0.05:ratio=6:attack=20:release=300[md];\
[3:a]aresample=44100,aformat=channel_layouts=mono,adelay=delays=$P:all=1,volume=0.9[fp];\
[4:a]aresample=44100,aformat=channel_layouts=mono,adelay=delays=$A:all=1,volume=0.6[fa];\
[v1][md][fp][fa]amix=inputs=4:normalize=0:duration=first,alimiter=limit=0.95,afade=t=out:st=$FADE:d=0.7,aformat=channel_layouts=stereo[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -t "$T" -movflags +faststart "$OUT"
ffprobe -v error -show_entries stream=codec_type,codec_name,channels:format=duration -of compact "$OUT"
ffmpeg -hide_banner -i "$OUT" -af volumedetect -f null - 2>&1 | grep -E "max_volume|mean_volume"
