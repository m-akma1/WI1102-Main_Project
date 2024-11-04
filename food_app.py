# PROGRAM PEMESANAN MAKANAN

# DESKRIPSI
# ...

# KAMUS
# ...


# ALGORITMA

import queue

# Models
class Menu:
    def __init__(self, id: int, nama: str, harga: int):
        self.id = id
        self.nama = nama
        self.harga = harga

    def __str__(self):
        return f"{self.nama} (Rp{self.harga})"


class Pesanan:
    def __init__(self, id: int, pesanan: list[Menu]):
        self.id = id
        self.daftar = pesanan
        self.status = "Belum Diproses"

    def tambah_pesanan(self, pesanan: Menu):
        self.daftar.append(pesanan)

    def __str__(self):
        daftar_menu = ''
        for menu in self.daftar :
            daftar_menu = daftar_menu.join(['\n-', str(menu)])
        return f"Pesanan ke #{self.id}: {daftar_menu} \nStatus Pesanan: {self.status}"

class User:
    def __init__(self, id, nama, no_meja):
        self.id = id
        self.nama = nama
        self.no_meja = no_meja
        self.pesanan = []

        
# Server Logic
class MenuDB:
    def __init__(self, data):
        self.menu = data

    def get_item(self, item_id):
        item_data = self.menu.get(str(item_id))
        if item_data:
            return Item(id=item_id, nama=item_data["name"], harga=item_data["price"])
        else:
            return None

class OrderQueue:
    def __init__(self):
        self.queue = queue.Queue()

    def add_order(self, order):
        self.queue.put(order)
        print(f"Order {order.id} added to queue.")

    def get_next_order(self):
        return self.queue.get() if not self.queue.empty() else None

# Client Interface
def simulate_user_order(menu_db, order_queue, user):
    item = menu_db.get_item(1)  # Example: ordering item with ID 1 (Burger)
    order = Order(id=1, items=[item])
    user.place_order(order)
    order_queue.add_order(order)

# Main App Flow
def main():
    # Setup
    menu_db = MenuDB(MENU_DATA)
    order_queue = OrderQueue()
    user = User(id=1, nama="Alice", no_meja=3)

    # Simulate placing an order
    simulate_user_order(menu_db, order_queue, user)

    # Process an order
    next_order = order_queue.get_next_order()
    if next_order:
        next_order.status = "Completed"
        print(f"Chef processed {next_order}")

if __name__ == "__main__":
    main()
