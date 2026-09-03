# harcama-takip v0.3 — liste ve sözlüklerle veri modelleme

def kdv_ekle(fiyat, kategori):
    if kategori == "gida":
        oran = 0.01
    elif kategori == "elektronik":
        oran = 0.20
    else:
        oran = 0.20
    return fiyat + (fiyat * oran)


harcamalar = []  # her eleman bir dict olacak: {"isim":..., "fiyat":..., "kategori":...}

while True:
    devam = input("Ürün eklemek ister misin? (e/h): ")
    if devam == "h":
        break

    urun_adi = input("Ürün adı: ")
    fiyat = float(input("Fiyat (TL): "))
    kategori = input("Kategori (gida/elektronik/diger): ")

    fiyat_kdvli = kdv_ekle(fiyat, kategori)

    harcama = {"isim": urun_adi, "fiyat": fiyat_kdvli, "kategori": kategori}
    harcamalar.append(harcama)

    print(f"{urun_adi} eklendi: {fiyat_kdvli:.2f} TL\n")

if len(harcamalar) == 0:
    print("Hiç harcama eklenmedi.")
else:
    # list comprehension: her harcamanın fiyatını tek listede topla
    tum_fiyatlar = [h["fiyat"] for h in harcamalar]
    genel_toplam = sum(tum_fiyatlar)

    # en pahalı harcamayı bul
    en_pahali = harcamalar[0]
    for h in harcamalar:
        if h["fiyat"] > en_pahali["fiyat"]:
            en_pahali = h

    print("--- Özet ---")
    print(f"Toplam {len(harcamalar)} ürün, genel toplam: {genel_toplam:.2f} TL")
    print(f"En pahalı: {en_pahali['isim']} ({en_pahali['fiyat']:.2f} TL)")

    # set comprehension: tekrarsız kategori listesi
    kategoriler = {h["kategori"] for h in harcamalar}
    print("\nKategoriye göre toplam:")
    for kat in kategoriler:
        kat_toplam = sum(h["fiyat"] for h in harcamalar if h["kategori"] == kat)
        print(f"  {kat}: {kat_toplam:.2f} TL")