import re
import tkinter as tk
from tkinter import messagebox


root = tk.Tk()
root.title("Employee Registration and Salary Utility System")
root.configure(bg="#ecf0f5")
root.resizable(True, True)

base_font = ("Arial", 10)
header_font = ("Arial", 12, "bold")


# -----------------------------
# Scrollable Content Container
# -----------------------------
main_frame = tk.Frame(root, bg="#ecf0f5")
main_frame.grid(row=0, column=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

canvas = tk.Canvas(main_frame, bg="#ecf0f5", highlightthickness=0)
v_scroll = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=v_scroll.set)

v_scroll.grid(row=0, column=1, sticky="ns")
canvas.grid(row=0, column=0, sticky="nsew")
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

content_frame = tk.Frame(canvas, bg="#ecf0f5")
canvas.create_window((0, 0), window=content_frame, anchor="nw")


def _update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))


content_frame.bind("<Configure>", _update_scroll_region)


# -----------------------------
# Part 1: Introduction (Theory)
# -----------------------------
intro_frame = tk.Frame(content_frame, bg="#d9e3ed", padx=10, pady=10, bd=1, relief="solid")
intro_frame.grid(row=0, column=0, padx=12, pady=10, sticky="ew")
intro_frame.grid_columnconfigure(0, weight=1)

intro_text = (
    "Overview:\n"
    "Tkinter is Python's built-in toolkit for creating graphical user interface (GUI) applications. "
    "It provides widgets like buttons, labels, and text fields to build desktop apps. In GUI development, "
    "Tkinter serves as an easy entry point to design windows, handle user input, and respond to events.\n\n"
    "Key features: (1) comes bundled with Python, (2) simple and beginner-friendly, "
    "(3) cross-platform compatible, and (4) enables rapid prototyping.\n\n"
    "For office systems like employee registration and payroll management, Tkinter provides form creation, "
    "input validation, and salary calculation with an interactive interface."
)

tk.Label(intro_frame, text=intro_text, bg="#d9e3ed", fg="#1a1a1a", font=base_font, justify="left", wraplength=640).grid(
    row=0, column=0, sticky="w"
)


# -----------------------------
# Part 2: Notice Window (Sticky Demo)
# -----------------------------
notice_frame = tk.Frame(content_frame, bg="#f5f5f5", padx=10, pady=10, bd=1, relief="solid")
notice_frame.grid(row=1, column=0, padx=12, pady=6, sticky="ew")
notice_frame.grid_columnconfigure((0, 1, 2), weight=1)

notice_title = tk.Label(
    notice_frame,
    text="Welcome to Employee Registration and Salary Management",
    bg="#f5f5f5",
    fg="#1a3a5c",
    font=header_font,
)
notice_title.grid(row=0, column=0, columnspan=3, pady=(0, 8))

# Sticky alignment demonstration
sticky_cell = tk.Frame(notice_frame, bg="#f0f0f0", bd=1, relief="solid", width=360, height=90)
sticky_cell.grid(row=1, column=0, columnspan=3, sticky="ew")
sticky_cell.grid_propagate(False)

label_n = tk.Label(sticky_cell, text="N", bg="#f0f0f0", fg="#222222", font=base_font)
label_e = tk.Label(sticky_cell, text="E", bg="#f0f0f0", fg="#222222", font=base_font)
label_s = tk.Label(sticky_cell, text="S", bg="#f0f0f0", fg="#222222", font=base_font)
label_w = tk.Label(sticky_cell, text="W", bg="#f0f0f0", fg="#222222", font=base_font)

label_n.grid(row=0, column=1, sticky="n")
label_e.grid(row=1, column=2, sticky="e")
label_s.grid(row=2, column=1, sticky="s")
label_w.grid(row=1, column=0, sticky="w")

for i in range(3):
    sticky_cell.grid_rowconfigure(i, weight=1)
    sticky_cell.grid_columnconfigure(i, weight=1)


# -----------------------------
# Part 3: Employee Registration Form
# -----------------------------
form_frame = tk.Frame(content_frame, bg="#fafafa", padx=12, pady=12, bd=1, relief="solid")
form_frame.grid(row=2, column=0, padx=12, pady=8, sticky="ew")
form_frame.grid_columnconfigure(1, weight=1)

form_title = tk.Label(form_frame, text="Employee Registration Details", bg="#fafafa", fg="#2c5282", font=header_font)
form_title.grid(row=0, column=0, columnspan=2, pady=(0, 8), sticky="w")

labels = ["First Name", "Last Name", "Email Address", "Department"]
entries = {}

for idx, text in enumerate(labels, start=1):
    tk.Label(form_frame, text=text + ":", bg="#fafafa", fg="#2c2c2c", font=base_font).grid(
        row=idx, column=0, sticky="w", pady=4
    )
    entry = tk.Entry(form_frame, font=base_font, width=34)
    entry.grid(row=idx, column=1, sticky="ew", pady=4, padx=(8, 0))
    entries[text] = entry


# -----------------------------
# Part 4: Salary Utility Calculator
# -----------------------------
calc_frame = tk.Frame(content_frame, bg="#fafafa", padx=12, pady=12, bd=1, relief="solid")
calc_frame.grid(row=3, column=0, padx=12, pady=8, sticky="ew")
calc_frame.grid_columnconfigure(1, weight=1)

calc_title = tk.Label(calc_frame, text="Salary Calculation Tool", bg="#fafafa", fg="#2c5282", font=header_font)
calc_title.grid(row=0, column=0, columnspan=2, pady=(0, 8), sticky="w")

wage_entry = tk.Entry(calc_frame, font=base_font, width=20)
workdays_entry = tk.Entry(calc_frame, font=base_font, width=20)


tk.Label(calc_frame, text="Daily Wage:", bg="#fafafa", fg="#2c2c2c", font=base_font).grid(
    row=1, column=0, sticky="w", pady=4
)
wage_entry.grid(row=1, column=1, sticky="w", pady=4, padx=(8, 0))

tk.Label(calc_frame, text="Working Days:", bg="#fafafa", fg="#2c2c2c", font=base_font).grid(
    row=2, column=0, sticky="w", pady=4
)
workdays_entry.grid(row=2, column=1, sticky="w", pady=4, padx=(8, 0))

result_label = tk.Label(calc_frame, text="Total Salary: --", bg="#fafafa", fg="#1b6e3a", font=base_font)
result_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=(6, 2))


# -----------------------------
# Part 5: Buttons and Actions
# -----------------------------
email_regex = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def clear_form():
    for entry in entries.values():
        entry.delete(0, tk.END)


def submit_form():
    first_name = entries["First Name"].get().strip()
    last_name = entries["Last Name"].get().strip()
    email = entries["Email Address"].get().strip()
    dept = entries["Department"].get().strip()

    if not all([first_name, last_name, email, dept]):
        messagebox.showerror("Validation Error", "All fields are required.")
        return

    if any(char.isdigit() for char in first_name) or any(char.isdigit() for char in last_name):
        messagebox.showerror("Validation Error", "First and Last names must not contain numbers.")
        return

    if not email_regex.match(email):
        messagebox.showerror("Validation Error", "Please enter a valid email address.")
        return

    messagebox.showinfo("Success", "Employee registered successfully.")
    clear_form()


def reset_calculator():
    wage_entry.delete(0, tk.END)
    workdays_entry.delete(0, tk.END)
    result_label.config(text="Total Salary: --")


def calculate_salary():
    wage = wage_entry.get().strip()
    days = workdays_entry.get().strip()

    if not wage or not days:
        messagebox.showerror("Validation Error", "Please fill in both salary fields.")
        return

    try:
        wage_val = float(wage)
        days_val = float(days)
    except ValueError:
        messagebox.showerror("Validation Error", "Daily Wage and Working Days must be numeric.")
        return

    if wage_val <= 0 or days_val <= 0:
        messagebox.showerror("Validation Error", "Values must be greater than 0.")
        return

    total = wage_val * days_val
    result_label.config(text=f"Total Salary: {total:,.2f}")


button_frame = tk.Frame(content_frame, bg="#ecf0f5", padx=12, pady=6)
button_frame.grid(row=4, column=0, sticky="ew")


def _resize_canvas(event):
    canvas.itemconfigure("all", width=event.width)


canvas.bind("<Configure>", _resize_canvas)

submit_btn = tk.Button(button_frame, text="Submit", font=base_font, bg="#2d6a4f", fg="white", width=15, command=submit_form)
clear_btn = tk.Button(button_frame, text="Clear", font=base_font, bg="#5a6c7d", fg="white", width=12, command=clear_form)
calc_btn = tk.Button(button_frame, text="Calculate", font=base_font, bg="#1b3a5c", fg="white", width=12, command=calculate_salary)
reset_btn = tk.Button(button_frame, text="Reset", font=base_font, bg="#5a6c7d", fg="white", width=12, command=reset_calculator)
exit_btn = tk.Button(button_frame, text="Exit", font=base_font, bg="#b85c5a", fg="white", width=10, command=root.destroy)

submit_btn.grid(row=0, column=0, padx=3, pady=4)
clear_btn.grid(row=0, column=1, padx=3, pady=4)
reset_btn.grid(row=0, column=2, padx=3, pady=4)
calc_btn.grid(row=0, column=3, padx=3, pady=4)
exit_btn.grid(row=0, column=4, padx=3, pady=4)



root.mainloop()
