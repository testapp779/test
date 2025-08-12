import tkinter as tk
from tkinter import ttk, messagebox
from user_manager import UserManager

class LoginScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Login")
        self.geometry("300x150")
        self.transient(parent)
        self.grab_set()

        self.user_manager = UserManager()
        self.user_role = None

        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = ttk.Entry(main_frame)
        self.username_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(main_frame, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(main_frame, show="*")
        self.password_entry.grid(row=1, column=1, sticky="ew")

        self.password_entry.bind("<Return>", self.attempt_login)

        login_button = ttk.Button(main_frame, text="Login", command=self.attempt_login)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def attempt_login(self, event=None):
        username = self.username_entry.get()
        password = self.password_entry.get()

        role = self.user_manager.verify_user(username, password)

        if role:
            self.user_role = role
            self.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def on_closing(self):
        # If the user closes the login window, exit the application
        self.parent.destroy()
