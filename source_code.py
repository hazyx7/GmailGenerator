import os
import random
import re
import csv
import tkinter as tk
from tkinter import messagebox

def generate_emails(base_email, count):
    if not re.match(r'^[a-zA-Z0-9]+@gmail\.com$', base_email):
        raise ValueError("Enter a valid Gmail address (e.g., yourname@gmail.com).")

    local, domain = base_email.split('@')
    max_possible = (2 ** (len(local) - 1)) * 10
    if count > max_possible:
        count = max_possible

    generated = set()
    attempts = 0
    max_attempts = count * 10

    dot = lambda: random.choice(['.', ''])
    plus = lambda: '+' + random.choice('123456789') if random.choice([True, False]) else ''

    while len(generated) < count and attempts < max_attempts:
        new_local = ''.join(f'{char}{dot()}' for char in local[:-1]) + local[-1]
        new_email = f"{new_local}{plus()}@{domain}"
        generated.add(new_email)
        attempts += 1

    return list(generated)

class GmailGenGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gmail Variation Generator - Hazyx7")
        self.root.geometry("480x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#121212")

        tk.Label(root, text="Gmail Variation Generator", font=("Arial", 16, "bold"),
                 fg="#00ffff", bg="#121212").pack(pady=15)

        self.email_entry = self._add_labeled_entry("Enter Gmail Address:")
        self.email_entry.bind("<KeyRelease>", self.update_max_count)

        self.max_label = tk.Label(root, text="", bg="#121212", fg="#bbbbbb", font=("Arial", 9))
        self.max_label.pack()

        self.amount_entry = self._add_labeled_entry("Number of Emails to Generate:")
        self.amount_entry.bind("<KeyRelease>", self.check_amount_limit)

        self.warn_label = tk.Label(root, text="", bg="#121212", fg="#ff6666", font=("Arial", 9, "italic"))
        self.warn_label.pack()

        self.generate_button = tk.Button(root, text="Generate", command=self.prepare_generation,
                                         bg="#00cc66", fg="white", font=("Arial", 11, "bold"),
                                         relief="flat", bd=0, highlightthickness=0, width=15, cursor="hand2")
        self.generate_button.pack(pady=15)
        self.generate_button.bind("<Enter>", lambda e: self.generate_button.config(bg="#00b359"))
        self.generate_button.bind("<Leave>", lambda e: self.generate_button.config(bg="#00cc66"))

        self.save_txt_button = tk.Button(root, text="Save as .txt", command=self.save_as_txt,
                                         bg="#1e90ff", fg="white", font=("Arial", 10, "bold"),
                                         relief="flat", bd=0, width=15, cursor="hand2")
        self.save_csv_button = tk.Button(root, text="Save as .csv", command=self.save_as_csv,
                                         bg="#ff9933", fg="white", font=("Arial", 10, "bold"),
                                         relief="flat", bd=0, width=15, cursor="hand2")

        self.open_file_button = tk.Button(root, text="Open File", command=self.open_file,
                                          bg="#444444", fg="white", font=("Arial", 10),
                                          relief="flat", bd=0, width=15, cursor="hand2")
        self.open_file_button.pack_forget()

        root.bind("<Return>", lambda event: self.prepare_generation())

        self.max_possible = 0
        self.generated_emails = []
        self.output_path = ""

    def _add_labeled_entry(self, label_text):
        tk.Label(self.root, text=label_text, bg="#121212", fg="white", font=("Arial", 10)).pack()
        entry = tk.Entry(self.root, width=40, font=("Arial", 10))
        entry.pack(pady=5)
        return entry

    def update_max_count(self, event=None):
        email = self.email_entry.get().strip().lower()
        match = re.match(r'^([a-zA-Z0-9]+)@gmail\.com$', email)
        if match:
            local = match.group(1)
            self.max_possible = (2 ** (len(local) - 1)) * 10
            self.max_label.config(text=f"Max variations: {self.max_possible}")
        else:
            self.max_possible = 0
            self.max_label.config(text="")
        self.check_amount_limit()

    def check_amount_limit(self, event=None):
        try:
            amount = int(self.amount_entry.get().strip())
            if self.max_possible and amount > self.max_possible:
                self.warn_label.config(
                    text=f"Warning: Max allowed is {self.max_possible}. Will auto-limit.")
            else:
                self.warn_label.config(text="")
        except ValueError:
            self.warn_label.config(text="")

    def prepare_generation(self):
        email = self.email_entry.get().strip().lower()
        try:
            amount = int(self.amount_entry.get().strip())
            if self.max_possible and amount > self.max_possible:
                amount = self.max_possible
            self.generated_emails = generate_emails(email, amount)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        self.save_txt_button.pack(pady=2)
        self.save_csv_button.pack(pady=2)

    def save_as_txt(self):
        self.output_path = "emails.txt"
        try:
            with open(self.output_path, "w") as f:
                f.write("\n".join(self.generated_emails))
            self.after_save()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save TXT:\n{e}")

    def save_as_csv(self):
        self.output_path = "emails.csv"
        try:
            with open(self.output_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Emails"])
                for email in self.generated_emails:
                    writer.writerow([email])
            self.after_save()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV:\n{e}")

    def after_save(self):
        messagebox.showinfo("Success", f"{len(self.generated_emails)} emails have been saved in '{self.output_path}'")
        self.open_file_button.pack(pady=5)
        self.save_txt_button.pack_forget()
        self.save_csv_button.pack_forget()

    def open_file(self):
        try:
            if self.output_path:
                os.startfile(self.output_path)
        except AttributeError:
            import subprocess
            subprocess.call(["open", self.output_path])

if __name__ == "__main__":
    root = tk.Tk()
    app = GmailGenGUI(root)
    root.mainloop()
