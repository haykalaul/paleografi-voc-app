# Aplikasi Peningkatan Kualitas Citra Paleografi Arsip VOC

Aplikasi web berbasis Python untuk meningkatkan kualitas citra paleografi arsip VOC menggunakan metode morfologi.

## Fitur Utama

- Unggah citra paleografi arsip VOC
- Berbagai operasi morfologi (dilasi, erosi, opening, closing, dll.)
- Binarisasi adaptif untuk perbaikan kontras
- Skeletonisasi untuk memperjelas struktur tulisan
- Denoising untuk menghilangkan noise
- Antarmuka pengguna yang intuitif dan responsif
- Visualisasi citra asli dan hasil secara berdampingan

## Teknologi yang Digunakan

- **Backend**: Python dengan Flask
- **Pemrosesan Citra**: OpenCV, scikit-image
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Library Lainnya**: NumPy, SciPy

## Cara Instalasi

1. Clone repository ini
   ```bash
   git clone https://github.com/haykal-proge/paleografi-voc-app.git
   cd paleografi-voc-app
   ```

2. Buat dan aktifkan virtual environment
   ```bash
   python -m venv venv
   
   # Untuk Windows
   venv\Scripts\activate
   
   # Untuk Unix/Linux
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Jalankan aplikasi
   ```bash
   python app.py
   ```

5. Buka browser dan akses `http://localhost:5000`

## Deploy ke PythonAnywhere

Jika ingin menerapkan aplikasi ini ke PythonAnywhere, ikuti langkah singkat berikut:

1. Siapkan repository publik atau private (mis. GitHub). Di mesin lokal:
   ```bash
   git add .
   git commit -m "Add project for deployment"
   git push origin main
   ```

2. Buat akun di https://www.pythonanywhere.com/ dan masuk.

3. Buat virtualenv di PythonAnywhere (contoh untuk Python 3.10):
   ```bash
   mkvirtualenv --python=python3.10 my-venv
   ```

4. Clone project di account PythonAnywhere (atau gunakan "Source code" -> "Clone a repo"):
   ```bash
   git clone https://github.com/username/paleografi-voc-app.git
   cd paleografi-voc-app
   workon my-venv
   pip install -r requirements.txt
   ```

5. Atur Web app di dashboard PythonAnywhere:
   - Klik "Web" -> "Add a new web app" -> pilih Manual configuration -> pilih versi Python yang sama dengan virtualenv.
   - Pada bagian "Virtualenv", isi path ke virtualenv Anda (mis. /home/username/.virtualenvs/my-venv).
   - Pada bagian "Source code", atur path ke folder hasil clone (mis. /home/username/paleografi-voc-app).

6. Edit file WSGI (link "WSGI configuration file" di dashboard) agar memuat aplikasi Flask dari `app.py`. Contoh minimal yang dapat Anda tambahkan/ubah:
   ```python
   import sys
   path = '/home/yourusername/paleografi-voc-app'
   if path not in sys.path:
       sys.path.insert(0, path)

   from app import app as application
   ```

7. Static files dan folder upload:
   - Di dashboard Web -> Static files, tambahkan mapping untuk `/static/` ke folder `/home/yourusername/paleografi-voc-app/static/`.
   - Jika aplikasi menulis ke `static/uploads/` atau `static/processed/`, pastikan folder tersebut memiliki permission tulis untuk user PythonAnywhere.

8. Reload web app dari dashboard. Jika ada error, lihat "Error log" dan "Server log" untuk detail.

Catatan penting:
- Pastikan `app.py` mengekspor objek Flask bernama `app` (contoh: `app = Flask(__name__)`). WSGI di atas mengimpor `app` dan merename menjadi `application`.
- Set `DEBUG = False` atau gunakan environment variable pada produksi.
- Jika menggunakan file konfigurasi (mis. `settings.py`), pastikan path dan konfigurasi upload/static sesuai environment PythonAnywhere.

## Struktur Direktori

```
paleografi-voc-app/
├── app.py                   # Aplikasi Flask utama
├── requirements.txt         # Dependensi Python
├── static/                  # Aset statis
│   ├── css/
│   │   └── style.css        # Gaya aplikasi
│   ├── js/
│   │   └── main.js          # Skrip JavaScript
│   ├── uploads/             # Direktori untuk citra yang diunggah (db local project)
│   └── processed/           # Direktori untuk citra hasil pemrosesan (db local project)
└── templates/               # Template HTML
    ├── index.html           # Halaman utama
    └── editor.html          # Halaman editor pemrosesan
```

## Panduan Penggunaan

1. **Unggah Citra**
   - Pada halaman utama, pilih file citra paleografi arsip VOC yang ingin diproses
   - Klik tombol "Unggah"

2. **Pengaturan Pemrosesan**
   - Pilih operasi morfologi yang diinginkan (dilasi, erosi, dll.)
   - Atur parameter seperti ukuran kernel, nilai threshold, dll.
   - Klik tombol "Proses Citra"

3. **Hasil**
   - Visualisasi citra asli dan hasil pemrosesan akan ditampilkan berdampingan
   - Unduh hasil pemrosesan dengan mengklik tombol "Unduh Hasil"

## Metode Morfologi untuk Citra Paleografi

Pendekatan morfologi matematis sangat berguna untuk meningkatkan kualitas citra paleografi karena:

1. **Dilasi**: Memperluas area terang, membantu memperjelas teks yang memudar
2. **Erosi**: Mempersempit area terang, membantu menghilangkan noise
3. **Opening**: Kombinasi erosi diikuti dilasi, efektif untuk menghilangkan noise kecil
4. **Closing**: Kombinasi dilasi diikuti erosi, efektif untuk menutup celah kecil
5. **Top Hat**: Efektif untuk mendeteksi puncak terang (tulisan) pada latar gelap
6. **Black Hat**: Efektif untuk mendeteksi puncak gelap pada latar terang
7. **Skeletonisasi**: Menipiskan objek hingga menjadi struktur garis, membantu analisis bentuk tulisan

## Tips Pemrosesan Citra Paleografi VOC

- Kombinasi perbaikan kontras + binarisasi adaptif sering memberikan hasil yang baik
- Untuk tulisan tinta yang sudah memudar, coba kombinasi dilasi ringan + top hat
- Untuk menghilangkan noise latar belakang, pertimbangkan operasi opening
- Skeletonisasi dapat membantu mengekstrak struktur dasar tulisan

## Lisensi

[MIT License](LICENSE)

## Kontak

Untuk pertanyaan dan bantuan lebih lanjut, silakan hubungi 
mail:[haikalaulilalbab@gmail.com]
IG: https://instagram.com/haykalaul_/