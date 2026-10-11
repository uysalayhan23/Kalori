# Open Food Facts: ilk 85 kayıt — içe aktarım kalite notları

Tarih: 2026-10-11. `packaged-foods.js` içindeki 85 kayıt, kullanıcının bilgisayarında OFF API Türkiye sorgusuyla elde edilip bu repoya aktarılmıştır.

- 85 ürün, 85 farklı barkod; `store` alanı tüm kayıtlarda boştur. `reportedStores` OFF topluluk verisidir, güncel mağaza stok onayı değildir.
- 84 kayıtta protein/yağ/karbonhidrat alanları doldurulmuş, bir kayıt eksiktir. Dolu olması bilgilerin bilimsel olarak doğrulandığı anlamına gelmez.
- Enerji/besin miktarı alanı tüm ürünlerde `100 g or 100 ml (verify product type/label)` biçiminde **belirsizdir**. Sıvılarda gram ve mililitreyi eşdeğer varsaymak doğru değildir.
- `verification: community_reported` korunmalıdır. Ürünleri tekil ambalaj etiketleriyle karşılaştırmadan `verified` olarak işaretleme.

## Manuel inceleme gereken örnekler

| Barkod | Ürün | Sorun |
|---|---|---|
| `8680908020014` | Indo Mie Körili Paket Noodle | 212 kcal bildirimi ile (10 g protein, 18 g yağ, 64 g karbonhidrat) makrolarının yaklaşık 458 kcal enerjiye karşılık gelmesi arasında büyük fark var. Pişmiş/kuru ölçüm temeli kontrol edilmeli. |
| `8691641529016` | Fiskobirlik Nuga | 685,714 kcal bildirimi ile makrolardan hesaplanan yaklaşık 546 kcal arasında büyük fark var. |
| `18921102` | Kuru İncir (Amigo) | 597 kcal ve %51,5 yağ kaydı, kuru incir adıyla uyuşmayabilir; ürün kimliği/etiketi araştırılmalı. |
| `1500144801659` | Uludağ Limonata | `quantity` alanı `60₺`; ürün miktarı olarak kullanılamaz. |
| `5000112664478` | Coca-Cola 330mk | `carbs: 35` değeri, `kcal: 42` ile aynı 100 birimi kullanıyor görünmüyor; paket toplamı/100 ml ayrımı doğrulanmalı. |
| `80176800` | Nutella 750 G | Ürün adında 750 G, miktar alanında 1000g yazıyor; çelişki. |

**Bu kayıtların hiçbirinin besin değeri bu notla düzeltilmiş sayılmaz.** Kaynak ambalaj belgesi olmadan sayı değiştirme, alerjen güvenliği ya da güncel market bulunabilirliği iddia etme.

## Kalan yayın öncesi koşullar

1. Bu şüpheli kayıtları ve kalan ürünleri üretici ambalajı ya da güvenilir tekil kaynakla denetle.
2. Sıvıların ölçüm birimi ve besinlerin kuru/pişmiş esasını düzelt.
3. Önceki 195 yaklaşık yiyeceğin kaynak bazında doğruluğunu ayrı incele.
4. Android cihazda arayüz, saklama ve çevrimdışı işlevleri test et.
5. APK build ve GitHub Actions kullanıcıdan açık izin alınana kadar çalıştırma.
