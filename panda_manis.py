import tkinter as tk
from tkinter import messagebox
import enum     # Modul Enumerasi, digunakan untuk membuat alias untuk mempermudah pengkategorian status pesanan
import datetime # Modul Tanggal dan Waktu, digunakan untuk mendapatkan data waktu dari komputer dalam membuat ID

class Item:
    """
    Representasi objek dari menu makanan atau minuman yang ada di menu restoran.
    
    Atribut:
    - ID Menu: `ID: int`
    - Nama: `nama: str`
    - Harga (Rp): `harga: int`

    Argumen initialisasi: `(nama: str, harga: int) -> Item`
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
    
    Atribut:
    - ID User: `ID: str`
    - Nama: `nama: str`
    - Nomor Telepon: `telp: str`

    Argumen initialisasi: `(nama: str, telp: str) -> User`
    """
    counter = 0 # Jumlah user yang telah dibuat
    users = {}  # Dictionary untuk menyimpan semua pengguna
    def __init__(self, nama: str, telp: str):
        User.counter += 1
        self.nama = nama
        self.telp = telp
        self.ID = self.id_generator()
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
        total = 0
        for item in self.items:
            total += item[0].harga * item[1]
        return total

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
# I think we don't need to create the array anymore since it already exist in the class level method of item
Menu = [
    Item("Ayam Goreng", 10000),
    Item("Ayam Bakar", 12000),
    Item("Ayam Geprek", 15000),
    Item("Mie Goreng", 12000),
    Item("Sate Kambing", 20000),
]

# GUI Setup using tkinter
class Interface:
    def __init__(self, root: tk.Tk):
        self.root: tk.Tk = root
        self.root.title("Food Ordering System")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        self.hal_utama()

    def hal_utama(self):
        """Membuat antarmuka utama untuk memilih sebagai pengguna atau koki"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.header = tk.Label(self.root, text="Selamat Datang di Panda Manis", font=("Arial", 18))
        self.header.pack(pady=20)

        self.tombol_daftar = tk.Button(self.root, text="Pengguna Baru", width=15, height=2, command=self.hal_daftar_pengguna)
        self.tombol_daftar.pack(pady=10)
        
        self.tombol_masuk = tk.Button(self.root, text="Login Pengguna", width=15, height=2, command=self.hal_masuk_pengguna)
        self.tombol_masuk.pack(pady=10)
        
        self.tombol_koki = tk.Button(self.root, text="Koki", width=15, height=2, command=self.hal_masuk_koki)
        self.tombol_koki.pack(pady=10)

    def hal_daftar_pengguna(self):
        """Membuat antarmuka untuk pengguna baru untuk melakukan pemesanan"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.header = tk.Label(self.root, text="Daftar Pengguna Baru", font=("Arial", 14))
        self.header.pack(pady=20)

        tk.Label(self.root, text="Nama: ").pack(pady=5)
        self.masukan_nama = tk.Entry(self.root)
        self.masukan_nama.pack(pady=10)

        tk.Label(self.root, text="Nomor Telepon: \nFormat: 628XXXXXXXX...").pack(pady=5)
        self.masukan_telp = tk.Entry(self.root)
        self.masukan_telp.pack(pady=10)

        tombol_kirim = tk.Button(self.root, text="Kirim", command=self.buat_user_baru)
        tombol_kirim.pack(pady=20)

        tombol_kembali = tk.Button(self.root, text="Kembali", command=self.hal_utama)
        tombol_kembali.pack(pady=5)

    def hal_masuk_pengguna(self):
        """Membuat antarmuka untuk pengguna yang sudah ada untuk login"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.header = tk.Label(self.root, text="Login Pengguna", font=("Arial", 14))
        self.header.pack(pady=20)

        tk.Label(self.root, text="Masukkan User ID: ").pack(pady=5)
        self.masukan_userID = tk.Entry(self.root)
        self.masukan_userID.pack(pady=10)

        tk.Label(self.root, text="Masukkan Nomor Telepon: ").pack(pady=5)
        self.masukan_telp_ = tk.Entry(self.root)
        self.masukan_telp_.pack(pady=10)

        tombol_masuk = tk.Button(self.root, text="Masuk", command=self.masuk_user)
        tombol_masuk.pack(pady=20)

        tombol_kembali = tk.Button(self.root, text="Kembali", command=self.hal_utama)
        tombol_kembali.pack(pady=5)

    def buat_user_baru(self):
        """Membuat order baru berdasarkan input dari pengguna"""
        nama = self.masukan_nama.get()
        telp = self.masukan_telp.get()

        # Validasi Nama
        nama = nama.strip()
        if not (nama.replace(" ", "").isalpha()):
            messagebox.showwarning("Input Error", "Nama hanya boleh mengandung huruf dan spasi!")
            return
        
        # Validasi Nomor Telepon
        if not (telp.startswith("628") and telp[3:].isdigit() and 8 <= len(telp[3:]) <= 12):
            messagebox.showwarning("Input Error", "Nomor telepon harus dalam format 628XXXXXXXXX!")
            return
        
        user = User(nama, telp)
        messagebox.showinfo("Berhasil", f"User berhasil dibuat dengan ID: {user.ID}")
        self.hal_utama()

    def masuk_user(self):
        """Fungsi untuk login pengguna yang sudah ada"""
        userID = self.masukan_userID.get()
        telp = self.masukan_telp_.get()

        if not (userID and telp):
            messagebox.showwarning("Input Error", "Semua bidang harus diisi!")
            return
        
        user_ditemukan = User.users.get(userID)
        if not user_ditemukan:
            messagebox.showerror("Login Gagal", "Pengguna tidak ditemukan!")
        else:
            user_telp = user_ditemukan.telp            
            if user_telp == telp:
                messagebox.showinfo("Login Berhasil", f"Selamat datang kembali, {user_ditemukan.nama}!")
                self.hal_beranda_user(user_ditemukan)
            else:
                messagebox.showerror("Login Gagal", "Nomor telepon tidak sesuai User ID!")

    def hal_beranda_user(self, user: User):
        """Membuat antarmuka beranda setelah login pengguna."""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text=f"Beranda Pengguna - {user.nama}", font=("Arial", 16)).pack(pady=10)

        # Order History
        tk.Label(self.root, text="Riwayat Pesanan:", font=("Arial", 14)).pack(pady=5)
        history_frame = tk.Frame(self.root)
        history_frame.pack(pady=5)
        
        orders = [order for order in Order.history if order.user == user]
        if orders:
            for order in orders:
                order_info = f"ID: {order.ID} | Meja: {order.meja} | Status: {order.status.value} | Total: Rp {order.cek_total():,.2f}"
                tk.Label(history_frame, text=order_info).pack(anchor='w')
        else:
            tk.Label(history_frame, text="Belum ada riwayat pesanan.").pack()

        # Create New Order Button
        tk.Button(self.root, text="Buat Pesanan Baru", command=lambda: self.hal_buat_pesanan_baru(user)).pack(pady=10)

        # Logout Button
        tk.Button(self.root, text="Logout", command=self.hal_utama).pack(pady=5)

    def hal_buat_pesanan_baru(self, user):
        """Membuat antarmuka untuk membuat pesanan baru."""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text=f"Buat Pesanan Baru - {user.nama}", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Nomor Meja: ").pack(pady=5)
        self.masukan_meja = tk.Entry(self.root)
        self.masukan_meja.pack(pady=5)

        tk.Label(self.root, text="Pilih Item Menu: ").pack(pady=5)
        self.daftar_menu = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        for item_id, item in Item.menu.items():
            self.daftar_menu.insert(tk.END, f"{item_id}. {item.nama} - Rp {item.harga:,.2f}")
        self.daftar_menu.pack(pady=20)

        tk.Label(self.root, text="Jumlah untuk masing-masing item (pisahkan dengan koma): ").pack(pady=5)
        self.masukan_qty = tk.Entry(self.root)
        self.masukan_qty.pack(pady=5)

        tk.Button(self.root, text="Tambahkan Pesanan", command=lambda: self.buat_pesanan(user)).pack(pady=10)
        tk.Button(self.root, text="Kembali", command=lambda: self.hal_beranda_user(user)).pack(pady=5)

    def buat_pesanan(self, user):
        """Menambahkan pesanan baru berdasarkan input dari pengguna."""
        meja = self.masukan_meja.get()
        item_terpilih = self.daftar_menu.curselection()
        qty = self.masukan_qty.get()

        # Validasi Nomor Meja
        if not (meja.isdigit() and 0 <= int(meja) <= 99):
            messagebox.showwarning("Input Error", "Nomor meja harus berupa angka antara 0 hingga 99!")
            return
        meja = int(meja)

        # Validasi Item dan Jumlah
        if not item_terpilih:
            messagebox.showwarning("Input Error", "Silakan pilih setidaknya satu item dari menu!")
            return
        
        daftar_qty = qty.split(",")
        if len(daftar_qty) != len(item_terpilih):
            messagebox.showwarning("Input Error", "Jumlah item yang dipilih dan jumlah yang dimasukkan tidak sesuai!")
            return
        
        try:
            daftar_qty = [int(qty.strip()) for qty in daftar_qty]
        except ValueError:
            messagebox.showwarning("Input Error", "Jumlah harus berupa angka dan dipisahkan dengan koma!")
            return
        
        # Membuat pesanan baru
        new_order = Order(meja, user)
        for idx, item_index in enumerate(item_terpilih):
            item_id = list(Item.menu.keys())[item_index]
            item = Item.menu[item_id]
            qty = daftar_qty[idx]
            new_order.tambah_item(item, qty)

        messagebox.showinfo("Berhasil", f"Pesanan berhasil dibuat dengan ID: {new_order.ID}")
        self.hal_beranda_user(user)

    def hal_masuk_koki(self):
        messagebox.showinfo("Koki", "Antarmuka koki sedang dibuat...")

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
