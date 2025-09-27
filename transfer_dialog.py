# file: transfer_dialog.py

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox

class TransferDialog(QDialog):
    def __init__(self, destination_accounts, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Transfer Pet")
        
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Pindahkan ke Akun:"))
        
        self.account_combo = QComboBox()
        for account in destination_accounts:
            self.account_combo.addItem(account['nama_akun'], account['id'])
            
        layout.addWidget(self.account_combo)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_selected_account_id(self):
        return self.account_combo.currentData()