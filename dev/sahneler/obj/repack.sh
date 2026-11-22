set -e
python3 pack.py spec1.json once1.jpg clean1.jpg && python3 inject_keys.py 1 obj_1.json 1a_b.jpg
python3 pack.py spec2.json once2b.jpg clean2b.jpg && python3 inject_keys.py 2 obj_2.json 2a.jpg
python3 pack.py spec3.json once3a.jpg clean3m.jpg && python3 inject_obj.py 3 a obj_3.json
python3 pack.py spec3c.json once3c.jpg clean3c.jpg && python3 inject_obj.py 3 c obj_3c.json
python3 pack.py spec4.json once4.jpg clean4.jpg && python3 inject_obj.py 4 a obj_4.json
python3 pack.py spec4c.json once4c.jpg clean4c.jpg && python3 inject_obj.py 4 c obj_4c.json
python3 pack.py spec5.json 5once.jpg 5clean.jpg && python3 inject_obj.py 5 a obj_5.json
python3 pack.py spec5c.json once5c.jpg clean5c.jpg && python3 inject_obj.py 5 c obj_5c.json
python3 pack.py spec6.json once6a.jpg clean6m.jpg && python3 inject_obj.py 6 a obj_6.json
python3 pack.py spec6c.json once6c.jpg clean6c.jpg && python3 inject_obj.py 6 c obj_6c.json
python3 pack.py spec7.json once7.jpg clean7.jpg && python3 inject_obj.py 7 a obj_7.json
python3 pack.py spec7c.json once7c.jpg clean7c.jpg && python3 inject_obj.py 7 c obj_7c.json
python3 pack.py spec8.json once8.jpg clean8.jpg && python3 inject_obj.py 8 a obj_8.json
python3 pack.py spec8c.json once8c.jpg clean8c.jpg && python3 inject_obj.py 8 c obj_8c.json
