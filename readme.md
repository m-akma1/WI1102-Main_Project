# Projek I: Sistem Pemesanan Makanan
**Projek I Mata Kuliah WI1102 - Berpikir Komputasional**  
Kelas 31 - Kelompok 5:
1. Tiara Clianta Andiwi (19624218) 
2. Muhammad Akmal (19624235) 
3. Ahmad Rinofaros Muchtar (19624250) 
4. Muh. Hartawan Haidir (19624264) 
5. Muthia Ariesta Anggraeni (19624284) 

## Tentang Program
**Nama: PANDA MANIS**  
**Kepanjangan:** ka**PAN** **DA**pat **MA**ka**N**an grat**IS**nya?

### Deskripsi
Program ini akan mensimulasikan sistem pemesanan makanan yang memungkinkan pengguna untuk memesan makanan mereka dan melihat statusnya selagi diproses. [Program](program/main.py) ini dibagi menjadi dua sisi: [*server*](program/server/) dan [*client*](program/client/). Sisi server bertanggung jawab dalam menginisasi menu, mengelola antrean pesanan, dan menyelesaikan pesanan. Sisi klien bertanggung jawab untuk membuat antarmuka, mengelola *user*, dan menampilkan status pesanan. 

### Fitur Utama
- Registrasi dan Login Pengguna: Pengguna dapat mendaftar sebagai pelanggan baru atau login sebagai pelanggan lama untuk melakukan pemesanan.
- Manajemen Pesanan: Pengguna dapat membuat pesanan baru, melihat pesanan sebelumnya, dan memeriksa status pesanan yang sudah ada.
- Dua Antarmuka: Sistem ini mencakup GUI yang dibuat menggunakan Tkinter dan CLI untuk kompatibilitas yang lebih luas.

### Cara Penggunaan
1. Pastikan Python sudah diinstal di komputer Anda. Jika belum, Anda bisa mengunduhnya [di sini](https://www.python.org/downloads/).  
2. Unduh zip file program ini dengan cara klik tombol "Code" hijau di atas dan pilih "Download ZIP", lalu ekstrak file zip yang sudah diunduh.
3. Buka terminal atau Command Prompt, pindah ke direktori tempat file program ini disimpan, lalu jalankan program dengan perintah berikut.
```sh
python main.py
```
4. Akan ada dua opsi Anda berinteraksi dengan sistem: melalui CLI (*Command Line Interface*) atau GUI (*Graphical User Interface*). 
5. Jendela baru GUI akan langsung muncul saat program dijalankan, sementara di saat bersamaan CLI akan tetap berjalan di terminal, Anda bisa memilih salah satu atau menjalankan keduanya bersamaan.

## Ringkasan Solusi Pemikiran Komputasional
Ringkasan solusi pemikiran komputasional yang kami terapkan dalam program ini dapat Anda lihat [di sini](docs.md).

## Struktur Program
Struktur program ini terdiri dari beberapa file dan folder yang masing-masing memiliki tanggung jawabnya sendiri. Berikut adalah struktur program secara umum:

    Project_I/
    |    program/
    |    |-- client/
    |    |     |-- CLI_Interface.py
    |    |     |-- GUI_Interface.py
    |    |     |-- user.py
    |    |     |-- logo.jpeg    
    |    |     |-- __init__.py
    |    |
    |    |-- server/
    |    |     |-- admin.py
    |    |     |-- item.py
    |    |     |-- order.py
    |    |     |-- __init__.py
    |    |
    |    |-- main.py
    |
    |-- README.md
    |-- docs.md

## Lisensi
Program ini dilisensikan di bawah [MIT License](LICENSE).

&copy;  2024. Bandung. Sekolah Teknik Elektro dan Informatika. Institut Teknologi Bandung.
