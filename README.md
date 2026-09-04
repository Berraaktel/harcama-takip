# harcama-takip

Kişisel harcamaları takip eden, terminal üzerinden çalışan basit bir Python aracı. Python öğrenirken haftalık olarak geliştirdiğim bir proje — her sürüm, o hafta öğrendiğim bir konuyu (döngüler, fonksiyonlar, OOP, dosya işlemleri, test yazma) uyguluyor.

## Özellikler

- Ürün ekleme: isim, fiyat, kategori
- Kategoriye göre otomatik KDV hesaplama
- Harcamaları `harcamalar.json` dosyasında kalıcı olarak saklama
- Toplam, en pahalı ürün ve kategoriye göre özet gösterme
- Hatalı girdilerde (harf, negatif sayı) çökmeden uyarı verme
- `pytest` ile yazılmış birim testleri
- Döviz kuru API entegrasyonu (Frankfurter API üzerinden TRY→USD/EUR)

## Kurulum ve çalıştırma

\`\`\`
git clone https://github.com/Berraaktel/harcama-takip.git
cd harcama-takip
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
\`\`\`

## Örnek kullanım

\`\`\`
Ürün eklemek ister misin? (e/h): e
Ürün adı: kalem
Fiyat (TL): 200
Kategori (gida/elektronik/diger): kirtasiye
kalem: 240.00 TL (kirtasiye)

Ürün eklemek ister misin? (e/h): h
--- Özet ---
Toplam 1 ürün, genel toplam: 240.00 TL
En pahalı: kalem: 240.00 TL (kirtasiye)
\`\`\`

## Testleri çalıştırma

\`\`\`
pytest -v
\`\`\`

## Kullanılan teknolojiler

Python 3, `json`, `pytest`

## Sürüm geçmişi

- v0.1 — temel hesaplama
- v0.2 — döngü ve fonksiyonlarla çoklu ürün girişi
- v0.3 — liste ve sözlüklerle veri modelleme
- v0.4 — OOP: Expense ve ExpenseTracker sınıfları
- v0.5 — JSON kalıcılık ve hata yönetimi
- v0.6 — pytest testleri ve dokümantasyon
- v1.0 — requests kütüphanesiyle gerçek zamanlı döviz kuru API entegrasyonu (Frankfurter API), kategori girişi validasyonu, requirements.txt eklendi