# Kalori — APK öncesi doğrulama ve kapanış kapıları

Tarih: 2026-10-11. Aktif repo `uysalayhan23/Kalori`, dal `main`.
**GitHub Actions asla çalıştırma. APK build için ayrı açık kullanıcı izni gerekir.**

## Uygulananlar
- Mobil uyumlu günlük ve öğün saatleri; geçmiş ve kısmi makro özetleri
- Çoklu yiyecekli öğün oluşturma, gramaj hesabı, günlük örnek menüler ve değiştirilebilir yiyecekler
- İsteğe bağlı kullanıcı profili ve ölçüm geçmişi
- Yiyecek kütüphanesinde marka, satış yeri, barkod, kişisel kayıt
- Barkoddan çevrimiçi OFF sorgulama, kullanıcı onayıyla çevrimdışı yerel kayıt
- 195 yaklaşık değerli başlangıç besini ve ortak katalog
- OFF ve USDA içe aktarma araçları; kaynak ve lisans metadata alanları
- Çevrimdışı statik ekran önbelleği ve web uygulaması manifesti
- Yerel test runner: `python tools/verify_pre_apk.py`

## Tamamlanmadan APK kabul edilemez
1. **Gerçek ürün verileri:** `packaged-foods.js` şu anda boş. Gerçek lisanslı Türkiye ürün veri seti indirilip kaynak/barkod/enerji/birim bazında denetlenmeli.
2. **Mevcut 195 kaydın doğrulanması:** Şu anda tekil USDA/TürKomp kaynak eşleşmesi yok. Reçete eşleşmeleri, yenilebilir kısım, pişmiş/çiğ ayrımı ve farklı tariflerin besin değerleri doğrulanmalı. Veri yoksa `unverified` kalmalı.
3. **Besin etiketleri:** Karışık 100 g/100 ml kayıtları, özellikle sıvılarda ayrı işaretlenip ölçü birimi değiştirilmeden matematiksel olarak kullanılmamalı.
4. **Özel diyet gereksinimleri:** Alerjen verisi yoksa kullanıcıya 'alerjensiz' denemez. VKİ'ye göre otomatik kalori kısıtlaması ya da ergenler için makro hedefleri yapılmaz; klinik gereksinimlerde uzman desteği gerekir.
5. **Uçtan uca QA:** Yerel testler, Android Chrome PWA/HTML davranışı, çevrimdışı çalışma, barkod API engelleri, veri saklama/backup geri yükleme, Türkçe erişilebilirlik ve ekran boyutları test edilmelidir.
6. **Android paketleme:** Henüz Android projesi, paket adı, imzalama, hedef SDK ve son APK sistemi tanımlanmadı. Build alınması yasaktır.
7. **Performans:** 5 MB JS veri bütçesi ve katalog binlerce satıra ulaştığında telefon üzerinde gerçek ölçüm gerekir. Büyük veritabanı için SQLite/FTS seçimi değerlendirilmeli.
8. **PWA:** Service worker yalnız HTTPS/localhost güvenli bağlamında çalışır; `file://` ile çalışmaz. Manifest için ikonlar ve cihaz kurulum QA'sı henüz yoktur.

## Yerel test (Actions değil)
```sh
python tools/verify_pre_apk.py
```
Python 3 zorunludur, Node.js varsa ayrıca JS syntax ve katalog testi yapılır. Testler bir cihazda veya yerel bilgisayarda çalıştırılana kadar 'PASSED' ilan edilemez.

## Veri lisansı ve gizlilik
Open Food Facts ODbL ve atıf/paylaşım yükümlülüklerini doğrula. TürKomp verilerini izin olmadan kitlesel kopyalama. Ürünlerin güncel BİM/A101/ŞOK/Migros/CarrefourSA stok durumlarını yalnız marka bilgisinden türetme. Yerel saklamanın güvenli yedekleme eksikleri giderilmelidir.

**Bu dokümanın varlığı APK öncesi tüm işlerin tamamlandığı anlamına gelmez.**
