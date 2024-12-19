import os
import ctypes
import tkinter as tk
from tkinter import messagebox, font, ttk
from PIL import Image, ImageTk # Import modul Image dan ImageTk dari PIL untuk menampilkan gambar
from server.admin import Admin
from server.order import Order, Status
from server.item import Item
from server.user import User

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Meningkatkan kualitas tampilan GUI pada layar dengan DPI tinggi
except Exception:
    pass

class admin_interface:
    """
    Class untuk membuat antarmuka admin.
    """
    font_family = "Segoe UI"
    fsize_t = 18
    fsize_h1 = 14
    fsize_h2 = 12
    fsize_h3 = 10
    fsize_n = 8
    
    # Path Logo 
    current_dir = os.path.dirname(__file__)
    image_path = os.path.join(current_dir, "new_logo.png")

    def __init__(self, root: tk.Tk, user_gui_class):
        # Inisialisasi jendela
        self.root = root
        self.root.withdraw()
        self.admin_window: tk.Tk = tk.Toplevel(root)
        self.user_gui_class = user_gui_class
        self.admin = Admin("afafufuf", "fufufafa")
        self.admin_window.title("Sistem Pemesanan Makanan - Admin")
        self.icon = ImageTk.PhotoImage(file=self.image_path)
        self.root.iconphoto(False, self.icon)

        # Set font default
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family=self.font_family, size=self.fsize_n)
        
        # Dapatkan ukuran layar monitor
        screen_width = self.admin_window.winfo_screenwidth()
        screen_height = self.admin_window.winfo_screenheight()

        # Set ukuran jendela
        window_width = 600
        window_height = 800
        
        # Hitung posisi jendela agar berada di tengah layar
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        
        # Set posisi jendela
        self.admin_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y-(window_height//20)}")
        self.admin_window.resizable(True, True)

        # Siapkan penghitung jendela user
        self.active_windows = {}
        self.win_counter = 0

        # Jalankan program
        self.hal_masuk_admin()
        self.buat_hal_user_baru()
        self.admin_window.protocol("WM_DELETE_WINDOW", self.tutup_hal)

    def mulai_hal(self):
        """Fungsi pembantu untuk menginisiasi pembuatan halaman"""
        # Membersihkan isi jendela sembelum mengisinya dengan widget baru
        for widget in self.admin_window.winfo_children():
            widget.destroy()

    def tutup_hal(self):
        """Fungsi untuk menutup jendela"""
        self.root.quit()
        self.root.destroy()

    def buat_frame(self) -> tk.Frame:
        """Fungsi pembantu untuk menginisiasi grid pada halaman"""
        # Persiapan membuat tata letak grid
        self.admin_window.grid_rowconfigure(0, weight=1)
        self.admin_window.grid_columnconfigure(0, weight=1)
        
        # Frame untuk menampilkan dashboard
        frame = tk.Frame(self.admin_window)
        frame.grid(row=0, column=0, sticky='nsew')
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        return frame

    def hal_masuk_admin(self):
        """Membuat halaman login admin."""
        self.mulai_hal()

        # Label Judul
        tk.Label(self.admin_window, text="PANDA MANIS", font=(self.font_family, self.fsize_t)).pack(pady=(20, 0))
        tk.Label(self.admin_window, text="kaPAN DApat MAkaNan gratISnya?", font=(self.font_family, self.fsize_h1)).pack(pady=5)

        try:
            # Tampilkan Gambar
            self.image = Image.open(self.image_path)
            self.image = self.image.resize((150, 150), Image.LANCZOS) 
            self.image = ImageTk.PhotoImage(self.image)
            label_image = tk.Label(self.admin_window, image=self.image)
            label_image.pack(pady=10)
        except FileNotFoundError:
            # Jika gambar tidak ditemukan
            pass

        # Label Info
        tk.Label(self.admin_window, text="Projek II Kelompok 5", font=(self.font_family, self.fsize_h2)).pack(pady=(10, 5))
        tk.Label(self.admin_window, text="Berpikir Komputasional - WI1102 Kelas 31", font=(self.font_family, self.fsize_h2)).pack(pady=5)
        tk.Label(self.admin_window, text="Sistem Pemesanan Makanan", font=(self.font_family, self.fsize_h2)).pack(pady=(5))
        tk.Label(self.admin_window, text="Selamat Datang!", font=(self.font_family, self.fsize_t)).pack(pady=10)

        # Label Info
        tk.Label(self.admin_window, text="Login Admin", font=(self.font_family, self.fsize_h2)).pack(pady=10)

        tk.Label(self.admin_window, text="Username:", font=(self.font_family, self.fsize_n)).pack()
        self.username_entry = tk.Entry(self.admin_window)
        self.username_entry.pack()

        tk.Label(self.admin_window, text="Password:", font=(self.font_family, self.fsize_n)).pack()
        self.password_entry = tk.Entry(self.admin_window, show="*")
        self.password_entry.pack()

        # Buat tombol untuk menampilkan password
        self.visible = tk.BooleanVar()
        tk.Checkbutton(self.admin_window, text="Tampilkan Password",font=(self.font_family, self.fsize_n) ,variable=self.visible, command= lambda: self.password_entry.config(show= "" if self.visible.get() else "*")).pack()

        tk.Button(self.admin_window, text="Login", width=15, height=2, command=self.masuk_admin).pack(pady=10)

        tk.Button(self.admin_window, text="Buat Jendela Baru", width=15, height=2, command=self.buat_hal_user_baru).pack(pady=10)

    def buat_hal_user_baru(self):
        self.win_counter += 1
        self.active_windows[self.win_counter] = self.user_gui_class(self.root, self, self.win_counter)

    def tutup_hal_user(self, win_id: int):
        self.active_windows.pop(win_id)

    def masuk_admin(self):
        """Mengarahkan ke halaman dashboard jika login berhasil."""
        login_success = self.admin.login(self.username_entry.get(), self.password_entry.get())
        if login_success:
            self.hal_beranda_admin()

    def hal_beranda_admin(self):
        """Halaman Dashboad Admin"""
        self.mulai_hal()
        frame_dashboard = self.buat_frame()
        
        # Label Judul
        tk.Label(frame_dashboard, text=f"Beranda Admin", font=(self.font_family, self.fsize_h1), anchor='center').grid(row=0, column=0, columnspan=4, pady=10, sticky='nsew')
        
        # Bagian Antrean Pesanan
        tk.Label(frame_dashboard, text="Antrean Pesanan", font=(self.font_family, self.fsize_h2), anchor='center').grid(row=1, column=0, columnspan=4, pady=5, sticky='nsew')
        
        # Frame untuk menampilkan Antrean pesanan
        frame_order_history = tk.Frame(frame_dashboard, width=600)
        frame_order_history.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="n")
        frame_order_history.grid_columnconfigure(0, weight=1)
        
        if Order.antrean:
            # Membuat header tabel riwayat pesanan
            tk.Label(frame_order_history, text="Order ID", font=(self.font_family, 12)).grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Meja", font=(self.font_family, 12)).grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Status", font=(self.font_family, 12)).grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Qtys", font=(self.font_family, 12)).grid(row=0, column=3, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Total", font=(self.font_family, 12)).grid(row=0, column=4, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Lihat Pesanan", font=(self.font_family, 12)).grid(row=0, column=5, padx=5, pady=5, sticky='nsew')

            # Menampilkan data pesanan
            for idx, order in enumerate(Order.antrean, start=1):
                order: Order
                tk.Label(frame_order_history, text=f"{order.ID}").grid(row=idx, column=0, padx=5, pady=2, sticky='nsew')
                tk.Label(frame_order_history, text=f"{order.meja}").grid(row=idx, column=1, padx=5, pady=2, sticky='nsew')
                tk.Label(frame_order_history, text=f"{order.status.value}").grid(row=idx, column=2, padx=5, pady=2, sticky='nsew')
                tk.Label(frame_order_history, text=f"{order.cek_jumlah()}").grid(row=idx, column=3, padx=5, pady=2, sticky='nsew')
                tk.Label(frame_order_history, text=f"Rp {order.cek_total():,.2f}").grid(row=idx, column=4, padx=5, sticky='nsew')
                tk.Button(frame_order_history, text="Lihat", command=lambda o=order: self.popup_detail_pesanan(o)).grid(row=idx, column=5, padx=5, pady=2, sticky='nsew')
        else:
            # Jika belum ada riwayat pesanan
            tk.Label(frame_order_history, text="Belum ada pesanan masuk.").grid(row=0, column=0, columnspan=2, pady=5)
        
        # Tombol Refresh
        tk.Button(frame_dashboard, text="Refresh", command=self.hal_beranda_admin).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Tombol Riwayat Pesanan
        tk.Button(frame_dashboard, text="Riwayat Pesanan", command=self.hal_riwayat_pesanan).grid(row=4, column=0, columnspan=2, pady=10)

        # Tombol Keluar
        tk.Button(frame_dashboard, text="Keluar", command=self.keluar_admin).grid(row=5, column=0, columnspan=2, pady=10)

    def hal_riwayat_pesanan(self):
        """Halaman Riwayat Pesanan"""
        self.mulai_hal()
        frame_dashboard = self.buat_frame()
        
        # Label Judul
        tk.Label(frame_dashboard, text="Riwayat Pesanan", font=(self.font_family, self.fsize_h1), anchor='center').grid(row=0, column=0, columnspan=4, pady=10, sticky='nsew')
        
        # Menghitung total item, dan pendapatan hari ini
        order_dibuat = 0
        item_diselesaikan = 0
        pendapatan_diterima = 0
        for order in Order.riwayat.values():
            if order.status == Status.PAID:
                pendapatan_diterima += order.cek_total()
                item_diselesaikan += order.cek_jumlah()
            if order.status != Status.CANCELED:
                order_dibuat += 1

        # Label Statistik Hari ini
        tk.Label(frame_dashboard, text="Statistik Hari Ini", font=(self.font_family, self.fsize_h2), anchor='center').grid(row=1, column=0, columnspan=4, pady=5, sticky='nsew')
        tk.Label(frame_dashboard, text=f"Total pesanan dibuat: {order_dibuat} pesanan", font=(self.font_family, self.fsize_n), anchor='w', justify="left").grid(row=2, column=0, columnspan=4, sticky='nsew', padx= 10)
        tk.Label(frame_dashboard, text=f"Total item diselesaikan: {item_diselesaikan}", font=(self.font_family, self.fsize_n), anchor='w', justify="left").grid(row=3, column=0, columnspan=4, sticky='nsew', padx= 10)
        tk.Label(frame_dashboard, text=f"Total pendapatan diterima: Rp {pendapatan_diterima:,.2f}", font=(self.font_family, self.fsize_n), anchor='w', justify="left").grid(row=4, column=0, columnspan=4, sticky='nsew', padx= 10)
        
        # Bagian Antrean Pesanan
        tk.Label(frame_dashboard, text="Daftar Pesanan", font=(self.font_family, self.fsize_h2), anchor='center').grid(row=5, column=0, columnspan=4, pady=5, sticky='nsew')
        
        # Frame untuk menampilkan Antrean pesanan
        frame_order_history = tk.Frame(frame_dashboard, width=600)
        frame_order_history.grid(row=6, column=0, columnspan=2, padx=20, pady=10, sticky="n")
        frame_order_history.grid_columnconfigure(0, weight=1)
        
        if Order.riwayat:
            # Membuat header tabel riwayat pesanan
            tk.Label(frame_order_history, text="Order ID", font=(self.font_family, 12)).grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Meja", font=(self.font_family, 12)).grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Status", font=(self.font_family, 12)).grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Qtys", font=(self.font_family, 12)).grid(row=0, column=3, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Total", font=(self.font_family, 12)).grid(row=0, column=4, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Struk Pesanan", font=(self.font_family, 12)).grid(row=0, column=5, padx=5, pady=5, sticky='nsew')

            # Menampilkan data pesanan
            for idx, order in enumerate(Order.riwayat.values(), start=1):
                order: Order
                tk.Label(frame_order_history, text=f"{order.ID}").grid(row=idx, column=0, padx=5, pady=2, sticky='nsew')
                tk.Label(frame_order_history, text=f"{order.meja}").grid(row=idx, column=1, padx=5, pady=2, sticky='nsew')
                tk.Label(frame_order_history, text=f"{order.status.value}").grid(row=idx, column=2, padx=5, pady=2, sticky='nsew')
                tk.Label(frame_order_history, text=f"{order.cek_jumlah()}").grid(row=idx, column=3, padx=5, pady=2, sticky='nsew')
                tk.Label(frame_order_history, text=f"Rp {order.cek_total():,.2f}").grid(row=idx, column=4, padx=5, sticky='nsew')
                tk.Button(frame_order_history, text="Struk", command=lambda o=order: self.popup_detail_pesanan(o)).grid(row=idx, column=5, padx=5, pady=2, sticky='nsew')
        else:
            # Jika belum ada riwayat pesanan
            tk.Label(frame_order_history, text="Belum ada pesanan masuk.").grid(row=0, column=0, columnspan=4, pady=5)
        
        # Tombol Refresh
        tk.Button(frame_dashboard, text="Refresh", command=self.hal_riwayat_pesanan).grid(row=7, column=0, columnspan=2, pady=10)
        
        # Tombol Keluar
        tk.Button(frame_dashboard, text="Kembali", command=self.hal_beranda_admin).grid(row=8, column=0, columnspan=2, pady=10)

    def popup_detail_pesanan(self, order: Order):
        """Membuat popup untuk mencetak struk pesanan."""
        popup = tk.Toplevel(self.admin_window)
        popup.title("Detail Pesanan")
        popup.geometry("800x400")
        popup.resizable(True, True)
        popup.geometry(f"+{popup.winfo_screenwidth() // 2 - 200}+{popup.winfo_screenheight() // 2 - 100}")

        text_frame = tk.Frame(popup, pady=10, padx=10)
        text_frame.pack(fill="both", expand=True)
        text = tk.Text(text_frame, wrap="word", height=5, relief="solid", borderwidth=1)
        text.insert("1.0", order.cetak_struk())
        text.config(state="disabled") 
        text.pack(fill="both", expand=True, padx=5, pady=5)

        # Tombol-Tombol
        button_frame = tk.Frame(popup, pady=10)
        button_frame.pack(fill="x")
        ttk.Button(button_frame, text="Proses Pesanan", command=lambda: self.konfirmasi_proses_pesanan(popup, order)).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(button_frame, text="Kembali", command=popup.destroy).grid(row=0, column=1, padx=10, pady=5)

        popup.transient()  # Membuat popup terikat pada jendela utama
        popup.grab_set()   # Memastikan popup harus ditutup sebelum jendela utama dapat diakses lagi
        popup.mainloop()

    def konfirmasi_proses_pesanan(self, popup: tk.Toplevel, order: Order):
        if not Order.antrean:
            messagebox.showerror("Error", "Tidak ada pesanan yang sedang diproses.")
            return
        if Order.antrean[0] != order:
            if not messagebox.askokcancel("Konfirmasi", "Pesanan ini bukan pesanan terdepan. Apakah Anda yakin ingin memprosesnya?"):
                return

        popup.destroy()
        self.hal_proses_pesanan(order)

    def hal_proses_pesanan(self, order: Order):
        """Membuat antarmuka untuk melihat detail pesanan."""
        if order.status != Status.CONFIRMED:
            messagebox.showerror("Error", f"Tidak dapat memproses pesanan ini. Status pesanan {order.status.value}.")
            return
        
        self.mulai_hal()
        frame_detail = self.buat_frame()
        user: User = User.daftar.get(order.user_id)
        order.status = Status.IN_PROGRESS

        # Label Detail Pesanan
        tk.Label(frame_detail, text="Detail Pesanan", font=(self.font_family, self.fsize_h1)).grid(row=0, column=0, columnspan=2, pady=10, sticky='nsew')
        tk.Label(frame_detail, text=f"{user}", font=(self.font_family, self.fsize_n), anchor="e", justify="left").grid(row=1, column=0, sticky='w', padx=10, pady=2)
        tk.Label(frame_detail, text=f"{order}", font=(self.font_family, self.fsize_n), anchor="e", justify="left").grid(row=4, column=0, sticky='w', padx=10, pady=2)

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
        tk.Label(frame_item, text="Selesai", font=(self.font_family, self.fsize_n)).grid(row=1, column=6, pady=5, sticky='nsew', padx=10)

        # Menampilkan detail item
        selesai = [tk.BooleanVar(value=False) for i in range(len(order.items))]
        for idx, (item, qty) in enumerate(order.items.items(), start=1):
            item: Item
            subtotal = item.harga * qty
            tk.Label(frame_item, text=f"{idx}").grid(row=idx + 1, column=0, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"#{item.ID:02}").grid(row=idx + 1, column=1, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"{item.nama}").grid(row=idx + 1, column=2, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"{qty}").grid(row=idx + 1, column=3, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"Rp {item.harga:,.2f}").grid(row=idx + 1, column=4, sticky='w', padx=10, pady=2)
            tk.Label(frame_item, text=f"Rp {subtotal:,.2f}").grid(row=idx + 1, column=5, sticky='w', padx=10, pady=2)
            tk.Checkbutton(frame_item, variable=selesai[idx-1]).grid(row=idx + 1, column=6, sticky='w', padx=10, pady=2)
        tk.Label(frame_detail, text=f"Total Harga: Rp {order.cek_total():,.2f}", font=(self.font_family, self.fsize_n)).grid(row=8, column=0, columnspan=2, pady=10, sticky='n')
        
        # Tombol untuk proses pesanan
        tk.Button(frame_detail, text="Proses Pesanan", command=lambda o=order, s=selesai: self.admin.proses_order(o, s)).grid(row=9, column=0, columnspan=1, pady=5, sticky='n')
        
        # Tombol untuk kembali
        tk.Button(frame_detail, text="Kembali", command=lambda: self.kembali(order)).grid(row=9, column=1, columnspan=1, pady=5, sticky='n')

    def kembali(self, order: Order):
        """Konfirmasi kembali dari memproses pesanan"""
        if order.status == Status.IN_PROGRESS:
            if messagebox.askokcancel("Konfirmasi", "Apakah Anda yakin ingin kembali? Pesanan ini akan tetap ditandai sebagai DIPROSES sehingga user tidak akan dapat mengubahnya lagi."):
                self.hal_beranda_admin()
        else:
            self.hal_beranda_admin()

    def keluar_admin(self):
        """Keluar sebagai admin."""
        if messagebox.askokcancel("Konfirmasi", "Apakah Anda yakin ingin keluar?"):
            self.admin.logout()
            self.hal_masuk_admin()
        else:
            return

