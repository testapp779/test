import json
from datetime import datetime

class PurchaseOrderManager:
    def __init__(self, po_file="pos_app/data/purchase_orders.json"):
        self.po_file = po_file
        self.purchase_orders = self.load_purchase_orders()

    def load_purchase_orders(self):
        try:
            with open(self.po_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_purchase_orders(self):
        with open(self.po_file, "w") as f:
            json.dump(self.purchase_orders, f, indent=4)

    def get_next_id(self):
        if not self.purchase_orders:
            return 1
        return max(po['id'] for po in self.purchase_orders) + 1

    def create_purchase_order(self, po_data):
        po_data['id'] = self.get_next_id()
        po_data['timestamp'] = datetime.now().isoformat()
        po_data['status'] = "Pending"
        self.purchase_orders.append(po_data)
        self.save_purchase_orders()
        return po_data

    def update_purchase_order_status(self, po_id, status):
        for po in self.purchase_orders:
            if po['id'] == po_id:
                po['status'] = status
                self.save_purchase_orders()
                return True
        return False
