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
   git clone [URL_REPOSITORY]
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