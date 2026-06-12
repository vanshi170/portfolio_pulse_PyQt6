import os
import json
from datetime import datetime

class PortfolioStorage:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PortfolioStorage, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
        
    def initialize(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        os.makedirs(self.data_dir, exist_ok=True)
        self.filepath = os.path.join(self.data_dir, "portfolio.json")
        self.holdings = self.load()
        
    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []
        
    def save(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.holdings, f, indent=4)
        except Exception as e:
            print(f"Failed to save portfolio: {e}")
            
    def get_holdings(self):
        return self.holdings
        
    def add_holding(self, symbol, quantity):
        # Check if exists, if so update quantity
        for h in self.holdings:
            if h["symbol"] == symbol:
                h["quantity"] += quantity
                self.save()
                return True
                
        # If not exists, append
        self.holdings.append({
            "symbol": symbol,
            "quantity": quantity,
            "date_added": datetime.now().isoformat()
        })
        self.save()
        return True
        
    def edit_holding(self, symbol, new_quantity):
        for h in self.holdings:
            if h["symbol"] == symbol:
                h["quantity"] = new_quantity
                self.save()
                return True
        return False
        
    def delete_holding(self, symbol):
        initial_len = len(self.holdings)
        self.holdings = [h for h in self.holdings if h["symbol"] != symbol]
        if len(self.holdings) != initial_len:
            self.save()
            return True
        return False
        
    def set_holdings(self, new_holdings):
        """Used for importing"""
        self.holdings = new_holdings
        self.save()

