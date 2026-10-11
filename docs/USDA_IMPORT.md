# USDA veri aktarımı — tekrar üretilebilir, çevrimdışı işlem

Güvenilir bir kaynak kimliği olmayan yaklaşık besin değerleri **doğrulanmış değildir**. İlk 195 kayıt bu durumdadır. Kaynaklardan alınan tekil analizler de ev yemeklerinin tüm varyantlarının kesin değeri anlamına gelmez.

1. https://fdc.nal.usda.gov/download-datasets/ üzerinden güncel Foundation Foods veya uygun SR Legacy / FNDDS dosyasını indir.
2. USDA kayıt ayrıntılarını JSON olarak çıkar. Bu aşamada kaynak besin adını, pişirme durumunu, yenilebilir 100 g referansını incele.
3. Ayrı bir insan denetimli eşleştirme dosyası oluştur:
```json
{
  "123456": {
    "name_tr": "Örnek Türkçe gıda adı",
    "category": "Temel gıdalar",
    "preparation": "Çiğ / haşlanmış / fırınlanmış — kayda göre",
    "preparation_confirmed": true,
    "per_100g_confirmed": true
  }
}
```
Buradaki `123456` **sadece biçim örneğidir, doğrulanmış bir USDA kimliği değildir**.

4. `python tools/import_usda.py --foods downloaded_details.json --mapping reviewed_mappings.json --output verified-foods.json`.
5. Komut eksik makro, yanlış birim, yanlış tip, eksik hazırlanma eşleştirmesi veya eksik enerji değerinde hata ile durur. FDC'de enerji nutrient 2048/2047/1008 farklı veri türlerinde farklı olabilir; tek bir kodu varsayma.
6. Veriyi uygulamaya dahil etmeden önce insan tarafından örnekleme, belirsizlik, kimlik, gramaj ve çiğ/pişmiş eşleşmesi doğrulaması gerekir. Çıktı şu aşamada otomatik olarak uygulamaya yüklenmez.
7. Statik katalog testi: `node tests/catalog.test.cjs`. Actions kullanma.

Bir besin için kaynak bulunamıyorsa `unverified` kalmalı; veri yokluğu hiçbir zaman sıfıra çevrilmemeli.

Kaynak: https://fdc.nal.usda.gov/api-guide/ ve https://fdc.nal.usda.gov/Foundation_Foods_Documentation/
