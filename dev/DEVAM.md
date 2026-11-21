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
- Yeni şehre geçerken yıldız ★100 ile sınırlı; fazlası 50 yıldız = 1 altın (en çok 12) olarak verilir (startChapter).

## 17 Kasım 2026 · Her şehre 2. büyük iş
- 3-10. şehirlerde 6 seviyeden sonra 4 seviye daha (6+6+7+8 = 27 görev). Sahne `JOB2[n]` (görev adları, açılma noktaları), maskeler `JOBMASK2`, resimler `JOBIMG[n+"c"]` (bitmiş) / `n+"d"` (harap). Kaynaklar `dev/sahneler/isler2/`, yüzler `dev/yuzler2/`. Üretim: scratchpad p2/ (clusA.py kmeans 26 küme, tasks2.py görev sırası, masks2.py, story2.py, build2.py → inject2.js).
- Hikâye (STORY2): sayfa bulunduktan sonra dede'nin o şehirde kaldığı ev/yer onarılır. Her şehre 4 kısa defter sayfası (sayfa 7-10), 1 konuşma (seviye 9 ortası), 1 yeni misafir (seviye 7'den sonra). Eski son sayfanın 'after' yazısı ikinci işi tanıtıyor; "N. bölüm" geçişi artık son sayfada.
- İstanbul 2. iş = Can Usta'nın Kuzguncuk köşkü; son sayfa kırmızı defter → 2. Sezon kancası.
- İSİMSİZ karakterler (Semih Play Store öncesi isim verecek): udcu (halanın torunu), yaylanine, hanci, bagdede, avanos (çömlekçinin kızı), veteriner, midyat (ustanın oğlu), kalfa (İstanbul eski kalfa, yüzü eklendi).

## 18 Kasım 2026 · Bulut kaydı + hızlı açılış
- Supabase projesi `dedemin-lokantasi` (ref yocwobzpekmeemsppztu, eu-central-1, org Sinav Arena). Tablo `saves(code pk, data jsonb, chapter, restored, build, updated_at)`, RLS açık, politika yok; erişim sadece `save_game(p_code,p_data,p_build)` ve `load_game(p_code)` RPC'leri (security definer). Kod: 10 harf, alfabe A-Z2-9 (I/O/0/1 yok), S.cloudId.
- İstemci: save() → cloudSoon() (30 sn gecikmeli, uzun aradan sonra 4 sn), sekme gizlenince keepalive ile push. Ayarlar (Defter > Ayarlar) bulut kodu, kopyala, "Buluttaki oyunu getir". Eski DL1 kodu "İnternetsiz yedek kod" altında.
- chapter/restored sütunları: oyuncuların nerede kaldığını görmek için (analitik).
- build_site.py artık sahne (JOBIMG \d+[a-d]) ve ürün (GIMG name:*) resimlerini img/<sha1>.webp dosyalarına çıkarıyor; index 11.9 MB → 4.6 MB. sw.js sadece /img/ isteklerini cache-first saklıyor.

## 20 Kasım 2026 · 2. Sezon iskeleti (Kırmızı Defter, şehir 11-20)
- Veri: dev/sezon2/cities1-4.py → gen.py → CITY_S2 / STORY_S2 / TO_S2 / MAPXY_S2 / JOBN_S2 (HTML'de CITY.push bloğunun hemen altında).
- Kapı: `S2_READY=[]` listesine şehir no eklenince o şehir oyuna girer. `?s2test` adresiyle hepsi geçici (S1 sahne) resimleriyle açılır, sadece test.
- S2 şehirlerinde 1. iş 27 görev (S2_TPL 3,4,4,5,5,6), 2. iş 27 görev (JOB2 mekanizması). Resimler gelince: JOB[n] (t: [ad,x,y,r] 26+1), JOBMASK[n], JOBIMG n a/b, JOB2[n] (t 27, p 26), JOBMASK2[n], JOBIMG n c/d; GIMG name:/face:/gen: anahtarları.
- Zincir harfleri AA..BD (iki harf). Kişi anahtarları benzersiz (amasyaogretmen vb.).
- İstanbul sonu: 11 varsa STORY2[10].end "Edirne'ye çağırıyor" olur, yoksa sezon sonu.

## Sezon 2 resim üretimi (Gemini, Chrome üzerinden) — 20 Kasım 2026
- Edirne (11) yayında. S2_READY=[11]. Araçlar: dev/sezon2/art/ (clus.py → tasks_<şehir>.py → build_city.py → proc_city.py → inject.py).
- Dosya adları: <şehir>-01..03 üreteç, 04..18 malzeme (zincir sırası), 19 hayvan; S1A/S1B/S2A/S2B sahne; Y1..Y4 yüz. "-NNb-" varsa onu kullanır.
- Safranbolu (12): sahneler + görev listeleri hazır (art_12.json), malzeme 01-08 + yüz Y1,Y2 hazır. Eksik: 09-19, Y3 (tarihçi), Y4 (safrancı nine). Gemini günlük sınırı doldu (~60 resim/gün).
- Yüz anahtarları: 13 elmaci,kayikci3,amasyaogretmen,keskekci · 14 cagci,hamamci,kayakci,emekliogretmen · 15 peynirci,kazci,arici2,coban · 16 cigkofteci,isotcu,baglamaci,siraci · 17 kebapci2,salgamci,bicibicici,pamukcu · 18 yagci,tostcu,kaptan,lorcu · 19 kaymakci,sucukcu,kaplicaci,degirmenci · 20 rizaoglu,rizatorun,muhtar,cirak2

### 21 Kasım durum (Gemini limiti 5 saatte bir ~40-60 resim)
- Yayında: 11 Edirne, 12 Safranbolu, 13 Amasya.
- Hazır: tüm yüzler (14-20), sahneler: erzurum, kars, adana, sanliurfa S2 (S1 çifti yeniden üretilecek: A ve B eşleşmiyor), ayvalik S1A/S1B/S2A.
- Görev listeleri hazır: tasks_erzurum, tasks_kars, tasks_adana (art_14/15/17.json üretildi).
- Malzeme: erzurum 01-08 hazır; 09'dan itibaren (qall2.json sırası) kaldı.
- Chrome: "Browser 2" (a3167c6d). Sekmeler: malzeme sohbeti 143732f4ee4a4e54, sahne sohbeti ae6560fb66d65662, yeni malzeme sohbeti 4f05a6cbbb495f89. __q4 + watchdog (__wd) kullan; sayfa yenilenirse ilk kaydı kontrol et.
