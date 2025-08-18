import json

class ProductManager:
    def __init__(self, products_file="pos_app/data/products.json", categories_file="pos_app/data/categories.json"):
        self.products_file = products_file
        self.categories_file = categories_file
        self.products = self.load_products()
        self.categories = self.load_categories()

    def load_categories(self):
        try:
            with open(self.categories_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_category_name(self, category_id):
        for category in self.categories:
            if category['id'] == category_id:
                return category['name']
        return "Uncategorized"

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
