const {JSDOM}=require("jsdom");const fs=require("fs");
let html=fs.readFileSync("/home/claude/dedemin-lokantasi.html","utf8");
let js=html.slice(html.indexOf("<script>")+8,html.lastIndexOf("</script>"));
const e=js.lastIndexOf("})");js=js.slice(0,e)+";window.__X={ART,CH,CITY,EXT,PEOPLE,CHAPTERS};"+js.slice(e);
const dom=new JSDOM("<!doctype html><body>"+html.replace(/<script>[\s\S]*<\/script>/,"")+"</body>",{runScripts:"outside-only",pretendToBeVisual:true,url:"https://x.test/"});
const w=dom.window;w.__FAST=1;w.eval(js);const X=w.__X;
const out={items:{},img:{}};
for(const c in X.CH){X.CH[c].items.forEach((it,i)=>{const k=c+(i+1);out.items[k]=it[1];out.img[k]=String(X.ART[k]).includes("<img");});}
out.city=X.CITY.map(C=>({n:C.n,place:C.place,chains:Object.fromEntries(Object.entries(C.chains).map(([c,d])=>[c,{gen:d.gen[1],items:d.items.map(x=>[x[0],x[4]])}])),people:Object.keys(C.people)}));
fs.writeFileSync("md/data.json",JSON.stringify(out));process.exit();
