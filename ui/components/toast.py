import os
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QTimer, QEasingCurve, QRect
from PyQt6.QtGui import QIcon, QPixmap

class Toast(QWidget):
    def __init__(self, parent, message, type="success", duration=3000):
        super().__init__(parent)
        self.message = message
        self.type = type
        self.duration = duration
        
        self.init_ui()
        
    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        
        self.container = QWidget(self)
        self.container.setObjectName("toast_container")
        
        # Color coding based on type
        bg_color = "#22c55e" if self.type == "success" else "#ef4444"
        if self.type == "info":
            bg_color = "#3b82f6"
            
        self.container.setStyleSheet(f"""
            QWidget#toast_container {{
                background-color: {bg_color};
                border-radius: 8px;
            }}
            QLabel {{
                color: white;
                font-weight: bold;
                font-family: 'Segoe UI';
                font-size: 14px;
            }}
        """)
        
        container_layout = QHBoxLayout(self.container)
        container_layout.setContentsMargins(15, 10, 15, 10)
        
        lbl_msg = QLabel(self.message)
        container_layout.addWidget(lbl_msg)
        
        layout.addWidget(self.container)
        self.setLayout(layout)
        
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)
        
        self.adjustSize()
        
    def show_toast(self):
        parent = self.parent()
        if parent:
            # Position at bottom right
            x = parent.width() - self.width() - 20
            y = parent.height() - self.height() - 20
            
            # Global coordinates
            global_pos = parent.mapToGlobal(parent.rect().topLeft())
            self.move(global_pos.x() + x, global_pos.y() + y)
            
        super().show()
        
        # Fade In
        self.anim_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim_in.setDuration(300)
        self.anim_in.setStartValue(0.0)
        self.anim_in.setEndValue(1.0)
        self.anim_in.start()
        
        # Timer to hide
        QTimer.singleShot(self.duration, self.hide_toast)
        
    def hide_toast(self):
        self.anim_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim_out.setDuration(300)
        self.anim_out.setStartValue(1.0)
        self.anim_out.setEndValue(0.0)
        self.anim_out.finished.connect(self.close)
        self.anim_out.start()
        
    @staticmethod
    def show(parent, message, type="success", duration=3000):
        toast = Toast(parent, message, type, duration)
        toast.show_toast()
