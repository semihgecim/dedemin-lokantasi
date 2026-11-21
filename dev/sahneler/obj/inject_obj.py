# inject_obj.py <n> <scene a|c> obj.json
import sys,json,re
F='/home/claude/dedemin-lokantasi.html';h=open(F,encoding='utf8').read()
n=sys.argv[1];sc=sys.argv[2];O=json.load(open(sys.argv[3]))
bk=n+('b' if sc=='a' else 'd');ck=n+('e' if sc=='a' else 'f')
tagT=f'/*OBJT{n}{sc}*/';tagM=f'/*OBJM{n}{sc}*/'
# remove old
h=re.sub(r'\n/\*OBJT%s%s\*/[^\n]*'%(n,sc),'',h);h=re.sub(r'\n/\*OBJM%s%s\*/[^\n]*'%(n,sc),'',h)
if 'const OBJ1={}' not in h:
    h=h.replace('const JOBMASK={','const OBJ1={},OBJ2={};\nconst JOBMASK={',1)
if sc=='a':
    t=[[nm,p[0],p[1],120] for nm,p in zip(O['names'],O['pos'])]
    lineT=tagT+f'JOB[{n}].t='+json.dumps(t,ensure_ascii=False)+';'
    i=h.index('\n',h.index('/*S2JOB11*/'));h=h[:i+1]+lineT+'\n'+h[i+1:]
keys={f'mk:{n}{sc}_{k}':m for k,m in enumerate(O['masks']) if m}
arr='['+','.join(f'GIMG["mk:{n}{sc}_{k}"]||""' for k in range(len(O['masks'])))+']'
if sc=='a':
    lineM=tagM+'Object.assign(GIMG,'+json.dumps(keys)+');'+f'JOBMASK[{n}]={arr};Object.assign(JOBIMG,{{"{bk}": "{O["before"]}","{ck}": "{O["clean"]}"}});JOBP[{n}]='+json.dumps(O['pos'])+f';OBJ1[{n}]={{k:"'+O['k']+'"};'
else:
    lineM=tagM+'Object.assign(GIMG,'+json.dumps(keys)+');'+f'JOBMASK2[{n}]={arr};Object.assign(JOBIMG,{{"{bk}": "{O["before"]}","{ck}": "{O["clean"]}"}});JOB2[{n}].t='+json.dumps(O['names'],ensure_ascii=False)+';JOB2['+n+'].p='+json.dumps(O['pos'])+f';OBJ2[{n}]={{k:"'+O['k']+'"};'
i=h.index('\n',h.index('/*S2ART19*/'));h=h[:i+1]+lineM+'\n'+h[i+1:]
open(F,'w',encoding='utf8').write(h);print('ok',len(lineM)//1024,'KB')
