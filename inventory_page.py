# file: inventory_page.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, 
    QListWidget, QTableWidget, QTableWidgetItem, QListWidgetItem, 
    QLineEdit, QMessageBox, QGridLayout, QHeaderView, QCheckBox
)
from PyQt6.QtCore import Qt
import database

# Impor dialog dari filenya sendiri
from transfer_dialog import TransferDialog

class InventoryPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.home_button = QPushButton("Kembali ke Home")
        self.home_button.setFixedWidth(120)

        #left sidebar: daftar akun
        left_panel = QFrame()
        left_panel.setFrameShape(QFrame.Shape.StyledPanel)
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("Daftar Akun"))
        
        self.account_list_widget = QListWidget()
        left_layout.addWidget(self.account_list_widget)

        self.account_name_input = QLineEdit()
        self.account_name_input.setPlaceholderText("Nama akun baru...")
        self.add_account_button = QPushButton("Tambah Akun")
        
        add_account_layout = QHBoxLayout()
        add_account_layout.addWidget(self.account_name_input)
        add_account_layout.addWidget(self.add_account_button)
        left_layout.addLayout(add_account_layout)
        
        self.delete_account_button = QPushButton("Hapus Akun Terpilih")
        left_layout.addWidget(self.delete_account_button)
        
        #right sidebar: daftar & form manajemen pet
        right_panel = QFrame()
        right_panel.setFrameShape(QFrame.Shape.StyledPanel)
        right_layout = QVBoxLayout(right_panel)
        
        pet_header_layout = QHBoxLayout()
        pet_header_layout.addWidget(QLabel("Daftar Pet"))
        self.pet_count_label = QLabel("")
        self.pet_count_label.setStyleSheet("font-style: italic; color: #666;")
        pet_header_layout.addWidget(self.pet_count_label)
        pet_header_layout.addStretch()
        self.select_all_checkbox = QCheckBox("Pilih Semua")
        pet_header_layout.addWidget(self.select_all_checkbox)
        right_layout.addLayout(pet_header_layout)
        
        self.pet_table_widget = QTableWidget()
        self.pet_table_widget.setColumnCount(7)
        self.pet_table_widget.setHorizontalHeaderLabels(["Pilih", "ID", "Nama Pet", "Umur", "Berat", "Base Weight", "Kategori Size"])
        right_layout.addWidget(self.pet_table_widget)

        header = self.pet_table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)

        pet_form_layout = QGridLayout()
        self.pet_name_input = QLineEdit()
        self.pet_age_input = QLineEdit()
        self.pet_weight_input = QLineEdit()
        
        pet_form_layout.addWidget(QLabel("Nama:"), 0, 0)
        pet_form_layout.addWidget(self.pet_name_input, 0, 1)
        pet_form_layout.addWidget(QLabel("Umur:"), 1, 0)
        pet_form_layout.addWidget(self.pet_age_input, 1, 1)
        pet_form_layout.addWidget(QLabel("Berat (kg):"), 2, 0)
        pet_form_layout.addWidget(self.pet_weight_input, 2, 1)
        right_layout.addLayout(pet_form_layout)

        pet_button_layout = QHBoxLayout()
        self.add_pet_button = QPushButton("Tambah")
        self.update_pet_button = QPushButton("Update")
        self.delete_pet_button = QPushButton("Hapus")
        self.transfer_pet_button = QPushButton("Transfer")
        pet_button_layout.addWidget(self.add_pet_button)
        pet_button_layout.addWidget(self.update_pet_button)
        pet_button_layout.addWidget(self.delete_pet_button)
        pet_button_layout.addWidget(self.transfer_pet_button)
        right_layout.addLayout(pet_button_layout)
        
        panels_layout = QHBoxLayout()
        panels_layout.addWidget(left_panel, 1) 
        panels_layout.addWidget(right_panel, 3) 
        
        page_layout = QVBoxLayout(self)
        page_layout.addWidget(self.home_button, alignment=Qt.AlignmentFlag.AlignLeft)
        page_layout.addLayout(panels_layout)

        #connect signals ke functions
        self.add_account_button.clicked.connect(self.handle_add_account)
        self.delete_account_button.clicked.connect(self.handle_delete_account)
        self.account_list_widget.currentItemChanged.connect(self.handle_account_selection_changed)
        self.pet_table_widget.cellClicked.connect(self.handle_pet_selection)
        self.add_pet_button.clicked.connect(self.handle_add_pet)
        self.update_pet_button.clicked.connect(self.handle_update_pet)
        self.delete_pet_button.clicked.connect(self.handle_delete_pet)
        self.transfer_pet_button.clicked.connect(self.handle_transfer_pet)
        self.select_all_checkbox.stateChanged.connect(self.handle_select_all_pets)
        
    def load_accounts(self):
        self.account_list_widget.clear()
        accounts = database.get_all_accounts()
        for account in accounts:
            item = QListWidgetItem(account['nama_akun']) 
            item.setData(Qt.ItemDataRole.UserRole, account['id'])
            self.account_list_widget.addItem(item)

    def display_pets(self, pets):
        self.pet_table_widget.setRowCount(0)
        self.select_all_checkbox.setChecked(False) 
        pet_count = len(pets)
        self.pet_count_label.setText(f" (Total: {pet_count})")
        
        for row_number, pet in enumerate(pets):
            self.pet_table_widget.insertRow(row_number)
            
            checkbox = QCheckBox()
            cell_widget = QWidget()
            cell_layout = QHBoxLayout(cell_widget)
            cell_layout.addWidget(checkbox)
            cell_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cell_layout.setContentsMargins(0,0,0,0)
            self.pet_table_widget.setCellWidget(row_number, 0, cell_widget)
            
            self.pet_table_widget.setItem(row_number, 1, QTableWidgetItem(str(pet['id'])))
            self.pet_table_widget.setItem(row_number, 2, QTableWidgetItem(pet['nama_pet']))
            self.pet_table_widget.setItem(row_number, 3, QTableWidgetItem(str(pet['age_pet'])))
            self.pet_table_widget.setItem(row_number, 4, QTableWidgetItem(str(pet['weight_pet'])))
            
            base_weight = 0.0
            try:
                age = pet['age_pet']
                weight = pet['weight_pet']
                if age <= 0:
                    base_weight_str = "N/A"
                else:
                    base_weight = weight / (1 + 0.090909 * (age - 1))
                    base_weight_str = f"{base_weight:.2f}"
            except (ValueError, TypeError):
                base_weight_str = "Error"
            self.pet_table_widget.setItem(row_number, 5, QTableWidgetItem(base_weight_str))

            kategori_str = "N/A"
            if base_weight > 0:
                if base_weight < 4:
                    kategori_str = "Small"
                elif base_weight < 5:
                    kategori_str = "Semi Huge"
                elif base_weight < 7:
                    kategori_str = "Huge"
                elif base_weight < 8:
                    kategori_str = "Semi Titanic"
                elif base_weight < 10:
                    kategori_str = "Titanic"
                else:
                    kategori_str = "Godly"
            self.pet_table_widget.setItem(row_number, 6, QTableWidgetItem(kategori_str))

    def handle_delete_account(self):
        current_item = self.account_list_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Akun Belum Dipilih", "Silakan pilih akun yang ingin dihapus dari daftar.")
            return

        account_id = current_item.data(Qt.ItemDataRole.UserRole)
        account_name = current_item.text()
        confirm_text = (f"Apakah Anda yakin ingin menghapus akun '{account_name}'?\n\n"
                        "PERINGATAN: Semua pet di dalam akun ini akan ikut terhapus secara permanen.")
        confirm = QMessageBox.question(self, "Konfirmasi Hapus Akun", confirm_text,
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm == QMessageBox.StandardButton.Yes:
            if database.delete_account(account_id):
                self.load_accounts()
                self.display_pets([])
                QMessageBox.information(self, "Sukses", f"Akun '{account_name}' berhasil dihapus.")
            else:
                QMessageBox.critical(self, "Gagal", "Gagal menghapus akun dari database.")

    def handle_select_all_pets(self, state):
        is_checked = state == Qt.CheckState.Checked.value
        for row in range(self.pet_table_widget.rowCount()):
            cell_widget = self.pet_table_widget.cellWidget(row, 0)
            checkbox = cell_widget.findChild(QCheckBox)
            if checkbox:
                checkbox.setChecked(is_checked)
    
    def get_checked_pets(self):
        checked_pets = []
        for row in range(self.pet_table_widget.rowCount()):
            cell_widget = self.pet_table_widget.cellWidget(row, 0)
            checkbox = cell_widget.findChild(QCheckBox)
            if checkbox and checkbox.isChecked():
                pet_info = {
                    'id': int(self.pet_table_widget.item(row, 1).text()),
                    'name': self.pet_table_widget.item(row, 2).text()
                }
                checked_pets.append(pet_info)
        return checked_pets

    def handle_delete_pet(self):
        pets_to_delete = self.get_checked_pets()
        if not pets_to_delete:
            QMessageBox.warning(self, "Pet Belum Dipilih", "Silakan centang satu atau lebih pet yang ingin dihapus.")
            return
        confirm = QMessageBox.question(self, "Konfirmasi Hapus", 
                                    f"Apakah Anda yakin ingin menghapus {len(pets_to_delete)} pet yang dipilih?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm == QMessageBox.StandardButton.Yes:
            success_count = 0
            for pet in pets_to_delete:
                if database.delete_pet(pet['id']):
                    success_count += 1
            QMessageBox.information(self, "Sukses", f"Berhasil menghapus {success_count} pet.")
            self.handle_account_selection_changed(self.account_list_widget.currentItem(), None)
            self.clear_pet_form()

    def handle_transfer_pet(self):
        pets_to_transfer = self.get_checked_pets()
        current_account_item = self.account_list_widget.currentItem()
        if not pets_to_transfer:
            QMessageBox.warning(self, "Pet Belum Dipilih", "Silakan centang satu atau lebih pet yang ingin ditransfer.")
            return
        if not current_account_item:
            QMessageBox.warning(self, "Akun Asal Belum Dipilih", "Silakan pilih akun asal terlebih dahulu.")
            return

        source_account_id = current_account_item.data(Qt.ItemDataRole.UserRole)
        all_accounts = database.get_all_accounts()
        destination_accounts = [acc for acc in all_accounts if acc['id'] != source_account_id]
        if not destination_accounts:
            QMessageBox.information(self, "Tidak Ada Tujuan", "Tidak ada akun lain untuk tujuan transfer.")
            return

        dialog = TransferDialog(destination_accounts, self)
        if dialog.exec():
            new_account_id = dialog.get_selected_account_id()
            success_count = 0
            for pet in pets_to_transfer:
                if database.transfer_pet(pet['id'], new_account_id):
                    success_count += 1
            QMessageBox.information(self, "Sukses", f"Berhasil mentransfer {success_count} pet.")
            self.handle_account_selection_changed(current_account_item, None)
            self.clear_pet_form()

    def handle_add_account(self):
        account_name = self.account_name_input.text().strip()
        if not account_name:
            QMessageBox.warning(self, "Input Kosong", "Nama akun tidak boleh kosong.")
            return
        if database.add_account(account_name):
            self.account_name_input.clear()
            self.load_accounts()
        else:
            QMessageBox.critical(self, "Gagal", "Gagal menambahkan akun ke database.")

    def handle_account_selection_changed(self, current, previous):
        self.clear_pet_form()
        if current is None:
            self.display_pets([])
            return
        account_id = current.data(Qt.ItemDataRole.UserRole)
        pets = database.get_pets_by_account_id(account_id)
        self.display_pets(pets)

    def handle_pet_selection(self, row, column):
        self.pet_name_input.setText(self.pet_table_widget.item(row, 2).text())
        self.pet_age_input.setText(self.pet_table_widget.item(row, 3).text())
        self.pet_weight_input.setText(self.pet_table_widget.item(row, 4).text())

    def clear_pet_form(self):
        self.pet_name_input.clear()
        self.pet_age_input.clear()
        self.pet_weight_input.clear()
        self.pet_table_widget.clearSelection()

    def handle_add_pet(self):
        current_account_item = self.account_list_widget.currentItem()
        if not current_account_item:
            QMessageBox.warning(self, "Akun Belum Dipilih", "Silakan pilih akun terlebih dahulu.")
            return
        
        account_id = current_account_item.data(Qt.ItemDataRole.UserRole)
        name = self.pet_name_input.text().strip()
        age = self.pet_age_input.text().strip()
        weight = self.pet_weight_input.text().strip().replace(',', '.')

        if not name or not age or not weight:
            QMessageBox.warning(self, "Input Kosong", "Semua field pet harus diisi.")
            return
        try:
            if database.add_pet(name, int(age), float(weight), account_id):
                self.handle_account_selection_changed(current_account_item, None)
                self.clear_pet_form()
            else:
                QMessageBox.critical(self, "Gagal", "Gagal menambahkan pet.")
        except ValueError:
            QMessageBox.critical(self, "Input Salah", "Umur harus angka dan berat harus angka (contoh: 3 atau 1.5).")

    def handle_update_pet(self):
        selected_pet_row = self.pet_table_widget.currentRow()
        if selected_pet_row < 0:
            QMessageBox.warning(self, "Pet Belum Dipilih", "Silakan pilih pet dari tabel untuk di-update.")
            return
        
        pet_id = int(self.pet_table_widget.item(selected_pet_row, 1).text())
        name = self.pet_name_input.text().strip()
        age = self.pet_age_input.text().strip()
        weight = self.pet_weight_input.text().strip().replace(',', '.')

        if not name or not age or not weight:
            QMessageBox.warning(self, "Input Kosong", "Semua field pet harus diisi.")
            return
        try:
            if database.update_pet(pet_id, name, int(age), float(weight)):
                self.handle_account_selection_changed(self.account_list_widget.currentItem(), None)
                self.clear_pet_form()
            else:
                QMessageBox.critical(self, "Gagal", "Gagal meng-update pet.")
        except ValueError:
            QMessageBox.critical(self, "Input Salah", "Umur harus angka dan berat harus angka (contoh: 3 atau 1.5).")