import json,re
F='/home/claude/dedemin-lokantasi.html'
h=open(F,encoding='utf8').read()
B=json.load(open('bodies.json'))
CODE=r'''// ---------- BODY v1: half-body customers standing on the scene strip
const BODY={};
/*BODYART*/
(function(){const st=document.createElement("style");st.textContent=`
.custhead .cust.body .pface,.boardscr .custhead .cust.body .pface{width:var(--bw,80px)!important;height:var(--bh,98px)!important;min-width:0!important;border-radius:0!important;box-shadow:none!important;background:none!important;overflow:visible!important;animation:bsway 3.2s ease-in-out infinite;transform-origin:50% 100%;margin-bottom:-10px}
.custhead .cust.body:nth-child(2) .pface{animation-delay:-1.1s}.custhead .cust.body:nth-child(3) .pface{animation-delay:-2.2s}
.custhead .cust.body .pface img{width:100%!important;height:100%!important;border-radius:0!important;object-fit:contain;object-position:50% 100%;filter:drop-shadow(0 4px 4px rgba(0,0,0,.35)) drop-shadow(0 0 2px #fff)}
.custhead .cust.body .pface:after,.custhead .cust.body .pface:before{display:none!important}
.custhead .cust.body{gap:0!important;position:relative}
.custhead .cust.body.ready .pface{animation:bhop .9s ease-in-out infinite}
.custhead .cust.body.ready .pface img{filter:drop-shadow(0 0 6px #35c46a) drop-shadow(0 0 3px #fff)}
.custhead .cust.body .bub{position:relative;z-index:3;margin-bottom:-6px}
.custhead .cust.body .hearts{bottom:6px}
@keyframes bsway{0%,100%{transform:rotate(-1.5deg)}50%{transform:rotate(1.5deg) translateY(-2px)}}
@keyframes bhop{0%,100%{transform:translateY(0)}40%{transform:translateY(-8px) scale(1.03,.98)}}
@media (prefers-reduced-motion:reduce){.custhead .cust.body .pface{animation:none!important}}`;document.head.appendChild(st);})();
{const _ro=renderOrders;renderOrders=function(){_ro.apply(this,arguments);const box=document.getElementById("orders");if(!box)return;
 box.querySelectorAll(".cust[data-i]").forEach(c=>{const o=S.orders[+c.dataset.i];if(!o)return;const b=BODY["body:"+o.p],f=c.querySelector(".pface");if(!b||!f)return;
  let im=f.querySelector("img");if(!im){f.textContent="";im=document.createElement("img");im.alt="";f.insertBefore(im,f.firstChild);}im.src=b;c.classList.add("body");});};}
'''
if '// ---------- BODY v1' not in h:
    i=h.index('function renderAll(){')
    h=h[:i]+CODE+h[i:]
line='/*BODYART*/Object.assign(BODY,'+json.dumps({'body:'+k:v for k,v in B.items()})+');'
h=re.sub(r'/\*BODYART\*/[^\n]*',lambda m:line,h,count=1)
open(F,'w',encoding='utf8').write(h);print(len(B))
