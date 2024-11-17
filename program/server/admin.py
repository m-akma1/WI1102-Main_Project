from server.order import Order, Status
from client.user import User
from client.GUI_Interface import GUI_Interface

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
        user: User = User.daftar.get(order.user_id)
        user.notifikasi(order)
