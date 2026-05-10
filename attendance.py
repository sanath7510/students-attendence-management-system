from attendance_statistics import open_statistics_window
import customtkinter as ctk
import pandas as pd
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import os
import webbrowser
import urllib.parse
from tkinter import filedialog, simpledialog, messagebox

ATTENDANCE_FILE = "attendance.csv"


# ================= FILE SETUP =================

def ensure_file():

    if not os.path.exists(ATTENDANCE_FILE):

        pd.DataFrame(columns=[
            "USN",
            "Name",
            "Course",
            "Subject",
            "SubjectCode",
            "Date",
            "Time",
            "Status"
        ]).to_csv(ATTENDANCE_FILE, index=False)


# ================= MARK PRESENT =================

def mark_present(usn, name, subject, subject_code):

    ensure_file()

    df = pd.read_csv(ATTENDANCE_FILE)

    today = datetime.now().strftime("%Y-%m-%d")

    current_time = datetime.now().strftime("%H:%M:%S")

    # ================= CHECK EXISTING RECORD =================

    mask = (
        (df["USN"].astype(str) == str(usn)) &
        (df["Date"].astype(str) == today) &
        (df["SubjectCode"].astype(str) == str(subject_code))
    )

    # ================= UPDATE ABSENT -> PRESENT =================

    if mask.any():

        df.loc[mask, "Status"] = "Present"

        df.loc[mask, "Time"] = current_time

    else:

        # ================= GET COURSE =================

        try:

            students_df = pd.read_csv("students.csv")

            student = students_df[
                students_df["USN"].astype(str)
                == str(usn)
            ]

            if not student.empty:

                course = student.iloc[0].get(
                    "Course",
                    ""
                )

            else:

                course = ""

        except:

            course = ""

        # ================= CREATE PRESENT RECORD =================

        new_row = {
            "USN": usn,
            "Name": name,
            "Course": course,
            "Subject": subject,
            "SubjectCode": subject_code,
            "Date": today,
            "Time": current_time,
            "Status": "Present"
        }

        df = pd.concat(
            [df, pd.DataFrame([new_row])],
            ignore_index=True
        )

    # ================= SAVE FILE =================

    df.to_csv(
        ATTENDANCE_FILE,
        index=False
    )


# ================= CREATE ABSENT RECORDS =================

def create_absent_records(subject_code):

    ensure_file()

    # ================= CHECK STUDENTS FILE =================

    if not os.path.exists("students.csv"):

        print("students.csv not found")
        return

    students_df = pd.read_csv("students.csv")

    if students_df.empty:

        print("No students registered")
        return

    # ================= LOAD ATTENDANCE =================

    df = pd.read_csv(ATTENDANCE_FILE)

    today = datetime.now().strftime("%Y-%m-%d")

    current_time = datetime.now().strftime("%H:%M:%S")

    records_added = 0

    # ================= LOOP THROUGH STUDENTS =================

    for _, student in students_df.iterrows():

        try:

            student_subject = str(
                student["SubjectCode"]
            ).strip()

            # Match selected subject
            if student_subject != str(subject_code).strip():
                continue

            usn = str(student["USN"]).strip()

            # ================= CHECK EXISTING RECORD =================

            exists = (
                (df["USN"].astype(str).str.strip() == usn) &
                (df["Date"].astype(str).str.strip() == today) &
                (
                    df["SubjectCode"]
                    .astype(str)
                    .str.strip()
                    == str(subject_code).strip()
                )
            ).any()

            # ================= CREATE ABSENT ENTRY =================

            if not exists:

                new_row = {
                    "USN": student["USN"],
                    "Name": student["Name"],
                    "Course": student.get("Course", ""),
                    "Subject": student["Subject"],
                    "SubjectCode": student["SubjectCode"],
                    "Date": today,
                    "Time": current_time,
                    "Status": "Absent"
                }

                df = pd.concat(
                    [df, pd.DataFrame([new_row])],
                    ignore_index=True
                )

                records_added += 1

        except Exception as e:

            print("Error:", e)

    # ================= SAVE FILE =================

    df.to_csv(
        ATTENDANCE_FILE,
        index=False
    )

    print(
        f"{records_added} absent records created"
    )

# ================= EXPORT CSV VIA WHATSAPP =================

def export_via_whatsapp(course_combobox):

    try:

        import pywhatkit
        import pyautogui
        import pyperclip
        import time

        receiver_number = simpledialog.askstring(
            "Receiver Number",
            "Enter WhatsApp Number\nExample: +919876543210"
        )

        if not receiver_number:
            return

        df = pd.read_csv(ATTENDANCE_FILE)

        selected_course = (
            course_combobox.get()
            .strip()
        )

        # ================= COURSE FILTER =================

        if (
            selected_course != "Select Course"
            and selected_course != ""
            and "Course" in df.columns
        ):

            df = df[
                df["Course"]
                .astype(str)
                .str.strip()
                .str.upper()
                ==
                selected_course.upper()
            ]

        # ================= EMPTY CHECK =================

        if df.empty:

            messagebox.showwarning(
                "No Data",
                "No attendance records found."
            )

            return

        # ================= SAVE CSV =================

        export_path = os.path.abspath(
            "Attendance_Report.csv"
        )

        df.to_csv(
            export_path,
            index=False
        )

        # ================= OPEN WHATSAPP =================

        pywhatkit.sendwhatmsg_instantly(
            receiver_number,
            "Attendance Report",
            wait_time=15,
            tab_close=False
        )

        # Wait for WhatsApp Web
        time.sleep(10)

        # ================= OPEN ATTACHMENT =================

        pyautogui.hotkey(
            "ctrl",
            "alt",
            "shift",
            "h"
        )

        time.sleep(3)

        # ================= PASTE FILE PATH =================

        pyperclip.copy(export_path)

        pyautogui.hotkey(
            "ctrl",
            "v"
        )

        time.sleep(2)

        pyautogui.press("enter")

        time.sleep(3)

        # ================= SEND FILE =================

        pyautogui.press("enter")

        messagebox.showinfo(
            "Success",
            "CSV File Sent Successfully"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

        # ================= COURSE FILTER =================

        if (
            selected_course != "Select Course"
            and selected_course != ""
            and "Course" in df.columns
        ):

            df = df[
                df["Course"]
                .astype(str)
                .str.strip()
                .str.upper()
                ==
                selected_course.upper()
            ]

        # ================= CHECK EMPTY =================

        if df.empty:

            messagebox.showwarning(
                "No Data",
                "No attendance records found."
            )

            return

        # ================= SAVE CSV =================

        export_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV Files", "*.csv")
            ],
            initialfile="Attendance_Report.csv"
        )

        if not export_path:

            return

        df.to_csv(
            export_path,
            index=False
        )

        # ================= OPEN WHATSAPP =================

        message = urllib.parse.quote(
            "Attendance CSV exported successfully."
        )

        whatsapp_url = (
            f"https://wa.me/{receiver_number}?text={message}"
        )

        webbrowser.open(
            whatsapp_url
        )

        # ================= SUCCESS =================

        messagebox.showinfo(
            "Success",
            "CSV Exported Successfully"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )
# ================= VIEW ATTENDANCE PAGE =================

def view_attendance_page(parent):

    ensure_file()

    ctk.CTkLabel(
        parent,
        text="Attendance Reports",
        font=("Arial", 28, "bold")
    ).pack(pady=20)

    # ================= FILTER FRAME =================

    filter_frame = ctk.CTkFrame(parent)

    filter_frame.pack(pady=20)

    # ================= DATE =================

    date_picker = DateEntry(
        filter_frame,
        date_pattern='yyyy-mm-dd'
    )

    date_picker.grid(
        row=0,
        column=0,
        padx=10
    )

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
                "Subject Dropdown Error:",
                e
            )

            return []

    subjects = load_subjects()

    dropdown = ttk.Combobox(
        filter_frame,
        textvariable=subject_var,
        values=subjects,
        state="readonly",
        width=30
    )

    dropdown.grid(
        row=0,
        column=1,
        padx=10
    )

    # Auto select first subject
    if subjects:

        dropdown.current(0)

    # ================= COURSE FILTER =================

    course_combobox = ctk.CTkComboBox(
        filter_frame,
        values=[
            "MCA",
            "BCA",
            "BTech",
            "MTech"
        ],
        width=170
    )

    course_combobox.set(
        "Select Course"
    )

    course_combobox.grid(
        row=0,
        column=2,
        padx=10
    )

    # ================= TABLE =================

    tree = ttk.Treeview(parent)

    cols = [
        "USN",
        "Name",
        "Course",
        "Subject",
        "SubjectCode",
        "Date",
        "Time",
        "Status"
    ]

    tree["columns"] = cols

    tree["show"] = "headings"

    for col in cols:

        tree.heading(
            col,
            text=col
        )

        tree.column(
            col,
            width=140
        )

    tree.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    # ================= LOAD DATA =================

    def load_data(data):

        tree.delete(
            *tree.get_children()
        )

        for _, row in data.iterrows():

            tree.insert(
                "",
                "end",
                values=list(row)
            )

       # ================= SEARCH =================

    def search():

        if not os.path.exists(
            ATTENDANCE_FILE
        ):

            return

        df = pd.read_csv(
            ATTENDANCE_FILE
        )

        if df.empty:

            load_data(df)

            return

        # ================= CLEAN DATA =================

        df["Date"] = (
            df["Date"]
            .astype(str)
            .str.strip()
        )

        df["SubjectCode"] = (
            df["SubjectCode"]
            .astype(str)
            .str.strip()
        )

        if "Course" in df.columns:

            df["Course"] = (
                df["Course"]
                .astype(str)
                .str.strip()
            )

        selected_date = str(
            date_picker.get()
        ).strip()

        selected_subject = str(
            subject_var.get()
        ).strip()

        selected_course = str(
            course_combobox.get()
        ).strip()

        # ================= START WITH FULL DATA =================

        filtered = df.copy()

        # ================= DATE FILTER =================

        if selected_date:

            filtered = filtered[
                filtered["Date"]
                == selected_date
            ]

        # ================= SUBJECT FILTER =================

        if selected_subject:

            filtered = filtered[
                filtered["SubjectCode"]
                == selected_subject
            ]
        # ================= COURSE FILTER =================

        if (
            selected_course != "Select Course"
            and selected_course != ""
            and "Course" in filtered.columns
        ):

            filtered = filtered[
                filtered["Course"]
                .astype(str)
                .str.upper()
                ==
                selected_course.upper()
            ]

        # ================= LOAD TABLE =================

        load_data(filtered)

      # ================= BUTTONS =================

    ctk.CTkButton(
        filter_frame,
        text="Search",
        command=search
    ).grid(
        row=0,
        column=3,
        padx=10
    )

    ctk.CTkButton(
        filter_frame,
        text="Statistical View",
        width=170,
        height=40,
        fg_color="#1F6AA5",
        hover_color="#144870",
        command=lambda: open_statistics_window(tree)
    ).grid(
        row=0,
        column=4,
        padx=10
    )

    ctk.CTkButton(
        filter_frame,
        text="Export via WhatsApp",
        command=lambda:
        export_via_whatsapp(
            course_combobox
        )
    ).grid(
        row=0,
        column=5,
        padx=10
    )

    # ================= LOAD DATA INITIALLY =================

    search()