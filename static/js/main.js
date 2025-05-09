/**
 * Script utama untuk aplikasi Paleografi Arsip VOC
 */

document.addEventListener('DOMContentLoaded', function() {
    // Ketika ada pada halaman utama
    const uploadForm = document.querySelector('form');
    if (uploadForm) {
        // Preview gambar yang akan diupload
        const fileInput = document.getElementById('file');
        if (fileInput) {
            fileInput.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        // Jika ingin menambahkan preview, bisa dimasukkan di sini
                        console.log('File selected:', fileInput.files[0].name);
                    }
                    reader.readAsDataURL(this.files[0]);
                }
            });
        }

        // Validasi form sebelum submit
        uploadForm.addEventListener('submit', function(event) {
            const fileInput = document.getElementById('file');
            if (!fileInput.files || fileInput.files.length === 0) {
                event.preventDefault();
                alert('Silakan pilih file citra terlebih dahulu.');
                return false;
            }

            const allowedTypes = ['image/jpeg', 'image/png', 'image/tiff'];
            if (!allowedTypes.includes(fileInput.files[0].type)) {
                event.preventDefault();
                alert('Format file tidak didukung. Silakan pilih file JPG, PNG, atau TIFF.');
                return false;
            }
        });
    }

    // Animasi untuk cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.1)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.05)';
        });
    });

    // Fungsi untuk tombol-tombol di editor
    if (window.location.pathname.includes('/editor')) {
        // Dependensi antar opsi
        const binarizeCheckbox = document.getElementById('binarize');
        const adaptiveThresholdCheckbox = document.getElementById('adaptiveThreshold');
        
        if (binarizeCheckbox && adaptiveThresholdCheckbox) {
            binarizeCheckbox.addEventListener('change', function() {
                if (this.checked) {
                    adaptiveThresholdCheckbox.checked = false;
                }
            });
            
            adaptiveThresholdCheckbox.addEventListener('change', function() {
                if (this.checked) {
                    binarizeCheckbox.checked = false;
                }
            });
        }

        // Skeletonisasi memerlukan binarisasi
        const skeletonizeCheckbox = document.getElementById('skeletonize');
        if (skeletonizeCheckbox) {
            skeletonizeCheckbox.addEventListener('change', function() {
                if (this.checked) {
                    if (!binarizeCheckbox.checked && !adaptiveThresholdCheckbox.checked) {
                        adaptiveThresholdCheckbox.checked = true;
                    }
                }
            });
        }
    }
});

// Fungsi untuk menampilkan loading spinner
function showLoading() {
    const loadingElement = document.getElementById('processingStatus');
    if (loadingElement) {
        loadingElement.style.display = 'block';
    }
}

// Fungsi untuk menyembunyikan loading spinner
function hideLoading() {
    const loadingElement = document.getElementById('processingStatus');
    if (loadingElement) {
        loadingElement.style.display = 'none';
    }
}

// Fungsi untuk menampilkan pesan error
function showError(message) {
    const errorElement = document.getElementById('errorMessage');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

// Fungsi untuk menyembunyikan pesan error
function hideError() {
    const errorElement = document.getElementById('errorMessage');
    if (errorElement) {
        errorElement.style.display = 'none';
    }
}