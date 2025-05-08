import tkinter as tk
from tkinter import ttk, messagebox
import re

class passStrChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Checker")
        self.root.geometry("450x400")
        self.root.configure(bg='#121212')

        # Set theme colour
        self.bg_color = '#121212'
        self.widget_bg = '#1e1e1e'
        self.text_color = '#e0e0e0'
        self.accent_color = '#4a4a4a'
        self.green = '#2ecc71'
        self.orange = '#e67e22'
        self.red = '#e74c3c'

        # Configure Style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Progressbar style
        self.style.configure("red.Horizontal.TProgressbar",troughcolor=self.widget_bg, background=self.red)
        self.style.configure("orange.Horizontal.TProgressbar",troughcolor=self.widget_bg, background=self.orange)
        self.style.configure("green.Horizontal.TProgressbar",troughcolor=self.widget_bg, background=self.green)

        # Lable style
        self.style.configure("TLable", background = self.bg_color, foreground = self.text_color)

        # Entry style
        self.style.configure("TEntry", fieldbackground = self.widget_bg, foreground = self.text_color, insertcolor = self.text_color)

        self.password_var = tk.StringVar()
        self.password_var.trace_add("write", self.check_strength)

        self.create_widgets()
        
    def create_widgets(self):
        # Main container frame 
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')

        # Title
        title = tk .Label(main_frame, text="Password Strength Analyzer", font=("Roboto", 14, "bold"), bg=self.bg_color, fg=self.text_color)
        title.pack(pady=(0, 15))

        # Password entry frame
        entry_frame = tk.Frame(main_frame, bg=self.bg_color)
        entry_frame.pack(fill='x', pady=5)

        tk.Label(entry_frame, text="Enter Password: ", bg=self.bg_color, fg=self.text_color).pack(side='left', padx=(0, 10), pady=5)
        self.entry = ttk.Entry(entry_frame, textvariable=self.password_var, show="*", width=30, style='TEntry')
        self.entry.pack(side="left", expand=True, fill='x')

        # Password Checkbutton
        self.show_pass = tk.BooleanVar()
        show_pass_btn = tk.Checkbutton(main_frame, text="Show Password", variable=self.show_pass, command=self.toggle_password, bg=self.bg_color, fg=self.text_color, selectcolor=self.widget_bg, activebackground=self.bg_color, activeforeground=self.text_color)
        show_pass_btn.pack(pady=5)

        # Strength Meter
        meter_frame = tk.Frame(main_frame, bg=self.bg_color)
        meter_frame.pack(fill='x', pady=10)

        self.progress = ttk.Progressbar(meter_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(side='left', expand=True, fill='x')

        self.strength_lable = tk.Label(meter_frame, text="None", font=("Roboto",10, "bold"), bg=self.bg_color, fg=self.accent_color, width=8)
        self.strength_lable.pack(side='left', padx=(10,0))

        # Criteria Frame
        self.criteria_frame = tk.Frame(main_frame, bg=self.bg_color)
        self.criteria_frame.pack(fill='x', pady=(15,5))

        # Criteria Labels
        tk.Label(self.criteria_frame, text="PASSWORD REQUIREMENTS:", font=("Roboto", 9), bg=self.bg_color, fg=self.accent_color).pack(anchor='w', pady=(0, 5))
        self.criteria_label = {
            "length": tk.Label(self.criteria_frame, text="✓ 8+ Characters", font=("Roboto",8), fg="gray", bg=self.bg_color),
            "upper": tk.Label(self.criteria_frame, text="✓ Uppercase Letter", font=("Roboto",8), fg="gray", bg=self.bg_color),
            "lower": tk.Label(self.criteria_frame, text="✓ Uppercase Letter", font=("Roboto",8), fg="gray", bg=self.bg_color),
            "number": tk.Label(self.criteria_frame, text="✓ Number", font=("Roboto",8), fg="gray", bg=self.bg_color),
            "special": tk.Label(self.criteria_frame, text="✓ Special Character", font=("Roboto",8), fg="gray", bg=self.bg_color)
        }

        for lable in self.criteria_label.values():
            lable.pack(anchor="w", pady=1)

    def toggle_password(self):
        self.entry.config(show="" if self.show_pass.get() else "*")

    def check_strength(self, *args):
        password = self.password_var.get()
        strength = 0
        max_strength = 5

        criteria = {
            "length": len(password) >= 8,
            "upper": re.search(r"[A-Z]", password),
            "lower": re.search(r"[a-z]",password),
            "number": re.search(r"[0-9]", password),
            "special": re.search(r"[!@#$%^&*(),.?\"_:{}|<>]", password)
        }

        for key, lable in self.criteria_label.items():
            if criteria[key]:
                lable.config(fg="green")
                strength += 1
            else:
                lable.config(fg="gray")

        progress_value = (strength / max_strength)*100
        self.progress["value"] = progress_value

        if strength <= 2:
            self.strength_lable.config(text="Weak", fg=self.red)
            self.progress["style"] = "red.Horizontal.TProgressbar"
        elif strength <= 4:
            self.strength_lable.config(text="Medium", fg=self.orange)
            self.progress["style"] = "orange.Horizontal.TProgressbar"
        else:
            self.strength_lable.config(text="Strong", fg=self.green)
            self.progress["style"] = "green.Horizontal.TProgressbar"
        
if __name__ == "__main__":
    root = tk.Tk()
    app = passStrChecker(root)
    root.mainloop()
    
