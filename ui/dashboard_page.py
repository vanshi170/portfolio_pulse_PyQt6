import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QIcon, QPixmap
from services.portfolio_manager import PortfolioManager

class StatCard(QWidget):
    def __init__(self, title, icon_name, value="0"):
        super().__init__()
        self.setObjectName("card")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setMinimumSize(220, 120)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        top_layout = QHBoxLayout()
        self.lbl_title = QLabel(title)
        self.lbl_title.setObjectName("subtitle")
        
        self.icon_name = icon_name
        self.lbl_icon = QLabel()
        self.update_icon()
            
        top_layout.addWidget(self.lbl_title)
        top_layout.addStretch()
        top_layout.addWidget(self.lbl_icon)
        
        self.lbl_value = QLabel(value)
        self.lbl_value.setObjectName("value_large")
        
        layout.addLayout(top_layout)
        layout.addStretch()
        layout.addWidget(self.lbl_value)
        
    def update_value(self, value):
        self.lbl_value.setText(value)
        
    def update_icon(self):
        from storage.settings import Settings
        theme = Settings().get("theme")
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icons", theme, f"{self.icon_name}.svg")
        if os.path.exists(icon_path):
            pixmap = QIcon(icon_path).pixmap(24, 24)
            self.lbl_icon.setPixmap(pixmap)

class DashboardPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.portfolio_manager = PortfolioManager()
        self.init_ui()
        self.refresh_data()
        
    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)
        
        title = QLabel("Dashboard")
        title.setObjectName("title")
        self.layout.addWidget(title)
        
        # Cards grid
        self.cards_layout = QGridLayout()
        self.cards_layout.setSpacing(20)
        
        self.card_total = StatCard("Total Value", "portfolio")
        self.card_count = StatCard("Holdings", "statistics")
        self.card_most_valuable = StatCard("Top Value", "dashboard")
        self.card_avg = StatCard("Avg Investment", "analytics")
        self.card_largest = StatCard("Largest Position", "info")
        
        self.cards_layout.addWidget(self.card_total, 0, 0)
        self.cards_layout.addWidget(self.card_count, 0, 1)
        self.cards_layout.addWidget(self.card_most_valuable, 0, 2)
        self.cards_layout.addWidget(self.card_avg, 1, 0)
        self.cards_layout.addWidget(self.card_largest, 1, 1)
        
        self.layout.addLayout(self.cards_layout)
        self.layout.addStretch()

    def update_icons(self):
        self.card_total.update_icon()
        self.card_count.update_icon()
        self.card_most_valuable.update_icon()
        self.card_avg.update_icon()
        self.card_largest.update_icon()
        
    def refresh_data(self):
        data = self.portfolio_manager.get_portfolio_data()
        currency_sym = self.portfolio_manager.get_currency_symbol()
        
        total_val = data["total_value"]
        count = data["count"]
        holdings = data["holdings"]
        
        self.card_total.update_value(f"{currency_sym}{total_val:,.2f}")
        self.card_count.update_value(str(count))
        
        if count > 0:
            avg_val = total_val / count
            most_valuable_stock = max(holdings, key=lambda x: x["total_value"])
            largest_pos_stock = max(holdings, key=lambda x: x["quantity"])
            
            self.card_avg.update_value(f"{currency_sym}{avg_val:,.2f}")
            self.card_most_valuable.update_value(most_valuable_stock["symbol"])
            self.card_largest.update_value(f"{largest_pos_stock['symbol']} ({largest_pos_stock['quantity']})")
        else:
            self.card_avg.update_value(f"{currency_sym}0.00")
            self.card_most_valuable.update_value("N/A")
            self.card_largest.update_value("N/A")
