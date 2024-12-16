"""
SISTEM PEMESANAN MAKANAN
PROJEK 2 MATA KULIAH WI1102 - BERPIKIR KOMPUTASIONAL
KELAS 31 - KELOMPOK 5:
1. 19624218 Tiara Clianta Andiwi
2. 19624235 Muhammad Akmal
3. 19624250 Ahmad Rinofaros Muchtar
4. 19624264 Muh. Hartawan Haidir
5. 19624284 Muthia Ariesta Anggraeni

(c) 2024. Bandung. Sekolah Teknik Elektro dan Informatika. Institut Teknologi Bandung.
"""

import tkinter as tk # Impor modul tkinter sebagai tk
from client import admin_interface as admin # Impor modul interface dari client
from client import user_interface as user # Impor modul interface dari client

# Jalankan kedua antarmuka secara bersamaan
if __name__ == "__main__":
    root = tk.Tk() # Membuat objek root dari kelas Tk
    admin_window = admin.admin_interface(root, user.user_interface) # Membuat objek admin_window dari kelas admin_interface
    root.mainloop()