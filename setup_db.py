import sqlite3


conn = sqlite3.connect('menu.db')
# Cursor nesnesi: SQL komutları için
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


conn.commit()
conn.close()

print("Veritabanı ve tablo başarıyla oluşturuldu.")
