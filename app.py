from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_menu_items():
    conn = sqlite3.connect('menu.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, isim, aciklama, fiyat, kategori, resim FROM menu_items")
    rows = cursor.fetchall()
    conn.close()

    menu_list = []
    for row in rows:
        menu_list.append({
            'id': row[0],
            'isim': row[1],
            'aciklama': row[2],
            'fiyat': row[3],
            'kategori': row[4],
            'resim': row[5]
        })
    return menu_list

@app.route("/")
def home():
    menuler = get_menu_items()
    return render_template("index.html", menuler=menuler)

@app.route("/menu")
def menu():
    menuler = get_menu_items()
    return render_template("menu.html", menuler=menuler)

if __name__ == "__main__":
    app.run(debug=True, port=5009)
