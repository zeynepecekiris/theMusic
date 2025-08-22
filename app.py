from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import socket
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Güvenlik için değiştirin

# Dosya yükleme ayarları
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Veritabanı bağlantısı
def get_db_connection():
    conn = sqlite3.connect('menu.db')
    conn.row_factory = sqlite3.Row
    return conn

# Veritabanını oluştur
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            aciklama TEXT,
            fiyat REAL NOT NULL,
            kategori TEXT,
            resim TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Dosya uzantısı kontrolü
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Admin giriş kontrolü
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def get_menu_items():
    conn = get_db_connection()
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

# Admin Panel Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            flash('Başarıyla giriş yapıldı!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Kullanıcı adı veya şifre hatalı!', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Çıkış yapıldı!', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    menu_items = conn.execute('SELECT * FROM menu_items ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('admin/dashboard.html', menu_items=menu_items)

@app.route('/admin/add', methods=['GET', 'POST'])
@admin_required
def admin_add_item():
    if request.method == 'POST':
        print("POST request received for adding item")
        print(f"Form data: {request.form}")
        print(f"Files: {request.files}")
        
        isim = request.form['isim']
        aciklama = request.form['aciklama']
        fiyat = request.form['fiyat']
        kategori = request.form['kategori']
        
        # Resim yükleme
        resim_filename = None
        if 'resim' in request.files:
            file = request.files['resim']
            print(f"File object: {file}")
            print(f"File filename: {file.filename}")
            
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                
                print(f"Secure filename: {filename}")
                print(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
                
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print(f"File path: {file_path}")
                
                file.save(file_path)
                resim_filename = filename
                print(f"File saved successfully: {resim_filename}")
            else:
                print("File validation failed")
        else:
            print("No 'resim' in request.files")
        
        # Veritabanına kaydet
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO menu_items (isim, aciklama, fiyat, kategori, resim)
            VALUES (?, ?, ?, ?, ?)
        ''', (isim, aciklama, fiyat, kategori, resim_filename))
        conn.commit()
        conn.close()
        
        print(f"Item saved to database with image: {resim_filename}")
        flash('Ürün başarıyla eklendi!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/add_item.html')

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_item(id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM menu_items WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        isim = request.form['isim']
        aciklama = request.form['aciklama']
        fiyat = request.form['fiyat']
        kategori = request.form['kategori']
        
        # Resim güncelleme
        resim_filename = item['resim']
        if 'resim' in request.files:
            file = request.files['resim']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                resim_filename = filename
        
        # Veritabanını güncelle
        conn.execute('''
            UPDATE menu_items 
            SET isim = ?, aciklama = ?, fiyat = ?, kategori = ?, resim = ?
            WHERE id = ?
        ''', (isim, aciklama, fiyat, kategori, resim_filename, id))
        conn.commit()
        conn.close()
        
        flash('Ürün başarıyla güncellendi!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    conn.close()
    return render_template('admin/edit_item.html', item=item)

@app.route('/admin/delete/<int:id>')
@admin_required
def admin_delete_item(id):
    conn = get_db_connection()
    
    # Resim dosyasını sil
    item = conn.execute('SELECT resim FROM menu_items WHERE id = ?', (id,)).fetchone()
    if item['resim']:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item['resim']))
        except:
            pass
    
    # Veritabanından sil
    conn.execute('DELETE FROM menu_items WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Ürün başarıyla silindi!', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == "__main__":
    # Veritabanını başlat
    init_db()
    
    # Create and configure socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Verify port availability
        sock.bind(('0.0.0.0', 5012))
        sock.close()
        
        # Start Flask application
        app.run(host='0.0.0.0', port=5012, debug=True, use_reloader=False)
        
    except socket.error as e:
        print(f"Server could not start: {e}")
        print("Possible solutions:")
        print("1. Another application is using port 5012 - try a different port")
        print("2. Wait a few minutes and try again")
        print("3. Check with: lsof -i :5012")
        print("❌ Port 5012 is busy, please check running processes")
        exit(1)