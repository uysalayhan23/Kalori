# Kalori — Beslenme Günlüğü ve Planlayıcı

Türkçe, mobil uyumlu, ilk sürümü internet olmadan kullanılabilen beslenme günlüğü.

## Çalıştırma
`index.html` dosyasını tarayıcıda açın. Kurulum, sunucu, GitHub Actions veya API anahtarı gerekmez.

## İlk sürüm
- Kahvaltı, öğle, akşam ve ara öğünlere yemek ekleme
- Besin başına enerji (kcal), protein, karbonhidrat ve yağ bilgisini isteğe bağlı kaydetme
- Tarihe göre öğün günlüğü; kayıt silme
- Su içme hatırlatma amacıyla gün içi bardak kaydı
- Yedi günlük dengeli öğün fikirleri (sabit örnekler)
- Verileri yalnızca cihazdaki `localStorage` içinde tutma ve JSON dışa aktarma

## Ürün ilkeleri
- Kalori sayısı hedef, limit veya başarı puanı değildir; yalnızca isteğe bağlı besin bilgisidir.
- Kilo, yaş, boy veya kilo verme hedefi istemez; otomatik enerji kısıtlaması yapmaz.
- Haftalık plan bir tıbbi diyet değil, düzenli ve çeşitli beslenmeye yönelik örnek fikirlerdir.
- Alerji, hastalık ya da özel gereksinimler için uzman değerlendirmesi gerekir.
- Bulut senkronizasyonu, doğrulanmış besin veri tabanı, barkod ve fotoğraf tanıma **henüz yok**.
- Saklama cihaz/tarayıcıya özeldir; tarayıcı verisi temizlenirse kayıtlar silinir. Dışa aktarılan JSON dosyasını güvenli saklayın.

## Yol haritası
1. PWA ve IndexedDB
2. Doğrulanmış besin veritabanı, porsiyon ölçüleri, kaynak gösterimi
3. Alerji ve beslenme tercihleriyle filtrelenen planlayıcı
4. İsteğe bağlı hesap/senkronizasyon, gizlilik ve veri silme kontrolleri
5. Erişilebilirlik ve otomatik testler

Geliştirme: normal GitHub akışı; Actions çalıştırılmadan, commitlerde [skip ci].
