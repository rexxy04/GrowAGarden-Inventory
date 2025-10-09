import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
import database

from home_page import HomePage
from inventory_page import InventoryPage
from transfer_page import TransferPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manajemen Inventaris Pet")
        self.setGeometry(100, 100, 900, 600) # Sedikit diperlebar

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Buat instance dari setiap halaman
        self.home_page = HomePage()
        self.inventory_page = InventoryPage()
        self.transfer_page = TransferPage()

        # Tambahkan halaman ke QStackedWidget
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.inventory_page)
        self.stacked_widget.addWidget(self.transfer_page)

        # Hubungkan sinyal tombol dari setiap halaman
        self.home_page.inventory_button.clicked.connect(self.go_to_inventory)
        self.home_page.transfer_button.clicked.connect(self.go_to_transfer)
        
        self.inventory_page.home_button.clicked.connect(self.go_to_home)
        self.transfer_page.home_button.clicked.connect(self.go_to_home)

    def go_to_inventory(self):
        self.inventory_page.load_accounts() # load data saat halaman dibuka
        self.inventory_page.load_master_pets_to_combobox() # load data master pet ke combobox
        self.stacked_widget.setCurrentIndex(1)

    def go_to_transfer(self):
        self.transfer_page.load_all_accounts() # load data saat halaman dibuka
        self.stacked_widget.setCurrentIndex(2)

    def go_to_home(self):
        self.stacked_widget.setCurrentIndex(0)

# Jalankan Aplikasi
if __name__ == "__main__":
    database.initialize_database()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())