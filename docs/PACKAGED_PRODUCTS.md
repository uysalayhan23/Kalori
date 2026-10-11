# Türkiye marketleri — paketli gıda aktarımı

## Amaç

BİM, A101, ŞOK, Migros, CarrefourSA ve diğer mağazalarda karşılaşılabilen atıştırmalık, tatlı, gofret, bisküvi, çikolata, cips, kraker, sütlü tatlı, içecek, kahvaltılık ve paketli yiyecekleri **ürün / marka / barkod** düzeyinde kaydetmek.

Hiçbir açık topluluk veritabanı, bu marketlerin **bütün güncel stoklarını** garanti etmez. Güncel market satışı resmi mağaza/etiket bilgisiyle ayrıca doğrulanmalıdır. `stores` alanı, Open Food Facts katılımcılarının bildirdiği geçmiş bilgi olabilir ve kesin satış iddiası değildir.

## Veri kaynağı ve lisans

Open Food Facts — https://world.openfoodfacts.org/data — veritabanı ODbL lisanslıdır. Veri atfı, veritabanı paylaşımı ve türetilmiş veritabanının aynı koşullarda paylaşılması için ODbL gerekliliklerine uyulmalıdır. Proje sahibi yayımlamadan önce lisans uyumluluğunu değerlendirmelidir. Etiketler kullanıcı katkılı olduğundan hata veya eski değerler içerebilir.

## Toplu aktarım

1. Open Food Facts tam TSV dışa aktarımını indirin. Aktarım oldukça büyük olabilir; Android APK içine doğrudan koymayın.
2. Python 3 ile yerel bilgisayarda, Actions çalıştırmadan:
   ```sh
   python tools/import_openfoodfacts.py --input en.openfoodfacts.org.products.csv --output packaged-foods.js --limit 15000
   ```
3. Çıktıyı kontrol edip `packaged-foods.js` dosyasına commit edin (`[skip ci]`).
4. Hem `foods.html` hem de `meal-builder.html`, `packaged-foods.js` dosyasını otomatik okur. İnternet bağlantısı gerekmez.
5. Çıktı boyutunu APK için değerlendirin; gelecek aşamada sıkıştırılmış SQLite/FTS veya bölgesel parçalar, barkod indeksleri ve güncelleme manifesti kullanılmalı.

## Kabul filtresi

- Türkiye etiketi ve 8–14 haneli barkod olmalı.
- Gerçek ürün adı ve `energy-kcal_100g` değeri bulunmalı.
- 100 g / 100 ml temeli ürüne göre ayrıca gözden geçirilmelidir.
- Makro alanları kaynakta yoksa `null` olur; sıfır varsayılmaz.
- Barkod ve Open Food Facts ürün sayfası saklanır; `verification=community_reported` kullanılır. **Topluluk kaydı, laboratuvar doğrulaması değildir.**
- Mağaza bilgisi varsa `reportedStores` içinde yalnız referans olarak tutulur; etiket üzerinde doğrulanmadıkça parantez içinde güncel satış yeri diye gösterilmez.
- Aynı ürünün farklı ambalaj, marka ve tarif varyantları barkodlarıyla ayrılır.
- Enerjisi bulunmayan veya tutarsız satırlar dışarıda bırakılır.

## Mevcut durum

`packaged-foods.js` şu anda **boş bir başlangıç dosyasıdır**. İçe aktarma aracı hazırdır ama gerçek dışa aktarım henüz indirilip işlenmedi. Dolayısıyla eklenmiş doğrulanmış market ürünü sayısı **0**; başlangıç 195 yemek/besin kaydı korunur.
