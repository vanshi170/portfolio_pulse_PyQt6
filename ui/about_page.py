import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt6.QtCore import Qt
from storage.statistics import Statistics

class AboutPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stats = Statistics()
        self.init_ui()
        
    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)
        
        title = QLabel("About & Statistics")
        title.setObjectName("title")
        self.layout.addWidget(title)
        
        # Info Card
        info_card = QWidget()
        info_card.setObjectName("card")
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(20, 20, 20, 20)
        
        app_name = QLabel("PortfolioPulse")
        app_name.setObjectName("value_large")
        
        version = QLabel("Version: 1.0.0\nFramework: PyQt6\nLanguage: Python 3.12+")
        version.setStyleSheet("color: #94a3b8; font-size: 14px;")
        
        info_layout.addWidget(app_name)
        info_layout.addWidget(version)
        self.layout.addWidget(info_card)
        
        # Stats Card
        stats_card = QWidget()
        stats_card.setObjectName("card")
        stats_layout = QVBoxLayout(stats_card)
        stats_layout.setContentsMargins(20, 20, 20, 20)
        
        stats_title = QLabel("Application Statistics")
        stats_title.setObjectName("subtitle")
        stats_layout.addWidget(stats_title)
        
        grid = QGridLayout()
        grid.setSpacing(15)
        
        grid.addWidget(QLabel("Total App Launches:"), 0, 0)
        grid.addWidget(QLabel(str(self.stats.get("total_launches"))), 0, 1)
        
        grid.addWidget(QLabel("Total Stocks Added:"), 1, 0)
        grid.addWidget(QLabel(str(self.stats.get("total_stocks_added"))), 1, 1)
        
        grid.addWidget(QLabel("Total Exports:"), 2, 0)
        grid.addWidget(QLabel(str(self.stats.get("total_exports"))), 2, 1)
        
        grid.addWidget(QLabel("Total Imports:"), 3, 0)
        grid.addWidget(QLabel(str(self.stats.get("total_imports"))), 3, 1)
        
        grid.addWidget(QLabel("Most Added Stock:"), 4, 0)
        grid.addWidget(QLabel(self.stats.get_most_added_stock()), 4, 1)
        
        stats_layout.addLayout(grid)
        self.layout.addWidget(stats_card)
        
        self.layout.addStretch()
        
    def refresh_data(self):
        # Re-create to refresh stats, or clear and rebuild layout
        # For simplicity, we can leave this static or implement a clear/rebuild.
        pass
