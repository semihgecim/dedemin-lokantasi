const {JSDOM}=require("jsdom");const fs=require("fs");
let html=fs.readFileSync("/home/claude/dedemin-lokantasi.html","utf8");
let js=html.slice(html.indexOf("<script>")+8,html.lastIndexOf("</script>"));
const e=js.lastIndexOf("})");js=js.slice(0,e)+";window.__X={ART,CITY,GEN_OF};"+js.slice(e);
const dom=new JSDOM("<!doctype html><body>"+html.replace(/<script>[\s\S]*<\/script>/,"")+"</body>",{runScripts:"outside-only",pretendToBeVisual:true,url:"https://x.test/"});
const w=dom.window;w.__FAST=1;w.eval(js);const X=w.__X;
let out='<html><body style="background:#eef3f3;font:12px sans-serif;margin:8px"><div style="display:grid;grid-template-columns:repeat(6,110px);gap:6px">';
for(const C of X.CITY)for(const c in C.chains)out+=`<div style="text-align:center;background:#fff;border-radius:10px;padding:4px"><div style="width:90px;height:90px;margin:auto">${X.ART["g"+c].replace("<svg ",'<svg width="90" height="90" ').replace("<img ",'<img style="width:90px;height:90px;object-fit:contain" ')}</div>${C.place}<br>${X.GEN_OF[c]}</div>`;
fs.writeFileSync("gens.html",out+"</div></body></html>");process.exit();
