# Projek I: Sistem Pemesanan Makanan
**Projek I Mata Kuliah WI1102 - Berpikir Komputasional**  
Kelas 31 - Kelompok 5:
1. Tiara Clianta Andiwi (19624218) 
2. Muhammad Akmal (19624235) 
3. Ahmad Rinofaros Muchtar (19624250) 
4. Muh. Hartawan Haidir (19624264) 
5. Muthia Ariesta Anggraeni (19624284) 

## Tentang Program
Program ini adalah simulasi dari sistem pemesanan makanan yang memungkinkan pengguna untuk memesan makanan dari meja mereka dan diberitahu saat pesanan mereka sudah siap. Program ini terdiri dari dua sisi: sisi server dan sisi klien. Sisi server bertanggung jawab untuk mengelola database menu, antrean pesanan, dan memproses pesanan. Sisi klien bertanggung jawab untuk menampilkan menu, mengambil pesanan pengguna, dan memberitahu pengguna saat pesanan sudah siap.

## Solusi Pemikiran Komputasional
### Dekomposisi
Dalam tahap ini, kami membagi persoalan dan memecahnya menjadi subpersoalan umum yang bisa diselesaikan dengan mudah. 
 
#### Cara Kerja Umum
Program ini akan mensimulasikan sistem pemesanan makanan untuk makan di tempat. Setiap pengguna dapat memesan dari meja mereka secara paralel dan diberitahu untuk mengambil pesanan mereka saat pesanan sudah siap. 

Sementara itu, koki akan memproses pesanan dari antrean pusat dan menandai pesanan sebagai selesai saat sudah selesai. Dari penjelasan di atas, kami mendekomposisi program ini menjadi dua sisi: sisi server dan sisi klien.

#### Sisi Server
Antarmuka ini hanya akan bisa diakses oleh koki atau pengelola restoran, sehingga akan dilindungi password. Sisi server akan memiliki beberapa fitur:
- Membuat database menu yang menyimpan semua stok ketersediaan item
- Membuat antrean pusat untuk memproses semua pesanan dari pengguna
- Membuat metode agar koki dapat melihat antrean dan memproses masing-masing pesanan
- Dalam tiap pesanan, ada beberapa item yang harus diproses
- Ketika setiap item telah diproses, tandai pesanan sebagai selesai
- Hapus pesanan dari antrean saat sudah selesai

#### Sisi Klien
Antarmuka ini digukan oleh pengguna untuk memesan makanan. Sisi klien akan memiliki beberapa fitur:
- Login dengan ID Pesanan jika sudah memiliki pesanan
- Membuat pesanan baru bagi pengguna yang belum memiliki pesanan
- Konfirmasi pesanan dan mengirim pesanan ke antrean pusat untuk diproses
- Melihat status pesanan dan diberitahu saat pesanan sudah siap dengan login dengan ID Pesanan

### Pengenalan Pola
Dalam mendesain program ini, kami mengenali pola-pola yang serupa sehingga bisa dikelompokkan menjadi beberapa fungsi:
- Prosedur yang dilakukan untuk memesan makanan bagi tiap pengguna sama, sehingga bisa dijadikan sebuah fungsi `tambah_order()`
- Metode koki dalam memproses pesanan juga sama, sehingga bisa dijadikan sebuah fungsi `proses_order()`

### Abstraksi
Abstraksi program dilakukan dengan cara menerapkan paradigma Object Oriented Programming (OOP) dalam Python. Penerapan OOP dalam program ini adalah dengan mendefinisikan `class` tertentu sesuai apa yang kami anggap relevan dalam mensimulasikan program.

Sebuah `class` merupakan kumpulan objek dari kategori yang sama. Setiap kelas akan memiliki atribut dan metode masing-masing. Atribut merupakan variabel yang terikat dengan kelas tersebut, sedangkan metode adalah fungsi yang terikat dengan kelas tersebut. Berikut adalah beberapa `class` yang akan kami definisikan dalam program ini:

#### 1. `class User`
Kelas ini akan berisi semua informasi berkaitan dengan data pemesan dan juga akan berisi `class order`, yang merupakan daftar pesanan yang dipesan oleh pengguna. 
- Atribut:
    - User ID: `id: int`
    - Nama: `nama: str`
    - No. Telepon: `telp: str`
    - Daftar Pesanan: `order: List[Order]`
- Metode:
    - Konstruktor: `__init__(self, nama: str, telp: str)`
    - Menambah pesanan: `tambah_order(self, order: Order)`
    - Membatalkan pesanan: `batal_order(self, order_id: int)`
    - Melihat pesanan: `cek_order(self, order_id: int) -> Order`
    - Melihat daftar pesanan: `cek_daftar_order(self) -> List[Order]`
    - Memberitahu pesanan siap: `siap_order(self, order_id: int)`
    - String representator: `__str__(self) -> str`

#### 2. `class Order`
Kelas ini mendefinisikan objek pesanan `List[Item, int]` yang merupakan suatu daftar menu dan status suatu pesanan tersebut. 
- Atribut:
    - ID Pesanan: `id: int`
    - No. Meja: `no_meja: int`
    - User pemesan: `user: User`
    - Daftar Pesanan: `daftar: List[[Item, int]]`
    - Status Pesanan: `status: str`
- Metode:
    - Konstruktor: `__init__(self, meja: int, user: User, items: List[Item], status: str)`
    - Menambah menu: `tambah_item(self, item: Item, qty: int)`
    - Mengedit menu: `edit_item(self, item_id: int, qty: int)`
    - Menghapus menu: `hapus_item(self, item_id: int)`
    - String representator: `__str__(self) -> str`

#### 3. `class Item`
Kelas ini akan berisi objek tentang menu makanan dan minuman yang ada di menu restoran.    
- Atribut:
    - ID Menu: `id: int`
    - Nama: `nama: str`
    - Harga: `harga: int`
- Metode:
    - Konstruktor: `__init__(self, id: int, name: str, price: float)`
    - String representator: `__str__(self) -> str`

#### 4. `class Admin`
Kelas ini nanti akan memuat satu objek (admin) yang semua informasi berkaitan dengan data pemesan dan juga akan berisi `class order` dalam bentuk `collections.deque` yang merupakan antrian pesanan yang dipesan oleh pengguna.
- Atribut:
    - Admin username: `nama: str`
    - Password: `password: str`
    - Daftar Pesanan: `pesanan: collections.deque(Order)`
- Metode:
    - Konstruktor: `__init__(self, nama: str, password: str)`
    - Melihat antrean: `lihat_antrean(self) -> collections.deque(Order)`
    - Melihat pesanan pertama: `lihat_order(self) -> Order`
    - Memproses pesanan: `proses_order(self, order_id: int)`
    - Tandai pesanan selesai: `selesai_order(self, order_id: int)`

### Algoritma
Algoritma dari program ini akan dijelaskan dalam bentuk flowchart dan _pseudocode_. Untuk sementara, algoritma dalam bentuk kunci dikotomi sebagai berikut:

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
_Source code_ program kami bisa dilihat [di sini](food_app.py).