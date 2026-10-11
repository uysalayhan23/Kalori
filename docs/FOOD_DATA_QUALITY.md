# Besin Veritabanı Kalite Standardı (2026-10-11)

## Denetim sonucu

- 195 başlangıç besini; hepsi başlangıçta yaklaşık örnek kcal/100 g verisiyle eklenmiştir.
- Kaynak kayıt kimliği, birincil analiz belgesi, ölçüm belirsizliği veya aynı tarifin malzeme gramları yoktur.
- **0/195 tekil kayıt sayısal doğruluk bakımından doğrulanmıştır.**
- Aynı katalog iki HTML dosyasında kopyalanıyordu; `food-catalog.js` altında tekilleştirildi.
- Kütüphanenin var olması, her bir değerin doğrulandığı anlamına gelmez.

## Zorunlu kaynaklama ve kabul ölçütleri

`verification`: `unverified` | `source_matched` | `recipe_calculated` | `lab_verified`.

Bir kayda `source_matched` denmesi için **tekil bir gıda kaydı kimliği**, kaynak URL'si, erişim/yayın tarihi, gıda/tür ve çiğ/pişmiş eşleşmesi, 100 g yenebilir kısım temeli, enerji yöntemi ve makro besin değerleri belgelenmelidir.

Bir yöresel yemeğin `recipe_calculated` olabilmesi için tüm malzeme gramajları, çiğ/pişmiş verim faktörü, ilave yağ ve pişmiş toplam verim kaydedilmeli; enerji/makro hesaplaması izlenebilir olmalıdır. Tarif varyantları ayrı tutulmalıdır. `lab_verified` yalnız ilgili tarife ait laboratuvar kaydıyla kullanılabilir.

Eksik makrolar **null** kalır, sıfır doldurulmaz. `0 kcal` yalnız gerçekten sıfır olan besin için kullanılabilir. Alerjen verisi bilinmiyorsa `bilinmiyor` olmalı, `yok` olarak yorumlanmamalıdır. Kişiye özel enerji sınırlaması, bu verilerle otomatik üretilmemelidir.

## Kaynaklar ve hukuki uygunluk

1. USDA FoodData Central: https://fdc.nal.usda.gov/download-datasets/ . İndirilebilir Foundation Foods, SR Legacy ve diğer veri tipleri; tekil eşleşme ile aktarılmalı.
2. TürKomp: https://turkomp.tarimorman.gov.tr/useofdata . Verilerinin uygulamada kullanımı ve çoğaltılması lisans/izin hükümlerine tabidir; izin sağlanmadan toplu aktarım yapılmamalıdır.

## Eksik ve devam edecek işler

1. USDA veri setini indirip lisansı, veri tipini, enerji kodunu ve birimleri otomatik doğrulayan içe aktarıcı.
2. Temel gıdalar için iki aşamalı ad/işleme eşleştirmesi ve manuel örneklem QA.
3. Türk yemekleri için malzeme/verim kaynaklı tarif motoru ve sürümlü varyantlar.
4. Protein/yağ/karbonhidrat tamlığı, kaynak tarihi ve güvenilirlik durumuna göre kullanıcı ekranı.
5. Katalog testleri: benzersiz ID, aralık, null, çiğ/pişmiş, birimler, round-trip hesaplama, eski kayıtlarla uyumluluk.
6. Uygulama içinde bilinmeyen veya doğrulanmamış besin verilerinin tıbbi karar veya kısıtlayıcı hedef için kullanılmaması.

**Not:** %100'e yakın mutlak kalori doğruluğu yemeklerin tarif, porsiyon ve pişirme farklılıkları yüzünden garanti edilemez. Önemli hedefimiz her bir sonucun izlenebilirliği ve ölçüm belirsizliğinin açıkça gösterilmesidir.

GitHub Actions kullanmadan statik geliştirme; commitlerde [skip ci].
