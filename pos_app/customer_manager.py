import json

class CustomerManager:
    def __init__(self, customers_file="pos_app/data/customers.json"):
        self.customers_file = customers_file
        self.customers = self.load_customers()

    def load_customers(self):
        try:
            with open(self.customers_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_customers(self):
        with open(self.customers_file, "w") as f:
            json.dump(self.customers, f, indent=4)

    def get_next_id(self):
        if not self.customers:
            return 1
        return max(c['id'] for c in self.customers) + 1

    def add_customer(self, customer_data):
        customer_data['id'] = self.get_next_id()
        self.customers.append(customer_data)
        self.save_customers()
        return customer_data

    def update_customer(self, customer_id, updated_data):
        for i, customer in enumerate(self.customers):
            if customer['id'] == customer_id:
                self.customers[i] = updated_data
                self.save_customers()
                return True
        return False
