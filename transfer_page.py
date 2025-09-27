# file: transfer_page.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, 
    QListWidget, QComboBox, QMessageBox, QListWidgetItem, QAbstractItemView # <-- Tambahkan QAbstractItemView
)
from PyQt6.QtCore import Qt
import database

class TransferPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # --- UI UTAMA ---
        self.home_button = QPushButton("Kembali ke Home")
        self.home_button.setFixedWidth(120)

        # Panel Kiri (Sumber)
        left_panel = QFrame()
        left_panel.setFrameShape(QFrame.Shape.StyledPanel)
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("Dari Akun:"))
        self.source_account_combo = QComboBox()
        self.source_pet_list = QListWidget()
        # --- AKTIFKAN MODE MULTI-SELECT ---
        self.source_pet_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        left_layout.addWidget(self.source_account_combo)
        left_layout.addWidget(self.source_pet_list)

        # Panel Tengah (Tombol Aksi)
        middle_panel = QFrame()
        middle_layout = QVBoxLayout(middle_panel)
        middle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.transfer_button = QPushButton(">>\nTransfer")
        self.transfer_button.setFixedSize(80, 80)
        middle_layout.addWidget(self.transfer_button)

        # Panel Kanan (Tujuan)
        right_panel = QFrame()
        right_panel.setFrameShape(QFrame.Shape.StyledPanel)
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(QLabel("Ke Akun:"))
        self.dest_account_combo = QComboBox()
        self.dest_pet_list = QListWidget()
        right_layout.addWidget(self.dest_account_combo)
        right_layout.addWidget(self.dest_pet_list)

        # Gabungkan semua panel
        panels_layout = QHBoxLayout()
        panels_layout.addWidget(left_panel)
        panels_layout.addWidget(middle_panel)
        panels_layout.addWidget(right_panel)

        page_layout = QVBoxLayout(self)
        page_layout.addWidget(self.home_button, alignment=Qt.AlignmentFlag.AlignLeft)
        page_layout.addLayout(panels_layout)

        # --- KONEKSI SINYAL ---
        self.source_account_combo.currentIndexChanged.connect(self.refresh_source_pets)
        self.dest_account_combo.currentIndexChanged.connect(self.refresh_dest_pets)
        self.transfer_button.clicked.connect(self.handle_transfer)

    def load_all_accounts(self):
        """ Memuat semua akun ke kedua combobox """
        accounts = database.get_all_accounts()
        source_id = self.source_account_combo.currentData()
        dest_id = self.dest_account_combo.currentData()

        self.source_account_combo.clear()
        self.dest_account_combo.clear()
        
        self.source_account_combo.addItem("- Pilih Akun -", -1)
        self.dest_account_combo.addItem("- Pilih Akun -", -1)

        for account in accounts:
            self.source_account_combo.addItem(account['nama_akun'], account['id'])
            self.dest_account_combo.addItem(account['nama_akun'], account['id'])
        
        source_idx = self.source_account_combo.findData(source_id)
        if source_idx != -1: self.source_account_combo.setCurrentIndex(source_idx)

        dest_idx = self.dest_account_combo.findData(dest_id)
        if dest_idx != -1: self.dest_account_combo.setCurrentIndex(dest_idx)

    def refresh_source_pets(self):
        """ Update daftar pet di panel kiri """
        self.source_pet_list.clear()
        account_id = self.source_account_combo.currentData()
        if account_id and account_id != -1:
            pets = database.get_pets_by_account_id(account_id)
            for pet in pets:
                item = QListWidgetItem(f"{pet['nama_pet']} (Age: {pet['age_pet']})")
                item.setData(Qt.ItemDataRole.UserRole, pet['id'])
                self.source_pet_list.addItem(item)
    
    def refresh_dest_pets(self):
        """ Update daftar pet di panel kanan """
        self.dest_pet_list.clear()
        account_id = self.dest_account_combo.currentData()
        if account_id and account_id != -1:
            pets = database.get_pets_by_account_id(account_id)
            for pet in pets:
                self.dest_pet_list.addItem(f"{pet['nama_pet']} (Age: {pet['age_pet']})")
    
    def handle_transfer(self):
        # --- LOGIKA BARU UNTUK MULTI-SELECT ---
        selected_pets = self.source_pet_list.selectedItems()
        dest_account_id = self.dest_account_combo.currentData()
        source_account_id = self.source_account_combo.currentData()

        if not selected_pets:
            QMessageBox.warning(self, "Seleksi Gagal", "Pilih satu atau lebih pet dari panel kiri yang ingin ditransfer.")
            return

        if not dest_account_id or dest_account_id == -1:
            QMessageBox.warning(self, "Seleksi Gagal", "Pilih akun tujuan di panel kanan.")
            return
        
        if source_account_id == dest_account_id:
            QMessageBox.warning(self, "Aksi Tidak Valid", "Akun sumber dan tujuan tidak boleh sama.")
            return

        success_count = 0
        for pet_item in selected_pets:
            pet_id_to_transfer = pet_item.data(Qt.ItemDataRole.UserRole)
            if database.transfer_pet(pet_id_to_transfer, dest_account_id):
                success_count += 1
        
        if success_count > 0:
            QMessageBox.information(self, "Sukses", f"Berhasil mentransfer {success_count} pet.")
            self.refresh_source_pets()
            self.refresh_dest_pets()
        else:
            QMessageBox.critical(self, "Gagal", "Gagal mentransfer pet.")