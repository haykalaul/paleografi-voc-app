# app.py yang sudah dimodifikasi

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from skimage import morphology, io, color, exposure, filters

# Inisialisasi aplikasi Flask
app = Flask(__name__)
app.secret_key = 'paleografi_voc_key'

# --- PERUBAHAN UTAMA: Gunakan direktori /tmp untuk file dinamis ---
UPLOAD_FOLDER = '/tmp/uploads'
PROCESSED_FOLDER = '/tmp/processed'
# -----------------------------------------------------------------

app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'tif', 'tiff'}

# Membuat direktori di /tmp jika belum ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# ... (Fungsi process_image Anda TIDAK PERLU DIUBAH, hanya perlu pastikan path-nya benar) ...
# Salin fungsi allowed_file dan process_image Anda di sini tanpa perubahan

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_image(image_path, operations):
    # Definisi fungsi process_image Anda di sini
    # Pastikan output path menggunakan PROCESSED_FOLDER yang baru
    img = cv2.imread(image_path)
    
    # ... (logika pemrosesan Anda) ...

    # Simpan hasil ke direktori /tmp/processed
    output_filename = f"processed_{os.path.basename(image_path)}"
    output_path = os.path.join(PROCESSED_FOLDER, output_filename)
    cv2.imwrite(output_path, processed_image) # ganti 'processed_image' dengan variabel hasil Anda
    
    return output_path

# ...

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Tidak ada file yang dipilih')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('Tidak ada file yang dipilih')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # --- PERUBAHAN: Simpan file ke /tmp/uploads ---
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        return redirect(url_for('editor', filename=filename))
    
    flash('Format file tidak didukung')
    return redirect(request.url)

@app.route('/editor/<filename>')
def editor(filename):
    # --- PERUBAHAN: URL gambar sekarang menunjuk ke route baru ---
    return render_template('editor.html', 
                           original_image=url_for('serve_upload', filename=filename),
                           filename=filename)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    filename = data.get('filename')
    operations = data.get('operations', {})
    
    if not filename:
        return jsonify({'error': 'Filename tidak ditemukan'}), 400
    
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File tidak ditemukan di /tmp'}), 404
    
    try:
        processed_path = process_image(filepath, operations)
        processed_filename = os.path.basename(processed_path)
        # --- PERUBAHAN: URL menunjuk ke route baru untuk file yang diproses ---
        processed_url = url_for('serve_processed', filename=processed_filename)
        
        return jsonify({
            'success': True,
            'processed_image': processed_url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- ROUTE BARU: Untuk menyajikan file dari direktori /tmp ---
@app.route('/uploads/<filename>')
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/processed/<filename>')
def serve_processed(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)
# -------------------------------------------------------------

@app.route('/download/<filename>')
def download(filename):
    processed_file = f"processed_{filename}"
    return send_from_directory(PROCESSED_FOLDER, processed_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)