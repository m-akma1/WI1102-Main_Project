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
    def __init__(self, nama: str, harga: int):
        Item.counter += 1
        self.nama = nama
        self.harga = harga
        self.ID = Item.counter
    
    def __str__(self):
        return f"#{self.ID:02d} | {self.nama:<15} | Rp {self.harga:10,.2f}"

class Status(enum.Enum):
    """Enumerasi status pesanan."""
    PENDING = "Menunggu dikonfirmasi"
    CONFIRMED = "Dikonfirmasi, dalam antrean"
    IN_PROGRESS = "Dalam proses"
    READY = "Siap diambil"
    COMPLETED = "Selesai"

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
    def __init__(self, meja: int, user: "User"):
        self.meja = meja
        self.user = user
        self.items = []
        self.status = Status.PENDING
        self.ID = self.id_generator()

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
        
    def edit_status(self, status):
        """Mengubah status pesanan."""
        self.status = status
    
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
    Item("Mie Goreng", 12000),
    Item("Sate Kambing", 20000),
]

# GUI Setup using tkinter
class FoodOrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Ordering System")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        self.create_main_interface()

    def create_main_interface(self):
        """Membuat antarmuka utama untuk memilih sebagai pengguna atau koki"""
        self.header = tk.Label(self.root, text="Selamat Datang di Panda Manis", font=("Arial", 18))
        self.header.pack(pady=20)

        self.user_button = tk.Button(self.root, text="Pengguna", width=15, height=2, command=self.user_interface)
        self.user_button.pack(pady=10)
        
        self.chef_button = tk.Button(self.root, text="Koki", width=15, height=2, command=self.chef_interface)
        self.chef_button.pack(pady=10)

    def user_interface(self):
        messagebox.showinfo("Pengguna", "Antarmuka pengguna sedang dibuat...")

    def chef_interface(self):
        messagebox.showinfo("Koki", "Antarmuka koki sedang dibuat...")

if __name__ == "__main__":
    root = tk.Tk()
    app = FoodOrderApp(root)
    root.mainloop()
