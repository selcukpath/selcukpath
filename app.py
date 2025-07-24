from database import init_db
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from werkzeug.utils import secure_filename
from database import init_db, get_db_connection
from models import Hasta, PatolojiRaporu
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Upload klasörünü oluştur
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# İzin verilen dosya uzantıları
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hasta_ekle', methods=['GET', 'POST'])
def hasta_ekle():
    if request.method == 'POST':
        ad = request.form['ad']
        soyad = request.form['soyad']
        tc_no = request.form['tc_no']
        dogum_tarihi = request.form['dogum_tarihi']
        telefon = request.form['telefon']
        
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO hastalar (ad, soyad, tc_no, dogum_tarihi, telefon)
                VALUES (?, ?, ?, ?, ?)
            ''', (ad, soyad, tc_no, dogum_tarihi, telefon))
            conn.commit()
            flash('Hasta başarıyla eklendi!', 'success')
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            flash('Bu TC numarası zaten kayıtlı!', 'error')
        finally:
            conn.close()
    
    return render_template('hasta_ekle.html')

@app.route('/rapor_ekle', methods=['GET', 'POST'])
def rapor_ekle():
    if request.method == 'POST':
        hasta_id = request.form['hasta_id']
        rapor_tarihi = request.form['rapor_tarihi']
        rapor_no = request.form['rapor_no']
        makroskopi = request.form['makroskopi']
        mikroskopi = request.form['mikroskopi']
        tani = request.form['tani']
        
        # Dosya yükleme
        filename = None
        if 'dosya' in request.files:
            file = request.files['dosya']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO patoloji_raporlari 
                (hasta_id, rapor_tarihi, rapor_no, makroskopi, mikroskopi, tani, dosya_yolu)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (hasta_id, rapor_tarihi, rapor_no, makroskopi, mikroskopi, tani, filename))
            conn.commit()
            flash('Rapor başarıyla eklendi!', 'success')
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            flash('Bu rapor numarası zaten kayıtlı!', 'error')
        finally:
            conn.close()
    
    # Hastaları getir
    conn = get_db_connection()
    hastalar = conn.execute('SELECT id, ad, soyad, tc_no FROM hastalar ORDER BY ad').fetchall()
    conn.close()
    
    return render_template('rapor_ekle.html', hastalar=hastalar)

@app.route('/arama')
def arama():
    return render_template('arama.html')

@app.route('/ara', methods=['POST'])
def ara():
    arama_tipi = request.form['arama_tipi']
    arama_terimi = request.form['arama_terimi']
    
    conn = get_db_connection()
    
    if arama_tipi == 'tc_no':
        sonuclar = conn.execute('''
            SELECT h.ad, h.soyad, h.tc_no, h.telefon, 
                   pr.rapor_no, pr.rapor_tarihi, pr.tani
            FROM hastalar h
            LEFT JOIN patoloji_raporlari pr ON h.id = pr.hasta_id
            WHERE h.tc_no LIKE ?
        ''', (f'%{arama_terimi}%',)).fetchall()
    
    elif arama_tipi == 'rapor_no':
        sonuclar = conn.execute('''
            SELECT h.ad, h.soyad, h.tc_no, h.telefon, 
                   pr.rapor_no, pr.rapor_tarihi, pr.tani
            FROM hastalar h
            JOIN patoloji_raporlari pr ON h.id = pr.hasta_id
            WHERE pr.rapor_no LIKE ?
        ''', (f'%{arama_terimi}%',)).fetchall()
    
    else:  # ad_soyad
        sonuclar = conn.execute('''
            SELECT h.ad, h.soyad, h.tc_no, h.telefon, 
                   pr.rapor_no, pr.rapor_tarihi, pr.tani
            FROM hastalar h
            LEFT JOIN patoloji_raporlari pr ON h.id = pr.hasta_id
            WHERE h.ad LIKE ? OR h.soyad LIKE ?
        ''', (f'%{arama_terimi}%', f'%{arama_terimi}%')).fetchall()
    
    conn.close()
    
    return render_template('sonuclar.html', sonuclar=sonuclar, arama_terimi=arama_terimi)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)