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

import threading # Impor modul threading untuk menjalankan kedua antarmuka secara bersamaan
import client.GUI_Interface # Impor modul GUI_Interface dari client
from client.CLI_Interface import CLI_Interface # Impor kelas CLI_Interface dari client

# Fungsi untuk menjalankan antarmuka CLI
def run_cli():
    CLI = CLI_Interface()
    CLI.selamat_datang()

# Fungsi untuk menjalankan antarmuka GUI
def run_gui():
    client.GUI_Interface.run()

# Jalankan kedua antarmuka secara bersamaan
if __name__ == "__main__":
    cli_thread = threading.Thread(target=run_cli)
    gui_thread = threading.Thread(target=run_gui)

    # Memulai kedua thread
    cli_thread.start()
    gui_thread.start()

    # Menunggu kedua thread selesai
    cli_thread.join()
    gui_thread.join()