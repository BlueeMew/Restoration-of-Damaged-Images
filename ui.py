from tkinter import Button, Label, filedialog
import tkinter as tk
from image_processing import *
from utils import showImage
import cv2
from masking import *
from fold_removal import *

def openImage(Width, Height):
    path = filedialog.askopenfilename(filetypes=[("Image files","*.jpg *.jpeg *.png")]) #can only open files of type .jpg,.jpeg,.png
    originalImage = cv2.imread(path,cv2.IMREAD_GRAYSCALE) #reading the file as grayscale
    originalImage=cv2.resize(originalImage, (450, 500))
    processedImage = originalImage.copy()
    showImage(originalImage, "Original Image", Width, Height, isOriginal=True) #Displaying original image
    showImage(processedImage, "Processed Image", Width, Height, isOriginal=False) #Displaying processed image
    return originalImage, processedImage

def resetImage(originalImage, Width, Height):
    processedImage = originalImage.copy() #copying the original image to processed image to reset it
    showImage(originalImage,"Original Image", Width, Height, isOriginal=True)
    showImage(processedImage,"Processed Image", Width, Height, isOriginal=False)
    return processedImage

def saveImage(processedImage):
    path = filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG files", "*.png"),("JPEG files", "*.jpg"),("All files", "*.*"),],) #path to save the image
    cv2.imwrite(path,processedImage)

def initializeUi(root, originalImage, processedImage,  Width, Height):
    def onUpload():
        nonlocal originalImage, processedImage
        originalImage, processedImage = openImage(Width, Height)
    def onReset():
        nonlocal processedImage
        processedImage = resetImage(originalImage, Width, Height)
    def onHistogramEQ():
        nonlocal processedImage
        processedImage = apply_histogram_equalization(processedImage, Width, Height)
        showImage(processedImage, "Processed Image", Width, Height, isOriginal=False)
    def onUnsharp():
        nonlocal processedImage
        processedImage = apply_unsharp_masking(processedImage, Width, Height)
        showImage(processedImage, "Processed Image", Width, Height, isOriginal=False)
    def onGamma():
        nonlocal processedImage
        processedImage = adjust_brightness_gamma(processedImage, Width, Height)
        showImage(processedImage, "Processed Image", Width, Height, isOriginal=False)
    def onSave():
        saveImage(processedImage)
    def onStain():
        nonlocal processedImage
        processedImage = stain_removal(processedImage)
        showImage(processedImage, "Processed Image", Width, Height, isOriginal=False)
    def onMedianBlur():
        nonlocal processedImage 
        processedImage = median_blur(processedImage)
        processedImage=cv2.cvtColor(processedImage,cv2.COLOR_BGR2GRAY)
        showImage(processedImage, "Processed Image", Width, Height, isOriginal=False)
    def onRemoveFold():
        nonlocal processedImage
        processedImage = Nofold(processedImage)
        showImage(processedImage, "Processed Image", Width, Height, isOriginal=False)

    #buttons for each function
    Button(root,text="Upload Image",command=onUpload).pack(pady=10)
    Button(root,text="Median Filter",command=onMedianBlur).pack(pady=10)
    Button(root,text="stain removal",command=onStain).pack(pady=10)
    Button(root,text="Remove Folds",command=onRemoveFold).pack(pady=10)
    Button(root,text="Reset Image",command=onReset).pack(pady=10)
    Button(root,text="Save Image",command=onSave).pack(pady=10)
    Button(root,text="Histogram Equalization",command=onHistogramEQ).pack(pady=10,padx=10,side=tk.LEFT)
    Button(root,text="Unsharp Masking",command=onUnsharp).pack(pady=10,padx=10,side=tk.LEFT)
    Button(root,text="Brightness & Gamma Correction", command=onGamma).pack(pady=10,padx=10,side=tk.LEFT)