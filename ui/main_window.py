import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QStackedWidget, QLabel, QPushButton, QApplication)
from PyQt6.QtGui import QIcon, QShortcut, QKeySequence
from PyQt6.QtCore import Qt
from ui.components.sidebar import Sidebar
from ui.dashboard_page import DashboardPage
from ui.portfolio_page import PortfolioPage
from ui.analytics_page import AnalyticsPage
from ui.export_center_page import ExportCenterPage
from ui.settings_page import SettingsPage
from ui.about_page import AboutPage
from storage.settings import Settings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.setWindowTitle("PortfolioPulse")
        self.setMinimumSize(1200, 800)
        
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "generated", "app_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        self.init_ui()
        self.setup_shortcuts()
        self.apply_theme()
        
    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self.change_page)
        self.main_layout.addWidget(self.sidebar)
        
        # Content Area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        self.setup_header()
        
        # Stacked Widget
        self.stack = QStackedWidget()
        self.pages = {
            "dashboard": DashboardPage(),
            "portfolio": PortfolioPage(),
            "analytics": AnalyticsPage(),
            "export": ExportCenterPage(),
            "settings": SettingsPage(),
            "about": AboutPage()
        }
        
        for page in self.pages.values():
            self.stack.addWidget(page)
            
        self.content_layout.addWidget(self.stack)
        self.main_layout.addWidget(self.content_widget)
        
        # Wire signals
        self.pages["portfolio"].data_changed.connect(self.refresh_all_data)
        
    def setup_header(self):
        self.header = QWidget()
        self.header.setFixedHeight(60)
        self.header.setObjectName("sidebar") # Reuse sidebar style for header border
        
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        # Logo
        lbl_logo = QLabel()
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "generated", "app_icon.png")
        if os.path.exists(logo_path):
            lbl_logo.setPixmap(QIcon(logo_path).pixmap(32, 32))
            
        lbl_appname = QLabel("PortfolioPulse")
        lbl_appname.setStyleSheet("font-weight: bold; font-size: 18px;")
        
        header_layout.addWidget(lbl_logo)
        header_layout.addWidget(lbl_appname)
        header_layout.addStretch()
        
        # Action Buttons
        self.btn_theme = QPushButton()
        self.btn_theme.setObjectName("sidebar_btn")
        self.btn_theme.clicked.connect(self.toggle_theme)
        
        self.btn_info = QPushButton()
        self.btn_info.setObjectName("sidebar_btn")
        self.btn_info.clicked.connect(lambda: self.change_page("about"))
        
        self.update_icons()
        
        header_layout.addWidget(self.btn_theme)
        header_layout.addWidget(self.btn_info)
        
        self.content_layout.addWidget(self.header)
        
    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+N"), self).activated.connect(self.pages["portfolio"].open_add_dialog)
        QShortcut(QKeySequence("Ctrl+D"), self).activated.connect(self.toggle_theme)
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(lambda: self.change_page("portfolio"))
        QShortcut(QKeySequence("Ctrl+E"), self).activated.connect(lambda: self.change_page("export"))
        QShortcut(QKeySequence("F11"), self).activated.connect(self.toggle_fullscreen)
        
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
            
    def toggle_theme(self):
        current = self.settings.get("theme")
        new_theme = "light" if current == "dark" else "dark"
        self.settings.set("theme", new_theme)
        self.apply_theme()
        self.update_icons()
        self.refresh_all_data() # To update chart colors
        
    def update_icons(self):
        theme = self.settings.get("theme")
        icon_name = "sun" if theme == "dark" else "moon"
        
        # Header icons
        theme_icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icons", theme, f"{icon_name}.svg")
        self.btn_theme.setIcon(QIcon(theme_icon_path))
        
        info_icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icons", theme, "info.svg")
        self.btn_info.setIcon(QIcon(info_icon_path))
        
        # Sidebar icons
        self.sidebar.update_icons()
        
        # Page icons
        if hasattr(self, "pages"):
            for page in self.pages.values():
                if hasattr(page, "update_icons"):
                    page.update_icons()
        
    def apply_theme(self):
        theme = self.settings.get("theme")
        qss_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles", f"{theme}.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r") as f:
                self.setStyleSheet(f.read())
        self.update_icons()
                
    def change_page(self, page_id):
        if page_id in self.pages:
            self.stack.setCurrentWidget(self.pages[page_id])
            if hasattr(self.pages[page_id], "refresh_data"):
                self.pages[page_id].refresh_data()
                
    def refresh_all_data(self):
        for page in self.pages.values():
            if hasattr(page, "refresh_data"):
                page.refresh_data()
