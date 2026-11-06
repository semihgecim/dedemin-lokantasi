// full play-through bot for the two-tier task system (jsdom, fast animations)
const {JSDOM}=require("jsdom");const fs=require("fs");
const html=fs.readFileSync(process.argv[3]||"/home/claude/dedemin-lokantasi.html","utf8");
const startCh=+(process.argv[2]||1);
const dom=new JSDOM("<!doctype html><body>"+html+"</body>",{runScripts:"outside-only",pretendToBeVisual:true,url:"https://x.test/"});
const w=dom.window;w.__FAST=1;let off=0;const rn=w.Date.now.bind(w.Date);w.Date.now=()=>rn()+off;
let errs=0;w.addEventListener("error",e=>{errs++;console.log("ERR",e.message)});
if(startCh>=2){const b=Array(49).fill(null);const pc=startCh-1,G={1:["f","s","b"],2:["k","p","m"]}[pc]||["A","B","C"];b[44]={g:G[0]};b[45]={g:G[1]};b[46]={g:G[2]};
 const st={chapter:pc,board:b,stars:0,tdone:0,coins:0,energy:30,eAt:Date.now(),restored:{1:5,2:8}[pc]||6,found:{},served:14,seenIntro:true,orders:[null,null,null]};st["intro"+pc]=true;
 if(pc>=3){const L="ABCDEFGHIJKLMNOPQRSTUVWX".substr((pc-3)*3,3);b[44]={g:L[0]};b[45]={g:L[1]};b[46]={g:L[2]};}
 w.localStorage.setItem("dedemin-lokantasi.v3",JSON.stringify(st));}
w.eval(html.slice(html.indexOf("<script>")+8,html.lastIndexOf("</script>")));
const d=w.document;const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const tap=i=>{const it=d.querySelector(`.item[data-i="${i}"]`);if(!it)return;const e1=new w.Event("pointerdown",{bubbles:true});e1.clientX=0;e1.clientY=0;it.dispatchEvent(e1);const e2=new w.Event("pointerup",{bubbles:true});e2.clientX=0;e2.clientY=0;d.dispatchEvent(e2);};
const closeSheet=()=>{const c=d.getElementById("closePage");if(!d.getElementById("sheet").hidden&&c){const t=d.querySelector(".paper h3").textContent;c.click();return t;}return null;};
(async()=>{
 await sleep(30);let t=closeSheet();const pages=[];if(t)pages.push(t);
 if(startCh>=2){d.getElementById("rBtn").click();await sleep(30);pages.push(closeSheet());await sleep(30);pages.push(closeSheet());}
 let unlocked=0,served=0,tasks=0,sold=0,rounds=0,gens;
 const stopLbl=startCh===10?"Hikâye tamamlandı":startCh+". bölüm tamam";
 while(rounds<6000){rounds++;
   const lbl=d.getElementById("rLbl").textContent; if(lbl.startsWith(stopLbl))break; {const SS=JSON.parse(w.localStorage.getItem("dedemin-lokantasi.v3")||"{}");if(SS.chapter>startCh){console.log("passed into next chapter");break;}}
   if(startCh===1&&d.getElementById("lvlTxt").textContent.includes("/8"))break;
   if(rounds%100===0)fs.appendFileSync("bot3.log",["r",rounds,d.getElementById("lvlTxt").textContent,"|",d.getElementById("rLbl").textContent,"| items",d.querySelectorAll(".item").length,"stars",d.getElementById("stars").textContent,"energy",d.getElementById("energy").textContent].join(" ")+"\n");
   off+=6000*3;
   gens=[...d.querySelectorAll(".item.gen")].map(e=>+e.dataset.i);
   for(const g of gens){tap(g);}
   const want={};[...d.querySelectorAll(".need")].forEach(n=>{want[n.dataset.k]=(want[n.dataset.k]||0)+1;});
   let merged=true;while(merged){merged=false;const items=[...d.querySelectorAll(".item:not(.gen):not(.locked)")].map(e=>({i:+e.dataset.i,k:e.className.match(/c-(\w)/)[1]+e.querySelector(".lv").textContent}));const seen={};
     const have={};items.forEach(x=>{have[x.k]=(have[x.k]||0)+1;});
     for(const x of items){if(want[x.k]&&have[x.k]<=want[x.k]+1)continue;if(seen[x.k]!==undefined){const before=d.querySelectorAll(".item").length;tap(seen[x.k]);tap(x.i);merged=d.querySelectorAll(".item").length<before;break;}seen[x.k]=x.i;}}
   let s2=0;while(d.querySelectorAll(".item").length>40&&s2<6){
     const want=new Set([...d.querySelectorAll(".need")].map(n=>n.className.match(/c-(\w)/)[1]+"|"+n.getAttribute("title")));
     const its=[...d.querySelectorAll(".item:not(.gen):not(.locked)")].map(e=>({i:+e.dataset.i,c:e.className.match(/c-(\w)/)[1],l:+e.querySelector(".lv").textContent}));
     const cnt={};its.forEach(x=>{const k=x.c+x.l;cnt[k]=(cnt[k]||0)+1;});
     // sell the lowest item that nobody wants and that has no merge partner
     const nm=(c,l)=>w.eval("void 0")||null;
     its.sort((a,b)=>a.l-b.l);
     const cand=its.find(x=>cnt[x.c+x.l]===1&&!want[x.c+x.l])||its.find(x=>!want[x.c+x.l])||its[0];
     tap(cand.i);d.getElementById("sell").click();s2++;sold++;}
   {const lk=[...d.querySelectorAll(".item.locked")].map(e=>({i:+e.dataset.i,k:e.className.match(/c-(\w)/)[1]+e.querySelector(".lv").textContent}));
    for(const L of lk){const f=[...d.querySelectorAll(".item:not(.gen):not(.locked)")].find(e=>e.className.match(/c-(\w)/)[1]+e.querySelector(".lv").textContent===L.k);if(f){tap(+f.dataset.i);tap(L.i);unlocked++;break;}}}
   for(const c of d.querySelectorAll(".cust.ready")){c.click();served++;}
   await sleep(5);
   const rb=d.getElementById("rBtn");if(!rb.disabled){rb.click();tasks++;await sleep(20);const pt=closeSheet();if(pt)pages.push(pt);}
 }
 console.log(`ch${startCh}: rounds ${rounds} served ${served} tasks ${tasks} sold ${sold} unlocked ${unlocked} locked-left ${d.querySelectorAll(".item.locked").length} | end: ${d.getElementById("rLbl").textContent} / ${d.getElementById("rName").textContent}`);
 console.log("pages:",pages.filter(Boolean).join(" > "));console.log("errors:",errs);process.exit(0);
})();
