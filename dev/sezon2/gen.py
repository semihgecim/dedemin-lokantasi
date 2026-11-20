import json
exec(open('cities1.py').read());exec(open('cities2.py').read());exec(open('cities3.py').read());exec(open('cities4.py').read())
def pg(t):
  d={'title':t[0],'date':t[1]}
  if len(t)>2 and t[2]:d['note']=t[2]
  if len(t)>3:d['hand']=t[3]
  if len(t)>4 and t[4]:d['after']=t[4]
  return d
out=[];st={};to={};xy={};jn={}
for c in S2:
  n=c['n']
  ppl={}
  for k,v in c['people'].items():
    o={'name':v[0],'col':v[1],'likes':v[2],'ask':v[3],'thanks':v[4]}
    if len(v)>5 and v[5]:o['pet']=True
    ppl[k]=o
  out.append({'n':n,'s2':1,'place':c['place'],'book':"Can Usta'nın kırmızı defteri",'sign':c['place'].upper(),'open':c['job1'],'theme':{},'fill':{},
    'chains':{k:{'name':v[0],'gen':list(v[1]),'items':[list(i) for i in v[2]]} for k,v in c['chains'].items()},
    'people':ppl,'hello':c['hello'],'pages':[pg(p) for p in c['pages']],'dlg':{str(k):[{'p':a,'t':b} for a,b in v] for k,v in c['dlg'].items()},'job1':c['job1']})
  w=c['who'];st[n]={'a6':c['a6'],'end':c['end'],'p':[pg(p) for p in c['p2']],'dlg':[{'p':a,'t':b} for a,b in c['dlg2']],
    'who':{'k':w[0],'name':w[1],'col':w[2],'likes':w[3],'ask':w[4],'thanks':w[5]}}
  to[n]=c['to'];xy[n]=c['xy'];jn[n]=[c['job1'],c['job2']]
js="\n// ===== 2. SEZON: Kırmızı Defter (şehirler 11-20) =====\n"
js+="const CITY_S2="+json.dumps(out,ensure_ascii=False)+";\n"
js+="const STORY_S2="+json.dumps(st,ensure_ascii=False)+";\n"
js+="const TO_S2="+json.dumps(to,ensure_ascii=False)+",MAPXY_S2="+json.dumps(xy)+",JOBN_S2="+json.dumps(jn,ensure_ascii=False)+";\n"
open('s2data.js','w').write(js);print(len(js)//1024,'KB')
