import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QLineEdit, QComboBox, QMenu, QDialog,
                             QFormLayout, QSpinBox, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QSortFilterProxyModel
from PyQt6.QtGui import QIcon
from services.portfolio_manager import PortfolioManager
from storage.portfolio_storage import PortfolioStorage
from storage.statistics import Statistics
from ui.components.toast import Toast

class AddStockDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Stock")
        self.setFixedSize(350, 200)
        self.pm = PortfolioManager()
        
        layout = QFormLayout(self)
        
        self.combo_symbol = QComboBox()
        self.combo_symbol.addItems(sorted(self.pm.get_supported_stocks()))
        
        self.spin_qty = QSpinBox()
        self.spin_qty.setRange(1, 1000000)
        self.spin_qty.setValue(1)
        
        layout.addRow("Stock Symbol:", self.combo_symbol)
        layout.addRow("Quantity:", self.spin_qty)
        
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Add to Portfolio")
        self.btn_add.setObjectName("accent")
        self.btn_add.clicked.connect(self.accept)
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_add)
        
        layout.addRow(btn_layout)

class PortfolioPage(QWidget):
    data_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pm = PortfolioManager()
        self.storage = PortfolioStorage()
        self.stats = Statistics()
        self.init_ui()
        self.refresh_data()
        
    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)
        
        # Header area
        header_layout = QHBoxLayout()
        title = QLabel("Portfolio")
        title.setObjectName("title")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by symbol or name...")
        self.search_input.setFixedWidth(250)
        self.search_input.textChanged.connect(self.filter_table)
        
        self.btn_add = QPushButton(" Add Stock")
        self.btn_add.setObjectName("accent")
        self.btn_add.clicked.connect(self.open_add_dialog)
        self.update_icons()
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.search_input)
        header_layout.addWidget(self.btn_add)
        
        self.layout.addLayout(header_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Symbol", "Name", "Price", "Quantity", "Total Value", "Allocation %"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setDefaultSectionSize(45)
        
        self.layout.addWidget(self.table)
        
        # Empty State
        self.empty_card = QWidget()
        self.empty_card.setObjectName("card")
        empty_layout = QVBoxLayout(self.empty_card)
        lbl_empty = QLabel("No Stocks Added Yet\nClick 'Add Stock' to build your portfolio.")
        lbl_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_empty.setObjectName("subtitle")
        empty_layout.addWidget(lbl_empty)
        self.layout.addWidget(self.empty_card)
        self.empty_card.hide()

    def update_icons(self):
        from storage.settings import Settings
        theme = Settings().get("theme")
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icons", theme, "add.svg")
        self.btn_add.setIcon(QIcon(icon_path))

    def refresh_data(self):
        self.table.setSortingEnabled(False)
        data = self.pm.get_portfolio_data()
        holdings = data["holdings"]
        currency_sym = self.pm.get_currency_symbol()
        
        self.table.setRowCount(len(holdings))
        
        if len(holdings) == 0:
            self.table.hide()
            self.empty_card.show()
        else:
            self.table.show()
            self.empty_card.hide()
            
        for row, h in enumerate(holdings):
            item_sym = QTableWidgetItem(h["symbol"])
            item_name = QTableWidgetItem(h["name"])
            
            # Use numeric sorting properly by using Qt.ItemDataRole.EditRole or sorting by value
            item_price = QTableWidgetItem()
            item_price.setData(Qt.ItemDataRole.DisplayRole, f"{currency_sym}{h['price']:,.2f}")
            item_price.setData(Qt.ItemDataRole.UserRole, h['price'])
            
            item_qty = QTableWidgetItem()
            item_qty.setData(Qt.ItemDataRole.DisplayRole, str(h["quantity"]))
            item_qty.setData(Qt.ItemDataRole.UserRole, h["quantity"])
            
            item_val = QTableWidgetItem()
            item_val.setData(Qt.ItemDataRole.DisplayRole, f"{currency_sym}{h['total_value']:,.2f}")
            item_val.setData(Qt.ItemDataRole.UserRole, h['total_value'])
            
            item_alloc = QTableWidgetItem()
            item_alloc.setData(Qt.ItemDataRole.DisplayRole, f"{h['allocation']:.1f}%")
            item_alloc.setData(Qt.ItemDataRole.UserRole, h['allocation'])
            
            self.table.setItem(row, 0, item_sym)
            self.table.setItem(row, 1, item_name)
            self.table.setItem(row, 2, item_price)
            self.table.setItem(row, 3, item_qty)
            self.table.setItem(row, 4, item_val)
            self.table.setItem(row, 5, item_alloc)
            
        self.table.setSortingEnabled(True)
        self.filter_table(self.search_input.text())
        
    def filter_table(self, text):
        text = text.lower()
        for row in range(self.table.rowCount()):
            sym = self.table.item(row, 0).text().lower()
            name = self.table.item(row, 1).text().lower()
            if text in sym or text in name:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)
                
    def open_add_dialog(self):
        dlg = AddStockDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            sym = dlg.combo_symbol.currentText()
            qty = dlg.spin_qty.value()
            self.storage.add_holding(sym, qty)
            self.stats.track_stock_added(sym)
            Toast.show(self.window(), f"Successfully added {qty} shares of {sym}")
            self.data_changed.emit()
            
    def show_context_menu(self, pos):
        item = self.table.itemAt(pos)
        if item is None:
            return
            
        row = item.row()
        symbol = self.table.item(row, 0).text()
        
        menu = QMenu()
        act_delete = menu.addAction("Delete Stock")
        from storage.settings import Settings
        theme = Settings().get("theme")
        act_delete.setIcon(QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icons", theme, "delete.svg")))
        
        action = menu.exec(self.table.viewport().mapToGlobal(pos))
        if action == act_delete:
            self.storage.delete_holding(symbol)
            Toast.show(self.window(), f"Deleted {symbol} from portfolio", "info")
            self.data_changed.emit()
