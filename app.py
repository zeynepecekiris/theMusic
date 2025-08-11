from flask import Flask, render_template
import sqlite3
import socket
from gevent import monkey
monkey.patch_all()

app = Flask(__name__, static_folder='static')

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
    # Create and configure socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Verify port availability
        sock.bind(('0.0.0.0', 5011))
        sock.close()  # Close our test socket - Flask will create its own
        
        # Start Flask application
        app.run(host='0.0.0.0', port=5011, debug=True, use_reloader=False)
        
    except socket.error as e:
        print(f"Server could not start: {e}")
        print("Possible solutions:")
        print("1. Another application is using port 5011 - try a different port")
        print("2. Wait a few minutes and try again")
        print("3. Check with: lsof -i :5011")
    finally:
        # Ensure socket is always closed
        if 'sock' in locals():
            sock.close()
        app.run(host='0.0.0.0', port=5012, debug=False)