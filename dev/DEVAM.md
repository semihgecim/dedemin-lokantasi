# Dedemin Lokantası · yeni sohbette devam notu

Bu klasör, oyunu yeni bir Claude sohbetinde kaldığı yerden sürdürmek için.
Yeni sohbette Claude'a şunu söyle: **"semihgecim/dedemin-lokantasi reposunu ekle ve dev/DEVAM.md dosyasını oku, oyuna devam edelim."**

## Dosyalar
- `dev/dedemin-lokantasi.html` → oyunun ASIL kaynak dosyası (tek dosya, HTML+JS). Değişiklikler burada yapılır.
- `index.html` (kök) → yayındaki oyun; `dev/tools/build_site.py` kaynaktan üretir. `beta/` → `dev/tools/night/build_beta.py`.
- Yayın: GitHub Pages → semihgecim.me/dedemin-lokantasi/ (main'e push = yayın).
- `dev/tools/` → test araçları (jsdom/playwright): `bot4.js N` (N. bölümü bot oynar), `botall.js`, `night/fuzz.js` (rastgele hata taraması), `night/mig.js` (eşimin gerçek kaydı açılıyor mu — her yayından önce MUTLAKA çalıştır), `gens.js` (üreteç görselleri sayfası).
- Araçlardaki dosya yolları eski oturuma göre yazılı (`/home/claude/...`, scratchpad); yeni oturumda yolları düzelt.
- `dev/gemini/` → Gemini'ye verilen eksik resim listeleri (1: 121 resim, 2: 134 resim) ve stil referansları (referans-yemek/malzeme/uretec/karakter.png).

## Kurallar (Semih'in istekleri)
- Doğrudan ana uygulamaya yayınla; büyük değişikliklerden önce haber ver. İzin için tekrar tekrar sorma.
- Telefon titremesin (titreşim kapalı).
- Yeni karakterlere isim vermesini Semih'ten iste; o isim koyana kadar tanımlayıcı isim kullan.
- Eşinin kaydını asla bozma (mig.js). Kayıt anahtarı `dedemin-lokantasi.v3`, yedek `.bak`.
- Resimleri her zaman ORİJİNALLERDEN işle (rembg isnet-general-use → alpha>128 kırp → 176 tuvale ölçekle, alttan 172 → webp q95). Tekrar tekrar sıkıştırma yapma.

## Oyunun durumu (7 Kasım 2026)
- 10 bölüm/şehir: Bursa, Antep, İzmir, Trabzon, Hatay, Konya, Kapadokya, Van, Mardin, İstanbul. Botla hepsi geçiliyor.
- 7x7 tahta, enerji 100, zincirler 8 seviye (6-8. seviyeler o bölümde baştan açık).
- Sipariş karışımı ORDER_MIX + görev başına en az 2 yüksek seviye sipariş.
- Altın kesesi: Çeyrek(1) → Yarım(3) → Tam(7) → Cumhuriyet altını(16) tahtada birleşir; baloncuk satın alma (1-3 altın) ya da patlat +1 enerji; 4 altın = +50 enerji; 8 altın = depoya +1 yer (max 8). İleride Play Store'da gerçek parayla satılabilir.
- Hatıra kutusu (kartpostal, hatıra eşyası, yerel lezzet) tamamen gerçek resimli.
- Üreteçler şehir başına kendi çizimleri (genArt); Gemini resimleri gelince değiştirilecek.

## Bekleyen işler
1. Semih Gemini'den resimleri (dev/gemini listeleri) gönderdikçe oyuna yerleştir. Aynı adlı malzemeler (Un 6 yerde, Et 4, Hamur 4, Şeker/Şerbet/Çay/Çay yaprağı 2'şer) tek resimle tüm yerlere konur; Süt/Yufka/Kazandibi/Keşkül/Tatlı tepsisi Bursa resimlerini kullanır.
2. 3-10. şehir dükkân sahneleri gelince, sahnedeki görev parçalarını (ağlar, kepenk, tabela, tente…) her resme ayrı ayrı oturt (Bursa/Antep'teki gibi). Deneme Van sahnesi stil olarak onaylandı.
3. Stil: yemek/eşya yarı gerçekçi boyalı, çizgisiz; karakterler ince kahverengi çizgili, krem daire içinde.

## Not (14 Kasım 2026)
- Tüm ürün/üreteç/karakter resimleri Gemini ile tamamlandı.
- Semih: "Boğaz ziyafeti" resmi biraz saçma (balığın yanında ayran ve çay olmaz); sonra yenisi istenecek.
- 3-10. şehir dükkân sahneleri oyuna yerleştirildi: `SCNIMG` (resimler) + `SCN` (her şehrin kapı/pencere/tabela/çatı koordinatları) + yeni `renderSceneCity`. Onarım parçaları bu koordinatlara göre oturur. Orijinal sahneler `dev/sahneler/`. 'Bacayı ör' görevi 'Bacanın kurumunu temizle' oldu (resimde baca zaten var).
- 15 Kasım 2026: 3-10. bölümlerde dükkân onarımı kaldırıldı. Her şehrin kendi "büyük işi" var (İzmir çay bahçesi, Trabzon tekne, Hatay mahalle sofrası, Konya düğün avlusu, Kapadokya balon, Van göl iskelesi, Mardin konak damı, İstanbul Karaköy iskelesi). `JOB[n]` = isim, kırpma merkezi (cx) ve 33 görev [ad, x, y, yarıçap] (1200x900 resim koordinatı). Sahne = harap resim + görev yapıldıkça o noktadan bitmiş resim açılır (`renderSceneCity`, SVG mask). Resimler `JOBIMG`, orijinaller `dev/sahneler/isler/`. Harita da gerçek Türkiye haritası (`MAPXY`).
- Sahne dönüşümü (15 Kasım akşam): her görev, önce/sonra resimlerinin FARK haritasından (diff) çıkarılan bir bölgeyi açar (`JOBMASK`, `JOBP` konumlar). Üretimi: scratchpad bi/clus3.py (kmeans, balon ve vapur tek parça). Görev animasyonunda yakınlaştırma (rzoom) iş sahnelerinde kapalı. Dar ekranda (rectc) müşteri şeridi yatay/kompakt, malzemeler --isz ile kareden taşabilir.
- Lokantam (15 Kasım): harita sayfasındaki düğmeden açılır. 20 hatıra = her şehrin 3. seviyesi + şehir sonu. Resimler dev/sahneler/lokanta (boş/dolu), maskeler dev/tools/lok.py ile. S.lok = görülen hatıra sayısı.
- Gizem: Asena (kırmızı defterli kız, Can Usta'nın torunu), 3-9. şehirlerde 2. ve 4. seviye konuşmalarında izleri; İstanbul sonu + son mektup 'Kırmızı mürekkep' 2. Sezon kancası. Asena Teyze adı Aybüke Teyze oldu.
- Ekonomi (15 Kasım): enerji dolumu 6 sn → 90 sn/enerji (MAXE 100), görev 40 → 50 yıldız. Bot Trabzon'u ~950 enerjiyle bitiriyor; bir şehir artık ~1-2 günlük oyun.
