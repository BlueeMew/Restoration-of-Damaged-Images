import cv2
import numpy as np
from utils import *

# Global variables
drawing = False  # True if mouse is pressed
ix, iy = -1, -1  # Initial mouse coordinates
brush_size = 10  # Initial brush size

#function for removing noise in an image
def median_blur(image):
    filtered_image = cv2.medianBlur(image, 5)  # Kernel size of 5
    return cv2.cvtColor(filtered_image, cv2.COLOR_GRAY2BGR)

#function for creating mask for the damaged part of image
def create_mask(image):
   
    binary_mask = np.zeros(image.shape[:2], dtype=np.uint8)
    red_pixels = (image[:, :, 2] == 255) & (image[:, :, 0] == 0) & (image[:, :, 1] == 0)
    binary_mask[red_pixels] = 255  # Set painted areas to white
    return binary_mask

#function for filling the masked parts

def inpaint_image(image, mask):
    
    return cv2.inpaint(image, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

#function for sharpening the image as initially we have blurred a little to remove noise

# def sharpen_image(image):
#     blurred = cv2.GaussianBlur(image, (9, 9), 2)
#     sharpened = cv2.addWeighted(image, 1.5, blurred, -0.5, 0)
#     return sharpened

#function for highlighting damages using the mouse

def highlight_damages(event, x, y, flags, param):
    global ix, iy, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(param, (ix, iy), (x, y), (0, 0, 255), brush_size)  # Paint red
            ix, iy = x, y 
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

def stain_removal(img):
    global brush_size  

    cv2.imshow('original-image',img)
    cv2.waitKey(0)
    if img is None:
        print("Error: Could not open or find the image.")
        return
    # resize_image(img,800,600)
    #  Remove noise
    #img = remove_noise(img)
    img=cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # Create a window for painting damages
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', highlight_damages, param=img)

    while True:

        img_copy = img.copy()
        if drawing: 
            cv2.circle(img_copy, (ix, iy), brush_size, (0, 255, 0), 1)
        
        cv2.imshow('Image', img_copy)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        if key == ord('+'):
            brush_size += 1
        elif key == ord('-') and brush_size > 1:
            brush_size -= 1

    # Generate mask and inpaint the image
    mask = create_mask(img)
    cv2.imshow('img-mask',mask)
    cv2.waitKey(0)
    inpainted_image = inpaint_image(img, mask)

    #  Sharpen the image
    # sharpened_image = sharpen_image(inpainted_image)
    img=cv2.cvtColor(inpainted_image,cv2.COLOR_BGR2GRAY)
    cv2.imshow('Restored Image', inpainted_image)
    cv2.waitKey(0)
    # Remove all windows
    cv2.destroyAllWindows()
    return img