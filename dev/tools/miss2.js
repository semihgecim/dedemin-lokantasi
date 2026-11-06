const {JSDOM}=require("jsdom");const fs=require("fs");
let html=fs.readFileSync("/home/claude/dedemin-lokantasi.html","utf8");
let js=html.slice(html.indexOf("<script>")+8,html.lastIndexOf("</script>"));
const e=js.lastIndexOf("})");js=js.slice(0,e)+";window.__X={ART,CITY,EXT,LBL:typeof LABEL!=='undefined'?LABEL:null};"+js.slice(e);
const dom=new JSDOM("<!doctype html><body>"+html.replace(/<script>[\s\S]*<\/script>/,"")+"</body>",{runScripts:"outside-only",pretendToBeVisual:true,url:"https://x.test/"});
const w=dom.window;w.__FAST=1;w.eval(js);const X=w.__X;
const im=k=>String(X.ART[k]).includes("<img");
for(const C of X.CITY){const out=[];for(const ch in C.chains){const d=C.chains[ch];const it=d.items||[];it.forEach((x,i)=>{if(!im(ch+(i+1)))out.push(ch+(i+1)+" "+x[0])});const g=d.gen;if(g&&!im(g[0]))out.push(g[0]+" "+g[1]);}
 console.log(C.n,C.place,"| scene?",JSON.stringify(Object.keys(C)).includes("img"),"| missing:",out.join(", "));}
for(const c in X.EXT){const m=X.EXT[c].map((x,i)=>[c+(i+(c=="b"?5:6)),x[0]]).filter(([k])=>!im(k));if(m.length)console.log("EXT",c,m.map(a=>a.join(" ")).join(", "))}
console.log("ch2 nonimg:",["k1","k2","k3","k4","k5","p1","p2","p3","p4","p5","m1","m2","m3","m4","m5","gk","gp","gm"].filter(k=>!im(k)).join(" "));
console.log("k1",String(X.ART.k1).slice(0,150));console.log("A1",String(X.ART.A1).slice(0,150));process.exit();
