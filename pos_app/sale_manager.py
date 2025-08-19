import json
from datetime import datetime

class SaleManager:
    def __init__(self, sales_file="data/sales.json"):
        self.sales_file = sales_file

    def get_sales(self):
        try:
            with open(self.sales_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def record_sale(self, cart, total, customer_id, discount_percentage):
        sales = self.get_sales()

        sale = {
            "timestamp": datetime.now().isoformat(),
            "items": cart,
            "total": total,
            "customer_id": customer_id,
            "discount_percentage": discount_percentage
        }
        sales.append(sale)

        with open(self.sales_file, "w") as f:
            json.dump(sales, f, indent=4)
