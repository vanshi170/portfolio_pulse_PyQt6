import os
import matplotlib
matplotlib.use('QtAgg')
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from services.portfolio_manager import PortfolioManager
from storage.settings import Settings

class ChartCard(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setObjectName("card")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        
        lbl_title = QLabel(title)
        lbl_title.setObjectName("subtitle")
        self.layout.addWidget(lbl_title)
        
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        
    def clear(self):
        self.figure.clear()
        
    def draw(self):
        self.figure.tight_layout()
        self.canvas.draw()

class AnalyticsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pm = PortfolioManager()
        self.settings = Settings()
        self.init_ui()
        self.refresh_data()
        
    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        
        title = QLabel("Analytics")
        title.setObjectName("title")
        self.layout.addWidget(title)
        
        grid = QGridLayout()
        grid.setSpacing(20)
        
        self.chart_allocation = ChartCard("Portfolio Allocation (%)")
        self.chart_holdings = ChartCard("Holdings Value")
        self.chart_dist = ChartCard("Value Distribution")
        self.chart_top = ChartCard("Top 5 Holdings")
        
        grid.addWidget(self.chart_allocation, 0, 0)
        grid.addWidget(self.chart_holdings, 0, 1)
        grid.addWidget(self.chart_dist, 1, 0)
        grid.addWidget(self.chart_top, 1, 1)
        
        self.layout.addLayout(grid)
        
    def get_theme_colors(self):
        is_dark = self.settings.get("theme") == "dark"
        text_color = "white" if is_dark else "black"
        bg_color = "#151c2e" if is_dark else "#ffffff"
        chart_bg = "#0a0f1c" if is_dark else "#f8fafc"
        return text_color, chart_bg
        
    def refresh_data(self):
        data = self.pm.get_portfolio_data()
        holdings = data["holdings"]
        
        if not holdings:
            for c in [self.chart_allocation, self.chart_holdings, self.chart_dist, self.chart_top]:
                c.clear()
                c.draw()
            return
            
        labels = [h["symbol"] for h in holdings]
        values = [h["total_value"] for h in holdings]
        allocs = [h["allocation"] for h in holdings]
        
        text_color, bg_color = self.get_theme_colors()
        
        # 1. Allocation Pie Chart
        self.chart_allocation.clear()
        ax1 = self.chart_allocation.figure.add_subplot(111)
        self.chart_allocation.figure.patch.set_facecolor(bg_color)
        ax1.pie(allocs, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'color': text_color})
        ax1.axis('equal')
        self.chart_allocation.draw()
        
        # 2. Holdings Bar Chart
        self.chart_holdings.clear()
        ax2 = self.chart_holdings.figure.add_subplot(111)
        self.chart_holdings.figure.patch.set_facecolor(bg_color)
        ax2.bar(labels, values, color='#3b82f6')
        ax2.tick_params(colors=text_color)
        for spine in ax2.spines.values():
            spine.set_edgecolor(text_color)
        ax2.set_facecolor(bg_color)
        self.chart_holdings.draw()
        
        # 3. Value Distribution
        self.chart_dist.clear()
        ax3 = self.chart_dist.figure.add_subplot(111)
        self.chart_dist.figure.patch.set_facecolor(bg_color)
        ax3.hist(values, bins=10, color='#06b6d4', edgecolor='white')
        ax3.tick_params(colors=text_color)
        ax3.set_facecolor(bg_color)
        self.chart_dist.draw()
        
        # 4. Top 5 Holdings
        self.chart_top.clear()
        ax4 = self.chart_top.figure.add_subplot(111)
        self.chart_top.figure.patch.set_facecolor(bg_color)
        
        top_h = sorted(holdings, key=lambda x: x["total_value"], reverse=True)[:5]
        t_labels = [h["symbol"] for h in top_h]
        t_values = [h["total_value"] for h in top_h]
        
        ax4.barh(t_labels, t_values, color='#22c55e')
        ax4.invert_yaxis()
        ax4.tick_params(colors=text_color)
        ax4.set_facecolor(bg_color)
        self.chart_top.draw()
