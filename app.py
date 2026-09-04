# harcama-takip v1.1 — AI destekli dogal dil girisi (Groq API)

from dotenv import load_dotenv
import os
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

import json
import requests

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

    def en_ucuz(self):
        en_dusuk = self.harcamalar[0]
        for e in self.harcamalar:
            if e.fiyat < en_dusuk.fiyat:
                en_dusuk = e
        return en_dusuk

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
            pass

def kdv_ekle(fiyat, kategori):
    if kategori == "gıda":
        oran = 0.01
    elif kategori == "elektronik":
        oran = 0.20
    else:
        oran = 0.20
    return fiyat + (fiyat * oran)

def kur_bilgisi_al():
    try:
        yanit = requests.get(
            "https://api.frankfurter.app/latest?from=TRY&to=USD,EUR",
            timeout=5
        )
        yanit.raise_for_status()
        veri = yanit.json()
        return veri["rates"]
    except requests.exceptions.RequestException:
        return None

def ai_ile_harcama_cikar(cumle):
    if not GROQ_API_KEY:
        return None
    try:
        yanit = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "openai/gpt-oss-20b",
                "messages": [
                    {
                        "role": "system",
                        "content": "Kullanicinin yazdigi harcama cumlesinden urun adi, fiyat (sadece sayi, TL) ve kategori (gıda, elektronik veya diger) cikar. SADECE gecerli JSON dondur, baska hicbir aciklama ekleme. Format: {\"isim\": \"...\", \"fiyat\": 0.0, \"kategori\": \"...\"}"
                    },
                    {"role": "user", "content": cumle}
                ],
                "temperature": 0
            },
            timeout=10
        )
        yanit.raise_for_status()
        icerik = yanit.json()["choices"][0]["message"]["content"]
        veri = json.loads(icerik)
        if "isim" not in veri or "fiyat" not in veri or "kategori" not in veri:
            return None
        return veri
    except (requests.exceptions.RequestException, KeyError, json.JSONDecodeError, ValueError):
        return None

def manuel_giris():
    urun_adi = input("Ürün adı: ")

    try:
        fiyat = float(input("Fiyat (TL): "))
    except ValueError:
        print("Geçersiz fiyat, sayı girmen lazım. Tekrar dene.\n")
        return None

    if fiyat < 0:
        print("Fiyat negatif olamaz, tekrar dene.\n")
        return None

    gecerli_kategoriler = ["gıda", "elektronik", "diger"]
    kategori = input("Kategori (gıda/elektronik/diger): ")
    if kategori not in gecerli_kategoriler:
        print("Geçersiz kategori. Lütfen gıda, elektronik veya diger yaz.\n")
        return None

    return urun_adi, fiyat, kategori

def ai_giris():
    cumle = input("Ne aldığını anlat: ")
    veri = ai_ile_harcama_cikar(cumle)
    if veri is None:
        print("AI ile çıkarılamadı, elle giriş yapalım.\n")
        return None

    gecerli_kategoriler = ["gıda", "elektronik", "diger"]
    kategori = veri["kategori"] if veri["kategori"] in gecerli_kategoriler else "diger"
    return veri["isim"], veri["fiyat"], kategori

def main():
    tracker = ExpenseTracker()
    tracker.yukle()

    if tracker.harcamalar:
        print(f"Önceki kayıtlardan {len(tracker.harcamalar)} harcama yüklendi.\n")

    while True:
        devam = input("Ürün eklemek ister misin? (e/h): ")
        if devam == "h":
            break

        secim = input("Nasıl eklemek istersin? (1) Elle gir (2) Cümleyle anlat (AI): ")

        if secim == "2":
            sonuc = ai_giris()
            if sonuc is None:
                sonuc = manuel_giris()
        else:
            sonuc = manuel_giris()

        if sonuc is None:
            continue

        urun_adi, fiyat, kategori = sonuc
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
        print(f"En ucuz: {tracker.en_ucuz()}")

        print("\nKategoriye göre toplam:")
        for kat, toplam in tracker.summary_by_category().items():
            print(f"  {kat}: {toplam:.2f} TL")

        kurlar = kur_bilgisi_al()
        if kurlar:
            toplam_tl = tracker.total()
            print(f"\nGüncel kurla karşılığı:")
            print(f"  {toplam_tl * kurlar['USD']:.2f} USD")
            print(f"  {toplam_tl * kurlar['EUR']:.2f} EUR")
        else:
            print("\nDöviz kuru bilgisine şu an ulaşılamadı (internet yok ya da API cevap vermedi).")

if __name__ == "__main__":
    main()
