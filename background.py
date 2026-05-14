from tkinter import *
from PIL import Image, ImageTk

def set_background(window, image_path="attendence.jpeg"):
    window.update()

    width = window.winfo_width()
    height = window.winfo_height()

    if width < 100:
        width = 1200
    if height < 100:
        height = 700

    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((width, height), Image.LANCZOS)

    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = Label(window, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    bg_label.lower()

    return bg_label
