from tkinter import messagebox # Untuk menampilkan notifikasi pesan
from server.order import Order, Status # Import class Order dan Enum Status dari file order.py

class User:
    """
    Berisi semua informasi berkaitan dengan data pemesan.

    Atribut Global:
    - Penghitung user: `counter: int`
    - Daftar user: `daftar: dictionary`

    Atribut Lokal:
    - ID User: `ID: str`
    - Nama: `nama: str`
    - Telepon: `telp: str`
    - Daftar Pesanan: `orders: dictionary`

    Argumen initialisasi: `User(nama: str, telp: str) -> User`

    Metode:
    - `id_generator(nama: str) -> str`: Membuat ID unik untuk user.
    - `login(user_id: str, telp: str) -> bool`: Login ke sistem dengan memasukkan nomor telepon.
    - `tambah_order(order: Order)`: Menambahkan pesanan ke dalam daftar pesanan pengguna.
    - `lihat_daftar() -> str`: Melihat daftar pesanan yang dimiliki pengguna.
    - `notifikasi(order: Order)`: Memberitahu pengguna bahwa pesanannya sudah siap.
    - `__str__() -> str`: Membuat string untuk mencetak objek user.
    """

    counter = 0 # Jumlah user yang telah dibuat
    daftar = {} # Daftar user yang ada
    def __init__(self, nama: str, telp: str):
        self.nama = nama
        self.telp = telp
        self.orders = {}
        self.ID = self.id_generator(self.nama)
        User.daftar[self.ID] = self
        return
    
    @classmethod
    def id_generator(cls, nama: str) -> str:
        """
        Membuat ID komposit unik dengan format:
        U-XXX-ABC:
          - U mengindikasikan ini adalah ID User
          - XXX adalah urutan nomor user yang dibuat
          - ABC adalah inisial nama user
        """
        initial = nama[:3].upper()
        User.counter += 1
        return f"U-{User.counter:03d}-{initial}"

    @classmethod
    def login(cls, user_id: str, telp: str) -> bool:
        """Login ke sistem dengan memasukkan nomor telepon."""
        if user_id in User.daftar:
            if telp == User.daftar[user_id].telp:
                messagebox.showinfo("Berhasil", "Login berhasil. Selamat datang!")
                return True
            else:
                messagebox.showerror("Gagal", "Nomor telepon salah. Coba lagi.")
                return False
        else:
            messagebox.showerror("Gagal", "User ID tidak dikenal, coba lagi.")
            return False

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
    
    def notifikasi(self, order: "Order"):
        """Memberitahu pengguna bahwa pesanannya sudah siap."""
        info = messagebox.showinfo("Pesanan Siap", f"Pesanan Anda #{order.ID} sudah siap diambil.")

    def __str__(self) -> str:
        output = f"User ID: {self.ID}\n"
        output += f"Nama: {self.nama}\n"
        output += f"Telepon: {self.telp}\n"
        return output
