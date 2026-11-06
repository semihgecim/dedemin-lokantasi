const {JSDOM}=require("jsdom");const fs=require("fs");
const html=fs.readFileSync("/home/claude/dedemin-lokantasi.html","utf8");
const ch=+(process.argv[2]||1),steps=+(process.argv[3]||3000);
const dom=new JSDOM("<!doctype html><body>"+html+"</body>",{runScripts:"outside-only",pretendToBeVisual:true,url:"https://x.test/"});
const w=dom.window;w.__FAST=1;let errs=[];w.addEventListener("error",e=>errs.push(e.message));
if(ch>1){const L=ch===2?"kpm":"ABCDEFGHIJKLMNOPQRSTUVWX".substr((ch-3)*3,3);const b=Array(49).fill(null);b[44]={g:L[0]};b[45]={g:L[1]};b[46]={g:L[2]};
 const st={chapter:ch,board:b,stars:30,tdone:0,energy:60,eAt:Date.now(),restored:0,found:{},served:0,seenIntro:true,orders:[null,null,null]};st["intro"+ch]=true;
 w.localStorage.setItem("dedemin-lokantasi.v3",JSON.stringify(st));}
w.eval(html.slice(html.indexOf("<script>")+8,html.lastIndexOf("</script>")));
const d=w.document;const R=n=>Math.floor(Math.random()*n);
const ev=(el,t)=>{const e=new w.Event(t,{bubbles:true});e.clientX=0;e.clientY=0;el.dispatchEvent(e);};
const tap=i=>{const it=d.querySelector(`.item[data-i="${i}"]`);if(!it)return;ev(it,"pointerdown");ev(d,"pointerup");};
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{await sleep(20);let bad=0;
 for(let s=0;s<steps;s++){
  const a=R(20);
  try{
   if(a<9){const its=[...d.querySelectorAll(".item")].map(e=>+e.dataset.i);if(its.length)tap(its[R(its.length)]);}
   else if(a<11){const c=d.querySelectorAll(".cell")[R(49)];c&&c.click();}
   else if(a<13){const c=d.querySelectorAll(".cust")[R(3)];c&&c.click();}
   else if(a<14){d.getElementById("sell").click();}
   else if(a<16){d.getElementById("rBtn").click();await sleep(5);}
   else if(a<17){d.getElementById("questBtn").click();const b=[...d.querySelectorAll(".qbtn:not([disabled])")];if(b.length)b[0].click();const c=d.getElementById("closeQ");c&&c.click();}
   else if(a<18){d.getElementById("bookBtn").click();const c=d.getElementById("closeBook");c&&c.click();}
   else {const c=d.getElementById("closePage");if(c&&!d.getElementById("sheet").hidden)c.click();const t=d.getElementById("takeDaily");if(t&&!d.getElementById("sheet").hidden)t.click();}
  }catch(e){errs.push("throw "+e.message);}
  if(s%7===0)await sleep(1);
  const S=JSON.parse(w.localStorage.getItem("dedemin-lokantasi.v3"));
  if(!S)continue;const pr=[];if(S.board.length!==49)pr.push("board len");if(!Number.isFinite(S.stars)||S.stars<0)pr.push("stars "+S.stars);if(!Number.isFinite(S.energy)||S.energy<0)pr.push("energy "+S.energy);
  if(S.board.filter(x=>x&&x.g).length!==3)pr.push("gens "+S.board.filter(x=>x&&x.g).length);
  if(S.orders.length!==3)pr.push("orders len");
  S.board.forEach(x=>{if(x&&x.c&&!(x.l>=1))pr.push("bad lvl")});
  if(pr.length&&bad++<5)console.log("step",s,pr.join(","));
 }
 await sleep(50);const S=JSON.parse(w.localStorage.getItem("dedemin-lokantasi.v3"));
 console.log(`ch${ch}: steps ${steps} ch-now ${S.chapter} restored ${S.restored} stars ${S.stars} energy ${S.energy} nullOrders ${S.orders.filter(o=>!o).length} errs ${errs.length}`,errs.slice(0,5));process.exit(0);
})();
