import sqlite3

DATABASE = 'patoloji.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS hastalar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ad TEXT NOT NULL,
        soyad TEXT NOT NULL,
        tc_no TEXT UNIQUE NOT NULL,
        dogum_tarihi DATE,
        telefon TEXT,
        kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS patoloji_raporlari (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hasta_id INTEGER NOT NULL,
        rapor_tarihi DATE NOT NULL,
        rapor_no TEXT UNIQUE NOT NULL,
        makroskopi TEXT,
        mikroskopi TEXT,
        tani TEXT,
        dosya_yolu TEXT,
        kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (hasta_id) REFERENCES hastalar (id)
    )''')
    
    conn.commit()
    conn.close()
    print("Veritabanı hazır!")

if __name__ == '__main__':
    init_db()