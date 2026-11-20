import re,json
md=open('gemini/sezon2-kalan-sehirler.md').read()
exec(open('sezon2/cities1.py').read());exec(open('sezon2/cities2.py').read());exec(open('sezon2/cities3.py').read());exec(open('sezon2/cities4.py').read())
C={c['n']:c for c in S2}
secs=re.split(r'\n## (\d+) · ',md)
P={}
for i in range(1,len(secs)-1,2):
  n=int(secs[i]);body=secs[i+1]
  q=re.findall(r'^\s*\d+\.\s*(?:\d\. iş [AB]: )?`([^`]+)`',body,re.M)
  P[n]=q
for n,q in P.items():
  c=C[n];ch=list(c['chains'].items());ppl=[k for k,v in c['people'].items() if not (len(v)>5 and v[5])];pet=[k for k,v in c['people'].items() if len(v)>5 and v[5]]
  print(n,c['place'],len(q),'gens',[v[1][1] for k,v in ch],'people',ppl,'who',c['who'][0],'pet',pet)
json.dump(P,open('/tmp/claude-0/-home-claude/c0d5230d-7105-5da4-b31a-134b6e127703/scratchpad/s2job/prompts.json','w'),ensure_ascii=False)
