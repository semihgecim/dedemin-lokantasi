ffmpeg -v error -y -framerate 2 -pattern_type glob -i 'play_*.png' -vf "scale=720:-2,format=yuv420p" -c:v libx264 -preset veryfast -crf 23 /mnt/user-data/outputs/hatay-onarim.mp4
