# Projek I: Sistem Pemesanan Makanan
**Projek I Mata Kuliah WI1102 - Berpikir Komputasional**  
Kelas 31 - Kelompok 5:
1. Tiara Clianta Andiwi (19624218) 
2. Muhammad Akmal (19624235) 
3. Ahmad Rinofaros Muchtar (19624250) 
4. Muh. Hartawan Haidir (19624264) 
5. Muthia Ariesta Anggraeni (19624284) 

## Tentang Program
Program ini adalah simulasi sistem pemesanan makanan yang memungkinkan pengguna untuk memesan makanan dari meja mereka dan diberitahu saat pesanan mereka sudah siap. Program ini terdiri dari dua sisi: sisi server dan sisi klien. Sisi server bertanggung jawab untuk mengelola database menu, antrean pesanan, dan memproses pesanan. Sisi klien bertanggung jawab untuk menampilkan menu, mengambil pesanan pengguna, dan memberitahu pengguna saat pesanan sudah siap.

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
- Prosedur yang dilakukan untuk memesan makanan bagi tiap pengguna sama, sehingga bisa dijadikan sebuah fungsi `buat_pesanan()`
- Metode koki dalam memproses pesanan juga sama, sehingga bisa dijadikan sebuah fungsi `proses_pesanan()`

### Abstraksi
Abstraksi program dilakukan dengan cara menerapkan paradigma Object Oriented Programming (OOP) dalam Python. Penerapan OOP dalam program ini adalah dengan mendefinisikan `class` tertentu sesuai apa yang kami anggap relevan dalam mensimulasikan program.

Sebuah `class` merupakan kumpulan objek dari kategori yang sama. Setiap kelas akan memiliki atribut dan metode masing-masing. Atribut merupakan variabel yang terikat dengan kelas tersebut, sedangkan metode adalah fungsi yang terikat dengan kelas tersebut. Berikut adalah beberapa `class` yang akan kami definisikan dalam program ini:

#### 1. `class User`
Kelas ini akan berisi semua informasi berkaitan dengan data pemesan dan juga akan berisi `class order`, yang merupakan daftar pesanan yang dipesan oleh pengguna. 
- Atribut:
    - User ID: `id: int`
    - Nama: `nama: str`
    - No. Telepon: `telp: str`
    - No. Meja: `no_meja: int`
    - Daftar Pesanan: `pesanan: List[Order]`
- Metode:
    - Konstruktor: `__init__(self, nama: str, telp: str, no_meja: int)`
    - Menambah pesanan: `tambah_order(self, order: Order)`
    - Membatalkan pesanan: `batal_order(self, order_id: int)`
    - Melihat pesanan: `cek_order(self, order_id: int) -> Order`
    - Melihat daftar pesanan: `cek_daftar_order(self) -> List[Order]`
    - String konverter: `__str__(self) -> str`

#### 2. `class Order`
Kelas ini mendefinisikan objek pesanan `List[Item, int]` yang merupakan suatu daftar menu dan status suatu pesanan tersebut. 
- Atribut:
    - ID Pesanan: `id: int`
    - Daftar Pesanan: `daftar: List[[Item, int]]`
    - Status Pesanan: `status: str`
- Metode:
    - Konstruktor: `__init__(self, id: int, items: List[Item], status: str)`
    - Menambah menu: `tambah_item(self, item: Item, qty: int)`
    - Mengedit menu: `edit_item(self, item_id: int, qty: int)`
    - Menghapus menu: `hapus_item(self, item_id: int)`
    - String konverter: `__str__(self) -> str`

#### 3. `class Item`
Kelas ini akan berisi objek tentang menu makanan dan minuman yang ada di menu restoran.    
- Atribut:
    - ID Menu: `id: int`
    - Nama: `nama: str`
    - Harga: `harga: int`
- Methods:
    - Konstruktor: `__init__(self, id: int, name: str, price: float)`
    - String konverter: `__str__(self) -> str`

### Algoritma

## Implementasi Program
