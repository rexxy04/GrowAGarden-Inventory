import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame, QListWidget, QTableWidget,
    QTableWidgetItem, QListWidgetItem
)
from PyQt6.QtCore import Qt

# Impor fungsi-fungsi dari file database.py kita
import database

# --- Halaman 1: Homepage (Tidak ada perubahan) ---
class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Aplikasi Inventaris Pet")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.inventory_button = QPushButton("📦\n\nKelola Inventaris")
        self.transfer_button = QPushButton("🔄\n\nTransfer Pet")
        
        button_style = """
            QPushButton {
                font-size: 16px;
                height: 100px;
                width: 200px;
                border: 1px solid #AAAAAA;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """
        self.inventory_button.setStyleSheet(button_style)
        self.transfer_button.setStyleSheet(button_style)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.inventory_button)
        button_layout.addWidget(self.transfer_button)
        
        layout.addLayout(button_layout)


# --- Halaman 2: Halaman Inventaris (Banyak Perubahan!) ---
class InventoryPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QHBoxLayout(self)
        
        # Tombol Kembali
        self.home_button = QPushButton("Kembali ke Home")
        self.home_button.setFixedWidth(120)

        # Panel Kiri: Daftar Akun
        left_panel = QFrame()
        left_panel.setFrameShape(QFrame.Shape.StyledPanel)
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("Daftar Akun"))
        
        # Ganti QLabel dengan QListWidget
        self.account_list_widget = QListWidget()
        left_layout.addWidget(self.account_list_widget)
        
        # Panel Kanan: Daftar Pet
        right_panel = QFrame()
        right_panel.setFrameShape(QFrame.Shape.StyledPanel)
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(QLabel("Daftar Pet"))
        
        # Ganti QLabel dengan QTableWidget
        self.pet_table_widget = QTableWidget()
        self.pet_table_widget.setColumnCount(4) # ID, Nama, Umur, Berat
        self.pet_table_widget.setHorizontalHeaderLabels(["ID", "Nama Pet", "Umur", "Berat"])
        right_layout.addWidget(self.pet_table_widget)

        # Gabungkan panel-panel
        panels_layout = QHBoxLayout()
        panels_layout.addWidget(left_panel, 1) 
        panels_layout.addWidget(right_panel, 3) 
        
        # Layout utama halaman inventaris
        page_layout = QVBoxLayout()
        page_layout.addWidget(self.home_button, alignment=Qt.AlignmentFlag.AlignLeft)
        page_layout.addLayout(panels_layout)

        self.setLayout(page_layout)

    def load_accounts(self):
        """Memuat daftar akun dari database dan menampilkannya."""
        self.account_list_widget.clear() # Bersihkan daftar sebelum memuat
        accounts = database.get_all_accounts()
        for account in accounts:
            # Kita simpan ID di dalam item untuk referensi nanti
            item = QListWidgetItem(account['name'])
            item.setData(Qt.ItemDataRole.UserRole, account['id']) # Simpan ID akun
            self.account_list_widget.addItem(item)
            

# --- Jendela Utama Aplikasi (Ada sedikit tambahan) ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manajemen Inventaris Pet")
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.home_page = HomePage()
        self.inventory_page = InventoryPage()

        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.inventory_page)

        self.home_page.inventory_button.clicked.connect(self.go_to_inventory)
        self.home_page.transfer_button.clicked.connect(self.go_to_inventory)
        self.inventory_page.home_button.clicked.connect(self.go_to_home)

    def go_to_inventory(self):
        # Panggil load_accounts setiap kali kita pindah ke halaman inventaris
        self.inventory_page.load_accounts()
        self.stacked_widget.setCurrentIndex(1)

    def go_to_home(self):
        self.stacked_widget.setCurrentIndex(0)

# --- Jalankan Aplikasi ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())