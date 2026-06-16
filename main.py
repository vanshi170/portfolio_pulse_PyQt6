import sys
import os
import time
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt, QTimer
from ui.main_window import MainWindow
from storage.statistics import Statistics

def main():
    app = QApplication(sys.argv)
    
    # Track launch stat
    stats = Statistics()
    stats.increment("total_launches")
    
    # Setup Splash Screen
    splash_path = os.path.join(os.path.dirname(__file__), "assets", "generated", "splash_logo.png")
    
    if os.path.exists(splash_path):
        pixmap = QPixmap(splash_path)
        # Resize if it's too big
        if pixmap.width() > 600:
            pixmap = pixmap.scaledToWidth(600, Qt.TransformationMode.SmoothTransformation)
        splash = QSplashScreen(pixmap, Qt.WindowType.WindowStaysOnTopHint)
        splash.showMessage("PortfolioPulse\nLoading Dashboard...", Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter, QColor("white"))
        splash.show()
        app.processEvents()
        
        # Simulate loading duration
        time.sleep(2.0)
    else:
        splash = None

    window = MainWindow()
    window.show()
    
    if splash:
        splash.finish(window)
        
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
