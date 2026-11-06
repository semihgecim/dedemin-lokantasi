import os
exec(open("/tmp/claude-0/-home-claude/c0d5230d-7105-5da4-b31a-134b6e127703/scratchpad/build_site.py").read().replace('open("/home/claude/dedemin-lokantasi/index.html","w",encoding="utf8").write(page); print("built")','PAGE=page'))
p=PAGE.replace('href="apple-touch-icon.png"','href="../apple-touch-icon.png"').replace('href="icon-192.png"','href="../icon-192.png"').replace('href="manifest.webmanifest"','href="manifest.webmanifest"')
p=p.replace('const KEY="dedemin-lokantasi.v3";','const KEY="dedemin-lokantasi.beta";').replace('content="Dedemin Lokantası"','content="Dedemin Beta"')
assert 'dedemin-lokantasi.beta' in p
os.makedirs("/home/claude/dedemin-lokantasi/beta",exist_ok=True)
open("/home/claude/dedemin-lokantasi/beta/index.html","w",encoding="utf8").write(p);print("beta built")
