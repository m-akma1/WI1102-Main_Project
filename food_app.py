"""
SISTEM PEMESANAN MAKANAN
PROJEK 1 MATA KULIAH WI1102 - BERPIKIR KOMPUTASIONAL
KELAS 31 - KELOMPOK 5:
1. 19624218 Tiara Clianta Andiwi
2. 19624235 Muhammad Akmal
3. 19624250 Ahmad Rinofaros Muchtar
4. 19624264 Muh. Hartawan Haidir
5. 19624284 Muthia Ariesta Anggraeni

(c) 2024. Bandung. Sekolah Teknik Elektro dan Informatika. Institut Teknologi Bandung.
"""

"""
DESKRIPSI
Program ini adalah simulasi dari sistem pemesanan makanan yang memungkinkan pengguna untuk memesan makanan dari meja mereka dan diberitahu saat pesanan mereka sudah siap. Program ini terdiri dari dua sisi: *sisi server* dan *sisi klien* yang disatukan dalam satu sisi antarmuka. 

Sisi server bertanggung jawab untuk mengelola database menu, antrean pesanan, dan memproses pesanan. Sisi klien bertanggung jawab untuk menampilkan menu, mengambil pesanan pengguna, dan memberitahu pengguna saat pesanan sudah siap. Sisi antarmuka menyatukan kedua sisi agar dapat berjalan dalam satu logika yang selaras.
"""

"""
KAMUS
Modul yang digunakan:
- `enum`
- `datetime`
- `time`

Kelas yang didefinisikan:
- `Item`
- `Status`
- `Order`
- `User`
- `Admin`
- `CLI_Interface`

Variabel global:
- `Menu: list[Item]`
- `header: CLI_Interface`
- `main_program: CLI_Interface`
"""

# ALGORITMA

## Impor modul yang diperlukan
import enum     # Modul Enumerasi, digunakan untuk membuat alias untuk mempermudah pengkategorian status pesanan
import datetime # Modul Tanggal dan Waktu, digunakan untuk mendapatkan data waktu dari komputer dalam membuat ID
import time     # Modul waktu untuk menunda tiap output agar tampilan lebih cantik

## Definisi kelas yang digunakan dalam program

class Item:
    """
    Representasi objek dari menu makanan atau minuman yang ada di menu restoran.
    
    Atribut Global:
    - Penghitung item: `counter: int`
    - Menu: `menu: dictionary`

    Atribut Lokal:
    - ID Menu: `ID: int`
    - Nama: `nama: str`
    - Harga (Rp): `harga: int`

    Argumen initialisasi: `Item(nama: str, harga: int) -> Item`
    """
    counter = 0 # Jumlah item yang telah dibuat
    menu = {}   # Daftar menu yang ada
    def __init__(self, nama: str, harga: int):
        Item.counter += 1
        self.nama = nama
        self.harga = harga
        self.ID = Item.counter
        Item.menu[self.ID] = self

    def lihat_menu() -> str:
        """Membuat string untuk mencetak daftar menu makanan dan minuman."""
        # Output adalah variabel string sebagai kontainer sementara hingga f-string selesai diprint
        output = "\n"
        output += f"^" * 38 + "\n"
        output += "{}\n".format("Menu Makanan dan Minuman".center(38, "-"))
        output += f" {'ID'} | {'Item':^15} | {'Harga':^15}\n"
        output += f"-" * 38 + "\n"
        for item in Item.menu.values():
            output += f"{item}\n"
        output += f"^" * 38 + "\n"
        return output

    
    def __str__(self):
        return f"#{self.ID:02d} | {self.nama:<15} | Rp {self.harga:10,.2f}"

class Status(enum.Enum):
    """Enumerasi status pesanan untuk mempermudah pengelompokan."""
    PENDING = "Menunggu dikonfirmasi"
    CANCELED = "Dibatalkan"
    CONFIRMED = "Dikonfirmasi, dalam antrean"
    IN_PROGRESS = "Dalam proses"
    READY = "Siap diambil"
    COMPLETED = "Selesai"

class Order:
    """
    Representasi sebuah pesanan.
    
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
    """
    counter = 0 # Jumlah order yang telah dibuat
    riwayat = {} # Daftar order yang telah dibuat
    antrean = [] # Antrean order yang belum diproses
    def __init__(self, meja: int, user: "User"):
        self.meja = meja
        self.user = user
        self.items = []
        self.total = 0
        self.jumlah = 0
        self.status = Status.PENDING
        self.ID = self.id_generator()
        Order.riwayat[self.ID] = self

    def id_generator(self) -> str:
        """
        Membuat ID komposit unik dengan format:
        `O-XXX-NO-USR--HHMMSS`
          - `O` mengindikasikan ini adalah ID Order (Pesanan)
          - `XXX` mengindikasikan nomor order
          - `NO` adalah 2 digit nomor meja
          - `USR` menunjuk pada inisial user
          - `HHMMSS` adalah waktu ketika pesanan dibuat
        """
        Order.counter += 1
        timestamp = datetime.datetime.now().strftime("%H%M%S")
        return f"O-{Order.counter:03d}-{self.meja:02d}-{self.user.ID[-3:]}-{timestamp}"
    
    def cek_total(self) -> int:
        """Menghitung total harga pesanan."""
        total = 0
        for item in self.items:
            total += item[0].harga * item[1]
        self.total = total
        return self.total

    def cek_jumlah(self) -> int:
        """Menghitung jumlah item dalam pesanan."""
        jumlah = 0
        for item in self.items:
            jumlah += item[1]
        self.jumlah = jumlah
        return self.jumlah
    
    def tambah_item(self, item: Item, qty: int):
        """
        Menambahkan item ke dalam pesanan jika belum ada.
        Jika sudah ada, tambahkan jumlahnya.
        """
        for row in self.items:
            if row[0] == item:
                row[1] += qty
                return
        self.items.append([item, qty])
    
    def edit_item(self, item: "Item", qty: int):
        """Mengedit jumlah item dalam pesanan jika ada."""
        try:
            self.items[self.items.index(item)][1] = qty
            if qty <= 0:
                self.hapus_item(item)
        except:
            print("Item tidak ditemukan.")
    
    def hapus_item(self, item: "Item"):
        """Menghapus item dari pesanan jika ada."""
        try: 
            self.items.pop(self.items.index(item))
        except:
            print("Item tidak ditemukan.")
        
    def edit_status(self, status):
        """Mengubah status pesanan."""
        self.status = status

    def cetak_struk(self) -> str:
        """Membuat string untuk mencetak struk pesanan."""
        output = "~" * 67 + "\n"
        output += f"ID Pesanan: {self.ID:>54}\n"
        output += f"Nama: {self.user.nama:}\n"
        output += f"Telp: {self.user.telp}\n"
        output += f"Meja: {self.meja:02d}\nStatus Pesanan: {self.status.value}\n"
        output += f"{'No':<2} |  ID | {'Item':^15} | {'Harga':^13} | {'Qty':^5} | {"Subtotal":^13}\n"
        output += "-" * 67 + "\n"
        for item in self.items:
            item: list[Item, int]
            output += f"{self.items.index(item)+1:02d} | {item[0]} | {item[1]:^5} | Rp {item[0].harga * item[1]:10,.2f}\n"
        output += "-" * 67 + "\n"
        output += f"Total | Rp {self.cek_total():,.2f}\n".rjust(67)
        output += "~" * 67 + "\n"
        return output

    def __str__(self):
        output = f"ID Pesanan: {self.ID}\n"
        output += f"Meja: {self.meja}\n"
        output += f"Status Pesanan: {self.status.value}\n"
        output += f"Jumlah Item: {self.cek_jumlah()}\n"
        output += f"Total Harga: Rp {self.cek_total():,.2f}\n"
        return output
    
class User:
    """
    Berisi semua informasi berkaitan dengan data pemesan.

    Atribut Global:
    - Penghitung user: `counter: int`
    - Daftar: `daftar: dictionary`

    Atribut Lokal:
    - ID User: `ID: str`
    - Nama: `nama: str`
    - Telepon: `telp: str`
    - Daftar Pesanan: `orders: dictionary`
    """

    counter = 0 # Jumlah user yang telah dibuat
    daftar = {} # Daftar user yang ada
    def __init__(self, nama: str, telp: str):
        self.nama = nama
        self.telp = telp
        self.orders = {}
        self.ID = self.id_generator()
        User.daftar[self.ID] = self
        return
    
    def id_generator(self) -> str:
        """
        Membuat ID komposit unik dengan format:
        U-XXX-ABC:
          - U mengindikasikan ini adalah ID User
          - XXX adalah urutan nomor user yang dibuat
          - ABC adalah inisial nama user
        """
        initial = self.nama[:3].upper()
        User.counter += 1
        return f"U-{User.counter:03d}-{initial}"

    def tambah_order(self, order: Order):
        """Menambahkan pesanan ke dalam daftar pesanan pengguna."""
        self.orders[order.ID] = order
        Order.antrean.append(order)
        order.status = Status.CONFIRMED

    def lihat_daftar(self) -> str:
        """Melihat daftar pesanan yang dimiliki pengguna."""
        output = ""
        for order in self.orders.values():
            output += f"{order}\n"
        return output
    
    def notifikasi(self, order: Order):
        """
        Memberitahu pengguna bahwa pesanannya sudah siap.
        Ke depannya jika memungkinkan akan mengirim SMS Notifikasi
        """
        print(f"Pesanan {order.ID} sudah siap diambil, mengirim notifikasi...")
        time.sleep(1)
        print(f"Notifikasi berhasil dikirim ke +{self.telp} dengan kode {order.ID[-3:]}")
        order.status = Status.COMPLETED

    def __str__(self):
        output = f"User ID: {self.ID}\n"
        output += f"Nama: {self.nama}\n"
        output += f"Telepon: {self.telp}\n"
        return output
    
class Admin:
    """
    Berisi semua informasi berkaitan dengan data dan perintah admin.

    Atribut (tersembunyi):
    - Username: `_username: str`
    - Password: `_password: str`

    Atribut Lokal:
    - Autentikasi: `auth: bool`

    Argumen initialisasi: `Admin(username: str, password: str) -> Admin`
    Untuk menggunakan kemmampuan Admin, Admin harus login terlebih dahulu.
    """
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password
        self.auth = False
        return
    
    def login(self, username: str, password: str) -> bool:
        """Login ke sistem dengan memasukkan password."""
        if username == self._username:
            if password == self._password:
                self.auth = True
                print("Login berhasil!")
                return True
            else:
                print("Password salah.")
                return False
        else:
            print("Username tidak dikenal.")
            return False

    def logout(self):
        """Logout dari sistem."""
        if self.auth:
            self.auth = False
            print("Logout berhasil.")
        else:
            print("Anda belum login.")

    def lihat_antrean(self):
        """Melihat semua pesanan yang belum diproses."""
        if not self.auth:
            print("Anda harus login terlebih dahulu.")
            return
        
        if not Order.antrean:
            print("Antrean kosong\n")
            return
        for urutan, order in enumerate(Order.antrean, start=1):
            print(f"#Urutan ke-{urutan}")
            print(f"{order}\n")
        
    def proses_order(self):
        """Mengambil pesanan terdepan dari antrean, mengubah statusnya, lalu memproses tiap itemnya."""
        if not self.auth:
            print("Anda harus login terlebih dahulu.")
            return
        
        if not Order.antrean:
            print("Antrean kosong\n")
            return
        order: Order = Order.antrean.pop(0)
        order.edit_status(Status.IN_PROGRESS)
        print(f"Memproses pesanan {order.ID}...")
        print("Untuk setiap pesanan, tekan Enter untuk konfirmasi item selesai diproses.\n")
        for i, item in enumerate(order.items, start=1):
            input(f"{i}. Memproses {item[1]} porsi {item[0].nama}...")
        
        self.selesai_order(order)

    def selesai_order(self, order: Order):
        """
        Menyelesaikan pesanan, mengubah statusnya, dan memberitahu pengguna.
        """
        if not self.auth:
            print("Anda harus login terlebih dahulu.")
            return
        
        order.edit_status(Status.READY)
        print(f"Pesanan {order.ID} selesai diproses.\n")
        print(order.cetak_struk())
        order.user.notifikasi(order)

class CLI_Interface:
    """
    Antarmuka antara sisi klien dan sisi server dalam bentuk CLI (Command Line Interface).
    """
    admin = Admin("admin", "admin")
    def __init__(self):
        pass

    def print_dl(self, text: str, **kwargs):
        """Mencetak baris dengan jeda waktu tertentu."""
        print(text, **kwargs)
        time.sleep(0.5)

    def print_dc(self, text: str, **kwargs):
        """Mencetak karakter dengan jeda waktu tertentu."""
        for char in text:
            print(char, end="")
            time.sleep(0.005)
        print(**kwargs)

    def header_halaman(self, pesan: str):
        """Membuat header pada halalamn"""
        self.print_dc("\n" + f"#{'=' * 100}#")
        self.print_dc(f"{pesan.center(100, "-")}")
        self.print_dc(f"#{'=' * 100}#" + "\n")

    def valid(self):
        """Validasi masukan berupa Pertanyaan Ya/Tidak"""
        while True:
            masukan =input("(Y/T) > ")
            if masukan == "Y" or masukan == "y":
                return True
            elif masukan == "T" or masukan == "t":
                return False
            else:
                self.print_dl("Masukan tidak dikenal.\n")

    def keluar(self):
        """Konfirmasi untuk keluar Program"""
        self.header_halaman("KELUAR")
        self.print_dl("Apakah Anda yakin ingin keluar dari aplikasi?", end = " ")
        if self.valid():
            exit()
        return

    def halaman_utama(self):
        """Halaman utama dan pertama ketika memulai program"""
        while True:
            self.header_halaman("HALAMAN UTAMA")
            self.print_dc(f"Pilih peran:")
            self.print_dc("1. Koki")
            self.print_dc("2. Pengguna")
            self.print_dc("X. Keluar")
            peran = input("> ")
            if peran == "1":
                self.masuk_koki()
            elif peran == "2":
                self.portal_pengguna()
            elif peran == "X" or peran == "x":
                self.keluar()
            else:
                self.print_dl("Masukan tidak dikenal.\n")
    
    def masuk_koki(self):
        """Portal masuk bagi koki."""
        self.header_halaman("MASUK: KOKI")
        while True:
            username = input("Username: > ")
            password = input("Password: > ")
            if CLI_Interface.admin.login(username, password):
                self.beranda_koki()
                break
            else:
                self.print_dl("Login gagal. Coba lagi?", end = " ")
                if not self.valid():
                    return

    def beranda_koki(self):
        """"Halaman beranda bagi koki"""
        self.header_halaman("BERANDA KOKI")
        while True:
            self.print_dc("A. Lihat Antrean")
            self.print_dc("B. Proses Pesanan")
            self.print_dc("C. Riwayat Pesanan")
            self.print_dc("X. Logout")
            pilihan = input("> ")
            if pilihan == "A" or pilihan == "a":
                self.header_halaman("ANTREAN PESANAN")
                CLI_Interface.admin.lihat_antrean()
            elif pilihan == "B"or pilihan == "b":
                self.header_halaman("PROSES PESANAN")
                self.print_dc("Anda akan memproses pesanan terdepan. Lanjutkan?", end = " ")
                if self.valid():
                    CLI_Interface.admin.proses_order()
            elif pilihan == "C"or pilihan == "c":
                self.header_halaman("RIWAYAT PESANAN")
                if not Order.riwayat:
                    self.print_dl("Antrean kosong\n")
                else:
                    for order in Order.riwayat.values():
                        self.print_dl(order)
            elif pilihan == "X" or pilihan == "x":
                self.print_dc("Anda akan logout dan kembali ke halaman utama. Lanjutkan?", end = " ")
                if self.valid():
                    self.admin.logout()
                    break
            else:
                self.print_dl("Masukan tidak dikenal.\n")
    
    def portal_pengguna(self):
        """Memisahkan pengguna yang sudah/belum punya User ID"""
        self.header_halaman("PORTAL PENGGUNA")
        self.print_dc("Apakah Anda sudah memiliki User ID?", end = " ")
        if self.valid():
            self.masuk_pengguna()
        else:
            self.daftar_pengguna()
    
    def masuk_pengguna(self):
        """Portal login dengan User ID"""
        self.header_halaman("MASUK PENGGUNA")
        while True:
            user_id = input("Masukkan User ID: > ")
            user = User.daftar.get(user_id)
            if user:
                telp = input("Masukkan No. Telepon: > ")
                self.beranda_pengguna(user)
                break
            else:
                print("User ID tidak ditemukan. Coba lagi?", end = " ")
                if not self.valid():
                    break
            
    def daftar_pengguna(self):
        """Membuat user baru dan login otomatis"""
        self.header_halaman("DAFTAR PENGUNA BARU")
        self.print_dl("Masukkan nama dan nomor telepon Anda!")
        self.print_dc("Keterangan: masukkan nomor telelpon dengan diawali 62\nContoh: 628123456789\n")
        while True:
            nama = input("Nama: > ").strip()
            if not nama.replace(" ", "").isalpha():
                self.print_dl("Nama hanya boleh berisi huruf dan/atau spasi!\n")
                continue
            telp = input("No. Telepon: > ").strip()
            if not (telp.startswith("628") and telp[3:].isdigit() and 8 <= len(telp[3:]) <= 12):
                self.print_dl("Nomor telepon harus dalam format 628XXXXXXXXX!\n")
                continue
            self.print_dc("Apakah data yang dimasukkan di atas sudah benar?", end = " ")
            if self.valid():
                user = User(nama, telp)
                self.print_dl("User berhasil dibuat!")
                self.print_dl(f"User ID Anda adalah: {user.ID}")
                self.beranda_pengguna(user)
                break
            else:
                self.print_dl("Silakan masukkan data kembali.\n")

    def beranda_pengguna(self, user: User):
        """Halaman beranda bagi pengguna"""
        self.header_halaman("BERANDA PENGGUNA")
        self.print_dl(user)
        self.print_dc(f"Selamat datang, {user.nama}!\n")
        while True:
            self.print_dc("A. Buat Pesanan Baru")
            self.print_dc("B. Lihat Daftar Pesanan")
            self.print_dc("X. Logout")
            pilihan = input("> ")
            if pilihan == "A" or pilihan == "a":
                self.buat_pesanan(user)
            elif pilihan == "B"or pilihan == "b":
                self.pesanan_pengguna(user)
            elif pilihan == "X" or pilihan == "x":
                self.print_dc("Anda akan logout dan kembali ke halaman utama. Lanjutkan?", end = " ")
                if self.valid():
                    break
            else:
                self.print_dl("Masukan tidak dikenal.")
                    
    def buat_pesanan(self, user: User):
        """Antarmuka membuat pesanann baru"""
        self.header_halaman("BUAT PESANAN BARU")
        while True:
            try: 
                meja = int(input("Masukkan Nomor Meja: "))
                self.print_dl("Apakah nomor meja sudah benar?", end = " ")
                if self.valid():
                    break
            except:
                self.print_dl("Masukan tidak valid.")
                continue
        order = Order(meja, user)
        self.print_dc(f"Pesanan untuk meja {meja} a.n. {user.nama} dibuat.")
        self.print_dc(Item.lihat_menu())
        self.print_dc("Masukkan ID menu yang ingin dipesan dan jumlahnya.")
        while True:
            try:
                item_id = input("\nID Menu: > ")
                item = Menu[int(item_id)-1]
                qty = int(input("Jumlah: > "))
                if not (qty > 0):
                    self.print_dl("Jumlah harus berupa bilangan positif")
                    continue
            except:
                self.print_dl("Masukan tidak valid.")
                continue
            self.print_dc(f"Anda memilih: {item} | {qty} porsi")
            self.print_dl("Konfirmasi Item?", end = " ")
            if self.valid():
                order.tambah_item(item, qty)
                self.print_dl("Item berhasil ditambahkan.")
                self.print_dl("Tambah item?", end = " ")
                if self.valid():
                    continue
                else:
                    break        
        self.print_dc(f"\n{"KONFIRMASI PESANAN":^67}")
        self.print_dl(order.cetak_struk())
        self.print_dc("Konfirmasi Pesanan?")
        self.print_dl("Pesanan yang telah dikonfirmasi tidak bisa dibatalkan dan akan dikenakan biaya total.")
        if self.valid():
            user.tambah_order(order)
            self.print_dl("Pesanan berhasil dikonfirmasi!")
        else:
            order.edit_status(Status.CANCELED)
            self.print_dl("Pesanan dibatalkan.")
        self.print_dl("\nAnda kembali ke menu pengguna.")

    def pesanan_pengguna(self, user: User):
        """Antarmuka daftar pesanan pengguna"""
        self.header_halaman("DAFTAR PESANAN PENGGUNA")
        self.print_dl(user.lihat_daftar())
        self.print_dc("Apakah Anda ingin melihat detail pesanan?", end = " ")
        if self.valid():
            while True:
                order_id = input("Masukkan ID Pesanan: ")
                order: Order = user.orders.get(order_id)
                if order:
                    self.print_dl(order.cetak_struk())
                    break
                else:
                    self.print_dc("Pesanan tidak ditemukan. Coba lagi?", end = " ")
                    if not self.valid():
                        break
        self.print_dl("\nAnda kembali ke menu pengguna.")

## Inisialisasi Program

### Daftar Menu
Menu = [
    Item("Ayam Goreng", 10000),
    Item("Ayam Bakar", 12000),
    Item("Ayam Geprek", 15000),
    Item("Ayam Kremes", 12000),
    Item("Bakso Sapi", 10000),
    Item("Bakso Beranak", 12000),
    Item("Mie Ayam", 12000),
    Item("Mie Goreng", 12000),
    Item("Mie Rebus", 12000),
    Item("Mie Pangsit", 12000),
    Item("Soto Ayam", 15000),
    Item("Soto Betawi", 20000),
    Item("Soto Padang", 25000),
    Item("Sate Ayam", 15000),
    Item("Sate Kambing", 20000),
    Item("Sate Padang", 25000),
    Item("Nasi Putih", 5000),
    Item("Nasi Goreng", 15000),
    Item("Nasi Uduk", 12000),
    Item("Nasi Kuning", 12000),
    Item("Air Mineral", 3000),
    Item("Es Teh", 5000),
    Item("Es Jeruk", 6000),
    Item("Es Campur", 8000),
    Item("Jus Alpukat", 10000),
    Item("Jus Mangga", 10000),
    Item("Jus Jeruk", 10000),
]

### Menjalankan Program
header = CLI_Interface()
header.print_dc(" ")
header.print_dc("~"*100)
header.print_dc("PANDA MANIS".center(100))
header.print_dc("kaPAN DApat MAkanan gratISnya?".center(100))
header.print_dc("~"*100)

main_program = CLI_Interface().halaman_utama()