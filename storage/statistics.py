import os
import json

class Statistics:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Statistics, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
        
    def initialize(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        os.makedirs(self.data_dir, exist_ok=True)
        self.filepath = os.path.join(self.data_dir, "statistics.json")
        
        self.default_stats = {
            "total_launches": 0,
            "total_stocks_added": 0,
            "total_exports": 0,
            "total_imports": 0,
            "stock_add_counts": {} # e.g. {"AAPL": 5, "TSLA": 2}
        }
        self.stats = self.load()
        
    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    return {**self.default_stats, **json.load(f)}
            except Exception:
                pass
        return self.default_stats.copy()
        
    def save(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.stats, f, indent=4)
        except Exception as e:
            print(f"Failed to save statistics: {e}")
            
    def increment(self, key, amount=1):
        self.stats[key] = self.stats.get(key, 0) + amount
        self.save()
        
    def track_stock_added(self, symbol):
        self.increment("total_stocks_added")
        if "stock_add_counts" not in self.stats:
            self.stats["stock_add_counts"] = {}
        self.stats["stock_add_counts"][symbol] = self.stats["stock_add_counts"].get(symbol, 0) + 1
        self.save()
        
    def get(self, key):
        return self.stats.get(key, self.default_stats.get(key))
        
    def get_most_added_stock(self):
        counts = self.stats.get("stock_add_counts", {})
        if not counts:
            return "N/A"
        return max(counts, key=counts.get)
        
    def reset(self):
        self.stats = self.default_stats.copy()
        self.save()

