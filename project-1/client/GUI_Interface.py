import os        # Import modul os untuk mengakses path logo
import ctypes    # Import modul ctypes untuk mengatur DPI agar GUI lebih jelas
import tkinter as tk # Import modul tkinter sebagai tk untuk membuat GUI
from tkinter import messagebox, font # Untuk menampilkan pesan error atau informasi dan mengubah font
from PIL import Image, ImageTk # Import modul Image dan ImageTk dari PIL untuk menampilkan gambar
from client.user import User # Import class User dari file user.py
from server.item import Item # Import class Item dari file item.py
from server.order import Order, Status # Import class Order dan Enum Status dari file order.py

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Meningkatkan kualitas tampilan GUI pada layar dengan DPI tinggi
except Exception:
    pass

class GUI_Interface:
    """
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
    - `header: tk.Label` -> Label untuk judul halaman

    Argumen initialisasi: `GUI_Interface(root: tk.Tk) -> GUI_Interface`

    Metode:
    - `mulai_hal()`: Fungsi pembantu untuk menginisiasi pembuatan halaman
    - `buat_frame()`: Fungsi pembantu untuk menginisiasi grid pada halaman
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
    """
    font_family = "Segoe UI"
    fsize_t = 18
    fsize_h1 = 14
    fsize_h2 = 12
    fsize_h3 = 10
    fsize_n = 8

    def __init__(self, root: tk.Tk):
        self.root: tk.Tk = root
        self.root.title("Sistem Pemesanan Makanan")
        
        # Set font default
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family=self.font_family, size=self.fsize_n)
        
        # Set ukuran jendela
        window_width = 600
        window_height = 700
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Dapatkan ukuran layar monitor
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Hitung posisi jendela agar berada di tengah layar
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        
        # Set posisi jendela
        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y-30}")
        self.root.resizable(True, True)
        self.hal_utama()

    def mulai_hal(self):
        """Fungsi pembantu untuk menginisiasi pembuatan halaman"""
        # Membersihkan isi jendela sembelum mengisinya dengan widget baru
        for widget in self.root.winfo_children():
            widget.destroy()

    def buat_frame(self) -> tk.Frame:
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
        tk.Label(self.root, text="PANDA MANIS", font=(self.font_family, self.fsize_t)).pack(pady=(20, 0))
        tk.Label(self.root, text="kaPAN DApat MAkaNan gratISnya?", font=(self.font_family, self.fsize_h1)).pack(pady=5)

        # Path Logo Meme
        current_dir = os.path.dirname(__file__)
        image_path = os.path.join(current_dir, "logo.jpeg")

        try:
            # Tampilkan Gambar
            self.image = Image.open(image_path)
            self.image = self.image.resize((146, 194), Image.LANCZOS) 
            self.image = ImageTk.PhotoImage(self.image)
            label_image = tk.Label(self.root, image=self.image)
            label_image.pack(pady=10)
        except FileNotFoundError:
            # Jika gambar tidak ditemukan
            pass

        # Label Info
        tk.Label(self.root, text="Projek I Kelompok 5", font=(self.font_family, self.fsize_h2)).pack(pady=(20, 5))
        tk.Label(self.root, text="Berpikir Komputasional - WI1102 Kelas 31", font=(self.font_family, self.fsize_h2)).pack(pady=5)
        tk.Label(self.root, text="Sistem Pemesanan Makanan", font=(self.font_family, self.fsize_h2)).pack(pady=(5, 10))
        tk.Label(self.root, text="Selamat Datang!", font=(self.font_family, self.fsize_t)).pack(pady=20)

        # Tombol Daftar Pengguna Baru
        self.tombol_daftar = tk.Button(self.root, text="Pengguna Baru", width=15, height=2, command=self.hal_daftar_pengguna)
        self.tombol_daftar.pack(pady=10)
        
        # Tombol Masuk bagi Pengguna Lama        
        self.tombol_masuk = tk.Button(self.root, text="Login Pengguna", width=15, height=2, command=self.hal_masuk_pengguna)
        self.tombol_masuk.pack(pady=10)

        # Tombol Keluar
        self.tombol_keluar = tk.Button(self.root, text="Keluar", width=15, height=2, command=self.root.quit)
        self.tombol_keluar.pack(pady=10)

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
        messagebox.showinfo("Berhasil", f"User berhasil dibuat dengan ID: {user.ID}\n Ingat ID Anda untuk masuk selanjutnya.")
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
        user_ditemukan: User = User.daftar.get(userID)
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
            tk.Label(frame_order_history, text="Lihat Pesanan", font=(self.font_family, 12)).grid(row=0, column=4, padx=5, pady=5, sticky='nsew')

            # Menampilkan data pesanan
            for idx, order in enumerate(user.orders.values(), start=1):
                order: Order
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

        # Menampilkan detail item
        for idx, (item, qty) in enumerate(order.items, start=1):
            item: Item
            subtotal = item.harga * qty
            tk.Label(frame_item, text=f"{idx}").grid(row=idx + 1, column=0, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"#{item.ID:02}").grid(row=idx + 1, column=1, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"{item.nama}").grid(row=idx + 1, column=2, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"{qty}").grid(row=idx + 1, column=3, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"Rp {item.harga:,.2f}").grid(row=idx + 1, column=4, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"Rp {subtotal:,.2f}").grid(row=idx + 1, column=5, sticky='w', padx=10, pady=2)
        tk.Label(frame_detail, text=f"Total Harga: Rp {order.cek_total():,.2f}", font=(self.font_family, self.fsize_n)).grid(row=8, column=0, columnspan=2, pady=10, sticky='n')

        # Tombol untuk kembali
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

        # Frame kontainer
        tk.Label(frame_pesanan, text="Daftar Menu", font=(self.font_family, self.fsize_h2)).grid(row=3, column=0, columnspan=2, pady=10, sticky='nsew')
        frame_canvas = tk.Frame(frame_pesanan, width=600)
        frame_canvas.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="n")
        frame_canvas.grid_columnconfigure(0, weight=1)

        # Scrollbar untuk daftar menu
        canvas = tk.Canvas(frame_canvas)
        canvas.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        scrollbar = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame untuk menampilkan daftar menu
        frame_menu = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame_menu, anchor='nw')
        frame_menu.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        frame_menu.grid_columnconfigure(0, weight=1)

        # Header Tabel Menu
        tk.Label(frame_menu, text="ID").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        tk.Label(frame_menu, text="Item").grid(row=0, column=1, sticky='w', padx=5, pady=2)
        tk.Label(frame_menu, text="Harga").grid(row=0, column=2, sticky='w', padx=5, pady=2)
        tk.Label(frame_menu, text="Qty").grid(row=0, column=3, sticky='w', padx=5, pady=2)

        # Menampilkan daftar menu dan menerima input jumlah pesanan
        self.entries_qty = {}
        for item_id, item in Item.menu.items():
            item: Item
            tk.Label(frame_menu, text=f"#{item.ID}").grid(row=item_id, column=0, sticky='w', padx=5, pady=2)
            tk.Label(frame_menu, text=item.nama).grid(row=item_id, column=1, sticky='w', padx=5, pady=2)
            tk.Label(frame_menu, text=f"Rp {item.harga:,.2f}").grid(row=item_id, column=2, sticky='w', padx=5, pady=2)
            entry_qty = tk.Entry(frame_menu, width=5)
            entry_qty.grid(row=item_id, column=3, padx=5, pady=2)
            self.entries_qty[item] = entry_qty
        
        # Tombol untuk konfirmasi pesanan
        tk.Button(frame_pesanan, text="Konfirmasi Pesanan", command=lambda: self.hal_konfirmasi_pesanan(user)).grid(row=5, column=0, columnspan=2, pady=10, sticky='n')

        # Tombol untuk kembali
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
            entry: tk.Entry
            qty = entry.get()
            if qty.isdigit() and int(qty) > 0:
                items_pesanan.append((item, int(qty)))
        
        # Validasi Jumlah Item
        if not items_pesanan:
            messagebox.showwarning("Input Error", "Silakan masukkan jumlah untuk setidaknya satu item!")
            return
        
        self.mulai_hal()
        frame_konfirmasi = self.buat_frame()

        # Label Detail Pesanan
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

        # Menampilkan detail item
        total_harga = 0
        for idx, (item, qty) in enumerate(items_pesanan, start=1):
            item: Item
            subtotal = item.harga * qty
            total_harga += subtotal
            tk.Label(frame_item, text=f"{idx}").grid(row=idx + 1, column=0, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"#{item.ID:02}").grid(row=idx + 1, column=1, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"{item.nama}").grid(row=idx + 1, column=2, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"{qty}").grid(row=idx + 1, column=3, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"Rp {item.harga:,.2f}").grid(row=idx + 1, column=4, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"Rp {subtotal:,.2f}").grid(row=idx + 1, column=5, sticky='w', padx=10, pady=2)
        tk.Label(frame_konfirmasi, text=f"Total Harga: Rp {total_harga:,.2f}", font=(self.font_family, self.fsize_n+2)).grid(row=7, column=0, columnspan=2, pady=10, sticky='n')

        # Tombol untuk membuat pesanan
        tk.Button(frame_konfirmasi, text="Buat Pesanan", command=lambda: self.buat_pesanan(user, meja, items_pesanan)).grid(row=8, column=0, pady=5, sticky='n', columnspan=2)

        # Tombol untuk kembali
        tk.Button(frame_konfirmasi, text="Kembali", command=lambda: self.batalkan_pesanan(user, meja, items_pesanan)).grid(row=9, column=0, pady=5, sticky='n', columnspan=2)

    def buat_pesanan(self, user: User, meja: int, items_pesanan: list):
        """Membuat pesanan baru berdasarkan input dari pengguna"""
        pesanan_baru = Order(meja, user.ID)
        for item, qty in items_pesanan:
            pesanan_baru.tambah_item(item, qty)
        user.tambah_order(pesanan_baru)
        messagebox.showinfo("Berhasil", f"Pesanan berhasil dibuat dengan ID: {pesanan_baru.ID}")
        self.hal_beranda_user(user)

    def batalkan_pesanan(self, user: User, meja: int, items_pesanan: list):
        """Membatalkan pesanan yang sedang dibuat"""
        pesanan_baru = Order(meja, user.ID)
        for item, qty in items_pesanan:
            pesanan_baru.tambah_item(item, qty)
        user.tambah_order(pesanan_baru)
        pesanan_baru.edit_status(Status.CANCELED)
        Order.antrean.remove(pesanan_baru)
        messagebox.showinfo("Info", "Pesanan dibatalkan. Pesanan tetap akan ada di riwayat namun tidak akan diproses.")
        self.hal_beranda_user(user)

def run():
    """Fungsi untuk menjalankan aplikasi melalui GUI"""
    root = tk.Tk()
    app = GUI_Interface(root)
    root.mainloop()