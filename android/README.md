# Kalori Android kaynak taslağı — APK build YASAK

Bu dizin Android WebView temelli **başlangıç kaynak iskeletidir**. Tamamlanmış/derlenmiş/cihazda test edilmiş Android uygulaması değildir.

- Android SDK, Gradle, Java 17 ve uygun Android Gradle Plugin sürümüyle ileride derlenebilir.
- Build/assemble/install/Actions çalıştırılması kullanıcı açık iznine kadar yasaktır.
- Statik dosyaları hazırlamak için proje kökünde `python tools/sync_android_assets.py` komutunu kullanın; bu komut derleme yapmaz.
- Android 8+ hedeflenmiştir (`minSdk 26`), ancak cihaz uyumluluğu **test edilmemiştir**.
- Dosyalar `file:///android_asset/index.html` üzerinden açılır. Service Worker güvenli bağlamı sağlamadığı için bu pakette çalışmaz; dosyalar zaten `assets` içinde çevrimdışıdır.
- WebView veri saklama davranışı ve Open Food Facts API'nin `file://` kaynağından CORS erişimi gerçek cihaz üzerinde test edilmelidir.
- Paket `applicationId=com.kalori.journal` sadece taslak olup yayınlama öncesi kesinleşmelidir.
- Uygulama içindeki görseller, ikonlar, ekran okuyucu davranışları, veri yedekleme, Android 15 edge-to-edge, hata yönetimi ve ağ izinleri için QA gerekir.
- Besin kaynakları henüz doğrulanmadığından sağlık açısından güvenilir bir sürüm olduğu iddia edilmez.
- Güvenlik: local HTML sayfalarında `file:` güvenlik sınırları sınırlıdır; uzak linkler harici tarayıcıda açılır. İçerik dışarıdan yüklenmeden yayınlanmamalıdır.
- GitHub Actions kullanılmaz; commitlerde `[skip ci]`.
