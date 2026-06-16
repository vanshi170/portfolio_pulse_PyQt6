import os
import json
import csv
from datetime import datetime
from storage.portfolio_storage import PortfolioStorage
from storage.statistics import Statistics

class ExportImportManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExportImportManager, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
        
    def initialize(self):
        self.storage = PortfolioStorage()
        self.stats = Statistics()
        
    def export_json(self, filepath):
        try:
            holdings = self.storage.get_holdings()
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(holdings, f, indent=4)
            self.stats.increment("total_exports")
            return True, "Export successful"
        except Exception as e:
            return False, str(e)
            
    def export_csv(self, filepath):
        try:
            holdings = self.storage.get_holdings()
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Symbol", "Quantity", "Date Added"])
                for h in holdings:
                    writer.writerow([h["symbol"], h["quantity"], h.get("date_added", "")])
            self.stats.increment("total_exports")
            return True, "Export successful"
        except Exception as e:
            return False, str(e)
            
    def export_txt(self, filepath):
        try:
            holdings = self.storage.get_holdings()
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("PortfolioPulse Export\n")
                f.write("=" * 30 + "\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                for h in holdings:
                    f.write(f"Symbol: {h['symbol']}\n")
                    f.write(f"Quantity: {h['quantity']}\n")
                    f.write(f"Added: {h.get('date_added', 'N/A')}\n")
                    f.write("-" * 30 + "\n")
            self.stats.increment("total_exports")
            return True, "Export successful"
        except Exception as e:
            return False, str(e)
            
    def import_json(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            if not isinstance(data, list):
                return False, "Invalid JSON format. Expected a list of holdings."
                
            # Basic validation
            valid_holdings = []
            for item in data:
                if "symbol" in item and "quantity" in item:
                    valid_holdings.append({
                        "symbol": str(item["symbol"]).upper(),
                        "quantity": int(item["quantity"]),
                        "date_added": item.get("date_added", datetime.now().isoformat())
                    })
                    
            if not valid_holdings:
                return False, "No valid holdings found to import."
                
            self.storage.set_holdings(valid_holdings)
            self.stats.increment("total_imports")
            return True, f"Successfully imported {len(valid_holdings)} holdings"
        except Exception as e:
            return False, str(e)
            
    def import_csv(self, filepath):
        try:
            valid_holdings = []
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if not header:
                    return False, "CSV file is empty"
                    
                for row in reader:
                    if len(row) >= 2:
                        symbol = row[0].strip().upper()
                        try:
                            quantity = int(row[1].strip())
                            date_added = row[2] if len(row) > 2 else datetime.now().isoformat()
                            valid_holdings.append({
                                "symbol": symbol,
                                "quantity": quantity,
                                "date_added": date_added
                            })
                        except ValueError:
                            continue
                            
            if not valid_holdings:
                return False, "No valid holdings found to import."
                
            self.storage.set_holdings(valid_holdings)
            self.stats.increment("total_imports")
            return True, f"Successfully imported {len(valid_holdings)} holdings"
        except Exception as e:
            return False, str(e)
