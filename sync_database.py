#!/usr/bin/env python3
"""
Database Status Script
Local database durumunu gösterir
"""

import sqlite3
import os
from datetime import datetime

def get_local_db_connection():
    """Local database bağlantısı"""
    conn = sqlite3.connect('menu.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_local_items():
    """Local database'deki ürünleri al"""
    conn = get_local_db_connection()
    items = conn.execute('SELECT * FROM menu_items ORDER BY id').fetchall()
    conn.close()
    return [dict(item) for item in items]

def backup_database():
    """Database backup oluştur"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"menu_backup_{timestamp}.db"
    
    try:
        import shutil
        shutil.copy2('menu.db', backup_name)
        print(f"✅ Database backup created: {backup_name}")
        return backup_name
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return None

def show_database_status():
    """Database durumunu göster"""
    local_items = get_local_items()
    
    print("\n" + "="*60)
    print("📊 HEALTHY OR GUILTY - DATABASE STATUS")
    print("="*60)
    print(f"📁 Local Database: menu.db")
    print(f"📦 Total Items: {len(local_items)}")
    print(f"🕒 Last Modified: {datetime.fromtimestamp(os.path.getmtime('menu.db'))}")
    print("\n🍔 Current Menu Items:")
    
    for item in local_items:
        print(f"  {item['id']}. {item['isim']}")
        print(f"     💰 Fiyat: {item['fiyat']}₺")
        print(f"     📂 Kategori: {item['kategori']}")
        print(f"     🖼️ Resim: {item['resim'] if item['resim'] else 'Yok'}")
        print()
    
    print("="*60)

def main():
    """Ana fonksiyon"""
    print("🔄 DATABASE SYNC TOOL")
    
    # Database durumunu göster
    show_database_status()
    
    # Backup oluştur
    backup_file = backup_database()
    
    print("\n💡 SYNC INSTRUCTIONS:")
    print("="*40)
    print("🔼 Local → Heroku:")
    print("   1. git add .")
    print("   2. git commit -m 'Update menu items'")
    print("   3. git push heroku main")
    print()
    print("🔽 Heroku → Local:")
    print("   1. Heroku admin panelindeki ürünleri")
    print("   2. Local admin paneline manuel ekle")
    print("   3. http://127.0.0.1:5012/admin")
    print()
    print("🔗 Admin Panel Links:")
    print(f"   Local:  http://127.0.0.1:5012/admin")
    print(f"   Heroku: https://[APP_NAME].herokuapp.com/admin")

if __name__ == "__main__":
    main() 