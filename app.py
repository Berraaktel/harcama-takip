# harcama-takip v0.5 — JSON kalıcılık ve hata yönetimi

import json

DOSYA_ADI = "harcamalar.json"


class Expense:
    def __init__(self, isim, fiyat, kategori):
        self.isim = isim
        self.fiyat = fiyat
        self.kategori = kategori

    def __str__(self):
        return f"{self.isim}: {self.fiyat:.2f} TL ({self.kategori})"

    def to_dict(self):
        return {"isim": self.isim, "fiyat": self.fiyat, "kategori": self.kategori}


class ExpenseTracker:
    def __init__(self):
        self.harcamalar = []

    def add_expense(self, expense):
        self.harcamalar.append(expense)

    def total(self):
        return sum(e.fiyat for e in self.harcamalar)

    def en_pahali(self):
        en_yuksek = self.harcamalar[0]
        for e in self.harcamalar:
            if e.fiyat > en_yuksek.fiyat:
                en_yuksek = e
        return en_yuksek

    def summary_by_category(self):
        kategoriler = {e.kategori for e in self.harcamalar}
        sonuc = {}
        for kat in kategoriler:
            sonuc[kat] = sum(e.fiyat for e in self.harcamalar if e.kategori == kat)
        return sonuc

    def kaydet(self):
        veri = [e.to_dict() for e in self.harcamalar]
        with open(DOSYA_ADI, "w") as dosya:
            json.dump(veri, dosya, ensure_ascii=False, indent=2)

    def yukle(self):
        try:
            with open(DOSYA_ADI, "r") as dosya:
                veri = json.load(dosya)
                for kayit in veri:
                    self.harcamalar.append(Expense(kayit["isim"], kayit["fiyat"], kayit["kategori"]))
        except FileNotFoundError:
            pass  # dosya hiç yoksa (ilk çalıştırma), boş başla, hata verme


def kdv_ekle(fiyat, kategori):
    if kategori == "gıda":
        oran = 0.01
    elif kategori == "elektronik":
        oran = 0.20
    else:
        oran = 0.20
    return fiyat + (fiyat * oran)


tracker = ExpenseTracker()
tracker.yukle()

if tracker.harcamalar:
    print(f"Önceki kayıtlardan {len(tracker.harcamalar)} harcama yüklendi.\n")

while True:
    devam = input("Ürün eklemek ister misin? (e/h): ")
    if devam == "h":
        break

    urun_adi = input("Ürün adı: ")

    try:
        fiyat = float(input("Fiyat (TL): "))
    except ValueError:
        print("Geçersiz fiyat, sayı girmen lazım. Tekrar dene.\n")
        continue

    if fiyat < 0:
        print("Fiyat negatif olamaz, tekrar dene.\n")
        continue

    kategori = input("Kategori (gıda/elektronik/diger): ")

    fiyat_kdvli = kdv_ekle(fiyat, kategori)
    yeni_harcama = Expense(urun_adi, fiyat_kdvli, kategori)
    tracker.add_expense(yeni_harcama)

    print(f"{yeni_harcama}\n")

tracker.kaydet()

if len(tracker.harcamalar) == 0:
    print("Hiç harcama eklenmedi.")
else:
    print("--- Özet ---")
    print(f"Toplam {len(tracker.harcamalar)} ürün, genel toplam: {tracker.total():.2f} TL")
    print(f"En pahalı: {tracker.en_pahali()}")

    print("\nKategoriye göre toplam:")
    for kat, toplam in tracker.summary_by_category().items():
        print(f"  {kat}: {toplam:.2f} TL")