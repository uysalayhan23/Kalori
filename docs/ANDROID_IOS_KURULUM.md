# Kalori — Android ve iPhone kurulumu

Her iki platformun ortak kaynakları depo kökündeki altı HTML sayfası, `kalori-ui.css`, `kalori-nav.js`, veri dosyaları ve PWA manifestidir. Her platformun **cihazdaki kayıt alanı ayrıdır**; otomatik senkronizasyon yoktur.

## Android: kurulabilir APK
- Mevcut Android uygulaması `android/` altındaki WebView projesidir.
- Güncel kaynaklardan **yeni APK üretmek gerekir**; önceki APK'lar son kaynak değişikliklerini içermez.
- Debug APK derlemek için Android SDK 35, Java 17, Gradle 8.9 ve Android Gradle Plugin 8.7.3 gerekir.
- Daha önce başarıyla oluşturulan bir APK, yalnızca derlendiği commit'teki ekranları içerir.
- Android için de HTTPS üzerinden yayımlanan PWA, destekleyen tarayıcılarda ana ekrana eklenebilir.

## iPhone / iPad: bilgisayarsız web uygulaması
- Bu, App Store'daki yerel Swift/IPA uygulaması **değildir**. Mac/Xcode olmadan kullanılabilecek PWA sürümüdür.
- Depo henüz canlı yayımlanmamışsa HTTPS yayımı gerekir. Beklenen GitHub Pages adresi `https://uysalayhan23.github.io/Kalori/` şeklindedir; **Pages etkinleşmeden bu adresin çalıştığı varsayılmamalıdır**.
- GitHub deposunda **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: main → Folder: /(root) → Save** yoluyla yayın yapılabilir.
- **Dikkat:** GitHub Pages, `Deploy from a branch` seçilse bile bir GitHub Actions dağıtım çalışması başlatır. Kullanıcı Actions'a ayrıca izin vermedikçe yayımlama etkinleştirilmemelidir.
- Site yayımlandıktan sonra iPhone'da Safari ile açın. Paylaş menüsü → **Ana Ekrana Ekle** → **Web Uygulaması Olarak Aç** → **Ekle**.
- Kalori simgesi Ana Ekrana gelir. İlk ziyaret internete ihtiyaç duyar; sonrasında uygulama kabuğu Service Worker önbelleğinde saklanır. Bağlantı veya depolama durumuna göre bazı özellikler kısıtlanabilir.
- iPhone'da JSON dosya dışa aktarma/geri yükleme ve çevrimdışı kullanım **gerçek cihazda henüz test edilmedi**.

## Verileri koruma
- Android APK ve iPhone PWA'nın yerel veri alanları birbirinden bağımsızdır. Önceki APK'daki kayıtlar iPhone'a otomatik taşınmaz.
- Kayıtları taşımanın yolu eski cihazdan **JSON dışa aktar** ve yeni cihazda **Yedekten geri yükle** işlevleridir; ilk kullanım öncesi iOS'ta dosya seçiminin gerçekten çalıştığını test edin.
- Tarayıcı/site verilerinin silinmesi, uygulamanın kaldırılması veya depolama temizliği günlükleri silebilir. Düzenli JSON yedeği alın.
- GitHub Pages'de kaynaklar kamuya açık olacak, ancak günlük verileri sunucuya gönderilmek üzere tasarlanmamıştır; günlükler cihazda saklanır.
- Uygulama medikal öneri veya besin hedefi belirlemek için tasarlanmamıştır.

## Gelecekte yerel iOS IPA
- App Store/TestFlight sürümü için ayrı iOS Xcode hedefi, Apple imzalama ve uygun dağıtım şartları gerekir. Bu aşamada IPA üretilmemiştir.
