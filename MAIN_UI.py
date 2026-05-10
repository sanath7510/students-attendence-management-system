from attendance_statistics import open_statistics_window
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import pandas as pd
import os

from register import register_page
from attendance import view_attendance_page
from view_qr import view_qr_page
from main import (
    start_face_attendance,
    start_qr_attendance
)

# ================= APP SETTINGS =================

ctk.set_appearance_mode("dark")

root = ctk.CTk()

root.geometry("1200x850")

root.title("Hybrid AI Attendance System")

# ================= MAIN CONTAINER =================

container = ctk.CTkFrame(root)

container.pack(
    fill="both",
    expand=True
)

# ================= FRAMES =================

dashboard_frame = ctk.CTkFrame(container)

register_frame = ctk.CTkFrame(container)

attendance_frame = ctk.CTkFrame(container)

view_frame = ctk.CTkFrame(container)

qr_frame = ctk.CTkFrame(container)

# ================= FRAME SWITCH =================

def show_frame(frame):

    for f in (
        dashboard_frame,
        register_frame,
        attendance_frame,
        view_frame,
        qr_frame
    ):

        f.pack_forget()

    frame.pack(
        fill="both",
        expand=True
    )

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
        command=lambda f=frame:
        show_frame(f)
    ).pack(pady=15)

# ================= EXIT BUTTON =================

ctk.CTkButton(
    dashboard_frame,
    text="Exit",
    width=320,
    height=50,
    fg_color="red",
    command=root.destroy
).pack(pady=15)

# ================= REGISTER PAGE =================

ctk.CTkButton(
    register_frame,
    text="Back",
    command=lambda:
    show_frame(dashboard_frame)
).pack(
    anchor="nw",
    padx=10,
    pady=10
)

register_page(register_frame)

# ================= ATTENDANCE PAGE =================

ctk.CTkButton(
    attendance_frame,
    text="Back",
    command=lambda:
    show_frame(dashboard_frame)
).pack(
    anchor="nw",
    padx=10,
    pady=10
)

ctk.CTkLabel(
    attendance_frame,
    text="Start Attendance",
    font=("Arial", 32, "bold")
).pack(pady=30)

# ================= SUBJECT DROPDOWN =================

subject_var = ctk.StringVar()

def load_subjects():

    try:

        if not os.path.exists("students.csv"):

            return []

        students_df = pd.read_csv(
            "students.csv"
        )

        if students_df.empty:

            return []

        subjects = sorted(
            students_df["SubjectCode"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        return subjects

    except Exception as e:

        print(
            "Dropdown Error:",
            e
        )

        return []

subjects = load_subjects()

subject_dropdown = ctk.CTkComboBox(
    attendance_frame,
    values=subjects if subjects else ["No Subjects"],
    variable=subject_var,
    width=300
)

subject_dropdown.pack(pady=20)

# Set first subject automatically
if subjects:

    subject_dropdown.set(subjects[0])

else:

    subject_dropdown.set("No Subjects")

# ================= REFRESH BUTTON =================

def refresh_dropdown():

    subjects = load_subjects()

    if subjects:

        subject_dropdown.configure(
            values=subjects
        )

        subject_dropdown.set(
            subjects[0]
        )

    else:

        subject_dropdown.configure(
            values=["No Subjects"]
        )

        subject_dropdown.set(
            "No Subjects"
        )

ctk.CTkButton(
    attendance_frame,
    text="Refresh Subjects",
    width=220,
    command=refresh_dropdown
).pack(pady=10)

# ================= ATTENDANCE MODE =================

mode_var = tk.StringVar(
    value="Face"
)

ctk.CTkLabel(
    attendance_frame,
    text="Select Attendance Mode",
    font=("Arial", 20)
).pack(pady=15)

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

# ================= START ATTENDANCE =================

def start_selected_attendance():

    subject_code = (
        subject_var.get()
        .strip()
    )

    if (
        not subject_code
        or subject_code == "No Subjects"
    ):

        print(
            "No subject selected"
        )

        return

    mode = mode_var.get()

    print(
        "Starting Attendance:",
        subject_code,
        mode
    )

    if mode == "Face":

        start_face_attendance(
            subject_code
        )

    elif mode == "QR":

        start_qr_attendance(
            subject_code
        )

ctk.CTkButton(
    attendance_frame,
    text="Start Attendance",
    width=320,
    height=50,
    command=start_selected_attendance
).pack(pady=30)

# ================= VIEW ATTENDANCE =================

ctk.CTkButton(
    view_frame,
    text="Back",
    command=lambda:
    show_frame(dashboard_frame)
).pack(
    anchor="nw",
    padx=10,
    pady=10
)

view_attendance_page(view_frame)

# ================= VIEW QR =================

ctk.CTkButton(
    qr_frame,
    text="Back",
    command=lambda:
    show_frame(dashboard_frame)
).pack(
    anchor="nw",
    padx=10,
    pady=10
)

view_qr_page(qr_frame)

# ================= START APP =================

show_frame(
    dashboard_frame
)

root.mainloop()