from tkinter import messagebox # Import messagebox dari tkinter
from server.order import Order, Status # Import class Order dan Enum Status dari file order.py
from client.user import User # Import class User dari file user.py

class Admin:
    """
    Berisi semua informasi berkaitan dengan data dan perintah admin. Untuk menggunakan kemmampuan Admin, Admin harus login terlebih dahulu.

    Atribut Lokal:
    - Username (tersembunyi): `_username: str`
    - Password (tersembunyi): `_password: str`
    - Autentikasi: `auth: bool`

    Argumen initialisasi: `Admin(username: str, password: str) -> Admin`

    Metode:
    - `login(username: str, password: str) -> bool`: Login ke sistem dengan memasukkan password.
    - `logout()`: Logout dari sistem.
    - `lihat_antrean()`: Melihat semua pesanan yang belum diproses.
    - `proses_order()`: Mengambil pesanan terdepan dari antrean, mengubah statusnya, lalu memproses tiap itemnya.
    - `selesai_order(order: Order)`: Menyelesaikan pesanan, mengubah statusnya, dan memberitahu pengguna.
    """
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password
        self.auth = False
        self.pemasukan = 0
        return
    
    def login(self, username: str, password: str) -> bool:
        """Login ke sistem dengan memasukkan password."""
        if username == self._username:
            if password == self._password:
                self.auth = True
                messagebox.showinfo("Berhasil", "Login berhasil. Selamat datang, Admin!")
                return True
            else:
                messagebox.showerror("Gagal", "Password salah. Coba lagi.")
                return False
        else:
            messagebox.showerror("Gagal", "Username tidak dikenal, coba lagi.")
            return False

    def logout(self):
        """Logout dari sistem."""
        if self.auth:
            self.auth = False
            messagebox.showinfo("Berhasil", "Logout berhasil.")
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
        
    def proses_order(self, order: Order, selesai: list):
        """Mengambil pesanan terdepan dari antrean, mengubah statusnya, lalu memproses tiap itemnya."""
        if order.status in {Status.CANCELED, Status.READY, Status.PAID}:
            messagebox.showerror("Error", "Tidak dapat memproses pesanan ini. Pesanan dibatalkan atau sudah selesai.")
            return
        
        for i, (item, qty) in enumerate(order.items.items(), start=0):
            if selesai[i].get() == 0:
                messagebox.showerror("Error", f"Item {item.nama} x {qty} buah belum diselesaikan.")
                return
        order = Order.antrean.pop(0)        
        order.status = Status.READY
        
        print(f"Pesanan {order.ID} selesai diproses.\n")
        print(order.cetak_struk())
        user: User = User.daftar.get(order.user_id)
        user.notifikasi(order)
