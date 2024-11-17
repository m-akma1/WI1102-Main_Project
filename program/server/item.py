class Item:
    """
    Representasi objek dari menu makanan atau minuman yang ada di menu restoran.
    
    Atribut Global:
    - Penghitung item: `counter: int`
    - Menu: `menu: dictionary`

    Atribut Lokal:
    - ID Menu: `ID: int`
    - Nama: `nama: str`
    - Harga (Rp): `harga: int`

    Argumen initialisasi: `Item(nama: str, harga: int) -> Item`
    """
    counter = 0 # Jumlah item yang telah dibuat
    menu = {}   # Daftar menu yang ada
    def __init__(self, nama: str, harga: int):
        Item.counter += 1
        self.nama = nama
        self.harga = harga
        self.ID = Item.counter
        Item.menu[self.ID] = self

    def lihat_menu() -> str:
        """Membuat string untuk mencetak daftar menu makanan dan minuman."""
        # Output adalah variabel string sebagai kontainer sementara hingga f-string selesai diprint
        output = "\n"
        output += f"^" * 38 + "\n"
        output += "{}\n".format("Menu Makanan dan Minuman".center(38, "-"))
        output += f" {'ID'} | {'Item':^15} | {'Harga':^15}\n"
        output += f"-" * 38 + "\n"
        for item in Item.menu.values():
            output += f"{item}\n"
        output += f"^" * 38 + "\n"
        return output

    
    def __str__(self):
        return f"#{self.ID:02d} | {self.nama:<15} | Rp {self.harga:10,.2f}"
    
Menu = [
    Item("Ayam Goreng", 10000),
    Item("Ayam Bakar", 12000),
    Item("Ayam Geprek", 15000),
    Item("Ayam Kremes", 12000),
    Item("Bakso Sapi", 10000),
    Item("Bakso Beranak", 12000),
    Item("Mie Ayam", 12000),
    Item("Mie Goreng", 12000),
    Item("Mie Rebus", 12000),
    Item("Mie Pangsit", 12000),
    Item("Soto Ayam", 15000),
    Item("Soto Betawi", 20000),
    Item("Soto Padang", 25000),
    Item("Sate Ayam", 15000),
    Item("Sate Kambing", 20000),
    Item("Sate Padang", 25000),
    Item("Nasi Putih", 5000),
    Item("Nasi Goreng", 15000),
    Item("Nasi Uduk", 12000),
    Item("Nasi Kuning", 12000),
    Item("Air Mineral", 3000),
    Item("Es Teh", 5000),
    Item("Es Jeruk", 6000),
    Item("Es Campur", 8000),
    Item("Jus Alpukat", 10000),
    Item("Jus Mangga", 10000),
    Item("Jus Jeruk", 10000),
]