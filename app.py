from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from skimage import morphology, io, color, exposure, filters

app = Flask(__name__)
app.secret_key = 'paleografi_voc_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['PROCESSED_FOLDER'] = 'static/processed/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'tif', 'tiff'}

# Membuat direktori jika belum ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_image(image_path, operations):
    """Memproses citra dengan berbagai operasi morfologi"""
    # Baca gambar
    img = cv2.imread(image_path)
    
    # Simpan gambar asli untuk referensi
    original_img = img.copy()
    
    # Konversi ke grayscale jika belum
    if len(img.shape) > 2:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    
    # Proses gambar berdasarkan operasi yang dipilih
    processed = gray.copy()
    
    # Pra-pemrosesan dasar
    if 'denoise' in operations:
        processed = cv2.fastNlMeansDenoising(processed, None, 10, 7, 21)
    
    if 'contrast' in operations:
        processed = exposure.equalize_hist(processed)
        processed = (processed * 255).astype(np.uint8)
    
    # Operasi morfologi
    kernel_size = int(operations.get('kernel_size', 3))
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    
    if 'dilate' in operations:
        processed = cv2.dilate(processed, kernel, iterations=1)
    
    if 'erode' in operations:
        processed = cv2.erode(processed, kernel, iterations=1)
    
    if 'opening' in operations:
        processed = cv2.morphologyEx(processed, cv2.MORPH_OPEN, kernel)
    
    if 'closing' in operations:
        processed = cv2.morphologyEx(processed, cv2.MORPH_CLOSE, kernel)
    
    if 'tophat' in operations:
        processed = cv2.morphologyEx(processed, cv2.MORPH_TOPHAT, kernel)
    
    if 'blackhat' in operations:
        processed = cv2.morphologyEx(processed, cv2.MORPH_BLACKHAT, kernel)
    
    if 'gradient' in operations:
        processed = cv2.morphologyEx(processed, cv2.MORPH_GRADIENT, kernel)
    
    # Binarisasi (thresholding)
    if 'binarize' in operations:
        threshold_value = int(operations.get('threshold', 127))
        _, processed = cv2.threshold(processed, threshold_value, 255, cv2.THRESH_BINARY)
    
    if 'adaptive_threshold' in operations:
        block_size = int(operations.get('block_size', 11))
        processed = cv2.adaptiveThreshold(processed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY, block_size, 2)
    
    # Skeletonisasi untuk memperjelas struktur tulisan
    if 'skeletonize' in operations:
        # Pastikan gambar biner
        if 'binarize' not in operations and 'adaptive_threshold' not in operations:
            _, temp = cv2.threshold(processed, 127, 255, cv2.THRESH_BINARY)
            processed = temp
        
        # Inversi warna jika tulisan berwarna hitam
        if operations.get('invert_before_skeletonize', False):
            processed = 255 - processed
            
        # Normalisasi untuk skeletonisasi
        processed_binary = processed > 0
        skeleton = morphology.skeletonize(processed_binary)
        processed = (skeleton * 255).astype(np.uint8)
        
        if operations.get('invert_before_skeletonize', False):
            processed = 255 - processed
    
    # Simpan hasil
    output_path = os.path.join(app.config['PROCESSED_FOLDER'], 
                              f"processed_{os.path.basename(image_path)}")
    cv2.imwrite(output_path, processed)
    
    return output_path

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
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return redirect(url_for('editor', filename=filename))
    
    flash('Format file tidak didukung')
    return redirect(request.url)

@app.route('/editor/<filename>')
def editor(filename):
    return render_template('editor.html', 
                          original_image=url_for('static', filename=f'uploads/{filename}'),
                          filename=filename)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    filename = data.get('filename')
    operations = data.get('operations', {})
    
    if not filename:
        return jsonify({'error': 'Filename tidak ditemukan'}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File tidak ditemukan'}), 404
    
    try:
        processed_path = process_image(filepath, operations)
        processed_url = url_for('static', filename=f'processed/processed_{filename}')
        
        return jsonify({
            'success': True,
            'processed_image': processed_url
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    # Implementasi download file hasil pemrosesan
    processed_file = f"processed_{filename}"
    return send_from_directory(app.config['PROCESSED_FOLDER'], processed_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)