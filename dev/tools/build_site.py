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
{head_part}</head>
<body>
{body_part}
</body>
</html>
'''
open("/home/claude/dedemin-lokantasi/index.html","w",encoding="utf8").write(page); print("built")
