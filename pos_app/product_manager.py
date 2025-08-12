import json

class ProductManager:
    def __init__(self, products_file="data/products.json"):
        self.products_file = products_file
        self.products = self.load_products()

    def load_products(self):
        try:
            with open(self.products_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_products(self):
        with open(self.products_file, "w") as f:
            json.dump(self.products, f, indent=4)

    def add_product(self, product):
        self.products.append(product)
        self.save_products()

    def update_product(self, product_index, updated_product):
        self.products[product_index] = updated_product
        self.save_products()

    def delete_product(self, product_index):
        del self.products[product_index]
        self.save_products()
