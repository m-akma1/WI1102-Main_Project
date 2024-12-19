from server.item import Item # Import class Item dari file item.py
from enum import Enum # Untuk membuat enumerasi status pesanan

class Status(Enum):
    """Enumerasi status pesanan untuk mempermudah pengelompokan."""
    PENDING = "MENUNGGU"
    CANCELED = "DIBATALKAN"
    CONFIRMED = "DALAM ANTREAN"
    IN_PROGRESS = "DALAM PROSES"
    READY = "SIAP"
    PAID = "LUNAS"

class Order:
    """
    Representasi sebuah pesanan.
    
    Atribut Global:
    - Penghitung order: `counter: int`
    - Riwayat order: `riwayat: dictionary`
    - Antrean order: `antrean: list`

    Atribut Lokal:
    - ID Pesanan: `id: str`
    - No. Meja: `meja: int`
    - User pemesan: `user: User`
    - Daftar Pesanan: `items: list`
    - Total harga: `total: int`
    - Jumlah item: `jumlah: int`
    - Status Pesanan: `status: Status`

    Argumen initialisasi: `Order(meja: int, user: User) -> Order`

    Metode:
    - `id_generator() -> str`: Membuat ID unik untuk pesanan.
    - `cek_total() -> int`: Menghitung total harga pesanan.
    - `cek_jumlah() -> int`: Menghitung jumlah item dalam pesanan.
    - `tambah_item(item: Item, qty: int)`: Menambahkan item ke dalam pesanan jika belum ada.
    - `edit_item(item: Item, qty: int)`: Mengedit jumlah item dalam pesanan jika ada.
    - `cetak_struk() -> str`: Membuat string untuk mencetak struk pesanan.
    - `__str__() -> str`: Membuat string untuk mencetak objek order.
    """
    counter = 0 # Jumlah order yang telah dibuat
    riwayat = {} # Daftar order yang telah dibuat
    antrean = [] # Antrean order yang belum diproses
    def __init__(self, meja: int, user_id: str):
        self.meja = meja
        self.items = {}
        self.total = 0
        self.jumlah = 0
        self.user_id = user_id
        self.status = Status.PENDING
        self.ID = self.id_generator()
        Order.riwayat[self.ID] = self

    def id_generator(self) -> str:
        """
        Membuat ID komposit unik dengan format:
        `O-XXX-NO-USR--HHMMSS`
          - `O` mengindikasikan ini adalah ID Order (Pesanan)
          - `XXX` mengindikasikan nomor order
          - `NO` adalah 2 digit nomor meja
          - `USR` menunjuk pada inisial user
        """
        Order.counter += 1
        return f"O-{Order.counter:03d}-{self.meja:02d}-{self.user_id[-3:]}"
    
    def cek_total(self) -> int:
        """Menghitung total harga pesanan."""
        total = 0
        for item, qty in self.items.items():
            total += item.harga * qty
        self.total = total
        return self.total

    def cek_jumlah(self) -> int:
        """Menghitung jumlah item dalam pesanan."""
        jumlah = 0
        for qty in self.items.values():
            jumlah += qty
        self.jumlah = jumlah
        return self.jumlah
    
    def tambah_item(self, item: Item, qty: int):
        """Menambah atau mengedit item  dalam pesanan"""
        if  qty <= 0:
            return
        self.items[item] = qty
        self.cek_jumlah()
        self.cek_total()
        
    def cetak_struk(self) -> str:
        """Membuat string untuk mencetak struk pesanan."""
        output = "~" * 67 + "\n"
        output += f"ID Pesanan: {self.ID:>54}\n"
        output += f"User ID: {self.user_id:}\n"
        output += f"Meja: {self.meja:02d}\n"
        output += f"Status Pesanan: {self.status.value}\n\n"
        output += f"{'No':<2} |  ID | {'Item':^15} | {'Harga':^13} | {'Qty':^5} | {"Subtotal":^13}\n"
        output += "-" * 67 + "\n"
        for i, (item, qty) in enumerate(self.items.items(), start=1):
            output += f"{i:02d} | #{(item.ID):02d} | {(item.nama)} | {(qty):^5} | Rp {(item.harga * qty):10,.2f}\n"
        output += "-" * 67 + "\n"
        output += f"Total | Rp {self.cek_total():,.2f}\n".rjust(67)
        output += "~" * 67 + "\n"
        return output

    def __str__(self) -> str:
        output = f"ID Pesanan: {self.ID}\n"
        output += f"Meja: {self.meja}\n"
        output += f"Status Pesanan: {self.status.value}\n"
        output += f"Jumlah Item: {self.cek_jumlah()}\n"
        output += f"Total Harga: Rp {self.cek_total():,.2f}\n"
        return output