import threading
import client.GUI_Interface
from client.CLI_Interface import CLI_Interface

def run_cli():
    CLI = CLI_Interface()
    CLI.selamat_datang()

def run_gui():
    client.GUI_Interface.run()

if __name__ == "__main__":
    cli_thread = threading.Thread(target=run_cli)
    gui_thread = threading.Thread(target=run_gui)

    # Start both threads
    cli_thread.start()
    gui_thread.start()

    # Wait for both threads to finish
    cli_thread.join()
    gui_thread.join()
