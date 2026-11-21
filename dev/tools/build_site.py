import time
B=str(int(time.time()))
h=open("/home/claude/dedemin-lokantasi.html",encoding="utf8").read()
i=h.index('<div class="app"'); head_part=h[:i].replace('<meta name="claude:viewport-fit-sides" content="cover">\n',''); body_part=h[i:]
page=f'''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Dedemin Lokantası">
<meta name="theme-color" content="#10302a">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" type="image/png" href="icon-192.png">
<link rel="manifest" href="manifest.webmanifest">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0;font:14px system-ui,sans-serif}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
<script>window.__BUILD="{B}";</script>
{head_part}</head>
<body>
{body_part}
<script>(function(){{function chk(){{try{{fetch("version.txt?u="+Date.now(),{{cache:"no-store"}}).then(function(r){{return r.ok?r.text():""}}).then(function(t){{t=(t||"").trim();if(/^\d+$/.test(t)&&t!==window.__BUILD){{var k="upd"+t;try{{if(sessionStorage.getItem(k))return;sessionStorage.setItem(k,1);}}catch(e){{}}location.replace(location.pathname+"?v="+t);}}}}).catch(function(){{}});}}catch(e){{}}}}
setTimeout(chk,1500);document.addEventListener("visibilitychange",function(){{if(document.visibilityState==="visible")chk();}});}})();</script>
</body>
</html>
'''
# --- hızlı açılış: büyük resimleri ayrı dosyalara taşı (sahneler + ürün resimleri) ---
import re,base64,hashlib,os
IMGD="/home/claude/dedemin-lokantasi/img";os.makedirs(IMGD,exist_ok=True);used=set()
def ext(m):
    key,typ,b64=m.group(1),m.group(2),m.group(3);raw=base64.b64decode(b64)
    fn=hashlib.sha1(raw).hexdigest()[:16]+"."+("webp" if typ=="webp" else typ);used.add(fn)
    fp=os.path.join(IMGD,fn)
    if not os.path.exists(fp):open(fp,"wb").write(raw)
    return '"%s": "img/%s"'%(key,fn)
page=re.sub(r'"(\d+[a-d]|name:[^"]{1,60}|body:[a-z0-9]{1,30})": "data:image/(webp|png|jpeg);base64,([A-Za-z0-9+/=]+)"',ext,page)
for f in os.listdir(IMGD):
    if f not in used:os.remove(os.path.join(IMGD,f))
sw='''const C="dl-img-v1";
self.addEventListener("install",e=>self.skipWaiting());
self.addEventListener("activate",e=>e.waitUntil(self.clients.claim()));
self.addEventListener("fetch",e=>{const u=new URL(e.request.url);if(e.request.method!=="GET"||!u.pathname.includes("/img/"))return;
 e.respondWith(caches.open(C).then(c=>c.match(e.request).then(r=>r||fetch(e.request).then(n=>{if(n.ok)c.put(e.request,n.clone());return n;}))));});
'''
open("/home/claude/dedemin-lokantasi/sw.js","w").write(sw)
page=page.replace("</body>",'<script>if("serviceWorker" in navigator&&location.protocol==="https:")navigator.serviceWorker.register("sw.js").catch(function(){});</script>\n</body>',1)
open("/home/claude/dedemin-lokantasi/index.html","w",encoding="utf8").write(page); open("/home/claude/dedemin-lokantasi/version.txt","w").write(B+"\n"); print("built")
