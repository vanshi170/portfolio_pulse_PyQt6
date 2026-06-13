from storage.portfolio_storage import PortfolioStorage
from storage.settings import Settings

class PortfolioManager:
    _instance = None
    
    # Assignment Requirement: Hardcoded stock dictionary
    HARDCODED_PRICES = {
        "AAPL": 180,
        "MSFT": 420,
        "NVDA": 145,
        "GOOGL": 185,
        "AMZN": 225,
        "META": 740,
        "TSLA": 325,
        "NFLX": 1420,
        "AMD": 175,
        "INTC": 23,
        "ORCL": 250,
        "IBM": 310,
        "CRM": 410,
        "UBER": 95,
        "SHOP": 145
    }
    
    COMPANY_NAMES = {
        "AAPL": "Apple Inc.",
        "MSFT": "Microsoft Corporation",
        "NVDA": "NVIDIA Corporation",
        "GOOGL": "Alphabet Inc.",
        "AMZN": "Amazon.com Inc.",
        "META": "Meta Platforms Inc.",
        "TSLA": "Tesla Inc.",
        "NFLX": "Netflix Inc.",
        "AMD": "Advanced Micro Devices",
        "INTC": "Intel Corporation",
        "ORCL": "Oracle Corporation",
        "IBM": "IBM Corporation",
        "CRM": "Salesforce Inc.",
        "UBER": "Uber Technologies Inc.",
        "SHOP": "Shopify Inc."
    }

    CURRENCY_MULTIPLIERS = {
        "USD": 1.0,
        "INR": 83.5,
        "EUR": 0.92,
        "GBP": 0.79
    }
    
    CURRENCY_SYMBOLS = {
        "USD": "$",
        "INR": "₹",
        "EUR": "€",
        "GBP": "£"
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PortfolioManager, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
        
    def initialize(self):
        self.storage = PortfolioStorage()
        self.settings = Settings()
        
    def get_supported_stocks(self):
        return list(self.HARDCODED_PRICES.keys())
        
    def is_valid_stock(self, symbol):
        return symbol in self.HARDCODED_PRICES
        
    def get_currency_symbol(self):
        currency = self.settings.get("currency")
        return self.CURRENCY_SYMBOLS.get(currency, "$")
        
    def convert_value(self, usd_value):
        currency = self.settings.get("currency")
        multiplier = self.CURRENCY_MULTIPLIERS.get(currency, 1.0)
        return usd_value * multiplier
        
    def get_portfolio_data(self):
        holdings = self.storage.get_holdings()
        
        total_usd_value = 0
        enriched_holdings = []
        
        # First pass to calculate total value in USD
        for h in holdings:
            symbol = h["symbol"]
            price_usd = self.HARDCODED_PRICES.get(symbol, 0)
            value_usd = price_usd * h["quantity"]
            total_usd_value += value_usd
            
        # Second pass to build full data including % allocation
        for h in holdings:
            symbol = h["symbol"]
            qty = h["quantity"]
            price_usd = self.HARDCODED_PRICES.get(symbol, 0)
            value_usd = price_usd * qty
            
            allocation = (value_usd / total_usd_value * 100) if total_usd_value > 0 else 0
            
            # Convert to selected currency
            price_converted = self.convert_value(price_usd)
            value_converted = self.convert_value(value_usd)
            
            enriched_holdings.append({
                "symbol": symbol,
                "name": self.COMPANY_NAMES.get(symbol, symbol),
                "quantity": qty,
                "price": price_converted,
                "total_value": value_converted,
                "allocation": allocation,
                "date_added": h.get("date_added", "")
            })
            
        total_converted_value = self.convert_value(total_usd_value)
        
        return {
            "total_value": total_converted_value,
            "holdings": enriched_holdings,
            "count": len(enriched_holdings)
        }
