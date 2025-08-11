import sqlite3


conn = sqlite3.connect('menu.db')
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS menu_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isim TEXT,
    aciklama TEXT,
    fiyat REAL,
    kategori TEXT,
    resim TEXT
)
""")
sample_data = [
    ("Anago Sweet Glaze", "Tatlı yılan balığı sosuyla kaplanmış eşsiz bir lezzet.", 42342.0, "salatalar, içecekler, tatlılar, ana yemek, atıştırmalık", "static/stock-photo-japanese-cuisine-anago-oshizushi-wiki-with-sweet-sauce-for-gourmet-lunch-image-142904026.jpg"),
    ("Bluefin Otoro", "Mavi yüzgeçli ton balığının en değerli kısmı, yumuşacık dokusuyla.", 213234.0, "salatalar, içecekler, tatlılar, ana yemek, atıştırmalık", "bluefin.png"),
    ("Engawa Flame Kissed", "Izgara halibut kanadı, ateşle öpülmüş gibi aromatik bir tat.", 232234.0, "salatalar, içecekler, tatlılar, ana yemek, atıştırmalık", "engawa.png"),
    ("Sayori Elegance", "İnce yapılı sayori balığının zarif sunumu.", 23423.0, "salatalar, içecekler, tatlılar, ana yemek, atıştırmalık", "sayori.png"),
    ("Shiro Ebi Symphony", "Tatlı beyaz karidesin dengeli ve narin lezzeti.", 23234.0, "salatalar, içecekler, tatlılar, ana yemek, atıştırmalık", "shiroebi.png"),
    ("Uni & Caviar Nigiri", "Deniz kestanesi ve havyarın mükemmel birleşimi.", 34234.0, "salatalar, içecekler, tatlılar, ana yemek, atıştırmalık", "uni.png")
]


cursor.executemany("""
INSERT INTO menu_items (isim, aciklama, fiyat, kategori, resim)
VALUES (?, ?, ?, ?, ?)
""", sample_data)


conn.commit()
conn.close()

print("Veritabanı ve tablo başarıyla oluşturuldu.")
