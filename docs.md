# Ringkasan Solusi Berpikir Komputasional
## Dekomposisi
Program terbagi dalam 2 modul: `server` dan `client`. Dalam setiap subfolder, terdapat beberapa file yang bertindak sebagai modul dengan tanggung jawab masing-masing. 
### Modul `server/`:
  - `admin.py`: menginisiasi akun admin dan pengelolaan pesanan.
  - `item.py`: menginisiasi menu dan setiap item di dalamnya.
  - `order.py`: menginisiasi pesanan, antrean, riwayat, dan status pesanan.
### Modul `client/`:
  - `CLI_interface.py`: menginisiasi antarmuka CLI.
  - `GUI_interface.py`: menginisiasi antarmuka GUI (khusus pengguna).
  - `user.py`: menginisiasi akun pengguna dan pembuatan pesanan.

## Pengenalan Pola
Di seluruh sistem, pola serupa muncul dalam cara menangani berbagai entitas (misalnya, pengguna, pesanan, item). Dengan mengenali pola ini, kami dapat menggeneralisasi dan menggunakan kembali kode secara efektif.

### Penanganan Data Serupa
Baik pesanan maupun pengguna memiliki atribut yang perlu disimpan, diambil, dan divalidasi. Mengenali kesamaan ini membantu dalam merancang metode yang dapat digunakan kembali untuk validasi dan pengelolaan data.

### Antarmuka
CLI dan GUI keduanya memiliki fungsi serupa untuk berinteraksi dengan pengguna tetapi dalam format yang berbeda. Mengenali pola ini memungkinkan kami untuk berbagi sebagian besar logika yang mendasarinya sambil hanya mengubah metode interaksi.

## Abstraksi
Abstraksi program dilakukan dengan cara menerapkan paradigma Object Oriented Programming (OOP) dalam Python. Penerapan OOP dalam program ini adalah dengan mendefinisikan `class` tertentu sesuai apa yang kami anggap relevan dalam mensimulasikan program.

Sebuah `class` merupakan kumpulan objek dari kategori yang sama. Setiap kelas akan memiliki atribut dan metode masing-masing. Atribut merupakan variabel yang terikat dengan kelas tersebut, sedangkan metode adalah fungsi yang terikat dengan kelas tersebut. Berikut adalah beberapa `class` yang akan kami definisikan dalam program ini:

### 1. `class Item`
Representasi objek dari menu makanan atau minuman yang ada di menu restoran.

Atribut Global:
- Penghitung item: `counter: int`
- Menu: `menu: dictionary`

Atribut Lokal:
- ID Menu: `ID: int`
- Nama: `nama: str`
- Harga (Rp): `harga: int`

Argumen initialisasi: `Item(nama: str, harga: int) -> Item`

Metode:
- `lihat_menu() -> str`: Membuat string untuk mencetak daftar menu makanan dan minuman.
- `__str__() -> str`: Membuat string untuk mencetak objek item.

### 2. `class Status(Enum)`
Enumerasi status pesanan untuk mempermudah pengelompokan. Kelas ini adalah turunan `class Enum` dari *library* `enum`. 

Status pesanan yang mungkin adalah:
- `PENDING` = Menunggu dikonfirmasi
- `CANCELED` = Dibatalkan
- `CONFIRMED` = Dikonfirmasi, dalam antrean
- `IN_PROGRESS` = Dalam proses
- `READY` = Siap diambil
- `COMPLETED` = Selesai

### 3. `class Order`
Representasi sebuah pesanan atau order. Kelas ini juga bertanggung jawab dalam menyimpan antrean pesanan serta riwayat pesanan yang sudah selesai.

Atribut Global:
- Penghitung order: `counter: int`
- Riwayat order: `riwayat: dictionary`
- Antrean order: `antrean: list`

Atribut Lokal:
- ID Pesanan: `id: str`
- No. Meja: `meja: int`
- User pemesan: `user: User`
- Daftar Pesanan: `items: list`
- Total harga: `total: int`
- Jumlah item: `jumlah: int`
- Status Pesanan: `status: Status`

Argumen initialisasi: `Order(meja: int, user: User) -> Order`

Metode:
- `id_generator() -> str`: Membuat ID unik untuk pesanan.
- `cek_total() -> int`: Menghitung total harga pesanan.
- `cek_jumlah() -> int`: Menghitung jumlah item dalam pesanan.
- `tambah_item(item: Item, qty: int)`: Menambahkan item ke dalam pesanan jika belum ada.
- `edit_item(item: Item, qty: int)`: Mengedit jumlah item dalam pesanan jika ada.
- `edit_status(status: Status)`: Mengubah status pesanan.
- `cetak_struk() -> str`: Membuat string untuk mencetak struk pesanan.
- `__str__() -> str`: Membuat string untuk mencetak objek order.

### 4. `class Admin`
Berisi semua informasi berkaitan dengan data dan perintah admin. Untuk menggunakan kemmampuan Admin, Admin harus login terlebih dahulu.

Atribut Lokal:
- Username (tersembunyi): `_username: str`
- Password (tersembunyi): `_password: str`
- Autentikasi: `auth: bool`

Argumen initialisasi: `Admin(username: str, password: str) -> Admin`

Metode:
- `login(username: str, password: str) -> bool`: Masuk ke sistem dengan memasukkan password.
- `logout()`: Keluar dari sistem.
- `lihat_antrean()`: Melihat semua pesanan yang belum diproses.
- `proses_order()`: Mengambil pesanan terdepan dari antrean, mengubah statusnya, lalu memproses tiap itemnya.
- `selesai_order(order: Order)`: Menyelesaikan pesanan, mengubah statusnya, dan memberitahu pengguna.

### 5. `class User`
Berisi semua informasi berkaitan dengan data pemesan.

Atribut Global:
- Penghitung user: `counter: int`
- Daftar user: `daftar: dictionary`

Atribut Lokal:
- ID User: `ID: str`
- Nama: `nama: str`
- Telepon: `telp: str`
- Daftar Pesanan: `orders: dictionary`

Argumen initialisasi: `User(nama: str, telp: str) -> User`

Metode:
- `id_generator() -> str`: Membuat ID unik untuk user.
- `tambah_order(order: Order)`: Menambahkan pesanan ke dalam daftar pesanan pengguna.
- `lihat_daftar() -> str`: Melihat daftar pesanan yang dimiliki pengguna.
- `notifikasi(order: Order)`: Memberitahu pengguna bahwa pesanannya sudah siap.
- `__str__() -> str`: Membuat string untuk mencetak objek user.

### 6. `class CLI_Interface`
Antarmuka antara sisi klien dan sisi server dalam bentuk CLI (Command Line Interface).

Atribut: admin: `Admin`, berupa objek admin yang digunakan untuk mengakses data dari sisi server. Untuk program ini, kami mengeset username admin adalah `pass` dan password admin adalah `username`.

Metode:
- `print_dl(text: str, **kwargs)`: Mencetak baris dengan jeda waktu tertentu.
- `print_dc(text: str, **kwargs)`: Mencetak karakter dengan jeda waktu tertentu.
- `header_halaman(pesan: str)`: Membuat header pada halaman.
- `valid() -> bool`: Validasi masukan berupa Pertanyaan Ya/Tidak.
- `keluar()`: Konfirmasi untuk keluar Program.
- `selamat_datang()`: Menampilkan pesan selamat datang.
- `halaman_utama()`: Halaman utama dan pertama ketika memulai program.
- `masuk_koki()`: Portal masuk bagi koki.
- `beranda_koki()`: Halaman beranda bagi koki.
- `portal_pengguna()`: Memisahkan pengguna yang sudah/belum punya User ID.
- `masuk_pengguna()`: Portal login dengan User ID.
- `daftar_pengguna()`: Membuat user baru dan login otomatis.
- `beranda_pengguna(user: User)`: Halaman beranda bagi pengguna.
- `buat_pesanan(user: User)`: Antarmuka membuat pesanann baru.
- `pesanan_pengguna(user: User)`: Antarmuka daftar pesanan pengguna.

### 7. `class GUI_Interface`
Antarmuka khusus pengguna dalam bentuk GUI (Graphical User Interface) melalui jendela interaktif.

Atribut Lokal:
`root: tk.Tk` -> Jendela utama aplikasi

Atribut Global:
- `font_family` -> Font yang akan digunakan
- `fsize_t` -> Ukuran font untuk judul
- `fsize_h1` -> Ukuran font untuk header 1
- `fsize_h2` -> Ukuran font untuk header 2
- `fsize_h3` -> Ukuran font untuk header 3
- `fsize_n` -> Ukuran font untuk teks biasa

Atibut Lokal:
- `root: tk.Tk` -> Jendela utama aplikasi
- `default_font: str` -> Font default untuk aplikasi
- `frame: tk.Frame` -> Frame utama aplikasi
- `header: tk.Label` -> Label untuk judul halaman

Argumen initialisasi: `GUI_Interface(root: tk.Tk) -> GUI_Interface`

Metode:
- `mulai_hal()`: Fungsi pembantu untuk menginisiasi pembuatan halaman
- `buat_frame() -> tk.Frame`: Fungsi pembantu untuk menginisiasi grid pada halaman
- `hal_utama()`: Membuat antarmuka utama untuk memilih sebagai pengguna atau koki
- `hal_daftar_pengguna()`: Membuat antarmuka untuk pengguna baru untuk melakukan pemesanan
- `hal_masuk_pengguna()`: Membuat antarmuka untuk pengguna yang sudah ada untuk login
- `buat_user_baru()`: Membuat order baru berdasarkan input dari pengguna
- `masuk_user()`: Fungsi untuk login pengguna yang sudah ada
- `hal_beranda_user(user: User)`: Membuat antarmuka beranda setelah login pengguna
- `hal_lihat_pesanan(user: User, order: Order)`: Membuat antarmuka untuk melihat detail pesanan
- `hal_buat_pesanan_baru(user: User)`: Membuat antarmuka untuk membuat pesanan baru
- `hal_konfirmasi_pesanan(user: User)`: Membuat antarmuka untuk konfirmasi pesanan yang akan dibuat
- `buat_pesanan(user: User)`: Membuat pesanan baru berdasarkan input dari pengguna
- `batalkan_pesanan(user: User, order: Order)`: Membatalkan pesanan yang telah dibuat

## Algoritma
Algoritma dari program ini akan dijelaskan dalam bentuk flowchart dan _pseudocode_ dalam laporan. Untuk sementara, di sini kami menjelaskanalgoritma dalam bentuk kunci dikotomi sebagai berikut:

    1. Mulai -> pilih peran:
        - Jika peran adalah koki, maka lanjut ke langkah 2
        - Jika peran adalah pengguna, maka lanjut ke langkah 3
        - Jika selesai, maka lanjut ke langkah 12
    2. Sebagai koki -> masukkan password:
        - Jika password benar, maka lanjut ke langkah 4
        - Jika password salah, maka ulangi langkah 2
        - Jika ingin kembali, maka kembali ke langkah 1
    3. Sebagai pengguna -> pilih opsi:
        - Jika sudah memiliki User ID, maka lanjut ke langkah 5
        - Jika belum memiliki User ID, maka lanjut ke langkah 6
        - Jika ingin kembali, maka kembali ke langkah 1
    4. Sebagai koki -> pilih opsi:
        - Jika ingin melihat antrean, maka lanjut ke langkah 7
        - Jika ingin memproses pesanan, maka lanjut ke langkah 8
        - Jika ingin kembali, maka kembali ke langkah 1
    5. Sudah memiliki User ID -> masukkan User ID:
        - Jika User ID benar, maka lanjut ke langkah 9
        - Jika User ID salah, maka ulangi langkah 5
        - Jika ingin kembali, maka kembali ke langkah 1
    6. Belum memiliki User ID -> masukkan data diri:
        - Masukkan nama dan nomor telepon
        - Sistem akan membuat User ID baru memberi opsi untuk membuat pesanan
        - Lanjut ke langkah 9
    7. Melihat antrean: 
        - Sistem menampilkan antrean pesanan yang belum diproses
        - Koki bisa memilih pesanan yang ingin diproses secara manual
        - Lanjut ke langkah 8
    8. Memproses pesanan (secara otomatis maupun manual):
        - Sistem akan menampilkan item dari pesanan yang dipilih
        - Koki bisa memilih untuk memproses item secara manual
        - Ketika semua item sudah diproses, sistem akan menandai pesanan sebagai selesai
        - Kembali ke langkah 4
    9. Dashboard pengguna:
        - Sistem menampilkan setiap pesanan pengguna dan statusnya
        - Jika ingin membuat pesanan, maka lanjut ke langkah 10
        - Jika ingin melihat status pesanan, maka lanjut ke langkah 11
        - Jika ingin kembali, maka kembali ke langkah 1
    10. Membuat pesanan:
        - Sistem menampilkan menu makanan dan minuman yang tersedia
        - Pengguna membuat pesanan -> sistem membuat ID Pesanan baru
        - Pengguna mengonfirmasi pesanan dan pembayaran
        - Pesanan akan masuk ke antrean pusat
        - Lanjut ke langkah 11
    11. Status pesanan:
        - Sistem menampilkan status pesanan pengguna
        - Jika pesanan sudah siap, maka pengguna akan diberitahu
        - Jika ingin kembali, maka kembali ke langkah 9
    12. Selesai -> program berhenti

## _Source Code_
_Source code_ program kami bisa dilihat di folder [program](program/).