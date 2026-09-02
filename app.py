# harcama-takip v0.1 — tek seferlik hesaplama
urun_adi = input("Ürün adı: ")
fiyat = float(input("Birim fiyat (TL): "))
adet = int(input("Adet: "))

ara_toplam = fiyat * adet
kdv = ara_toplam * 0.20
toplam = ara_toplam + kdv

print(f"\n--- Fiş ---")
print(f"{urun_adi} x{adet} = {ara_toplam:.2f} TL")
print(f"KDV (%20): {kdv:.2f} TL")
print(f"Toplam: {toplam:.2f} TL")