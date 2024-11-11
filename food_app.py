"""
SISTEM PEMESANAN MAKANAN
PROJEK 1 MATA KULIAH WI1102 - BERPIKIR KOMPUTASIONAL
KELAS 31 - KELOMPOK 5:
1. 19624218 Tiara Clianta Andiwi
2. 19624235 Muhammad Akmal
3. 19624250 Ahmad Rinofaros Muchtar
4. 19624264 Muh. Hartawan Haidir
5. 19624284 Muthia Ariesta Anggraeni

(c) 2024. Bandung. Sekolah Teknik Elektro dan Informatika. Institut Teknologi Bandung.
"""

"""
DESKRIPSI
Program ini adalah simulasi dari sistem pemesanan makanan yang memungkinkan pengguna untuk memesan makanan dari meja mereka dan diberitahu saat pesanan mereka sudah siap. Program ini terdiri dari dua sisi: sisi server dan sisi klien. Sisi server bertanggung jawab untuk mengelola database menu, antrean pesanan, dan memproses pesanan. Sisi klien bertanggung jawab untuk menampilkan menu, mengambil pesanan pengguna, dan memberitahu pengguna saat pesanan sudah siap.
"""

# KAMUS
# ...

# ALGORITMA

import enum
import datetime
import copy

class Item:
    """
    Representasi objek dari menu makanan atau minuman yang ada di menu restoran.
    
    Atribut:
    - ID Menu: `ID: int`
    - Nama: `nama: str`
    - Harga: `harga: int`
    """
    counter = 0
    def __init__(self, nama: str, harga: int):
        Item.counter += 1
        self.nama = nama
        self.harga = harga
        self.ID = Item.counter
    
    def __str__(self):
        return f"#{self.ID:02d}. {self.nama} | Rp{self.harga}\n"

class Status(enum.Enum):
    """Enumerasi status pesanan."""
    PENDING = "Menunggu dikonfirmasi"
    CONFIRMED = "Dikonfirmasi, dalam antrean"
    IN_PROGRESS = "Dalam proses"
    READY = "Siap diambil"
    COMPLETED = "Selesai"

# Daftar Menu
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

# Fungsi terpisah untuk melihat daftar menu
def lihat_menu():
    output = f"Menu Makanan dan Minuman:"
    output += f"{'No.':<5} {'Item':<15} {'Harga':<10}\n"
    output += f"-" * 30 + "\n"
    for item in Menu:
        output += f"{item}"
    
    print(output)

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
    """
    counter = 0
    def __init__(self, meja: int, user: "User"):
        self.meja = meja
        self.user = user
        self.items = []
        self.status = Status.PENDING
        self.ID = self.id_generator()

    def id_generator(self):
        """
        Membuat ID komposit unik dengan format:
        O-XXX-NO-USR--HHMMSS:
          - O mengindikasikan ini adalah ID Order (Pesanan)
          - XXX mengindikasikan nomor order
          - NO adalah 2 digit nomor meja
          - USR menunjuk pada inisial user
          - HHMMSS adalah waktu ketika pesanan dibuat
        """
        Order.counter += 1
        timestamp = datetime.datetime.now().strftime("%H%M%S")
        return f"O-{Order.counter:03d}-{self.meja:02d}-{self.user.ID[2:4]-{timestamp}}"
    
    def cek_total(self):
        """Menghitung total harga pesanan."""
        total = 0
        for item in self.items:
            total += item[0].harga * item[1]
        self.total = total
        return self.total
    
    def tambah_item(self, item: Item, qty: int):
        """
        Menambahkan item ke dalam pesanan jika belum ada.
        Jika sudah ada, tambahkan jumlahnya.
        """
        if item in self.items:
            self.items[self.items.index(item)][1] += qty
        else :
            self.items.append([item, qty])
    
    def edit_item(self, item: "Item", qty: int):
        """Mengedit jumlah item dalam pesanan."""
        try:
            self.items[self.items.index(item)][1] = qty
            if qty <= 0:
                self.hapus_item(item)
        except:
            print("Item tidak ditemukan.")
    
    def hapus_item(self, item: "Item"):
        try: 
            self.items.pop(self.items.index(item))
        except:
            print("Item tidak ditemukan.")
        
    def edit_status(self, status):
        self.status = status
    
    def __str__(self):
        output = f"Pesanan {self.ID}\n"
        output += f"Nama: {self.user.nama}\nTelp: {self.user.telp})\n"
        output += f"Meja {self.meja}\nStatus Pesanan: {self.status}\n"
        output += f"{'No.':<5} {'Item':<15} {'Harga':<10} {'Jumlah':<10}\n"
        output += "-" * 40 + "\n"
        for i, item in self.items:
            item: list[Item, int]
            output += f"{i+1:<5} {item[0].nama:<15} Rp{item.harga:<10.2f} {item[1]:<10}\n"
        output += f"Total Harga: Rp{self.cek_total()}"
        return output
    
# Antrean Pesanan
order_queue = []

class User:
    """
    Berisi semua informasi berkaitan dengan data pemesan.

    Atribut:
    - User ID: `id: int`
    - Nama: `nama: str`
    - No. Telepon: `telp: str`
    - Daftar Pesanan: `order: List[Order]`
    """

    counter = 0
    def __init__(self, nama: str, telp: str):
        self.ID = self.id_generator()
        self.nama = nama
        self.telp = telp
        self.orders = {}
        return
    
    def id_generator(self):
        """
        Membuat ID komposit unik dengan format:
        U-XXX-ABC:
          - U mengindikasikan ini adalah ID User
          - XXX adalah urutan nomor user yang dibuat
          - ABC adalah inisial nama user
        """
        initial = self.nama[:3].upper()
        User.counter += 1
        return f"U-{User.counter:03d}-{initial}"

    def tambah_order(self, order: Order):
        """Menambahkan pesanan ke dalam daftar pesanan pengguna."""
        self.orders[order.ID] = order
        order_queue.append(order)
        order.status = Status.CONFIRMED
        return
        
    def lihat_order(self, order_id: str):
        """Melihat detail pesanan berdasarkan ID pesanan."""
        return self.orders.get(order_id)
    

    def lihat_daftar(self):
        """Melihat daftar pesanan yang dimiliki pengguna."""
        output = ""
        for order in self.orders:
            output += f"{order}\n"
        return output
    
    def notifikasi(self, order: Order):
        """Memberitahu pengguna bahwa pesanannya sudah siap."""
        if order.status == Status.READY:
            print(f"Pesanan {order.ID} sudah siap diambil.")
            while True:
                jawab = input("Apakah pesanan sudah diambil? (Y/n) : ")
                if jawab == "Y":
                    order.edit_status(Status.COMPLETED)
                    break
                elif jawab == "N":
                    break
                else:
                    print("Input tidak dikenal.")
        return

    def __str__(self):
        output = f"User ID: {self.ID}\n"
        output += f"Nama: {self.nama}\n"
        output += f"Telepon: {self.telp}\n"
        return output
    
class Admin:
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password
        self.auth = False
        return
    
    def lihat_antrean(self):
        return self.antrean
    
    def lihat_order(self, order_id: int):
        order = 0 #self.antrean[self.antrean.index(order_id)]
        return order
    
    def proses_order(self, order_id: int):
        order: Order #= self.antrean[self.antrean.index(order_id)]
        for item in order.items:
            print(item)
        return
    
    def selesai_order(self, order_id: int):
        order: Order
        #order = self.antrean[self.antrean.index(order_id)]
        order.status = "Siap"
        return

##Mulai
#Langkah 1(Pilih Peran)
def langkah_satu():
    while True:
        print("Masukkan peran anda(Koki/Pengguna)",end=" ")
        peran = input()
        if peran == "Koki":
            user = Admin()
            langkah_dua()
            break
        elif peran == "Pengguna":
            user = User()
            langkah_tiga()
            break
        elif peran == "selesai":
            #Langkah 12
            pass
        else:
            print("Silahkan memasukkan password yang benar")
#Langkah 2(Koki masukkan password)
def langkah_dua():
    while True:
        print("Silahkan memasukkan username dan password")
        print("Username:", end=" ")
        user = Admin(input(), input())
        if user.password() == "benar":
            #Langkah 4
            break
        elif user.password() == "kembali":
            langkah_satu() 
            break
        else:
            print("Silahkan memasukkan password yang benar")
#Langkah 3(Pengguna pilih opsi)
def langkah_tiga():
    while True:
        print("Apakah anda sudah memiliki user ID?(Y/N)", end=" ")
        sudah = input()
        if sudah == "Y":
            #langkah 5
            break
        elif sudah == "N":
            #Langkah 6
            break
        elif sudah == "kembali":
            langkah_satu        
#Langkah 4(Koki pilih opsi)
def langkah_empat():
    while True:
        print("Apakah anda ingin melihat antrean atau memproses pesanan?(A/B)",end=" ")
        pilihan_1 = input()
        if pilihan_1 == "A":
            #Langkah 7
            break
        elif pilihan_1 == "B":
            #Langkah 8
            break
        elif pilihan_1 == "kembali":
            langkah_satu()
            break
        else:
            print("Input tidak dikenal, silahkan mengisi lagi")


#Langkah 5(Pengguna dengan user ID)
def langkah_lima():
    print("Silahkan memasukkan User ID:", end=" ")
    user_id = input()
    if user_id == "benar":
        #Langkah 9
        pass
    elif user_id == "kembali":
        langkah_satu()
    else: 
        print("Maaf, User ID anda tidak dikenali.")
        print("Silahkan mengisi ulang User ID atau membuat User ID baru(A/B)", end=" ")
        pilihan_2 = input()
        if pilihan_2 == "A":
            pass
        elif pilihan_2 == "B":
            #Langkah 6
            pass

#Langkah 6(Pengguna membuat user ID)
def langkah_enam():
    print("Silahkan memasukkan nama dan nomor telepon")
    print("Nama:", end=" ")
    #Mekanisme nama
    print("Nomor Telepon:",end=" ")
    #Mekanisme nomor telepon
    #Langkah 9

#Langkah 7(Koki melihat antrean)
def langkah_tujuh():
    #Tampilkan antrian pesanan yang belum diproses
    print("Silahkan memilih pesanan yang ingin diproses secara manual", end=" ")
    #manual = int(input()+1 
    #pesanan = array_pesanan[manual]
    #array_pesanan.append[manual]
    #Langkah 8

#Langkah 8(Koki memproses pesanan)
def langkah_delapan():
    #if array_pesanan == []: Kosong
        #Langkah 4
        pass

#Langkah 9(Pengguna melihat dashboard)
def langkah_sembilan():
    #Tampilkan array_pesanan
    print("Apakah anda ingin membuat pesanan?(Y/N)",end=" ")
    memesan = input()
    if memesan == "Y":
        #Langkah 10
        pass
    elif memesan == "N":
        pass
    elif memesan == "kembali":
        #Langkah 1
        pass

#Langkah 10(Pengguna membuat pesanan)
def langkah_sepuluh():
    #Tampilkan menu dan pesanan yang tersedia
    print("Silahkan memasukkan pesanan anda:",end=" ")
    #Mekanisme memasukkan ID Pesanan
    print(f"Apakah pesanan anda sesuai?")
    #ID pesanan ditambahkan dalam array pesanan atau antrean pusat
    #Langkah 11


#Langkah 11(Pengguna melihat status pesanan)
def langkah_sebelas():
    #Tampilkan status pesanan pengguna
    #Bila semua pesanan sudah siap, pengguna diberi notifikasi
    print("Apakah anda ingin kembali?", end=" ")
    kembali = input()
    if kembali == "kembali":
        #Langkah 9
        pass

#Langkah 12(Program berhenti)
def langkah_dua_belas():
    ##Selesai:
    pass


