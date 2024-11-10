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
    if array_pesanan == []:#Kosong
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