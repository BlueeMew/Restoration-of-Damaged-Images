from PIL import Image, ImageTk
from tkinter import Label
import tkinter as tk
import cv2

img_label_original = None
img_label_processed = None

def resize_image(image, max_width, max_height):
    return cv2.resize(image, (640, 640))

def showImage(image, title, window_width, window_height, isOriginal=False):
    global img_label_original, img_label_processed
    max_width, max_height = 300, 500

    img_pil = Image.fromarray(image)  # No need for RGB conversion for grayscale images
    img_tk = ImageTk.PhotoImage(img_pil)

    # Determine which label to update
    if isOriginal:
        if img_label_original is None:
            img_label_original = Label(image=img_tk)
            img_label_original.image = img_tk
            img_label_original.pack(side=tk.LEFT, padx=10, pady=10)
        else:
            img_label_original.config(image=img_tk)
            img_label_original.image = img_tk
    else:
        if img_label_processed is None:
            img_label_processed = Label(image=img_tk)
            img_label_processed.image = img_tk
            img_label_processed.pack(side=tk.RIGHT, padx=10, pady=10)
        else:
            img_label_processed.config(image=img_tk)
            img_label_processed.image = img_tk