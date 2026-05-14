from background import set_background
import cv2
import numpy as np
import os
import pandas as pd

from attendance import (
    mark_present,
    create_absent_records
)

# ================= QR DETECTOR =================

qr_detector = cv2.QRCodeDetector()

# ================= TRAIN MODEL =================

def train_model():

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces = []
    labels = []

    label_map = {}

    current_id = 0

    if not os.path.exists("students"):
        return

    for folder in os.listdir("students"):

        path = os.path.join("students", folder)

        if not os.path.isdir(path):
            continue

        label_map[current_id] = folder

        for img_name in os.listdir(path):

            img_path = os.path.join(path, img_name)

            img = cv2.imread(
                img_path,
                cv2.IMREAD_GRAYSCALE
            )

            if img is not None:

                faces.append(img)

                labels.append(current_id)

        current_id += 1

    if len(faces) == 0:
        return

    recognizer.train(
        faces,
        np.array(labels)
    )

    os.makedirs("trainer", exist_ok=True)

    recognizer.save(
        "trainer/trainer.yml"
    )

    np.save(
        "trainer/labels.npy",
        label_map
    )

# ================= QR SCAN =================

def scan_qr(frame):

    data, bbox, _ = qr_detector.detectAndDecode(frame)

    if data:
        return data

    return None

# ================= CAMERA AUTO DETECT =================

def get_camera():

    cap = None

    for i in range(3):

        camera = cv2.VideoCapture(
            i,
            cv2.CAP_DSHOW
        )

        if camera.isOpened():

            cap = camera

            print(f"Camera {i} connected")

            break

    if cap is None:

        print("No camera detected")

        return None

    cap.set(3, 1280)
    cap.set(4, 720)

    return cap

# ================= FACE ATTENDANCE =================

def start_face_attendance(subject_code):

    create_absent_records(subject_code)

    if not os.path.exists("trainer/trainer.yml"):

        print("Trainer model not found")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    recognizer.read("trainer/trainer.yml")

    labels = np.load(
        "trainer/labels.npy",
        allow_pickle=True
    ).item()

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    students_df = pd.read_csv("students.csv")

    cap = get_camera()

    if cap is None:
        return

    marked_students = set()

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

            try:

                label_id, confidence = recognizer.predict(face)

            except:
                continue

            if confidence < 70:

                usn = labels[label_id]

                student = students_df[
                    (students_df["USN"] == usn) &
                    (
                        students_df["SubjectCode"]
                        == subject_code
                    )
                ]

                if not student.empty:

                    row = student.iloc[0]

                    if usn not in marked_students:

                        mark_present(
                            usn,
                            row["Name"],
                            row["Subject"],
                            subject_code
                        )

                        marked_students.add(usn)

                    text = f"{usn} Verified"

                    color = (0, 255, 0)

                else:

                    text = "Wrong Subject"

                    color = (0, 165, 255)

            else:

                text = "Unknown"

                color = (0, 0, 255)

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                color,
                2
            )

            cv2.putText(
                frame,
                text,
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )

        cv2.imshow(
            "Face Attendance",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        # Close on Q or ENTER
        if key == ord('q') or key == 13:
            break

    cap.release()

    cv2.destroyAllWindows()

# ================= QR ATTENDANCE =================

def start_qr_attendance(subject_code):

    create_absent_records(subject_code)

    students_df = pd.read_csv("students.csv")

    cap = get_camera()

    if cap is None:
        return

    marked_students = set()

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        qr_data = scan_qr(frame)

        if qr_data:

            try:

                qr_parts = qr_data.split("|")

                usn = qr_parts[0]

                student = students_df[
                    (students_df["USN"] == usn) &
                    (
                        students_df["SubjectCode"]
                        == subject_code
                    )
                ]

                if not student.empty:

                    row = student.iloc[0]

                    if usn not in marked_students:

                        mark_present(
                            usn,
                            row["Name"],
                            row["Subject"],
                            subject_code
                        )

                        marked_students.add(usn)

                    text = f"{usn} QR Verified"

                    color = (0, 255, 0)

                else:

                    text = "Wrong Subject"

                    color = (0, 165, 255)

            except:

                text = "Invalid QR"

                color = (0, 0, 255)

            cv2.putText(
                frame,
                text,
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                color,
                3
            )

        cv2.imshow(
            "QR Attendance",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        # Close on Q or ENTER
        if key == ord('q') or key == 13:
            break

    cap.release()

    cv2.destroyAllWindows()