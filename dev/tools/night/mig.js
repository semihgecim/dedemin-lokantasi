const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
const ctx=await b.newContext({viewport:{width:412,height:892}});await ctx.route(/fonts\.(googleapis|gstatic)/,r=>r.abort());
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
// old-style save: mid chapter 2, coins era fields, no daily
await p.addInitScript(()=>{if(sessionStorage.getItem('seeded'))return;sessionStorage.setItem('seeded','1');const b=Array(49).fill(null);b[44]={g:"k"};b[45]={g:"p"};b[46]={g:"m"};b[20]={c:"k",l:3};b[21]={c:"p",l:2};
 localStorage.setItem("dedemin-lokantasi.v3",JSON.stringify({chapter:2,board:b,coins:120,stars:14,tdone:2,energy:40,eAt:Date.now(),restored:4,found:{k2:1,k3:1},served:80,seenIntro:true,intro2:true,orders:[{p:"torun",items:[{c:"k",l:2}]},{p:"nine",items:[{c:"p",l:2}]},{p:"kopek",items:[{c:"m",l:1}]}]}));});
await p.goto('file:///home/claude/dedemin-lokantasi/index.html');await p.waitForTimeout(1500);
const st=await p.evaluate(()=>({sheet:!document.getElementById("sheet").hidden,h3:(document.querySelector(".paper h3")||{}).textContent,lvl:document.getElementById("lvlTxt").textContent,r:document.getElementById("rName").textContent,stars:document.getElementById("stars").textContent}));
console.log(st);
if(st.sheet)await p.evaluate(()=>document.getElementById("takeDaily").click());
await p.evaluate(()=>document.getElementById("goBoard").click());await p.waitForTimeout(500);
console.log("items",await p.evaluate(()=>document.querySelectorAll(".item").length),"errors",errs);await b.close();})();
