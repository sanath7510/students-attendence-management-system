from background import set_background

from attendance_statistics import open_statistics_window
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

from register import register_page
from attendance import view_attendance_page
from view_qr import view_qr_page
from main import (
    start_face_attendance,
    start_qr_attendance
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("1200x850")
root.title("Hybrid AI Attendance System")

FACULTY_FILE = "faculty_data.csv"

if not os.path.exists(FACULTY_FILE):
    pd.DataFrame(columns=[
        "Faculty_Name",
        "Subject_Name",
        "Subject_Code",
        "Password"
    ]).to_csv(FACULTY_FILE, index=False)

container = ctk.CTkFrame(root, fg_color="#232734")
container.pack(fill="both", expand=True)

dashboard_frame = ctk.CTkFrame(container, fg_color="#232734")
register_menu_frame = ctk.CTkFrame(container, fg_color="#232734")
student_register_frame = ctk.CTkFrame(container, fg_color="#232734")
faculty_register_frame = ctk.CTkFrame(container, fg_color="#232734")
attendance_frame = ctk.CTkFrame(container, fg_color="#232734")
view_frame = ctk.CTkFrame(container, fg_color="#232734")
qr_frame = ctk.CTkFrame(container, fg_color="#232734")

ALL_FRAMES = [
    dashboard_frame,
    register_menu_frame,
    student_register_frame,
    faculty_register_frame,
    attendance_frame,
    view_frame,
    qr_frame
]

def show_frame(frame):
    for f in ALL_FRAMES:
        f.pack_forget()
    frame.pack(fill="both", expand=True)

# ================= DASHBOARD =================

card = ctk.CTkFrame(
    dashboard_frame,
    corner_radius=18,
    fg_color="#2e3445",
    width=450,
    height=600
)
card.place(relx=0.5, rely=0.5, anchor="center")

ctk.CTkLabel(
    card,
    text="Hybrid AI Attendance System",
    font=("Segoe UI", 34, "bold")
).pack(pady=(40,10))

ctk.CTkLabel(
    card,
    text="Face Recognition + QR Smart Attendance",
    font=("Segoe UI", 15)
).pack(pady=(0,30))

buttons = [
    ("Registration", register_menu_frame),
    ("Start Attendance", attendance_frame),
    ("View Attendance", view_frame),
    ("View QR", qr_frame)
]

for text_btn, frame in buttons:
    ctk.CTkButton(
        card,
        text=text_btn,
        width=320,
        height=50,
        corner_radius=12,
        font=("Segoe UI", 16, "bold"),
        command=lambda f=frame: show_frame(f)
    ).pack(pady=14)

ctk.CTkButton(
    card,
    text="Exit",
    width=320,
    height=50,
    corner_radius=12,
    fg_color="red",
    hover_color="#aa0000",
    font=("Segoe UI", 16, "bold"),
    command=root.destroy
).pack(pady=14)

# ================= REGISTRATION MENU =================

ctk.CTkButton(
    register_menu_frame,
    text="Back",
    command=lambda: show_frame(dashboard_frame)
).pack(anchor="nw", padx=15, pady=15)

ctk.CTkLabel(
    register_menu_frame,
    text="Registration",
    font=("Segoe UI", 32, "bold")
).pack(pady=40)

ctk.CTkButton(
    register_menu_frame,
    text="Student Registration",
    width=320,
    height=50,
    command=lambda: show_frame(student_register_frame)
).pack(pady=20)

ctk.CTkButton(
    register_menu_frame,
    text="Faculty Registration",
    width=320,
    height=50,
    command=lambda: show_frame(faculty_register_frame)
).pack(pady=20)

# ================= STUDENT REGISTER =================

ctk.CTkButton(
    student_register_frame,
    text="Back",
    command=lambda: show_frame(register_menu_frame)
).pack(anchor="nw", padx=15, pady=15)

register_page(student_register_frame)

# ================= FACULTY REGISTER =================

ctk.CTkButton(
    faculty_register_frame,
    text="Back",
    command=lambda: show_frame(register_menu_frame)
).pack(anchor="nw", padx=15, pady=15)

ctk.CTkLabel(
    faculty_register_frame,
    text="Faculty Registration",
    font=("Segoe UI", 30, "bold")
).pack(pady=25)

form = ctk.CTkFrame(faculty_register_frame, corner_radius=16)
form.pack(pady=20, padx=20)

entries = {}

fields = [
    ("Faculty Name", "faculty"),
    ("Subject Name", "subject"),
    ("Subject Code", "code"),
    ("Create Password", "password"),
    ("Confirm Password", "confirm")
]

for label, key in fields:
    ctk.CTkLabel(form, text=label, font=("Segoe UI", 15, "bold")).pack(pady=(12,2))
    show = "*" if "password" in key or "confirm" in key else ""
    ent = ctk.CTkEntry(form, width=320, height=40, show=show)
    ent.pack(pady=5)
    entries[key] = ent

def register_faculty():
    faculty = entries["faculty"].get().strip()
    subject = entries["subject"].get().strip()
    code = entries["code"].get().strip()
    password = entries["password"].get().strip()
    confirm = entries["confirm"].get().strip()

    if not all([faculty, subject, code, password, confirm]):
        messagebox.showerror("Error", "All fields are required")
        return

    if password != confirm:
        messagebox.showerror("Error", "Passwords do not match")
        return

    df = pd.read_csv(FACULTY_FILE)

    if not df[df["Subject_Code"].astype(str) == code].empty:
        messagebox.showerror("Error", "Subject code already registered")
        return

    new_row = pd.DataFrame([{
        "Faculty_Name": faculty,
        "Subject_Name": subject,
        "Subject_Code": code,
        "Password": password
    }])

    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(FACULTY_FILE, index=False)

    messagebox.showinfo("Success", "Faculty Registered Successfully")

    for e in entries.values():
        e.delete(0, "end")

ctk.CTkButton(
    form,
    text="Register",
    width=250,
    height=45,
    command=register_faculty
).pack(pady=20)

# ================= ATTENDANCE PAGE =================

ctk.CTkButton(
    attendance_frame,
    text="Back",
    command=lambda: show_frame(dashboard_frame)
).pack(anchor="nw", padx=15, pady=15)

ctk.CTkLabel(
    attendance_frame,
    text="Start Attendance",
    font=("Segoe UI", 32, "bold")
).pack(pady=25)

attendance_card = ctk.CTkFrame(attendance_frame, corner_radius=16)
attendance_card.pack(pady=20)

ctk.CTkLabel(attendance_card, text="Subject Code").pack(pady=(20,5))
subject_entry = ctk.CTkEntry(attendance_card, width=300, height=40)
subject_entry.pack(pady=10)

ctk.CTkLabel(attendance_card, text="Faculty Password").pack(pady=(10,5))
password_entry = ctk.CTkEntry(attendance_card, width=300, height=40, show="*")
password_entry.pack(pady=10)

mode_var = tk.StringVar(value="Face")

ctk.CTkRadioButton(
    attendance_card,
    text="Face Recognition",
    variable=mode_var,
    value="Face"
).pack(pady=10)

ctk.CTkRadioButton(
    attendance_card,
    text="QR Attendance",
    variable=mode_var,
    value="QR"
).pack(pady=10)

def verify_faculty(code, password):
    if not os.path.exists(FACULTY_FILE):
        return False

    df = pd.read_csv(FACULTY_FILE)

    match = df[
        (df["Subject_Code"].astype(str).str.strip() == code) &
        (df["Password"].astype(str).str.strip() == password)
    ]

    return not match.empty

def start_selected_attendance():
    code = subject_entry.get().strip()
    password = password_entry.get().strip()

    if not code or not password:
        messagebox.showerror("Error", "Enter subject code and password")
        return

    if not verify_faculty(code, password):
        messagebox.showerror("Error", "Invalid faculty credentials")
        return

    mode = mode_var.get()

    if mode == "Face":
        start_face_attendance(code)
    else:
        start_qr_attendance(code)

ctk.CTkButton(
    attendance_card,
    text="Start Attendance",
    width=300,
    height=45,
    command=start_selected_attendance
).pack(pady=25)

# ================= VIEW ATTENDANCE =================

ctk.CTkButton(
    view_frame,
    text="Back",
    command=lambda: show_frame(dashboard_frame)
).pack(anchor="nw", padx=15, pady=15)

view_attendance_page(view_frame)

# ================= VIEW QR =================

ctk.CTkButton(
    qr_frame,
    text="Back",
    command=lambda: show_frame(dashboard_frame)
).pack(anchor="nw", padx=15, pady=15)

view_qr_page(qr_frame)

show_frame(dashboard_frame)
root.mainloop()
