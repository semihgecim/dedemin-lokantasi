for s in 1 2 3 3c 4 4c 5 5c 6 6c 7 7c 8 8c 9 9c 10 10c 11 11c 12 12c 13 13c 14 14c 15 15c 16 16c 17 17c 18 18c 19 19c 20 20c; do
python3 labels2.py spec$s.json >/dev/null 2>&1 && python3 behind3.py spec$s.json 2>/dev/null | tail -1 || echo "$s FAIL"
done
echo ALLDONE
