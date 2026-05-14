from background import set_background

import customtkinter as ctk
from PIL import Image
import os

def view_qr_page(parent):

    ctk.CTkLabel(
        parent,
        text="View Student QR",
        font=("Arial", 30, "bold")
    ).pack(pady=20)

    usn_entry = ctk.CTkEntry(
        parent,
        width=350,
        height=45,
        placeholder_text="Enter USN"
    )

    usn_entry.pack(pady=15)

    image_label = ctk.CTkLabel(
        parent,
        text="QR will appear after entering USN",
        font=("Arial", 16)
    )

    image_label.pack(pady=20)

    status_label = ctk.CTkLabel(
        parent,
        text="",
        font=("Arial", 15)
    )

    status_label.pack(pady=10)

    def show_qr():

        usn = usn_entry.get().strip()

        # Prevent QR display without USN
        if usn == "":
            image_label.configure(
                image=None,
                text="Please Enter USN First"
            )

            status_label.configure(
                text="Enter USN",
                text_color="orange"
            )

            return

        qr_folder = "qr_codes"

        found = False

        if not os.path.exists(qr_folder):

            status_label.configure(
                text="QR folder not found",
                text_color="red"
            )

            return

        for folder in os.listdir(qr_folder):

            if usn.lower() in folder.lower():

                qr_path = os.path.join(
                    qr_folder,
                    folder,
                    "qr.png"
                )

                if os.path.exists(qr_path):

                    image = Image.open(qr_path)

                    qr_image = ctk.CTkImage(
                        light_image=image,
                        dark_image=image,
                        size=(300, 300)
                    )

                    image_label.configure(
                        image=qr_image,
                        text=""
                    )

                    image_label.image = qr_image

                    status_label.configure(
                        text="QR Found Successfully",
                        text_color="green"
                    )

                    found = True
                    break

        if not found:

            image_label.configure(
                image=None,
                text="No QR Available"
            )

            status_label.configure(
                text="USN Not Found",
                text_color="red"
            )

    ctk.CTkButton(
        parent,
        text="Show QR",
        width=250,
        height=45,
        command=show_qr
    ).pack(pady=15)
