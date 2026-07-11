import tkinter as tk
from tkinter import messagebox
import uuid
import subprocess

def current_hardware():
    mac = str(uuid.getnode())

    uuid_value = subprocess.check_output(
        "wmic csproduct get uuid",
        shell=True
    ).decode().split("\n")[1].strip()

    return mac + uuid_value

def copy_id():
    root.clipboard_clear()
    root.clipboard_append(hardware_id)
    messagebox.showinfo("Copied", "Hardware ID copied successfully!")

hardware_id = current_hardware()

root = tk.Tk()
root.title("MEP Scheduler - Hardware ID")
root.geometry("650x220")
root.resizable(False, False)

tk.Label(
    root,
    text="Hardware ID",
    font=("Arial", 14, "bold")
).pack(pady=10)

entry = tk.Entry(root, width=80, font=("Arial", 10))
entry.pack(pady=10)
entry.insert(0, hardware_id)
entry.config(state="readonly")

tk.Button(
    root,
    text="Copy Hardware ID",
    command=copy_id,
    width=20
).pack(pady=15)

root.mainloop()