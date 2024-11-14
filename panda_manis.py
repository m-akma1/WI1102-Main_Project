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
class FoodOrderApp:
    def __init__(self, root: tk.Tk):
        self.root: tk.Tk = root
        self.root.title("Food Ordering System")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        self.create_main_interface()

    def create_main_interface(self):
        """Membuat antarmuka utama untuk memilih sebagai pengguna atau koki"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.header = tk.Label(self.root, text="Selamat Datang di Panda Manis", font=("Arial", 18))
        self.header.pack(pady=20)

        self.user_button = tk.Button(self.root, text="Pengguna Baru", width=15, height=2, command=self.new_user_interface)
        self.user_button.pack(pady=10)
        
        self.login_button = tk.Button(self.root, text="Login Pengguna", width=15, height=2, command=self.login_user_interface)
        self.login_button.pack(pady=10)
        
        self.chef_button = tk.Button(self.root, text="Koki", width=15, height=2, command=self.chef_interface)
        self.chef_button.pack(pady=10)

    def new_user_interface(self):
        """Membuat antarmuka untuk pengguna baru untuk melakukan pemesanan"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text="Nama: ").pack(pady=5)
        self.nama_entry = tk.Entry(self.root)
        self.nama_entry.pack(pady=10)

        tk.Label(self.root, text="Nomor Telepon: \nFormat: 628XXXXXXXX...").pack(pady=5)
        self.telp_entry = tk.Entry(self.root)
        self.telp_entry.pack(pady=10)

        submit_button = tk.Button(self.root, text="Submit", command=self.create_user)
        submit_button.pack(pady=20)

        back_button = tk.Button(self.root, text="Kembali", command=self.create_main_interface)
        back_button.pack(pady=5)

    def login_user_interface(self):
        """Membuat antarmuka untuk pengguna yang sudah ada untuk login"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text="Masukkan User ID: ").pack(pady=5)
        self.login_userID_entry = tk.Entry(self.root)
        self.login_userID_entry.pack(pady=10)

        tk.Label(self.root, text="Masukkan Nomor Telepon: ").pack(pady=5)
        self.login_telp_entry = tk.Entry(self.root)
        self.login_telp_entry.pack(pady=10)

        login_button = tk.Button(self.root, text="Login", command=self.login_user)
        login_button.pack(pady=20)

        back_button = tk.Button(self.root, text="Kembali", command=self.create_main_interface)
        back_button.pack(pady=5)

    def create_user(self):
        """Membuat order baru berdasarkan input dari pengguna"""
        nama = self.nama_entry.get()
        telp = self.telp_entry.get()

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
        self.create_main_interface()

    def login_user(self):
        """Fungsi untuk login pengguna yang sudah ada"""
        userID = self.login_userID_entry.get()
        telp = self.login_telp_entry.get()

        if not (userID and telp):
            messagebox.showwarning("Input Error", "Semua bidang harus diisi!")
            return
        
        user_found = User.users.get()
        if not user_found:
            messagebox.showerror("Login Gagal", "Pengguna tidak ditemukan!")
        else:
            user_telp = user_found.telp            
            if user_telp == telp:
                messagebox.showinfo("Login Berhasil", f"Selamat datang kembali, {user_found.nama}!")
                self.create_main_interface()
            else:
                messagebox.showerror("Login Gagal", "Nomor telepon tidak sesuai User ID!")

    def chef_interface(self):
        messagebox.showinfo("Koki", "Antarmuka koki sedang dibuat...")

if __name__ == "__main__":
    root = tk.Tk()
    app = FoodOrderApp(root)
    root.mainloop()
