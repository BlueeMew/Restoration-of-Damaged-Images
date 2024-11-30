from PIL import Image, ImageTk
from tkinter import Label
import tkinter as tk
import cv2

imgLabelOriginal = None
imgLabelProcessed = None

def resize_image(image):
    return cv2.resize(image, (350, 400))        #resize image to 350 x 400

def showImage(image, title, isOriginal=False):
    global imgLabelOriginal, imgLabelProcessed

    imgpil = Image.fromarray(image)
    imgfin = ImageTk.PhotoImage(imgpil)

    if isOriginal:
        if imgLabelOriginal is None:
            imgLabelOriginal = Label(image=imgfin)
            imgLabelOriginal.image = imgfin
            imgLabelOriginal.pack(side=tk.LEFT, padx=10, pady=10)
        else:
            imgLabelOriginal.config(image=imgfin)
            imgLabelOriginal.image = imgfin
    else:
        if imgLabelProcessed is None:
            imgLabelProcessed = Label(image=imgfin)
            imgLabelProcessed.image = imgfin
            imgLabelProcessed.pack(side=tk.RIGHT, padx=10, pady=10)
        else:
            imgLabelProcessed.config(image=imgfin)
            imgLabelProcessed.image = imgfin