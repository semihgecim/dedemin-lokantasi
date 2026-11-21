import json,sys
P=json.load(open('s2job/prompts.json'));n,city=sys.argv[1],sys.argv[2]
q=P[n];L=[[q[i],f'{city}-{i+1:02d}.png'] for i in range(18)]+[[q[24],f'{city}-19.png']]
print(json.dumps(L,ensure_ascii=False))
