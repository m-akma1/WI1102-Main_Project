# SISTEM PEMESANAN MAKANAN
# PROJEK 1 MATA KULIAH WI1102 - BERPIKIR KOMPUTASIONAL
# KELAS 31 - KELOMPOK 5:
# 1. 19624218 Tiara Clianta Andiwi
# 2. 19624235 Muhammad Akmal
# 3. 19624250 Ahmad Rinofaros Muchtar
# 4. 19624264 Muh. Hartawan Haidir
# 5. 19624284 Muthia Ariesta Anggraeni

# (c) 2024. Bandung. Sekolah Teknik Elektro dan Informatika - Komputasi. Institut Teknologi Bandung.

# DESKRIPSI
# Program ini adalah simulasi dari sistem pemesanan makanan yang memungkinkan pengguna untuk memesan makanan dari meja mereka dan diberitahu saat pesanan mereka sudah siap. Program ini terdiri dari dua sisi: sisi server dan sisi klien. Sisi server bertanggung jawab untuk mengelola database menu, antrean pesanan, dan memproses pesanan. Sisi klien bertanggung jawab untuk menampilkan menu, mengambil pesanan pengguna, dan memberitahu pengguna saat pesanan sudah siap.

# KAMUS
# ...

# ALGORITMA

import collections


class User:
    ID: int

    def __init__(self, nama: str, telp: str):
        self.nama = nama
        self.telp = telp
        self.order = []
        return
    
    def tambah_order(self, order: "Order"):
        self.order.append(order)
        return
    
    def batal_order(self, order_id: int):
        self.order.pop(self.order.index(order_id))
        return
    
    def cek_order(self, order_id: int):
        order = self.order[self.order.index(order_id)]
        return order
    
    def cek_daftar_order(self):
        return self.order
    
    def siap_order(self, order_id: int):
        order = self.order[self.order.index(order_id)]
        if (order.status == "Siap"):
            # Hubungi pengguna
            print("Pesanan sudah siap!")
        return
    
    def __str__(self):
        return f"{self.nama} ({self.telp})"
    
class Order:
    ID: int
    def __init__(self, meja: int, user: User, items: list[list["Item", int]], status: str):
        self.meja = meja
        self.user = user
        self.status = status
        self.items = items
        return
    
    def tambah_item(self, item: "Item", qty: int):
        if item in self.items:
            self.items[self.items.index(item)][1] += qty
        else :
            self.items.append([item, qty])
        return
    
    def edit_item(self, item: "Item", qty: int):
        self.items[self.items.index(item)][1] = qty
        return
    
    def hapus_item(self, item: "Item"):
        self.items.pop(self.items.index(item))
        return
    
    def __str__(self):
        return f"Pesanan #{self.ID} \n a.n. {self.user.nama} ({self.user.telp}) \n Meja {self.meja} \n {self.items} \n Status: {self.status}"
    
class Item:
    ID: int
    def __init__(self, nama: str, harga: int):
        self.nama = nama
        self.harga = harga
        return
    
    def __str__(self):
        return f"Menu #{self.ID} : {self.nama} | Rp{self.harga})"

class Admin:
    antrean = collections.deque(Order)
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        return
    
    def lihat_antrean(self):
        return self.antrean
    
    def lihat_order(self, order_id: int):
        order = self.antrean[self.antrean.index(order_id)]
        return order
    
    def proses_order(self, order_id: int):
        order = self.antrean[self.antrean.index(order_id)]
        for item in order.items:
            print(item)
        return
    
    def selesai_order(self, order_id: int):
        order: Order
        order = self.antrean[self.antrean.index(order_id)]
        order.status = "Siap"
        return
    
