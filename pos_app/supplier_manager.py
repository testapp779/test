import json

class SupplierManager:
    def __init__(self, suppliers_file="pos_app/data/suppliers.json"):
        self.suppliers_file = suppliers_file
        self.suppliers = self.load_suppliers()

    def load_suppliers(self):
        try:
            with open(self.suppliers_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_suppliers(self):
        with open(self.suppliers_file, "w") as f:
            json.dump(self.suppliers, f, indent=4)

    def get_next_id(self):
        if not self.suppliers:
            return 1
        return max(s['id'] for s in self.suppliers) + 1

    def add_supplier(self, supplier_data):
        supplier_data['id'] = self.get_next_id()
        self.suppliers.append(supplier_data)
        self.save_suppliers()
        return supplier_data

    def update_supplier(self, supplier_id, updated_data):
        for i, supplier in enumerate(self.suppliers):
            if supplier['id'] == supplier_id:
                self.suppliers[i] = updated_data
                self.save_suppliers()
                return True
        return False
