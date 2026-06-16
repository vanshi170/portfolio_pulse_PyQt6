import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QComboBox, QPushButton, QLabel, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
from storage.settings import Settings
from storage.statistics import Statistics
from storage.portfolio_storage import PortfolioStorage
from ui.components.toast import Toast

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = Settings()
        self.stats = Statistics()
        self.portfolio_storage = PortfolioStorage()
        self.init_ui()
        
    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)
        
        title = QLabel("Settings")
        title.setObjectName("title")
        self.layout.addWidget(title)
        
        card = QWidget()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["Dark", "Light"])
        self.combo_theme.setCurrentText(self.settings.get("theme").capitalize())
        
        self.combo_currency = QComboBox()
        self.combo_currency.addItems(["USD", "INR", "EUR", "GBP"])
        self.combo_currency.setCurrentText(self.settings.get("currency"))
        
        form_layout.addRow("Theme:", self.combo_theme)
        form_layout.addRow("Currency:", self.combo_currency)
        
        card_layout.addLayout(form_layout)
        
        btn_save = QPushButton(" Save Settings")
        btn_save.clicked.connect(self.save_settings)
        card_layout.addWidget(btn_save, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.layout.addWidget(card)
        
        # Danger Zone
        danger_card = QWidget()
        danger_card.setObjectName("card")
        danger_layout = QVBoxLayout(danger_card)
        danger_layout.setContentsMargins(20, 20, 20, 20)
        
        danger_title = QLabel("Danger Zone")
        danger_title.setObjectName("subtitle")
        danger_title.setStyleSheet("color: #ef4444; font-weight: bold;")
        danger_layout.addWidget(danger_title)
        
        btn_reset_port = QPushButton("Reset Portfolio")
        btn_reset_port.setObjectName("danger")
        btn_reset_port.clicked.connect(self.reset_portfolio)
        
        btn_reset_stats = QPushButton("Reset Statistics")
        btn_reset_stats.setObjectName("danger")
        btn_reset_stats.clicked.connect(self.reset_stats)
        
        danger_layout.addWidget(btn_reset_port, alignment=Qt.AlignmentFlag.AlignLeft)
        danger_layout.addWidget(btn_reset_stats, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.layout.addWidget(danger_card)
        self.layout.addStretch()
        
    def save_settings(self):
        old_theme = self.settings.get("theme")
        new_theme = self.combo_theme.currentText().lower()
        new_currency = self.combo_currency.currentText()
        
        self.settings.set("theme", new_theme)
        self.settings.set("currency", new_currency)
        
        Toast.show(self.window(), "Settings saved successfully")
        
        parent_window = self.window()
        if hasattr(parent_window, "refresh_all_data"):
            parent_window.refresh_all_data()
            
        if old_theme != new_theme and hasattr(parent_window, "apply_theme"):
            parent_window.apply_theme()

    def refresh_data(self):
        self.combo_theme.setCurrentText(self.settings.get("theme").capitalize())
        self.combo_currency.setCurrentText(self.settings.get("currency"))
            
    def reset_portfolio(self):
        reply = QMessageBox.question(self, 'Reset Portfolio', 'Are you sure you want to delete all portfolio data?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.portfolio_storage.set_holdings([])
            Toast.show(self.window(), "Portfolio reset successfully", "info")
            parent_window = self.window()
            if hasattr(parent_window, "refresh_all_data"):
                parent_window.refresh_all_data()
                
    def reset_stats(self):
        reply = QMessageBox.question(self, 'Reset Statistics', 'Are you sure you want to reset all statistics?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.stats.reset()
            Toast.show(self.window(), "Statistics reset successfully", "info")
