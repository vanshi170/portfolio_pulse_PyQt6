import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QPropertyAnimation, pyqtSignal, QEasingCurve, QSize
from PyQt6.QtGui import QIcon, QPixmap

class Sidebar(QWidget):
    page_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        
        self.expanded_width = 250
        self.collapsed_width = 64
        self.is_expanded = True
        
        self.init_ui()
        
    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 20, 10, 20)
        self.layout.setSpacing(5)
        
        self.setFixedWidth(self.expanded_width)
        
        # Menu toggle button
        self.toggle_btn = QPushButton("Menu")
        self.toggle_btn.setObjectName("sidebar_btn")
        self.toggle_btn.setIconSize(QSize(24, 24))
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        self.layout.addWidget(self.toggle_btn)
        
        self.layout.addSpacing(20)
        
        self.buttons = {}
        
        self.add_nav_button("Dashboard", "dashboard", "dashboard")
        self.add_nav_button("Portfolio", "portfolio", "portfolio")
        self.add_nav_button("Analytics", "analytics", "analytics")
        self.add_nav_button("Export Center", "export", "export")
        
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addItem(spacer)
        
        self.add_nav_button("Settings", "settings", "settings")
        self.add_nav_button("About", "about", "about")
        
        # Select first by default
        self.buttons["dashboard"].setChecked(True)
        self.update_icons()
        
    def get_icon(self, name):
        from storage.settings import Settings
        theme = Settings().get("theme")
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "icons", theme, f"{name}.svg")
        return QIcon(icon_path)
        
    def add_nav_button(self, text, icon_name, page_id):
        btn = QPushButton(text)
        btn.setObjectName("sidebar_btn")
        btn.setCheckable(True)
        btn.setProperty("icon_name", icon_name)
        btn.setIconSize(QSize(24, 24))
        
        btn.clicked.connect(lambda checked, pid=page_id: self.on_nav_clicked(pid))
        
        self.buttons[page_id] = btn
        self.layout.addWidget(btn)
        
    def update_icons(self):
        self.toggle_btn.setIcon(self.get_icon("menu"))
        for btn in self.buttons.values():
            icon_name = btn.property("icon_name")
            if icon_name:
                btn.setIcon(self.get_icon(icon_name))
        
    def on_nav_clicked(self, page_id):
        # Uncheck all others
        for pid, btn in self.buttons.items():
            if pid != page_id:
                btn.setChecked(False)
            else:
                btn.setChecked(True)
                
        self.page_changed.emit(page_id)
        
    def toggle_sidebar(self):
        self.anim = QPropertyAnimation(self, b"minimumWidth")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        if self.is_expanded:
            self.anim.setStartValue(self.expanded_width)
            self.anim.setEndValue(self.collapsed_width)
            self.is_expanded = False
            self.toggle_btn.setText("")
            for btn in self.buttons.values():
                btn.setText("")
        else:
            self.anim.setStartValue(self.collapsed_width)
            self.anim.setEndValue(self.expanded_width)
            self.is_expanded = True
            self.toggle_btn.setText("Menu")
            
            # Restore texts
            texts = ["Dashboard", "Portfolio", "Analytics", "Export Center", "Settings", "About"]
            for btn, text in zip(self.buttons.values(), texts):
                btn.setText(text)
                
        self.anim.start()
