from background import set_background

import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ATTENDANCE_FILE = "attendance.csv"

def open_statistics_page(parent):

    for widget in parent.winfo_children():
        widget.destroy()

    title = ctk.CTkLabel(
        parent,
        text="Attendance Statistical View",
        font=("Arial", 30, "bold")
    )

    title.pack(pady=20)

    usn_entry = ctk.CTkEntry(
        parent,
        width=350,
        height=45,
        placeholder_text="Enter Student USN"
    )

    usn_entry.pack(pady=15)

    result_label = ctk.CTkLabel(
        parent,
        text="Enter USN to View Statistics",
        font=("Arial", 16)
    )

    result_label.pack(pady=10)

    chart_frame = ctk.CTkFrame(parent)
    chart_frame.pack(pady=20, fill="both", expand=True)

    def show_statistics():

        for widget in chart_frame.winfo_children():
            widget.destroy()

        usn = usn_entry.get().strip()

        if usn == "":
            result_label.configure(
                text="Please Enter USN",
                text_color="orange"
            )
            return

        try:
            df = pd.read_csv(ATTENDANCE_FILE)

        except:
            result_label.configure(
                text="Attendance File Not Found",
                text_color="red"
            )
            return

        if "USN" not in df.columns:
            result_label.configure(
                text="Invalid Attendance File",
                text_color="red"
            )
            return

        student_df = df[df["USN"].astype(str).str.lower() == usn.lower()]

        if student_df.empty:
            result_label.configure(
                text="USN Not Found",
                text_color="red"
            )
            return

        total = len(student_df)

        present = len(student_df[
            student_df["Status"].astype(str).str.lower() == "present"
        ])

        absent = total - present

        attendance_percentage = (present / total) * 100

        result_label.configure(
            text=f"Attendance Percentage: {attendance_percentage:.2f}%",
            text_color="green"
        )

        fig, ax = plt.subplots(figsize=(4, 4))

        ax.pie(
            [present, absent],
            labels=["Present", "Absent"],
            autopct='%1.1f%%'
        )

        ax.set_title("Attendance Statistics")

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    ctk.CTkButton(
        parent,
        text="Show Statistics",
        width=250,
        height=45,
        command=show_statistics
    ).pack(pady=15)

open_statistics_window = open_statistics_page
