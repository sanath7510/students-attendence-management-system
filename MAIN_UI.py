import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import pandas as pd

from register import register_page
from attendance import view_attendance_page
from view_qr import view_qr_page
from main import start_face_attendance, start_qr_attendance

ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.geometry("1200x850")
root.title("Hybrid AI Attendance System")

container = ctk.CTkFrame(root)
container.pack(fill="both", expand=True)

dashboard_frame = ctk.CTkFrame(container)
register_frame = ctk.CTkFrame(container)
attendance_frame = ctk.CTkFrame(container)
view_frame = ctk.CTkFrame(container)
qr_frame = ctk.CTkFrame(container)

def show_frame(frame):

    for f in (
        dashboard_frame,
        register_frame,
        attendance_frame,
        view_frame,
        qr_frame
    ):
        f.pack_forget()

    frame.pack(fill="both", expand=True)

# ================= DASHBOARD =================

ctk.CTkLabel(
    dashboard_frame,
    text="Hybrid AI Attendance System",
    font=("Arial", 34, "bold")
).pack(pady=40)

buttons = [
    ("Student Registration", register_frame),
    ("Start Attendance", attendance_frame),
    ("View Attendance", view_frame),
    ("View QR", qr_frame)
]

for text, frame in buttons:

    ctk.CTkButton(
        dashboard_frame,
        text=text,
        width=320,
        height=50,
        command=lambda f=frame: show_frame(f)
    ).pack(pady=15)

ctk.CTkButton(
    dashboard_frame,
    text="Exit",
    width=320,
    height=50,
    fg_color="red",
    command=root.destroy
).pack(pady=15)

# ================= REGISTER =================

ctk.CTkButton(
    register_frame,
    text="Back",
    command=lambda: show_frame(dashboard_frame)
).pack(anchor="nw", padx=10, pady=10)

register_page(register_frame)

# ================= ATTENDANCE =================

ctk.CTkButton(
    attendance_frame,
    text="Back",
    command=lambda: show_frame(dashboard_frame)
).pack(anchor="nw", padx=10, pady=10)

ctk.CTkLabel(
    attendance_frame,
    text="Select Subject Code",
    font=("Arial", 30, "bold")
).pack(pady=30)

subject_var = tk.StringVar()

dropdown = ttk.Combobox(
    attendance_frame,
    textvariable=subject_var,
    width=40,
    state="readonly"
)

dropdown.pack(pady=20)

def refresh_dropdown():

    try:

        students_df = pd.read_csv("students.csv")

        subjects = sorted(
            students_df["SubjectCode"]
            .dropna()
            .unique()
            .tolist()
        )

        dropdown["values"] = subjects

        if subjects:
            dropdown.current(0)

    except:
        pass

refresh_dropdown()

mode_var = tk.StringVar(value="Face")

ctk.CTkLabel(
    attendance_frame,
    text="Select Attendance Mode",
    font=("Arial", 18)
).pack(pady=10)

ctk.CTkRadioButton(
    attendance_frame,
    text="Face Recognition",
    variable=mode_var,
    value="Face"
).pack(pady=5)

ctk.CTkRadioButton(
    attendance_frame,
    text="QR Verification",
    variable=mode_var,
    value="QR"
).pack(pady=5)

def start_selected_attendance():

    subject_code = subject_var.get()

    mode = mode_var.get()

    if mode == "Face":
        start_face_attendance(subject_code)

    elif mode == "QR":
        start_qr_attendance(subject_code)

ctk.CTkButton(
    attendance_frame,
    text="Start Attendance",
    width=320,
    height=50,
    command=start_selected_attendance
).pack(pady=25)

# ================= VIEW ATTENDANCE =================

ctk.CTkButton(
    view_frame,
    text="Back",
    command=lambda: show_frame(dashboard_frame)
).pack(anchor="nw", padx=10, pady=10)

view_attendance_page(view_frame)

# ================= VIEW QR =================

ctk.CTkButton(
    qr_frame,
    text="Back",
    command=lambda: show_frame(dashboard_frame)
).pack(anchor="nw", padx=10, pady=10)

view_qr_page(qr_frame)

show_frame(dashboard_frame)

root.mainloop()