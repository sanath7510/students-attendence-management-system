from background import set_background
import customtkinter as ctk
import pandas as pd
import os
import cv2
import qrcode
import uuid

from main import train_model

# ================= FILE SETUP =================

students_file = "students.csv"

if not os.path.exists(students_file):

    pd.DataFrame(columns=[
        "USN",
        "Name",
        "Semester",
        "Course",
        "Subject",
        "SubjectCode"
    ]).to_csv(students_file, index=False)

# ================= FACE CAPTURE =================

def capture_faces(usn):

    os.makedirs(f"students/{usn}", exist_ok=True)

    cap = cv2.VideoCapture(
        0,
        cv2.CAP_DSHOW
    )

    if not cap.isOpened():

        print("Camera not accessible")
        return

    cap.set(3, 1280)
    cap.set(4, 720)

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = detector.detectMultiScale(
            gray,
            1.3,
            5
        )

        for (x, y, w, h) in faces:

            face = gray[y:y+h, x:x+w]

            face = cv2.resize(
                face,
                (200, 200)
            )

            count += 1

            cv2.imwrite(
                f"students/{usn}/{count}.jpg",
                face
            )

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Capturing {count}/50",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        cv2.imshow(
            "Registration Camera",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 50:
            break

    cap.release()

    cv2.destroyAllWindows()

# ================= QR GENERATION =================

def generate_student_qr(usn, name):

    unique_id = str(uuid.uuid4())[:8]

    qr_data = f"{usn}|{name}|{unique_id}"

    folder_name = f"{name}_{usn}"

    student_folder = os.path.join(
        "qr_codes",
        folder_name
    )

    os.makedirs(
        student_folder,
        exist_ok=True
    )

    qr_path = os.path.join(
        student_folder,
        "qr.png"
    )

    qr = qrcode.make(qr_data)

    qr.save(qr_path)

    print(f"QR Saved: {qr_path}")

# ================= REGISTRATION PAGE =================

def register_page(parent):

    # ===== MAIN SCROLLABLE PAGE =====

    main_scroll = ctk.CTkScrollableFrame(
        parent,
        width=1000,
        height=700
    )

    main_scroll.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    # ===== TITLE =====

    ctk.CTkLabel(
        main_scroll,
        text="Student Registration",
        font=("Arial", 32, "bold")
    ).pack(pady=20)

    # ===== NAME =====

    name_entry = ctk.CTkEntry(
        main_scroll,
        width=400,
        placeholder_text="Student Name"
    )

    name_entry.pack(pady=10)

    # ===== USN =====

    usn_entry = ctk.CTkEntry(
        main_scroll,
        width=400,
        placeholder_text="USN"
    )

    usn_entry.pack(pady=10)

    # ===== COURSE =====

    course_entry = ctk.CTkEntry(
        main_scroll,
        width=400,
        placeholder_text="Course"
    )

    course_entry.pack(pady=10)

    # ===== SEMESTER =====

    ctk.CTkLabel(
        main_scroll,
        text="Semester",
        font=("Arial", 16)
    ).pack(pady=5)

    sem_dropdown = ctk.CTkOptionMenu(
        main_scroll,
        values=[
            "1", "2", "3", "4",
            "5", "6", "7", "8"
        ],
        width=150
    )

    sem_dropdown.pack(pady=10)

    # ===== SUBJECT COUNT =====

    ctk.CTkLabel(
        main_scroll,
        text="Number of Subjects",
        font=("Arial", 16)
    ).pack(pady=5)

    subject_entries = []

    subjects_frame = ctk.CTkScrollableFrame(
        main_scroll,
        width=750,
        height=350
    )

    subjects_frame.pack(pady=15)

    def generate_subject_fields(count):

        subject_entries.clear()

        for widget in subjects_frame.winfo_children():
            widget.destroy()

        for i in range(count):

            subject_entry = ctk.CTkEntry(
                subjects_frame,
                width=300,
                placeholder_text=f"Subject {i+1}"
            )

            subject_entry.grid(
                row=i,
                column=0,
                padx=10,
                pady=8
            )

            code_entry = ctk.CTkEntry(
                subjects_frame,
                width=300,
                placeholder_text=f"Subject Code {i+1}"
            )

            code_entry.grid(
                row=i,
                column=1,
                padx=10,
                pady=8
            )

            subject_entries.append(
                (subject_entry, code_entry)
            )

    count_dropdown = ctk.CTkOptionMenu(
        main_scroll,
        values=[
            "1", "2", "3", "4",
            "5", "6", "7", "8"
        ],
        width=150,
        command=lambda x: generate_subject_fields(int(x))
    )

    count_dropdown.pack(pady=10)

    generate_subject_fields(1)

    # ===== STATUS =====

    status_label = ctk.CTkLabel(
        main_scroll,
        text="",
        font=("Arial", 16)
    )

    status_label.pack(pady=15)

    # ================= REGISTER FUNCTION =================

    def register_student():

        name = name_entry.get().strip()

        usn = usn_entry.get().strip()

        course = course_entry.get().strip()

        semester = sem_dropdown.get()

        if not name or not usn or not course:

            status_label.configure(
                text="Please fill all fields",
                text_color="red"
            )

            return

        df = pd.read_csv(students_file)

        for subject_entry, code_entry in subject_entries:

            subject = subject_entry.get().strip()

            code = code_entry.get().strip()

            if not subject or not code:
                continue

            exists = (
                (df["USN"] == usn) &
                (df["SubjectCode"] == code)
            ).any()

            if not exists:

                new_row = {
                    "USN": usn,
                    "Name": name,
                    "Semester": semester,
                    "Course": course,
                    "Subject": subject,
                    "SubjectCode": code
                }

                df = pd.concat(
                    [df, pd.DataFrame([new_row])],
                    ignore_index=True
                )

        df.to_csv(
            students_file,
            index=False
        )

        # ===== OPEN CAMERA =====

        status_label.configure(
            text="Opening Camera...",
            text_color="yellow"
        )

        parent.update()

        capture_faces(usn)

        # ===== QR GENERATION =====

        generate_student_qr(
            usn,
            name
        )

        # ===== TRAIN MODEL =====

        train_model()

        # ===== SUCCESS =====

        status_label.configure(
            text="Registration Successful",
            text_color="green"
        )

        # ===== CLEAR FIELDS =====

        name_entry.delete(0, "end")

        usn_entry.delete(0, "end")

        course_entry.delete(0, "end")

    # ================= REGISTER BUTTON =================

    ctk.CTkButton(
        main_scroll,
        text="Register Student",
        width=350,
        height=50,
        command=register_student
    ).pack(pady=25)