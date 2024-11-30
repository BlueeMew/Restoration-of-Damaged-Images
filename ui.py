from tkinter import Button, Label, filedialog, messagebox
import tkinter as tk
from image_processing import *
from utils import showImage
import cv2
from masking import *
from fold_removal import *

def openImage():
    path = filedialog.askopenfilename(filetypes=[("Image files","*.jpg *.jpeg *.png")]) #can only open files of type .jpg,.jpeg,.png
    originalImage = cv2.imread(path,cv2.IMREAD_GRAYSCALE) #reading the file as grayscale
    originalImage=cv2.resize(originalImage, (350, 400))
    processedImage = originalImage.copy()
    showImage(originalImage, "Original Image", isOriginal=True) #Displaying original image
    showImage(processedImage, "Processed Image", isOriginal=False) #Displaying processed image
    return originalImage, processedImage

def resetImage(originalImage):
    processedImage = originalImage.copy() #copying the original image to processed image to reset it
    showImage(originalImage,"Original Image",isOriginal=True)
    showImage(processedImage,"Processed Image",isOriginal=False)
    return processedImage

def saveImage(processedImage):
    path = filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG files", "*.png"),("JPEG files", "*.jpg"),("All files", "*.*"),],) #path to save the image
    cv2.imwrite(path,processedImage)

def initializeUi(root, originalImage, processedImage,  Width, Height):      #calling the imported and present functions to use when clicked on buttons
    Image_stack=[]          #stack for saving all instances so that we can undo an operation
    def save_state(img):
        Image_stack.append(img.copy())

    def onUpload():
        nonlocal originalImage, processedImage
        originalImage, processedImage = openImage()
        save_state(processedImage)
    def onReset():
        nonlocal processedImage
        processedImage = resetImage(originalImage)
        save_state(processedImage)
    def onHistogramEQ():
        nonlocal processedImage
        processedImage = applyHistogramEqualization(processedImage)
        showImage(processedImage, "Processed Image",isOriginal=False)
        save_state(processedImage)
    def onUnsharp():
        nonlocal processedImage
        processedImage = applyUnsharpMasking(processedImage)
        showImage(processedImage, "Processed Image",  isOriginal=False)
        save_state(processedImage)
    def onGamma():
        nonlocal processedImage
        processedImage = adjustBrightnessGamma(processedImage)
        showImage(processedImage, "Processed Image", isOriginal=False)
        save_state(processedImage)
    def onSave():
        saveImage(processedImage)
    def onStainInpaint():
        nonlocal processedImage
        processedImage, extra = stain_removal(processedImage)
        showImage(processedImage, "Processed Image", isOriginal=False)
        save_state(processedImage)
    def onStainGradFill():
        nonlocal processedImage
        extra, processedImage = stain_removal(processedImage)
        showImage(processedImage, "Processed Image", isOriginal=False)
        save_state(processedImage)
    def onMedianBlur():
        nonlocal processedImage 
        processedImage = median_blur(processedImage)                        #using inbuilt median blur 
        processedImage=cv2.cvtColor(processedImage,cv2.COLOR_BGR2GRAY)      #converting image to gray scale
        showImage(processedImage, "Processed Image", isOriginal=False)
        save_state(processedImage)
    def onRemoveFold():
        nonlocal processedImage
        processedImage = Nofold(processedImage)
        showImage(processedImage, "Processed Image", isOriginal=False)
        save_state(processedImage)
    def onUndo():
        nonlocal processedImage  
        if(len(Image_stack)>=1):
            processedImage = Image_stack.pop()
        else: messagebox.showwarning("Warning","No more undos left")
        showImage(processedImage, "Processed Image",isOriginal=False)
    #buttons for each function
    Button(root,text="Upload Image",command=onUpload).pack(pady=5)
    Button(root,text="Median Filter",command=onMedianBlur).pack(pady=5)
    Button(root,text="stain removal using inbuilt function",command=onStainInpaint).pack(pady=5)
    Button(root,text="stain removal using custom method",command=onStainGradFill).pack(pady=5)
    Button(root,text="Remove Folds",command=onRemoveFold).pack(pady=5)
    Button(root,text="Undo",command=onUndo).pack(pady=5)
    Button(root,text="Reset Image",command=onReset).pack(pady=5)
    Button(root,text="Save Image",command=onSave).pack(pady=5)
    Button(root,text="Histogram Equalization",command=onHistogramEQ).pack(pady=10,padx=10,side=tk.LEFT)
    Button(root,text="Unsharp Masking",command=onUnsharp).pack(pady=10,padx=10,side=tk.LEFT)
    Button(root,text="Brightness & Gamma Correction", command=onGamma).pack(pady=10,padx=10,side=tk.LEFT)