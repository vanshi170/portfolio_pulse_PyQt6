import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog
from PyQt6.QtGui import QIcon
from services.export_import_manager import ExportImportManager
from ui.components.toast import Toast

class ExportCenterPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.eim = ExportImportManager()
        self.init_ui()
        
    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)
        
        title = QLabel("Export Center")
        title.setObjectName("title")
        self.layout.addWidget(title)
        
        # EXPORT SECTION
        export_card = QWidget()
        export_card.setObjectName("card")
        export_layout = QVBoxLayout(export_card)
        export_layout.setContentsMargins(20, 20, 20, 20)
        export_layout.setSpacing(15)
        
        export_layout.addWidget(QLabel("Export Portfolio", objectName="subtitle"))
        
        btn_layout = QHBoxLayout()
        
        self.btn_exp_json = QPushButton(" Export JSON")
        self.btn_exp_json.clicked.connect(lambda: self.do_export("json"))
        
        self.btn_exp_csv = QPushButton(" Export CSV")
        self.btn_exp_csv.clicked.connect(lambda: self.do_export("csv"))
        
        self.btn_exp_txt = QPushButton(" Export TXT")
        self.btn_exp_txt.clicked.connect(lambda: self.do_export("txt"))
        
        btn_layout.addWidget(self.btn_exp_json)
        btn_layout.addWidget(self.btn_exp_csv)
        btn_layout.addWidget(self.btn_exp_txt)
        btn_layout.addStretch()
        
        export_layout.addLayout(btn_layout)
        self.layout.addWidget(export_card)
        
        # IMPORT SECTION
        import_card = QWidget()
        import_card.setObjectName("card")
        import_layout = QVBoxLayout(import_card)
        import_layout.setContentsMargins(20, 20, 20, 20)
        import_layout.setSpacing(15)
        
        import_layout.addWidget(QLabel("Import Portfolio", objectName="subtitle"))
        
        btn_imp_layout = QHBoxLayout()
        
        self.btn_imp_json = QPushButton(" Import JSON")
        self.btn_imp_json.clicked.connect(lambda: self.do_import("json"))
        
        self.btn_imp_csv = QPushButton(" Import CSV")
        self.btn_imp_csv.clicked.connect(lambda: self.do_import("csv"))
        
        btn_imp_layout.addWidget(self.btn_imp_json)
        btn_imp_layout.addWidget(self.btn_imp_csv)
        btn_imp_layout.addStretch()
        
        import_layout.addLayout(btn_imp_layout)
        self.layout.addWidget(import_card)
        
        self.layout.addStretch()
        self.update_icons()

    def update_icons(self):
        from storage.settings import Settings
        theme = Settings().get("theme")
        export_icon = QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icons", theme, "export.svg"))
        import_icon = QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icons", theme, "import.svg"))
        
        self.btn_exp_json.setIcon(export_icon)
        self.btn_exp_csv.setIcon(export_icon)
        self.btn_exp_txt.setIcon(export_icon)
        self.btn_imp_json.setIcon(import_icon)
        self.btn_imp_csv.setIcon(import_icon)
        
    def do_export(self, fmt):
        filters = {
            "json": "JSON Files (*.json)",
            "csv": "CSV Files (*.csv)",
            "txt": "Text Files (*.txt)"
        }
        path, _ = QFileDialog.getSaveFileName(self, f"Export {fmt.upper()}", "", filters[fmt])
        if path:
            success = False
            msg = ""
            if fmt == "json":
                success, msg = self.eim.export_json(path)
            elif fmt == "csv":
                success, msg = self.eim.export_csv(path)
            elif fmt == "txt":
                success, msg = self.eim.export_txt(path)
                
            if success:
                Toast.show(self.window(), f"Exported {fmt.upper()} successfully to {os.path.basename(path)}")
            else:
                Toast.show(self.window(), f"Export Failed: {msg}", "danger")
                
    def do_import(self, fmt):
        filters = {
            "json": "JSON Files (*.json)",
            "csv": "CSV Files (*.csv)"
        }
        path, _ = QFileDialog.getOpenFileName(self, f"Import {fmt.upper()}", "", filters[fmt])
        if path:
            success = False
            msg = ""
            if fmt == "json":
                success, msg = self.eim.import_json(path)
            elif fmt == "csv":
                success, msg = self.eim.import_csv(path)
                
            if success:
                Toast.show(self.window(), f"Imported {fmt.upper()} successfully: {msg}")
                # Refresh entire app
                parent_window = self.window()
                if hasattr(parent_window, "refresh_all_data"):
                    parent_window.refresh_all_data()
            else:
                Toast.show(self.window(), f"Import Failed: {msg}", "danger")
