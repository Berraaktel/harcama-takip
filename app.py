# harcama-takip v0.2 — döngü, fonksiyon ve kategoriye göre KDV

def kdv_ekle(fiyat, kategori):
    if kategori == "gida":
        oran = 0.01
    elif kategori == "elektronik":
        oran = 0.20
    else:
        oran = 0.20
    return fiyat + (fiyat * oran)


genel_toplam = 0
urun_sayisi = 0

while True:
    devam = input("Ürün eklemek ister misin? (e/h): ")
    if devam == "h":
        break

    urun_adi = input("Ürün adı: ")
    fiyat = float(input("Fiyat (TL): "))
    kategori = input("Kategori (gida/elektronik/diger): ")

    fiyat_kdvli = kdv_ekle(fiyat, kategori)
    genel_toplam = genel_toplam + fiyat_kdvli
    urun_sayisi = urun_sayisi + 1

    print(f"{urun_adi} eklendi: {fiyat_kdvli:.2f} TL\n")

print(f"--- Özet ---")
print(f"Toplam {urun_sayisi} ürün, genel toplam: {genel_toplam:.2f} TL")