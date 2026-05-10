
import customtkinter as ctk
import pandas as pd
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import os

ATTENDANCE_FILE = "attendance.csv"

def ensure_file():

    if not os.path.exists(ATTENDANCE_FILE):

        pd.DataFrame(columns=[
            "USN",
            "Name",
            "Subject",
            "SubjectCode",
            "Date",
            "Time",
            "Status"
        ]).to_csv(ATTENDANCE_FILE, index=False)

def mark_present(usn, name, subject, subject_code):

    ensure_file()

    df = pd.read_csv(ATTENDANCE_FILE)

    today = datetime.now().strftime("%Y-%m-%d")

    mask = (
        (df["USN"] == usn) &
        (df["Date"] == today) &
        (df["SubjectCode"] == subject_code)
    )

    df.loc[mask, "Status"] = "Present"

    df.to_csv(ATTENDANCE_FILE, index=False)

def create_absent_records(subject_code):

    ensure_file()

    students_df = pd.read_csv("students.csv")

    students_df = students_df[
        students_df["SubjectCode"] == subject_code
    ]

    df = pd.read_csv(ATTENDANCE_FILE)

    today = datetime.now().strftime("%Y-%m-%d")

    for _, student in students_df.iterrows():

        exists = (
            (df["USN"] == student["USN"]) &
            (df["Date"] == today) &
            (df["SubjectCode"] == subject_code)
        ).any()

        if not exists:

            new_row = {
                "USN": student["USN"],
                "Name": student["Name"],
                "Subject": student["Subject"],
                "SubjectCode": student["SubjectCode"],
                "Date": today,
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Status": "Absent"
            }

            df = pd.concat(
                [df, pd.DataFrame([new_row])],
                ignore_index=True
            )

    df.to_csv(ATTENDANCE_FILE, index=False)

def view_attendance_page(parent):

    ctk.CTkLabel(
        parent,
        text="Attendance Reports",
        font=("Arial", 28, "bold")
    ).pack(pady=20)

    filter_frame = ctk.CTkFrame(parent)

    filter_frame.pack(pady=20)

    date_picker = DateEntry(
        filter_frame,
        date_pattern='yyyy-mm-dd'
    )

    date_picker.grid(row=0, column=0, padx=10)

    try:

        df = pd.read_csv(ATTENDANCE_FILE)

        subjects = sorted(
            df["SubjectCode"]
            .dropna()
            .unique()
            .tolist()
        )

    except:
        subjects = []

    subject_var = ctk.StringVar()

    dropdown = ttk.Combobox(
        filter_frame,
        textvariable=subject_var,
        values=subjects,
        state="readonly",
        width=30
    )

    dropdown.grid(row=0, column=1, padx=10)

    tree = ttk.Treeview(parent)

    cols = [
        "USN",
        "Name",
        "Subject",
        "SubjectCode",
        "Date",
        "Time",
        "Status"
    ]

    tree["columns"] = cols

    tree["show"] = "headings"

    for col in cols:

        tree.heading(col, text=col)

        tree.column(col, width=140)

    tree.pack(fill="both", expand=True, padx=20, pady=20)

    def load_data(data):

        tree.delete(*tree.get_children())

        for _, row in data.iterrows():

            tree.insert("", "end", values=list(row))

    def search():

        if not os.path.exists(ATTENDANCE_FILE):
            return

        df = pd.read_csv(ATTENDANCE_FILE)

        selected_date = date_picker.get()

        selected_subject = subject_var.get()

        filtered = df[
            (df["Date"].astype(str) == selected_date) &
            (df["SubjectCode"].astype(str) == selected_subject)
        ]

        load_data(filtered)

    ctk.CTkButton(
        filter_frame,
        text="Search",
        command=search
    ).grid(row=0, column=2, padx=10)
