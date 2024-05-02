## CryptBook
# Made by Aryqman (Please do credit me if you end up using it :D)




import tkinter as tk
from tkinter import ttk
import hashlib
import random
import string
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import os

PASSWORDS_FILE = "passwords.txt"
SALT = "my_secret_salt"  # Use a secret salt to prevent rainbow table attacks
KEY_FILE = "key.txt"
def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE,"rb") as file:
            return file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE,"wb") as file:
            file.write(key)
        return key
    
KEY = load_key()
fernet = Fernet(KEY)

class PasswordManagerApp:

    def __init__(self, master):

        self.master = master

        self.master.title("Password Manager")

        self.master.geometry("450x300")

        self.master.configure(bg="#f0f0f0", padx=10, pady=10)


        font = ("Helvetica", 12)


        self.service_label = ttk.Label(self.master, text="Service:", font=font, foreground="#333")

        self.service_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)


        self.service_entry = ttk.Entry(self.master, font=font)

        self.service_entry.grid(row=0, column=1, padx=5, pady=5)


        self.username_label = ttk.Label(self.master, text="Username:", font=font, foreground="#333")

        self.username_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)


        self.username_entry = ttk.Entry(self.master, font=font)

        self.username_entry.grid(row=1, column=1, padx=5, pady=5)


        self.password_label = ttk.Label(self.master, text="Password:", font=font, foreground="#333")

        self.password_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)


        self.password_entry = ttk.Entry(self.master, show="*", font=font)

        self.password_entry.grid(row=2, column=1, padx=5, pady=5)


        self.generate_password_button = ttk.Button(self.master, text="Generate Password", command=self.generate_password, style='TButton')

        self.generate_password_button.grid(row=2, column=2, padx=5, pady=5)


        self.save_button = ttk.Button(self.master, text="Save", command=self.save_password, style='TButton')

        self.save_button.grid(row=3, column=1, padx=5, pady=5)


        self.get_button = ttk.Button(self.master, text="Get Password", command=self.get_password, style='TButton')

        self.get_button.grid(row=4, column=1, padx=5, pady=5)

        
        self.copy_button = tk.Button(master, text="Copy Password", command=self.copy_password)

        self.copy_button.grid(row=5, column=1)

    
    def check_password_strength(self, password):

        if len(password) < 8:

            return "Weak"

        has_upper = any(c.isupper() for c in password)

        has_lower = any(c.islower() for c in password)

        has_digit = any(c.isdigit() for c in password)

        has_symbol = any(c in string.punctuation for c in password)

        score = sum([has_upper, has_lower, has_digit, has_symbol])

        if score <= 3:

            return "Medium"

        elif score <= 4:

            return "Strong"

        else:

            return "Very Strong"

    def encrypt_password(self, password):

        return fernet.encrypt(password.encode()).decode()


    def decrypt_password(self, encrypted_password):

        return fernet.decrypt(encrypted_password.encode()).decode()


    def generate_password(self):
        password_length = 12
        max_attempts = 1000
        for _ in range(max_attempts):
            password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=password_length))
            strength = self.check_password_strength(password)
            if strength == "Very Strong":
                break
        else:
            messagebox.showerror("Error", "Failed to generate a strong password after {} attempts.".format(max_attempts))
            return
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(tk.END, password)
        messagebox.showinfo("Password Strength", f"Password Strength: {strength}")
    
    def save_password(self):
        service = self.service_entry.get()

        username = self.username_entry.get()

        password = self.password_entry.get()

        encrypted_password = self.encrypt_password(password)

        try:

            with open(PASSWORDS_FILE, "a") as file:

                file.write(f"{service},{username},{encrypted_password}\n")
                messagebox.showinfo("Success", "Password saved successfully!")

        except IOError as e:

            messagebox.showerror("Error", f"Error saving password: {e}")


    def get_password(self):

        service = self.service_entry.get()

        try:

            with open(PASSWORDS_FILE, "r") as file:

                for line in file:

                    parts = line.strip().split(",")

                    if len(parts) == 3 and parts[0] == service:

                        username, encrypted_password = parts[1], parts[2]

                        password = self.decrypt_password(encrypted_password)

                        messagebox.showinfo("Password", f"Service: {service}\nUsername: {username}\nPassword: {password}")

                        return

        except IOError as e:

            messagebox.showerror("Error", f"Error reading password file: {e}")


    def copy_password(self):

        service = self.service_entry.get()

        try:

            with open(PASSWORDS_FILE, "r") as file:

                for line in file:

                    parts = line.strip().split(",")

                    if len(parts) == 3 and parts[0] == service:

                        username, encrypted_password = parts[1], parts[2]

                        password = self.decrypt_password(encrypted_password)

                        self.master.clipboard_clear()

                        self.master.clipboard_append(password)

                        messagebox.showinfo("Copied", "Password copied to clipboard.")

                        return

        except IOError as e:

            messagebox.showerror("Error", f"Error reading password file: {e}")


def main():

    root = tk.Tk()

    app = PasswordManagerApp(root)

    root.mainloop()


if __name__ == "__main__":

    main()