
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def open_statistics_window(tree):

    try:

        rows = tree.get_children()

        if not rows:
            messagebox.showinfo(
                "No Data",
                "No attendance data found"
            )
            return

        names = []

        for row in rows:

            values = tree.item(row)["values"]

            if len(values) > 1:
                names.append(str(values[1]))

        if not names:
            messagebox.showinfo(
                "No Data",
                "No valid attendance records"
            )
            return

        df = pd.DataFrame(names, columns=["Name"])

        attendance_summary = (
            df.groupby("Name")
            .size()
            .reset_index(name="Present_Count")
        )

        total = attendance_summary["Present_Count"].sum()

        attendance_summary["Attendance_Percentage"] = (
            attendance_summary["Present_Count"] / total
        ) * 100

        stats_window = tk.Toplevel()

        stats_window.title(
            "Attendance Statistical View"
        )

        stats_window.geometry("950x700")

        title = tk.Label(
            stats_window,
            text="Attendance Analytics",
            font=("Arial", 18, "bold")
        )

        title.pack(pady=10)

        treeview = ttk.Treeview(
            stats_window,
            columns=(
                "Name",
                "Present_Count",
                "Attendance_Percentage"
            ),
            show="headings",
            height=8
        )

        treeview.heading("Name", text="Student Name")
        treeview.heading("Present_Count", text="Present Count")
        treeview.heading("Attendance_Percentage", text="Attendance %")

        treeview.column("Name", width=250)
        treeview.column("Present_Count", width=150)
        treeview.column("Attendance_Percentage", width=150)

        treeview.pack(fill="x", padx=10, pady=10)

        for _, row in attendance_summary.iterrows():

            treeview.insert(
                "",
                "end",
                values=(
                    row["Name"],
                    row["Present_Count"],
                    f"{round(row['Attendance_Percentage'],2)}%"
                )
            )

        fig, ax = plt.subplots(figsize=(6,6))

        ax.pie(
            attendance_summary["Present_Count"],
            labels=attendance_summary["Name"],
            autopct='%1.1f%%'
        )

        ax.set_title("Attendance Distribution")

        canvas = FigureCanvasTkAgg(
            fig,
            master=stats_window
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    except Exception as e:

        messagebox.showerror(
            "Statistics Error",
            str(e)
        )
