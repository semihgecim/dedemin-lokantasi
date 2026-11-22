for s in 5c 5 6 8 10c 17 17c 18c 20 20c; do python3 labels2.py spec$s.json >/dev/null && python3 behind3.py spec$s.json 2>/dev/null | tail -1; done
python3 gem_fix.py 5c 21 520,540,1200,900 empty/e5c_p2.png
python3 gem_fix.py 5 17 266,400,930,900 empty/t5_g2.png
python3 gem_fix.py 6 20 265,490,1140,885 empty/t6_g2.png
python3 gem_fix.py 6 21 265,490,1140,885 empty/t6_g2.png
python3 gem_fix.py 8 9 270,200,930,900 empty/t8b_g1x.png
python3 gem_fix.py 10c 20 200,640,670,900 empty/t10c_g2.png
python3 gem_fix.py 17 20 675,530,1200,900 empty/t17_g3.png
python3 gem_fix.py 17c 23 705,585,1200,900 empty/t17c_g1.png
python3 gem_fix.py 18c 22 620,600,1190,900 empty/t18c_g3.png
python3 gem_fix.py 20 19 310,550,1030,900 empty/t20_g1.png
python3 gem_fix.py 20c 17 130,505,830,900 empty/t20c_g1.png
