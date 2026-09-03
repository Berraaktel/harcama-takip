# harcama-takip v0.4 — OOP: Expense ve ExpenseTracker sınıfları

class Expense:
    def __init__(self, isim, fiyat, kategori):
        self.isim = isim
        self.fiyat = fiyat
        self.kategori = kategori

    def __str__(self):
        return f"{self.isim}: {self.fiyat:.2f} TL ({self.kategori})"


class ExpenseTracker:
    def __init__(self):
        self.harcamalar = []  # Expense nesnelerini tutan liste

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


def kdv_ekle(fiyat, kategori):
    if kategori == "gıda":
        oran = 0.01
    elif kategori == "elektronik":
        oran = 0.20
    else:
        oran = 0.20
    return fiyat + (fiyat * oran)


tracker = ExpenseTracker()

while True:
    devam = input("Ürün eklemek ister misin? (e/h): ")
    if devam == "h":
        break

    urun_adi = input("Ürün adı: ")
    fiyat = float(input("Fiyat (TL): "))
    kategori = input("Kategori (gıda/elektronik/diger): ")

    fiyat_kdvli = kdv_ekle(fiyat, kategori)
    yeni_harcama = Expense(urun_adi, fiyat_kdvli, kategori)
    tracker.add_expense(yeni_harcama)

    print(f"{yeni_harcama}\n")

if len(tracker.harcamalar) == 0:
    print("Hiç harcama eklenmedi.")
else:
    print("--- Özet ---")
    print(f"Toplam {len(tracker.harcamalar)} ürün, genel toplam: {tracker.total():.2f} TL")
    print(f"En pahalı: {tracker.en_pahali()}")

    print("\nKategoriye göre toplam:")
    for kat, toplam in tracker.summary_by_category().items():
        print(f"  {kat}: {toplam:.2f} TL")