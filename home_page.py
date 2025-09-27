# file: home_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

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