import tkinter as tk    # Modul Tkinter, digunakan untuk membuat antarmuka pengguna
from tkinter import messagebox # Modul Tkinter, digunakan untuk membuat pesan pop-up
import enum     # Modul Enumerasi, digunakan untuk membuat alias untuk mempermudah pengkategorian status pesanan
import datetime # Modul Tanggal dan Waktu, digunakan untuk mendapatkan data waktu dari komputer dalam membuat ID

class Item:
    """
    Representasi objek dari menu makanan atau minuman yang ada di menu restoran.
    
    Atribut Lokal:
    - ID Menu: `ID: int`
    - Nama: `nama: str`
    - Harga (Rp): `harga: int`

    Argumen initialisasi: `(nama: str, harga: int) -> Item`

    Atribut Global:
    - Penghitung item: `counter: int`
    - Daftar menu: `menu: {} (dictionary -> key: ID, value: Item)`
    """
    counter = 0 # Jumlah item yang telah dibuat
    menu = {} # Dictionary untuk menyimpan menu
    def __init__(self, nama: str, harga: int):
        Item.counter += 1
        self.nama = nama
        self.harga = harga
        self.ID = Item.counter
        Item.menu[self.ID] = self
    
    def __str__(self):
        return f"#{self.ID:02d} | {self.nama:<15} | Rp {self.harga:10,.2f}"

class Status(enum.Enum):
    """Enumerasi status pesanan."""
    PENDING = "Menunggu dikonfirmasi"
    CONFIRMED = "Dikonfirmasi, dalam antrean"
    IN_PROGRESS = "Dalam proses"
    READY = "Siap diambil"
    COMPLETED = "Selesai"

class User:
    """
    Representasi pengguna (customer).
    
    Atribut Lokal:
    - ID User: `ID: str`
    - Nama: `nama: str`
    - Nomor Telepon: `telp: str`
    - Daftar Pesanan:`orders: {} (dictionary -> key: ID, value: Order)`

    Argumen initialisasi: `(nama: str, telp: str) -> User`

    Atribut Global:
    - Penghitung item: `counter: int`
    - Daftar user: `users: {} (dictionary -> key: ID, value: User)`
    """
    counter = 0 # Jumlah user yang telah dibuat
    users = {}  # Dictionary untuk menyimpan semua pengguna
    def __init__(self, nama: str, telp: str):
        User.counter += 1
        self.nama = nama
        self.telp = telp
        self.ID = self.id_generator()
        self.orders = {}
        User.users[self.ID] = self
    
    def id_generator(self):
        """Membuat ID unik untuk setiap pengguna."""
        initial = self.nama[:3].upper()
        return f"U-{User.counter:03d}-{initial}"

class Order:
    """
    Representasi sebuah pesanan.
    
    Atribut:
    - ID Pesanan: `id: str`
    - No. Meja: `no_meja: int`
    - User pemesan: `user: User`
    - Daftar Pesanan: `items: List[[Item, int]]`
    - Status Pesanan: `status: str`
    - Total harga: `total: int`

    Argumen initialisasi: `(meja: int, user: User) -> Order`
    """
    counter = 0 # Jumlah order yang telah dibuat
    history = [] # Daftar semua order yang telah dibuat
    def __init__(self, meja: int, user: "User"):
        self.meja = meja
        self.user = user
        self.items = []
        self.status = Status.PENDING
        self.ID = self.id_generator()
        Order.history.append(self)

    def id_generator(self):
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
    
    def cek_total(self):
        """Menghitung total harga pesanan."""
        self.total: int
        total = 0
        for item in self.items:
            total += item[0].harga * item[1]
        self.total = total
        return self.total

    def cek_jumlah(self):
        """Menghitung jumlah item dalam pesanan."""
        jumlah = 0
        for item in self.items:
            jumlah += item[1]
        return jumlah
    
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
        
    def cetak_struk(self):
        """Membuat string untuk mencetak struk pesanan."""
        output = "~" * 67 + "\n"
        output += f"ID Pesanan: {self.ID:>54}\n"
        output += f"Nama: {self.user.nama:}\n"
        output += f"Telp: {self.user.telp}\n"
        output += f"Meja: {self.meja:02d}\nStatus Pesanan: {self.status.value}\n"
        output += f"{'No':<2} |  ID | {'Item':^15} | {'Harga':^13} | {'Qty':^5} | {'Subtotal':^13}\n"
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
        output += f"   Meja: {self.meja}\n"
        output += f"   Status Pesanan: {self.status.value}\n"
        output += f"   Jumlah Item: {self.cek_jumlah()}\n"
        output += f"   Total Harga: Rp {self.cek_total():,.2f}\n"
        return output
    
# Daftar Menu
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

class Interface:
    """
    Antarmuka pengguna dalam bentuk window.
    
    Atribut Lokal:
    `root: tk.Tk` -> Jendela utama aplikasi

    Atribut Global:
    - 
    """
    font_family = "Arial"
    fsize_t = 20
    fsize_h1 = 16
    fsize_h2 = 14
    fsize_h3 = 12
    fsize_n = 10

    def __init__(self, root: tk.Tk):
        self.root: tk.Tk = root
        self.root.title("Food Ordering System")
        self.root.geometry("600x600")
        self.root.resizable(True, True)
        
        self.hal_utama()

    def mulai_hal(self):
        """Fungsi pembantu untuk menginisiasi pembuatan halaman"""
        # Membersihkan isi jendela sembelum mengisinya dengan widget baru
        for widget in self.root.winfo_children():
            widget.destroy()

    def buat_frame(self):
        """Fungsi pembantu untuk menginisiasi grid pada halaman"""
        # Persiapan membuat tata letak grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Frame untuk menampilkan dashboard
        frame = tk.Frame(self.root)
        frame.grid(row=0, column=0, sticky='nsew')
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        return frame
        
        
    def hal_utama(self):
        """Membuat antarmuka utama untuk memilih sebagai pengguna atau koki"""
        self.mulai_hal()
        
        # Label Judul
        self.header = tk.Label(self.root, text="Selamat Datang di Restoran", font=(self.font_family, self.fsize_t))
        self.header.pack(pady=20)

        # Tombol Daftar Pengguna Baru
        self.tombol_daftar = tk.Button(self.root, text="Pengguna Baru", width=15, height=2, command=self.hal_daftar_pengguna)
        self.tombol_daftar.pack(pady=10)
        
        # Tombol Masuk bagi Pengguna Lama        
        self.tombol_masuk = tk.Button(self.root, text="Login Pengguna", width=15, height=2, command=self.hal_masuk_pengguna)
        self.tombol_masuk.pack(pady=10)

        # Tombol Masuk sebagai Koki        
        self.tombol_koki = tk.Button(self.root, text="Koki", width=15, height=2, command=self.hal_masuk_koki)
        self.tombol_koki.pack(pady=10)

    def hal_daftar_pengguna(self):
        """Membuat antarmuka untuk pengguna baru untuk melakukan pemesanan"""
        self.mulai_hal()
        
        # Label Judul
        self.header = tk.Label(self.root, text="Daftar Pengguna Baru", font=(self.font_family, self.fsize_h1))
        self.header.pack(pady=20)

        # Kontainer masukan nama
        tk.Label(self.root, text="Nama: ").pack(pady=5)
        self.masukan_nama = tk.Entry(self.root)
        self.masukan_nama.pack(pady=10)

        # Kontainer masukan telepon
        tk.Label(self.root, text="Nomor Telepon: \nFormat: 628XXXXXXXX...").pack(pady=5)
        self.masukan_telp = tk.Entry(self.root)
        self.masukan_telp.pack(pady=10)

        # Tombol kirim
        tombol_kirim = tk.Button(self.root, text="Kirim", command=self.buat_user_baru)
        tombol_kirim.pack(pady=20)

        # Tombol kembali
        tombol_kembali = tk.Button(self.root, text="Kembali", command=self.hal_utama)
        tombol_kembali.pack(pady=5)

    def hal_masuk_pengguna(self):
        """Membuat antarmuka untuk pengguna yang sudah ada untuk login"""
        self.mulai_hal()
        
        # Label Judul
        self.header = tk.Label(self.root, text="Login Pengguna", font=(self.font_family, self.fsize_h1))
        self.header.pack(pady=20)

        # Kontainer masukan User ID
        tk.Label(self.root, text="Masukkan User ID: ").pack(pady=5)
        self.masukan_userID = tk.Entry(self.root)
        self.masukan_userID.pack(pady=10)

        # Kontainer masukan Telepon
        tk.Label(self.root, text="Masukkan Nomor Telepon: ").pack(pady=5)
        self.masukan_telp_ = tk.Entry(self.root)
        self.masukan_telp_.pack(pady=10)

        # Tombol Masuk
        tombol_masuk = tk.Button(self.root, text="Masuk", command=self.masuk_user)
        tombol_masuk.pack(pady=20)

        # Tombol Kembali
        tombol_kembali = tk.Button(self.root, text="Kembali", command=self.hal_utama)
        tombol_kembali.pack(pady=5)

    def buat_user_baru(self):
        """Membuat order baru berdasarkan input dari pengguna"""
        nama = self.masukan_nama.get().strip()
        telp = self.masukan_telp.get().strip()

        # Validasi Nama
        if not (nama.replace(" ", "").isalpha()):
            messagebox.showwarning("Input Error", "Nama hanya boleh mengandung huruf dan spasi!")
            return
        
        # Validasi Nomor Telepon
        if not (telp.startswith("628") and telp[3:].isdigit() and 8 <= len(telp[3:]) <= 12):
            messagebox.showwarning("Input Error", "Nomor telepon harus dalam format 628XXXXXXXXX!")
            return
        
        # Buat user baru
        user = User(nama, telp)
        messagebox.showinfo("Berhasil", f"User berhasil dibuat dengan ID: {user.ID}")
        self.hal_beranda_user(user)

    def masuk_user(self):
        """Fungsi untuk login pengguna yang sudah ada"""
        userID = self.masukan_userID.get().strip()
        telp = self.masukan_telp_.get().strip()

        # Validasi input
        if not (userID and telp):
            messagebox.showwarning("Input Error", "Semua bidang harus diisi!")
            return
        
        # Cek apakah user ditemukan
        user_ditemukan = User.users.get(userID)
        if not user_ditemukan:
            messagebox.showerror("Login Gagal", "Pengguna tidak ditemukan!")
        else:
            if user_ditemukan.telp == telp:
                messagebox.showinfo("Login Berhasil", f"Selamat datang kembali, {user_ditemukan.nama}!")
                self.hal_beranda_user(user_ditemukan)
            else:
                messagebox.showerror("Login Gagal", "Nomor telepon tidak sesuai User ID!")

    def hal_beranda_user(self, user: User):
        """Membuat antarmuka beranda setelah login pengguna."""
        self.mulai_hal()
        frame_dashboard = self.buat_frame()
        
        # Label Judul
        tk.Label(frame_dashboard, text=f"Halo, {user.nama}!", font=(self.font_family, self.fsize_h1), anchor='center').grid(row=0, column=0, columnspan=4, pady=10, sticky='nsew')
        
        # Label Detail Pengguna
        tk.Label(frame_dashboard, text=f"User ID: {user.ID}", font=(self.font_family, self.fsize_n), anchor="w").grid(row=1, column=0, columnspan=4, padx=20, pady=2, sticky='nsew')
        tk.Label(frame_dashboard, text=f"Nama: {user.nama}", font=(self.font_family, self.fsize_n), anchor="w").grid(row=2, column=0, columnspan=4, padx=20, pady=2, sticky='nsew')
        tk.Label(frame_dashboard, text=f"Nomor Telepon: {user.telp}", font=(self.font_family, self.fsize_n), anchor="w").grid(row=3, column=0, columnspan=4, padx=20,  pady=2, sticky='nsew')
        
        # Bagian Riwayat Pesanan
        tk.Label(frame_dashboard, text="Riwayat Pesanan", font=(self.font_family, self.fsize_h2), anchor='center').grid(row=4, column=0, columnspan=4, pady=5, sticky='nsew')
        
        # Frame untuk menampilkan riwayat pesanan
        frame_order_history = tk.Frame(frame_dashboard, width=600)
        frame_order_history.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="n")
        frame_order_history.grid_columnconfigure(0, weight=1)
        
        if user.orders:
            # Membuat header tabel riwayat pesanan
            tk.Label(frame_order_history, text="Order ID", font=(self.font_family, 12)).grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Meja", font=(self.font_family, 12)).grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Status", font=(self.font_family, 12)).grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Total", font=(self.font_family, 12)).grid(row=0, column=3, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Lihat Pesanan").grid(row=0, column=4, padx=5, pady=5, sticky='nsew')

            # Menampilkan data pesanan
            for idx, order in enumerate(user.orders.values(), start=1):
                tk.Label(frame_order_history, text=f"{order.ID}").grid(row=idx, column=0, padx=5, pady=2, sticky='nsew')
                tk.Label(frame_order_history, text=f"{order.meja}").grid(row=idx, column=1, padx=5, pady=2, sticky='nsew')
                tk.Label(frame_order_history, text=f"{order.status.value}").grid(row=idx, column=2, padx=5, pady=2, sticky='nsew')
                tk.Label(frame_order_history, text=f"Rp {order.cek_total():,.2f}").grid(row=idx, column=3, padx=5, sticky='nsew')
                tk.Button(frame_order_history, text="Lihat", command=lambda o=order: self.hal_lihat_pesanan(user, o)).grid(row=idx, column=4, padx=5, pady=2, sticky='nsew')
        else:
            # Jika belum ada riwayat pesanan
            tk.Label(frame_dashboard, text="Belum ada riwayat pesanan.").grid(row=5, column=0, columnspan=4, pady=5)
        
        # Tombol untuk membuat pesanan baru
        tk.Button(frame_dashboard, text="Buat Pesanan Baru", command=lambda: self.hal_buat_pesanan_baru(user)).grid(row=len(user.orders) + 6, column=0, columnspan=1, pady=10)
        
        # Tombol Keluar
        tk.Button(frame_dashboard, text="Keluar", command=self.hal_utama).grid(row=len(user.orders) + 6, column=1, columnspan=2, pady=10)

    def hal_lihat_pesanan(self, user: User, order: Order):
        """Membuat antarmuka untuk melihat detail pesanan."""
        self.mulai_hal()
        frame_detail = self.buat_frame()

        # Label Detail Pesanan
        tk.Label(frame_detail, text="Detail Pesanan", font=(self.font_family, self.fsize_h1)).grid(row=0, column=0, columnspan=2, pady=10, sticky='nsew')
        tk.Label(frame_detail, text=f"User: {user.nama}", font=(self.font_family, self.fsize_n), anchor="e").grid(row=1, column=0, sticky='w', padx=10, pady=2)
        tk.Label(frame_detail, text=f"User ID: {user.ID}", font=(self.font_family, self.fsize_n), anchor="e").grid(row=2, column=0, sticky='w', padx=10, pady=2)
        tk.Label(frame_detail, text=f"Telepon: {user.telp}", font=(self.font_family, self.fsize_n), anchor="e").grid(row=3, column=0, sticky='w', padx=10, pady=2)
        tk.Label(frame_detail, text=f"Order ID: {order.ID}", font=(self.font_family, self.fsize_n), anchor="e").grid(row=4, column=0, sticky='w', padx=10, pady=2)
        tk.Label(frame_detail, text=f"Nomor Meja: {order.meja}", font=(self.font_family, self.fsize_n), anchor="e").grid(row=5, column=0, sticky='w', padx=10, pady=2)
        tk.Label(frame_detail, text=f"Status: {order.status.value}", font=(self.font_family, self.fsize_n), anchor="e").grid(row=6, column=0, sticky='w', padx=10, pady=2)

        # Frame untuk menampilkan Detail Item
        frame_item = tk.Frame(frame_detail, width=800)
        frame_item.grid(row=7, column=0, columnspan=2, padx=20, pady=10, sticky="n")
        frame_item.grid_columnconfigure(0, weight=1)
        
        # Label Detail Item
        tk.Label(frame_item, text="Detail Item", font=(self.font_family, self.fsize_h2)).grid(row=0, column=0, columnspan=6, pady=10, sticky='nsew')
        tk.Label(frame_item, text="No.", font=(self.font_family, self.fsize_n)).grid(row=1, column=0, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="ID", font=(self.font_family, self.fsize_n)).grid(row=1, column=1, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="Item", font=(self.font_family, self.fsize_n)).grid(row=1, column=2, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="Qty", font=(self.font_family, self.fsize_n)).grid(row=1, column=3, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="Harga", font=(self.font_family, self.fsize_n)).grid(row=1, column=4, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="Subtotal", font=(self.font_family, self.fsize_n)).grid(row=1, column=5, pady=5, sticky='nsew', padx=10)

        total_harga = 0
        for idx, (item, qty) in enumerate(order.items, start=1):
            subtotal = item.harga * qty
            total_harga += subtotal
            tk.Label(frame_item, text=f"{idx}").grid(row=idx + 1, column=0, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"#{item.ID:02}").grid(row=idx + 1, column=1, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"{item.nama}").grid(row=idx + 1, column=2, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"{qty}").grid(row=idx + 1, column=3, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"Rp {item.harga:,.2f}").grid(row=idx + 1, column=4, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"Rp {subtotal:,.2f}").grid(row=idx + 1, column=5, sticky='w', padx=10, pady=2)
                
        tk.Label(frame_detail, text=f"Total Harga: Rp {total_harga:,.2f}", font=(self.font_family, self.fsize_h3)).grid(row=8, column=0, columnspan=2, pady=10, sticky='n')
        tk.Button(frame_detail, text="Kembali", command=lambda: self.hal_beranda_user(user)).grid(row=9, column=0, columnspan=2, pady=5, sticky='n')

    def hal_buat_pesanan_baru(self, user: User):
        """Membuat antarmuka untuk membuat pesanan baru."""
        self.mulai_hal()
        frame_pesanan = self.buat_frame()
        
        # Label Judul
        tk.Label(frame_pesanan, text=f"Buat Pesanan Baru", font=(self.font_family, self.fsize_h1)).grid(row=0, column=0, columnspan=2, pady=10, sticky='nsew')

        # Kontainer Nomor Meja
        tk.Label(frame_pesanan, text="Nomor Meja: ").grid(row=1, column=0, columnspan=2, pady=10, sticky='nsew')
        self.masukan_meja = tk.Entry(frame_pesanan)
        self.masukan_meja.grid(row=2, column=0, columnspan=2, pady=10, sticky='n')

        # Frame untuk menampilkan daftar menu
        tk.Label(frame_pesanan, text="Daftar Menu", font=(self.font_family, self.fsize_h2)).grid(row=3, column=0, columnspan=2, pady=10, sticky='nsew')
        frame_canvas = tk.Frame(frame_pesanan, width=600)
        frame_canvas.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="n")
        frame_canvas.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(frame_canvas)
        canvas.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        scrollbar = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        frame_menu = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_menu, anchor='nw')
        frame_menu.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        frame_menu.grid_columnconfigure(0, weight=1)

        # Header Tabel Menu
        tk.Label(frame_menu, text="ID").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        tk.Label(frame_menu, text="Item").grid(row=0, column=1, sticky='w', padx=5, pady=2)
        tk.Label(frame_menu, text="Harga").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        tk.Label(frame_menu, text="Qty").grid(row=0, column=3, sticky='w', padx=5, pady=2)

        self.entries_qty = {}
        for item_id, item in Item.menu.items():
            tk.Label(frame_menu, text=f"#{item.ID}").grid(row=item_id, column=0, sticky='w', padx=5, pady=2)
            tk.Label(frame_menu, text=item.nama).grid(row=item_id, column=1, sticky='w', padx=5, pady=2)
            tk.Label(frame_menu, text=f"Rp {item.harga:,.2f}").grid(row=item_id, column=2, sticky='w', padx=5, pady=2)
            entry_qty = tk.Entry(frame_menu, width=5)
            entry_qty.grid(row=item_id, column=3, padx=5, pady=2)
            self.entries_qty[item] = entry_qty
        
        tk.Button(frame_pesanan, text="Konfirmasi Pesanan", command=lambda: self.hal_konfirmasi_pesanan(user)).grid(row=5, column=0, columnspan=2, pady=10, sticky='n')
        tk.Button(frame_pesanan, text="Kembali", command=lambda: self.hal_beranda_user(user)).grid(row=6, column=0, columnspan=2, pady=5, sticky='n')

    def hal_konfirmasi_pesanan(self, user: User):
        """Membuat antarmuka untuk konfirmasi pesanan yang akan dibuat."""
        meja = self.masukan_meja.get()

        # Validasi Nomor Meja
        if not (meja.isdigit() and 0 <= int(meja) <= 99):
            messagebox.showwarning("Input Error", "Nomor meja harus berupa angka antara 0 hingga 99!")
            return
        meja = int(meja)

        # Mengumpulkan item yang dipesan
        items_pesanan = []
        for item, entry in self.entries_qty.items():
            qty = entry.get()
            if qty.isdigit() and int(qty) > 0:
                items_pesanan.append((item, int(qty)))
        
        # Validasi Jumlah Item
        if not items_pesanan:
            messagebox.showwarning("Input Error", "Silakan masukkan jumlah untuk setidaknya satu item!")
            return
        
        # Membersihkan isi jendela sembelum mengisinya dengan widget baru
        for widget in self.root.winfo_children():
            widget.destroy()

        # Persiapan membuat tata letak grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Frame untuk menampilkan konfirmasi pesanan
        frame_konfirmasi = tk.Frame(self.root)
        frame_konfirmasi.grid(row=0, column=0, sticky='nsew')
        frame_konfirmasi.grid_columnconfigure(0, weight=1)

        tk.Label(frame_konfirmasi, text="Detail Pesanan", font=(self.font_family, self.fsize_h1)).grid(row=0, column=0, columnspan=2, pady=10, sticky='nsew')
        tk.Label(frame_konfirmasi, text=f"User: {user.nama}", font=(self.font_family, self.fsize_n), anchor="e").grid(row=1, column=0, sticky='w', padx=10, pady=2)
        tk.Label(frame_konfirmasi, text=f"User ID: {user.ID}", font=(self.font_family, self.fsize_n), anchor="e").grid(row=2, column=0, sticky='w', padx=10, pady=2)
        tk.Label(frame_konfirmasi, text=f"Telepon: {user.telp}", font=(self.font_family, self.fsize_n), anchor="e").grid(row=3, column=0, sticky='w', padx=10, pady=2)
        tk.Label(frame_konfirmasi, text=f"Nomor Meja: {meja}", font=(self.font_family, self.fsize_n), anchor="e").grid(row=4, column=0, sticky='w', padx=10, pady=2)
        tk.Label(frame_konfirmasi, text=f"Status: {Status.PENDING.value}", font=(self.font_family, self.fsize_n), anchor="e").grid(row=5, column=0, sticky='w', padx=10, pady=2)

        # Frame untuk menampilkan Detail Item
        frame_item = tk.Frame(frame_konfirmasi, width=800)
        frame_item.grid(row=6, column=0, columnspan=2, padx=20, pady=10, sticky="n")
        frame_item.grid_columnconfigure(0, weight=1)
        
        # Label Detail Item
        tk.Label(frame_item, text="Detail Item", font=(self.font_family, self.fsize_h2)).grid(row=0, column=0, columnspan=6, pady=10, sticky='nsew')
        tk.Label(frame_item, text="No.", font=(self.font_family, self.fsize_n)).grid(row=1, column=0, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="ID", font=(self.font_family, self.fsize_n)).grid(row=1, column=1, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="Item", font=(self.font_family, self.fsize_n)).grid(row=1, column=2, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="Qty", font=(self.font_family, self.fsize_n)).grid(row=1, column=3, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="Harga", font=(self.font_family, self.fsize_n)).grid(row=1, column=4, pady=5, sticky='nsew', padx=10)
        tk.Label(frame_item, text="Subtotal", font=(self.font_family, self.fsize_n)).grid(row=1, column=5, pady=5, sticky='nsew', padx=10)

        total_harga = 0
        for idx, (item, qty) in enumerate(items_pesanan, start=1):
            subtotal = item.harga * qty
            total_harga += subtotal
            tk.Label(frame_item, text=f"{idx}").grid(row=idx + 1, column=0, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"#{item.ID:02}").grid(row=idx + 1, column=1, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"{item.nama}").grid(row=idx + 1, column=2, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"{qty}").grid(row=idx + 1, column=3, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"Rp {item.harga:,.2f}").grid(row=idx + 1, column=4, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"Rp {subtotal:,.2f}").grid(row=idx + 1, column=5, sticky='w', padx=10, pady=2)
        
        tk.Label(frame_konfirmasi, text=f"Total Harga: Rp {total_harga:,.2f}", font=(self.font_family, self.fsize_h3)).grid(row=7, column=0, columnspan=2, pady=10, sticky='n')

        tk.Button(frame_konfirmasi, text="Buat Pesanan", command=lambda: self.buat_pesanan(user, meja, items_pesanan)).grid(row=8, column=0, pady=5, sticky='n')
        tk.Button(frame_konfirmasi, text="Kembali", command=lambda: self.hal_buat_pesanan_baru(user)).grid(row=9, column=0, pady=5, sticky='n')

    def buat_pesanan(self, user: User, meja: int, items_pesanan: list):
        """Membuat pesanan baru berdasarkan input dari pengguna"""
        pesanan_baru = Order(meja, user)
        for item, qty in items_pesanan:
            pesanan_baru.tambah_item(item, qty)
        user.orders[pesanan_baru.ID] = pesanan_baru
        messagebox.showinfo("Berhasil", f"Pesanan berhasil dibuat dengan ID: {pesanan_baru.ID}")
        self.hal_beranda_user(user)

    def hal_masuk_koki(self):
        messagebox.showinfo("Koki", "Antarmuka koki sedang dibuat...")

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
