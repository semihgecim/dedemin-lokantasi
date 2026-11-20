import json,sys,re
n=int(sys.argv[1]);city=sys.argv[2]
SRC='/home/claude/dedemin-lokantasi.html'
A=json.load(open(f's2job/art_{n}.json'));IT=json.load(open(f's2img/{city}/items.json'));FA=json.load(open(f's2img/{city}/faces.json'))
s=open(SRC).read()
# 1) JOB text data right after const JOB line
tag1=f'/*S2JOB{n}*/'
line1=tag1+f'JOB[{n}]='+json.dumps(A['JOB'],ensure_ascii=False)+';\n'
s=re.sub(re.escape(tag1)+r'.*\n','',s)
i=s.index('\nconst JOB=');j=s.index('\n',i+1)+1;s=s[:j]+line1+s[j:]
# 2) art block before S2 placeholder loop
tag2=f'/*S2ART{n}*/'
G=dict(IT);G.update(FA)
line2=(tag2+f'JOB2[{n}]='+json.dumps(A['JOB2'],ensure_ascii=False)+f';JOBMASK2[{n}]='+json.dumps(A['M2'])+f';JOBMASK[{n}]='+json.dumps(A['M1'])+
 ';Object.assign(JOBIMG,'+json.dumps(A['IMG'])+');Object.assign(GIMG,'+json.dumps(G,ensure_ascii=False)+');\n')
s=re.sub(re.escape(tag2)+r'.*\n','',s)
k=s.index('CITY.filter(c=>c.s2).forEach(c=>{const n=c.n,X=STORY_S2[n]');s=s[:k]+line2+s[k:]
# 3) ready list
m=re.search(r'const S2_READY=\[([^\]]*)\];',s);L=[int(x) for x in m.group(1).split(',') if x.strip()]
if n not in L:L.append(n)
s=s[:m.start()]+'const S2_READY=['+','.join(map(str,sorted(L)))+'];'+s[m.end():]
open(SRC,'w').write(s);print('injected',n,len(line1)+len(line2))
