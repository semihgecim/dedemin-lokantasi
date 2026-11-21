# inject_keys.py <ch> obj.json  (LV<ch> levels; images 'before','clean' + after file)
import sys,json,re,io,base64
from PIL import Image
F='/home/claude/dedemin-lokantasi.html';h=open(F,encoding='utf8').read()
n=sys.argv[1];O=json.load(open(sys.argv[2]));after=sys.argv[3]
h=re.sub(r'\n/\*OBJL%s\*/[^\n]*'%n,'',h);h=re.sub(r'\n/\*OBJK%s\*/[^\n]*'%n,'',h)
N=O['names'];K=[f'o{n}_{i}' for i in range(len(N))]
lineL=f'/*OBJL{n}*/(()=>{{const N='+json.dumps(N,ensure_ascii=False)+',K='+json.dumps(K)+f';let i=0;LV{n}.forEach(L=>L.tasks.forEach(t=>{{t.n=N[i];delete t.r;t.a=K[i];i++;}}));}})();'
i=h.index('\n',h.index('];',h.index(f'const LV{n}=[')));h=h[:i+1]+lineL+'\n'+h[i+1:]
A=Image.open(after).convert('RGB').resize((1200,900));b=io.BytesIO();A.save(b,'WEBP',quality=84);ad='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
keys={f'mk:{n}o_{k}':m for k,m in enumerate(O['masks']) if m}
kind={K[i]:O['k'][i] for i in range(len(K))};pos={K[i]:O['pos'][i] for i in range(len(K))}
lineK=f'/*OBJK{n}*/Object.assign(GIMG,'+json.dumps(keys)+');'+f'Object.assign(JOBIMG,{{"{n}a": "{ad}","{n}b": "{O["before"]}","{n}e": "{O["clean"]}"}});'+f'OBJC[{n}]={{keys:'+json.dumps(K)+f',masks:Object.fromEntries('+json.dumps(K)+f'.map((k,i)=>[k,GIMG["mk:{n}o_"+i]||""])),kind:'+json.dumps(kind)+',pos:'+json.dumps(pos)+'};'
i=h.index('\n',h.index('/*S2ART19*/'));h=h[:i+1]+lineK+'\n'+h[i+1:]
open(F,'w',encoding='utf8').write(h);print('ok',len(lineK)//1024,'KB')
