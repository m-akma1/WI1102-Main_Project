import ctypes
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from server.admin import Admin
from server.order import Order

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

    def __init__(self, root: tk.Tk, user_gui_class):
        # Inisialisasi jendela
        self.root = root
        self.root.withdraw()
        self.admin_window: tk.Tk = tk.Toplevel(root)
        self.user_gui_class = user_gui_class
        self.admin = Admin("afafufuf", "fufufafa")
        self.admin_window.title("Sistem Pemesanan Makanan - Admin")

        # Set font default
        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family=self.font_family, size=self.fsize_n)
        
        # Set ukuran jendela
        window_width = 600
        window_height = 800
        
        # Dapatkan ukuran layar monitor
        screen_width = self.admin_window.winfo_screenwidth()
        screen_height = self.admin_window.winfo_screenheight()
        
        # Hitung posisi jendela agar berada di tengah layar
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        
        # Set posisi jendela
        self.admin_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y-30}")
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

        # Label Info
        tk.Label(self.admin_window, text="Login Admin", font=(self.font_family, self.fsize_h2)).pack(pady=20)

        tk.Label(self.admin_window, text="Username:", font=(self.font_family, self.fsize_n)).pack()
        self.username_entry = tk.Entry(self.admin_window)
        self.username_entry.pack()

        tk.Label(self.admin_window, text="Password:", font=(self.font_family, self.fsize_n)).pack()
        self.password_entry = tk.Entry(self.admin_window, show="*")
        self.password_entry.pack()

        # Buat tombol untuk menampilkan password
        self.visible = tk.BooleanVar()
        tk.Checkbutton(self.admin_window, text="Tampilkan Password",font=(self.font_family, self.fsize_n) ,variable=self.visible, command= lambda: self.password_entry.config(show= "" if self.visible.get() else "*")).pack()

        tk.Button(self.admin_window, text="Login", width=15, height=2, command=self.login).pack(pady=20)

        tk.Button(self.admin_window, text="Buat Jendela Baru", width=15, height=2, command=self.buat_hal_user_baru).pack(pady=20)

    def buat_hal_user_baru(self):
        self.win_counter += 1
        self.active_windows[self.win_counter] = self.user_gui_class(self.root, self, self.win_counter)

    def tutup_hal_user(self, win_id: int):
        self.active_windows.pop(win_id)

    def login(self):
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
        tk.Label(frame_dashboard, text="Antrean Pesanan", font=(self.font_family, self.fsize_h2), anchor='center').grid(row=4, column=0, columnspan=4, pady=5, sticky='nsew')
        
        # Frame untuk menampilkan Antrean pesanan
        frame_order_history = tk.Frame(frame_dashboard, width=600)
        frame_order_history.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="n")
        frame_order_history.grid_columnconfigure(0, weight=1)
        
        if Order.antrean:
            # Membuat header tabel riwayat pesanan
            tk.Label(frame_order_history, text="Order ID", font=(self.font_family, 12)).grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Meja", font=(self.font_family, 12)).grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Status", font=(self.font_family, 12)).grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Total", font=(self.font_family, 12)).grid(row=0, column=3, padx=5, pady=5, sticky='nsew')
            tk.Label(frame_order_history, text="Lihat Pesanan", font=(self.font_family, 12)).grid(row=0, column=4, padx=5, pady=5, sticky='nsew')

            # Menampilkan data pesanan
            for idx, order in enumerate(Order.antrean, start=1):
                order: Order
                tk.Label(frame_order_history, text=f"{order.ID}").grid(row=idx, column=0, padx=5, pady=2, sticky='nsew')
                tk.Label(frame_order_history, text=f"{order.meja}").grid(row=idx, column=1, padx=5, pady=2, sticky='nsew')
                tk.Label(frame_order_history, text=f"{order.status.value}").grid(row=idx, column=2, padx=5, pady=2, sticky='nsew')
                tk.Label(frame_order_history, text=f"Rp {order.cek_total():,.2f}").grid(row=idx, column=3, padx=5, sticky='nsew')
                tk.Button(frame_order_history, text="Lihat", command=lambda o=order: self.hal_lihat_pesanan(o.ID)).grid(row=idx, column=4, padx=5, pady=2, sticky='nsew')
        else:
            # Jika belum ada riwayat pesanan
            tk.Label(frame_dashboard, text="Belum ada pesanan masuk.").grid(row=5, column=0, columnspan=4, pady=5)
        
        # Tombol untuk membuat pesanan baru
        tk.Button(frame_dashboard, text="Refresh", command=self.hal_beranda_admin).grid(row=len(Order.antrean) + 6, column=0, columnspan=1, pady=10)
        
        # Tombol Keluar
        tk.Button(frame_dashboard, text="Keluar", command=self.keluar_admin).grid(row=len(Order.antrean) + 6, column=1, columnspan=2, pady=10)

    def hal_lihat_pesanan(self, order_id: str):
        print(Order.riwayat[order_id].cetak_struk())

    def keluar_admin(self):
        """Keluar sebagai admin."""
        self.admin.logout()
        messagebox.showinfo("Keluar", "Anda telah keluar.")
        self.hal_masuk_admin()

