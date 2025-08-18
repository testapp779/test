import tkinter as tk
from tkinter import ttk, messagebox
from product_manager import ProductManager
from sale_manager import SaleManager
from user_manager import UserManager
from customer_manager import CustomerManager
from login_screen import LoginScreen
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pos_app.theme as theme

class POSApp(tk.Tk):
    def __init__(self, user_role):
        super().__init__()
        self.user_role = user_role
        self.title(f"Point of Sale - Logged in as {self.user_role}")
        self.geometry("1200x800")
        self.configure(bg=theme.BG_COLOR)

        self.setup_styles()

        self.product_manager = ProductManager()
        self.sale_manager = SaleManager()
        self.customer_manager = CustomerManager()

        self.current_cart = []
        self.current_total = 0.0
        self.current_customer_id = None

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        self.create_tabs_based_on_role()
        self.create_logout_button()

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        # General widget styling
        style.configure(".", background=theme.BG_COLOR, foreground=theme.FG_COLOR, font=theme.FONT_NORMAL)
        style.configure("TFrame", background=theme.BG_COLOR)
        style.configure("TLabel", background=theme.BG_COLOR, foreground=theme.FG_COLOR)
        style.configure("TLabelFrame", background=theme.BG_COLOR, foreground=theme.FG_COLOR, borderwidth=1)
        style.configure("TLabelFrame.Label", background=theme.BG_COLOR, foreground=theme.FG_COLOR, font=theme.FONT_BOLD)

        # Button styling
        style.configure("TButton", background=theme.BUTTON_BG_COLOR, foreground=theme.BUTTON_FG_COLOR, font=theme.FONT_BOLD, borderwidth=0, padding=5)
        style.map("TButton", background=[("active", "#4ca8e1")])

        # Entry styling
        style.configure("TEntry", fieldbackground=theme.FRAME_BG_COLOR, foreground=theme.FG_COLOR, insertbackground=theme.FG_COLOR, borderwidth=0)

        # Notebook (Tabs) styling
        style.configure("TNotebook", background=theme.BG_COLOR, borderwidth=0)
        style.configure("TNotebook.Tab", background=theme.BG_COLOR, foreground=theme.FG_COLOR, padding=[10, 5], font=theme.FONT_NORMAL, borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", theme.FRAME_BG_COLOR)], foreground=[("selected", theme.FG_COLOR)])

        # Treeview (Table) styling
        style.configure("Treeview", background=theme.FRAME_BG_COLOR, fieldbackground=theme.FRAME_BG_COLOR, foreground=theme.FG_COLOR, rowheight=25, borderwidth=0)
        style.configure("Treeview.Heading", background=theme.BUTTON_BG_COLOR, foreground=theme.BUTTON_FG_COLOR, font=theme.FONT_BOLD, padding=5)
        style.map("Treeview.Heading", background=[("active", "#4ca8e1")])

        # Custom styles
        style.configure("Total.TLabel", foreground=theme.FG_COLOR, background=theme.BG_COLOR, font=theme.FONT_TOTAL)
        style.configure("Accent.TButton", background=theme.BUTTON_BG_COLOR, foreground=theme.BUTTON_FG_COLOR, font=theme.FONT_BOLD, padding=10)
        style.map("Accent.TButton", background=[("active", "#4ca8e1")])

    def create_tabs_based_on_role(self):
        if self.user_role == "Admin":
            self.create_product_management_tab()
            self.create_customer_management_tab()
            self.create_sales_tab()
            self.create_sales_report_tab()
            self.create_analytics_tab()
        elif self.user_role == "Cashier":
            self.create_sales_tab()

    def create_logout_button(self):
        logout_button = ttk.Button(self, text="Logout", command=self.logout)
        logout_button.pack(side="bottom", anchor="se", padx=10, pady=10)

    def logout(self):
        self.destroy()
        main() # Restart the application

    def create_product_management_tab(self):
        product_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(product_frame, text="Product Management")

        # Product List
        product_list_frame = ttk.LabelFrame(product_frame, text="Products")
        product_list_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.product_list = tk.Listbox(product_list_frame, bg=theme.FRAME_BG_COLOR, fg=theme.FG_COLOR, selectbackground=theme.BUTTON_BG_COLOR, font=theme.FONT_NORMAL, borderwidth=0, highlightthickness=0)
        self.product_list.pack(fill="both", expand=True, padx=5, pady=5)
        self.product_list.bind("<<ListboxSelect>>", self.show_selected_product)
        self.load_products_to_listbox()

        # Product Details
        product_details_frame = ttk.LabelFrame(product_frame, text="Product Details")
        product_details_frame.pack(side="right", fill="y", ipadx=10, ipady=10)

        ttk.Label(product_details_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.product_name = ttk.Entry(product_details_frame)
        self.product_name.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(product_details_frame, text="Price:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.product_price = ttk.Entry(product_details_frame)
        self.product_price.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(product_details_frame, text="Quantity:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.product_quantity = ttk.Entry(product_details_frame)
        self.product_quantity.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(product_details_frame, text="Barcode:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.product_barcode = ttk.Entry(product_details_frame)
        self.product_barcode.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(product_details_frame, text="Category:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.product_category = ttk.Combobox(product_details_frame, state="readonly")
        self.product_category['values'] = [c['name'] for c in self.product_manager.categories]
        self.product_category.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(product_details_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add", command=self.add_product).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update", command=self.update_product).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_product).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_product_fields).pack(side="left", padx=5)

    def create_customer_management_tab(self):
        customer_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(customer_frame, text="Customers")

        # Customer List
        customer_list_frame = ttk.LabelFrame(customer_frame, text="Customers")
        customer_list_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.customer_tree = ttk.Treeview(customer_list_frame, columns=("id", "name", "email", "phone"), show="headings")
        self.customer_tree.heading("id", text="ID")
        self.customer_tree.heading("name", text="Name")
        self.customer_tree.heading("email", text="Email")
        self.customer_tree.heading("phone", text="Phone")
        self.customer_tree.pack(fill="both", expand=True)
        self.customer_tree.bind("<<TreeviewSelect>>", self.show_selected_customer)
        self.load_customers_to_treeview()

        # Right side frame for details and history
        right_frame = ttk.Frame(customer_frame)
        right_frame.pack(side="right", fill="y")

        # Customer Details
        customer_details_frame = ttk.LabelFrame(right_frame, text="Customer Details")
        customer_details_frame.pack(fill="x", ipadx=10, ipady=10)

        self.customer_id_label = ttk.Label(customer_details_frame, text="") # Hidden label to store ID

        ttk.Label(customer_details_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.customer_name = ttk.Entry(customer_details_frame)
        self.customer_name.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(customer_details_frame, text="Email:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.customer_email = ttk.Entry(customer_details_frame)
        self.customer_email.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(customer_details_frame, text="Phone:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.customer_phone = ttk.Entry(customer_details_frame)
        self.customer_phone.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        # Buttons
        customer_button_frame = ttk.Frame(customer_details_frame)
        customer_button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(customer_button_frame, text="Add", command=self.add_customer).pack(side="left", padx=5)
        ttk.Button(customer_button_frame, text="Update", command=self.update_customer).pack(side="left", padx=5)
        ttk.Button(customer_button_frame, text="Clear", command=self.clear_customer_fields).pack(side="left", padx=5)

        # Purchase History
        purchase_history_frame = ttk.LabelFrame(right_frame, text="Purchase History")
        purchase_history_frame.pack(fill="both", expand=True, pady=(10, 0))

        self.purchase_history_tree = ttk.Treeview(purchase_history_frame, columns=("timestamp", "items", "total"), show="headings")
        self.purchase_history_tree.heading("timestamp", text="Timestamp")
        self.purchase_history_tree.heading("items", text="Items")
        self.purchase_history_tree.heading("total", text="Total")
        self.purchase_history_tree.pack(fill="both", expand=True)

    def on_tab_changed(self, event):
        try:
            selected_tab_text = self.notebook.tab(self.notebook.select(), "text")
        except tk.TclError:
            return # No tab selected

        if selected_tab_text == "Sales":
            self.refresh_sales_product_list()
            self.barcode_entry.focus_set()
            self.sales_category_combo['values'] = ["All Categories"] + [c['name'] for c in self.product_manager.categories]
            self.sales_customer_combo['values'] = [c['name'] for c in self.customer_manager.customers]
        elif selected_tab_text == "Customers":
            self.load_customers_to_treeview()
        elif selected_tab_text == "Sales Report":
            self.load_sales_report()
        elif selected_tab_text == "Analytics":
            self.load_analytics()

    def on_sales_category_selected(self, event):
        category_name = self.sales_category_combo.get()
        if category_name == "All Categories":
            self.refresh_sales_product_list(category_id=0)
        else:
            category_id = next((c['id'] for c in self.product_manager.categories if c['name'] == category_name), None)
            if category_id:
                self.refresh_sales_product_list(category_id)

    def create_analytics_tab(self):
        analytics_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(analytics_frame, text="Analytics")

        # Top Products
        top_products_frame = ttk.LabelFrame(analytics_frame, text="Top Selling Products")
        top_products_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.top_products_tree = ttk.Treeview(top_products_frame, columns=("product", "quantity_sold", "revenue"), show="headings")
        self.top_products_tree.heading("product", text="Product")
        self.top_products_tree.heading("quantity_sold", text="Quantity Sold")
        self.top_products_tree.heading("revenue", text="Total Revenue")
        self.top_products_tree.pack(fill="both", expand=True)

        # Sales by Category
        sales_by_category_frame = ttk.LabelFrame(analytics_frame, text="Sales by Category")
        sales_by_category_frame.pack(side="left", fill="both", expand=True, padx=(5, 0))

        self.sales_by_category_tree = ttk.Treeview(sales_by_category_frame, columns=("category", "total_sales"), show="headings")
        self.sales_by_category_tree.heading("category", text="Category")
        self.sales_by_category_tree.heading("total_sales", text="Total Sales")
        self.sales_by_category_tree.pack(fill="both", expand=True)

        # Sales Chart
        chart_frame = ttk.LabelFrame(analytics_frame, text="Daily Sales")
        chart_frame.pack(side="bottom", fill="both", expand=True, pady=(10, 0))

        fig = plt.figure(figsize=(5, 4), dpi=100, facecolor=theme.BG_COLOR)
        self.sales_chart_ax = fig.add_subplot(111)
        self.sales_chart_ax.set_facecolor(theme.FRAME_BG_COLOR)
        self.sales_chart_ax.tick_params(axis='x', colors=theme.FG_COLOR)
        self.sales_chart_ax.tick_params(axis='y', colors=theme.FG_COLOR)
        self.sales_chart_ax.spines['bottom'].set_color(theme.FG_COLOR)
        self.sales_chart_ax.spines['top'].set_color(theme.FG_COLOR)
        self.sales_chart_ax.spines['right'].set_color(theme.FG_COLOR)
        self.sales_chart_ax.spines['left'].set_color(theme.FG_COLOR)

        self.sales_chart_canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        self.sales_chart_canvas.get_tk_widget().pack(fill="both", expand=True)

    def load_analytics(self):
        self.load_top_products()
        self.load_sales_by_category_report()
        self.load_sales_chart()

    def load_top_products(self):
        for i in self.top_products_tree.get_children():
            self.top_products_tree.delete(i)
        sales = self.sale_manager.get_sales()

        product_sales = {}
        for sale in sales:
            for item in sale['items']:
                name = item['name']
                if name not in product_sales:
                    product_sales[name] = {'quantity': 0, 'revenue': 0}
                product_sales[name]['quantity'] += item['quantity']
                product_sales[name]['revenue'] += item['price'] * item['quantity']

        sorted_products = sorted(product_sales.items(), key=lambda x: x[1]['quantity'], reverse=True)

        for product_name, data in sorted_products:
            self.top_products_tree.insert("", tk.END, values=(product_name, data['quantity'], f"${data['revenue']:.2f}"))

    def load_sales_by_category_report(self):
        for i in self.sales_by_category_tree.get_children():
            self.sales_by_category_tree.delete(i)
        sales = self.sale_manager.get_sales()

        category_sales = {}
        for sale in sales:
            for item in sale['items']:
                # Find product to get its category
                product = next((p for p in self.product_manager.products if p['name'] == item['name']), None)
                if product:
                    category_id = product.get('category_id', 1)
                    category_name = self.product_manager.get_category_name(category_id)

                    if category_name not in category_sales:
                        category_sales[category_name] = 0
                    category_sales[category_name] += item['price'] * item['quantity']

        sorted_categories = sorted(category_sales.items(), key=lambda x: x[1], reverse=True)

        for category_name, total in sorted_categories:
            self.sales_by_category_tree.insert("", tk.END, values=(category_name, f"${total:.2f}"))

    def load_sales_chart(self):
        self.sales_chart_ax.clear()
        sales = self.sale_manager.get_sales()

        daily_sales = {}
        for sale in sales:
            sale_date = datetime.fromisoformat(sale['timestamp']).date()
            if sale_date not in daily_sales:
                daily_sales[sale_date] = 0
            daily_sales[sale_date] += sale['total']

        sorted_days = sorted(daily_sales.items())
        if not sorted_days:
            self.sales_chart_ax.text(0.5, 0.5, "No Sales Data", ha='center', va='center', color=theme.FG_COLOR)
            self.sales_chart_canvas.draw()
            return

        dates = [day[0].strftime('%Y-%m-%d') for day in sorted_days]
        totals = [day[1] for day in sorted_days]

        self.sales_chart_ax.bar(dates, totals, color=theme.BUTTON_BG_COLOR)
        self.sales_chart_ax.set_title("Total Sales per Day", color=theme.FG_COLOR)
        self.sales_chart_ax.set_xlabel("Date", color=theme.FG_COLOR)
        self.sales_chart_ax.set_ylabel("Total Sales ($)", color=theme.FG_COLOR)
        plt.setp(self.sales_chart_ax.get_xticklabels(), rotation=45, ha="right")
        self.sales_chart_ax.figure.tight_layout()
        self.sales_chart_canvas.draw()

    def create_sales_report_tab(self):
        report_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(report_frame, text="Sales Report")

        # Filter frame
        filter_frame = ttk.LabelFrame(report_frame, text="Filter by Date")
        filter_frame.pack(fill="x", pady=(0, 10), ipady=5)

        ttk.Label(filter_frame, text="Start Date (YYYY-MM-DD):").pack(side="left", padx=5)
        self.start_date_entry = ttk.Entry(filter_frame)
        self.start_date_entry.pack(side="left", padx=5)

        ttk.Label(filter_frame, text="End Date (YYYY-MM-DD):").pack(side="left", padx=5)
        self.end_date_entry = ttk.Entry(filter_frame)
        self.end_date_entry.pack(side="left", padx=5)

        ttk.Button(filter_frame, text="Filter", command=self.load_sales_report).pack(side="left", padx=5)
        ttk.Button(filter_frame, text="Clear Filter", command=self.clear_sales_filter).pack(side="left", padx=5)

        report_tree_frame = ttk.LabelFrame(report_frame, text="All Sales")
        report_tree_frame.pack(fill="both", expand=True)

        self.sales_report_tree = ttk.Treeview(report_tree_frame, columns=("timestamp", "items", "total"), show="headings")
        self.sales_report_tree.heading("timestamp", text="Timestamp")
        self.sales_report_tree.heading("items", text="Items")
        self.sales_report_tree.heading("total", text="Total")
        self.sales_report_tree.pack(fill="both", expand=True)

    def clear_sales_filter(self):
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.load_sales_report()

    def load_sales_report(self):
        for i in self.sales_report_tree.get_children():
            self.sales_report_tree.delete(i)
        sales = self.sale_manager.get_sales()

        start_date_str = self.start_date_entry.get()
        end_date_str = self.end_date_entry.get()

        try:
            start_date = datetime.fromisoformat(start_date_str) if start_date_str else None
            end_date = datetime.fromisoformat(end_date_str + "T23:59:59.999999") if end_date_str else None
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        for sale in reversed(sales):
            sale_time = datetime.fromisoformat(sale["timestamp"])
            if (start_date and sale_time < start_date) or (end_date and sale_time > end_date):
                continue

            items_str = ", ".join([f"{item['name']} (x{item['quantity']})" for item in sale["items"]])
            total_str = f"${sale['total']:.2f}"
            self.sales_report_tree.insert("", tk.END, values=(sale['timestamp'], items_str, total_str))

    def refresh_sales_product_list(self, category_id=None):
        products = self.product_manager.products
        if category_id and category_id != 0: # 0 for 'All Categories'
             products = [p for p in products if p.get('category_id') == category_id]

        self.sales_product_combo['values'] = [p['name'] for p in products if p['quantity'] > 0]
        self.sales_product_combo.set("")

    def create_sales_tab(self):
        sales_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(sales_frame, text="Sales")

        left_frame = ttk.Frame(sales_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        customer_frame = ttk.LabelFrame(left_frame, text="Customer")
        customer_frame.pack(fill="x", pady=(0, 5), ipady=5)

        self.sales_customer_combo = ttk.Combobox(customer_frame, state="readonly")
        self.sales_customer_combo.pack(side="left", expand=True, fill="x", padx=5)
        self.sales_customer_combo.bind("<<ComboboxSelected>>", self.on_sales_customer_selected)

        self.selected_customer_label = ttk.Label(customer_frame, text="No Customer Selected")
        self.selected_customer_label.pack(side="left", padx=5)

        ttk.Button(customer_frame, text="Clear", command=self.clear_selected_customer).pack(side="left", padx=5)


        barcode_frame = ttk.LabelFrame(left_frame, text="Scan Barcode")
        barcode_frame.pack(fill="x", pady=(0, 5), ipady=5)

        self.barcode_entry = ttk.Entry(barcode_frame)
        self.barcode_entry.pack(fill="x", padx=5, pady=5)
        self.barcode_entry.bind("<Return>", self.add_product_by_barcode)

        product_selection_frame = ttk.LabelFrame(left_frame, text="Or Add Manually")
        product_selection_frame.pack(fill="x", pady=5, ipady=5)

        # Category Filter
        ttk.Label(product_selection_frame, text="Category:").pack(side="left", padx=5)
        self.sales_category_combo = ttk.Combobox(product_selection_frame, state="readonly", width=15)
        self.sales_category_combo['values'] = ["All Categories"] + [c['name'] for c in self.product_manager.categories]
        self.sales_category_combo.set("All Categories")
        self.sales_category_combo.pack(side="left", padx=(0, 10))
        self.sales_category_combo.bind("<<ComboboxSelected>>", self.on_sales_category_selected)

        ttk.Label(product_selection_frame, text="Product:").pack(side="left", padx=5)
        self.sales_product_combo = ttk.Combobox(product_selection_frame, state="readonly")
        self.sales_product_combo.pack(side="left", expand=True, fill="x", padx=5)

        ttk.Label(product_selection_frame, text="Qty:").pack(side="left", padx=5)
        self.sales_quantity_spinbox = ttk.Spinbox(product_selection_frame, from_=1, to=99, width=5)
        self.sales_quantity_spinbox.pack(side="left", padx=5)
        self.sales_quantity_spinbox.set(1)

        ttk.Button(product_selection_frame, text="Add", command=self.add_to_cart).pack(side="left", padx=5)

        cart_frame = ttk.LabelFrame(left_frame, text="Current Sale")
        cart_frame.pack(fill="both", expand=True, pady=(10, 0))

        self.cart_tree = ttk.Treeview(cart_frame, columns=("product", "quantity", "price"), show="headings")
        self.cart_tree.heading("product", text="Product")
        self.cart_tree.heading("quantity", text="Quantity")
        self.cart_tree.heading("price", text="Price")
        self.cart_tree.pack(fill="both", expand=True)

        right_frame = ttk.Frame(sales_frame)
        right_frame.pack(side="right", fill="y")

        total_frame = ttk.LabelFrame(right_frame, text="Total")
        total_frame.pack(pady=5, fill="x")

        self.total_label = ttk.Label(total_frame, text="$0.00", style="Total.TLabel")
        self.total_label.pack(padx=20, pady=20)

        ttk.Button(right_frame, text="Finalize Sale", command=self.finalize_sale, style="Accent.TButton").pack(fill="x", pady=5)
        ttk.Button(right_frame, text="Cancel Sale", command=self.cancel_sale).pack(fill="x", pady=5)

    def load_products_to_listbox(self):
        self.product_list.delete(0, tk.END)
        for product in self.product_manager.products:
            category_name = self.product_manager.get_category_name(product.get("category_id", 1))
            self.product_list.insert(tk.END, f"{product['name']} ({category_name}) - ${product['price']:.2f} - Qty: {product['quantity']}")

    def add_product_by_barcode(self, event=None):
        barcode = self.barcode_entry.get()
        if not barcode:
            return

        product = next((p for p in self.product_manager.products if p.get('barcode') == barcode), None)

        if not product:
            messagebox.showerror("Error", f"Product with barcode '{barcode}' not found.")
            self.barcode_entry.delete(0, tk.END)
            return

        self.add_product_to_cart(product, 1)
        self.barcode_entry.delete(0, tk.END)

    def add_to_cart(self):
        selected_product_name = self.sales_product_combo.get()
        if not selected_product_name:
            messagebox.showerror("Error", "Please select a product.")
            return

        try:
            quantity = int(self.sales_quantity_spinbox.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity.")
            return

        product = next((p for p in self.product_manager.products if p['name'] == selected_product_name), None)
        if not product:
            messagebox.showerror("Error", "Product not found.")
            return

        self.add_product_to_cart(product, quantity)

    def add_product_to_cart(self, product, quantity):
        if quantity > product['quantity']:
            messagebox.showerror("Error", "Not enough stock available.")
            return

        for item in self.current_cart:
            if item['name'] == product['name']:
                if item['quantity'] + quantity > product['quantity']:
                    messagebox.showerror("Error", "Not enough stock available for the new quantity.")
                    return
                item['quantity'] += quantity
                break
        else:
            cart_item = {
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity
            }
            self.current_cart.append(cart_item)

        self.update_cart_display()

    def update_cart_display(self):
        for i in self.cart_tree.get_children():
            self.cart_tree.delete(i)
        self.current_total = 0.0
        for item in self.current_cart:
            item_total = item['price'] * item['quantity']
            self.cart_tree.insert("", tk.END, values=(item['name'], item['quantity'], f"${item_total:.2f}"))
            self.current_total += item_total
        self.total_label.config(text=f"${self.current_total:.2f}")

    def finalize_sale(self):
        if not self.current_cart:
            messagebox.showerror("Error", "Cart is empty.")
            return

        if messagebox.askyesno("Confirm Sale", f"Finalize sale for ${self.current_total:.2f}?"):
            for item in self.current_cart:
                for i, product in enumerate(self.product_manager.products):
                    if product['name'] == item['name']:
                        product['quantity'] -= item['quantity']
                        self.product_manager.update_product(i, product)
                        break

            self.sale_manager.record_sale(self.current_cart, self.current_total, self.current_customer_id)
            self.load_products_to_listbox()
            self.cancel_sale()
            messagebox.showinfo("Success", "Sale finalized successfully.")

    def cancel_sale(self):
        self.current_cart = []
        self.update_cart_display()
        self.sales_product_combo.set('')
        self.sales_category_combo.set('All Categories')
        self.refresh_sales_product_list()
        self.clear_selected_customer()


    def show_selected_product(self, event):
        selected_indices = self.product_list.curselection()
        if not selected_indices:
            return

        selected_index = selected_indices[0]
        product = self.product_manager.products[selected_index]

        self.clear_product_fields()
        self.product_name.insert(0, product["name"])
        self.product_price.insert(0, f"{product['price']:.2f}")
        self.product_quantity.insert(0, product["quantity"])
        self.product_barcode.insert(0, product.get("barcode", ""))
        category_name = self.product_manager.get_category_name(product.get("category_id", 1))
        self.product_category.set(category_name)


    def add_product(self):
        name = self.product_name.get()
        price_str = self.product_price.get()
        quantity_str = self.product_quantity.get()
        barcode = self.product_barcode.get()
        category_name = self.product_category.get()

        if not category_name:
            messagebox.showerror("Error", "Please select a category.")
            return

        category_id = next((c['id'] for c in self.product_manager.categories if c['name'] == category_name), 1)

        if not all([name, price_str, quantity_str]):
            messagebox.showerror("Error", "Name, Price and Quantity are required.")
            return

        try:
            price = float(price_str)
            quantity = int(quantity_str)
        except ValueError:
            messagebox.showerror("Error", "Price and Quantity must be numbers.")
            return

        product = {"name": name, "price": price, "quantity": quantity, "barcode": barcode, "category_id": category_id}
        self.product_manager.add_product(product)
        self.load_products_to_listbox()
        self.clear_product_fields()

    def update_product(self):
        selected_indices = self.product_list.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select a product to update.")
            return

        selected_index = selected_indices[0]

        name = self.product_name.get()
        price_str = self.product_price.get()
        quantity_str = self.product_quantity.get()
        barcode = self.product_barcode.get()
        category_name = self.product_category.get()

        if not category_name:
            messagebox.showerror("Error", "Please select a category.")
            return

        category_id = next((c['id'] for c in self.product_manager.categories if c['name'] == category_name), 1)

        if not all([name, price_str, quantity_str]):
            messagebox.showerror("Error", "Name, Price and Quantity are required.")
            return

        try:
            price = float(price_str)
            quantity = int(quantity_str)
        except ValueError:
            messagebox.showerror("Error", "Price and Quantity must be numbers.")
            return

        updated_product = {"name": name, "price": price, "quantity": quantity, "barcode": barcode, "category_id": category_id}
        self.product_manager.update_product(selected_index, updated_product)
        self.load_products_to_listbox()
        self.clear_product_fields()

    def delete_product(self):
        selected_indices = self.product_list.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select a product to delete.")
            return

        selected_index = selected_indices[0]

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?"):
            self.product_manager.delete_product(selected_index)
            self.load_products_to_listbox()
            self.clear_product_fields()

    def clear_product_fields(self):
        self.product_name.delete(0, tk.END)
        self.product_price.delete(0, tk.END)
        self.product_quantity.delete(0, tk.END)
        self.product_barcode.delete(0, tk.END)
        self.product_category.set("")

    def load_customers_to_treeview(self):
        for i in self.customer_tree.get_children():
            self.customer_tree.delete(i)
        for customer in self.customer_manager.customers:
            self.customer_tree.insert("", tk.END, values=(customer['id'], customer['name'], customer['email'], customer['phone']))

    def show_selected_customer(self, event):
        selected_item = self.customer_tree.focus()
        if not selected_item:
            return

        customer_data = self.customer_tree.item(selected_item)['values']
        self.clear_customer_fields()

        self.customer_id_label.config(text=customer_data[0])
        self.customer_name.insert(0, customer_data[1])
        self.customer_email.insert(0, customer_data[2])
        self.customer_phone.insert(0, customer_data[3])

    def add_customer(self):
        name = self.customer_name.get()
        email = self.customer_email.get()
        phone = self.customer_phone.get()

        if not name:
            messagebox.showerror("Error", "Customer name is required.")
            return

        customer_data = {"name": name, "email": email, "phone": phone}
        self.customer_manager.add_customer(customer_data)
        self.load_customers_to_treeview()
        self.clear_customer_fields()

    def update_customer(self):
        customer_id_str = self.customer_id_label.cget("text")
        if not customer_id_str:
            messagebox.showerror("Error", "Please select a customer to update.")
            return

        customer_id = int(customer_id_str)
        name = self.customer_name.get()
        email = self.customer_email.get()
        phone = self.customer_phone.get()

        if not name:
            messagebox.showerror("Error", "Customer name is required.")
            return

        updated_data = {"id": customer_id, "name": name, "email": email, "phone": phone}
        if self.customer_manager.update_customer(customer_id, updated_data):
            self.load_customers_to_treeview()
            self.clear_customer_fields()
        else:
            messagebox.showerror("Error", "Failed to update customer.")

    def clear_customer_fields(self):
        self.customer_id_label.config(text="")
        self.customer_name.delete(0, tk.END)
        self.customer_email.delete(0, tk.END)
        self.customer_phone.delete(0, tk.END)

    def on_sales_customer_selected(self, event):
        customer_name = self.sales_customer_combo.get()
        customer = next((c for c in self.customer_manager.customers if c['name'] == customer_name), None)
        if customer:
            self.current_customer_id = customer['id']
            self.selected_customer_label.config(text=f"Selected: {customer['name']}")
        else:
            self.current_customer_id = None
            self.selected_customer_label.config(text="No Customer Selected")

    def clear_selected_customer(self):
        self.current_customer_id = None
        self.sales_customer_combo.set('')
        self.selected_customer_label.config(text="No Customer Selected")


def main():
    root = tk.Tk()
    root.withdraw()

    login = LoginScreen(root)
    root.wait_window(login)

    if login.user_role:
        app = POSApp(user_role=login.user_role)
        app.mainloop()
    else:
        pass

if __name__ == "__main__":
    main()
