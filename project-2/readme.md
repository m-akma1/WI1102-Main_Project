# Projek 2: Sistem Pemesanan Makanan
**Projek 2 Mata Kuliah WI1102 - Berpikir Komputasional**  
Kelas 31 - Kelompok 5:
1. Tiara Clianta Andiwi (19624218) 
2. Muhammad Akmal (19624235) 
3. Ahmad Rinofaros Muchtar (19624250) 
4. Muh. Hartawan Haidir (19624264) 
5. Muthia Ariesta Anggraeni (19624284) 

## Tentang Program
### Deskripsi
**Panda Manis** (Kapan Dapat Makanan Gratisnya?) merupakan kelanjutan dari [Projek 1](../project-1/) yang berisi peningkatan fitur dari projek sebelumnya. Program ini akan mensimulasikan sistem pemesanan makanan yang memungkinkan pengguna untuk memesan makanan mereka dan melihat statusnya selagi diproses. Program ini sepenuhnya dibuat menggunakan Python dengan Tkinter sebagai GUI (*Graphical User Interface*).

### Fitur Utama
Fitur dengan tanda (*) menandakan fitur baru yang ditambahkan pada projek ini:

#### User
- Registrasi dan Login Pengguna: Pengguna dapat mendaftar sebagai pelanggan baru atau login sebagai pelanggan lama untuk melakukan pemesanan.
- Pesan dan Konfirmasi Pesanan: Pengguna dapat memilih makanan dari menu yang tersedia dan mengonfirmasinya sebelum memesan.
- Riwayat Pesanan: Pengguna dapat melihat pesanan sebelumnya yang sudah dibuat maupun dibatalkan.
- Refresh Halaman*: Pengguna dapat memperbarui halaman untuk melihat perubahan terbaru pada status pesanan.
- Mengedit dan Membatalkan Pesanan*: Pengguna dapat mengedit maupun membatalkan pesanan yang sudah dibuat selama belum diproses admin.

#### Admin
- Antarmuka Grafis*: Seluruh antarmuka admin diperbarui dengan tampilan yang lebih baik dan mudah digunakan.
- Perlindungan Kata Sandi: Admin harus memasukkan kata sandi untuk masuk ke akun admin.
- Manajemen Antrean: Admin dapat melihat pesanan yang masuk, memproses pesanan, dan mengubah status pesanan.
- Statistik Pesanan*: Admin dapat melihat statistik pesanan yang sudah diproses dan total pendapatan yang diperoleh.
- Cetak Struk Pesanan*: Admin dapat mencetak struk pesanan yang sudah diproses.
- Buat Jendela Baru*: Admin dapat membuka jendela baru untuk digunakan beberapa user secara bersamaan.

#### Lain-Lain
- Antarmuka Grafis Penuh*: Program ini sepenuhnya menggunakan GUI untuk interaksi pengguna dan admin.
- Logika Program Diperbarui*: Logika pengeditan, pembatalan, dan pemprosesan pesanan diperbarui untuk memastikan pesanan tidak diedit/dibatalkan bersamaan saat diproses.

## Cara Penggunaan
### Prasyarat
- Python 3.7+
- Library: Pillow (PIL) untuk pengelolaan gambar.

### Menjalankan Aplikasi
1. Pastikan Python sudah diinstal di komputer Anda. Jika belum, Anda bisa mengunduhnya [di sini](https://www.python.org/downloads/).
2. Pastikan juga modul `PIL` (Pillow) sudah terinstal di Python Anda. Jika belum, Anda bisa menginstalnya dengan perintah berikut.
```sh
pip install pillow
```
2. Unduh zip file program ini dengan cara klik tombol "Code" hijau di atas dan pilih "Download ZIP", lalu ekstrak file zip yang sudah diunduh. Anda juga bisa *clone repositori* ini langsung ke komputer Anda.
3. Buka terminal atau Command Prompt, navigasikan ke direktori tempat file program ini disimpan, lalu jalankan program dengan perintah berikut.  
*Catatan: Pastikan Anda berada di dalam folder `project-2` sebelum menjalankan perintah berikut.*
```sh
python main.py
```

### Informasi Tambahan
- Antarmuka Admin dan User akan langsung muncul saat program dijalankan. Jendela Admin akan menjadi *root* program.
- Perhatikan hanya akan ada 1 jendela *Admin* meski memungkinkan terdapat beberapa jendela user dalam setiap satu proses. Untuk membuat beberapa jendela *User* berjalan bersamaan dalam satu proses, tekan tombol *Buat Jendela Baru*. 
- **Username dan password admin:**
    - **Username: `afafufuf`**
    - **Password: `fufufafa`**

## Struktur Projek
Proyek ini dibagi menjadi beberapa komponen berikut:

### **1. Sisi Server [(`server/`)](server/):**
- **`admin.py`:** Menangani tindakan administrator seperti login, memproses pesanan, dan mengelola antrean pesanan.
- **`item.py`:** Menentukan kelas `Item`, yang mewakili item menu individual.
- **`order.py`:** Menentukan kelas `Order` dan enum `Status` untuk melacak status pesanan.
- **`user.py`:** Menentukan kelas `User` untuk mengelola akun pengguna dan pesanan mereka.

### **2. Sisi Klien [(`client/`)](client/):**
- **`admin_interface.py`:** Menyediakan GUI untuk fungsionalitas admin, seperti login, dasbor, dan manajemen pesanan.
- **`user_interface.py`:** Menyediakan GUI untuk fungsionalitas pengguna, seperti registrasi, login, dan penempatan pesanan.

### **3. File Utama (`main.py`):**
Titik masuk aplikasi yang menginisialisasi dan menjalankan antarmuka admin dan pengguna.

### Struktur File

    Project_WI1102/
    |--- project-1/..
    |
    |--- project-2/
    |    |-- client/
    |    |     |-- admin_interface.py
    |    |     |-- user_interface.py
    |    |     |-- new_logo.png
    |    |     |-- __init__.py
    |    |
    |    |-- server/
    |    |     |-- admin.py
    |    |     |-- item.py
    |    |     |-- order.py
    |    |     |-- user.py
    |    |     |-- __init__.py
    |    |
    |    |-- main.py
    |    |-- README.md
    |
    |--- LICENSE
    |--- README.md

## Lisensi
Program ini dilisensikan di bawah [MIT License](../LICENSE).

&copy;  2024. Bandung. Sekolah Teknik Elektro dan Informatika. Institut Teknologi Bandung.