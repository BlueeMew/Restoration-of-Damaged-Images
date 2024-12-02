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

#function to extract edges
def extract_edges(image,kernel_size):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(kernel_size,kernel_size))
    dilated = cv2.dilate(image,kernel,iterations=1)       #doing dilation to image
    eroded = cv2.erode(image,kernel,iterations=1)         #doing erosion to image
    edges = dilated-eroded                                #dilation-erosion to get edges
    return edges

#function for creating mask for the damaged part of image
def create_mask(image):
   
    binary_mask = np.zeros(image.shape[:2], dtype=np.uint8)
    red_pixels = (image[:, :, 2] == 255) & (image[:, :, 0] == 0) & (image[:, :, 1] == 0)
    binary_mask[red_pixels] = 255  # Set painted areas to white
    return binary_mask

#function for filling the masked parts
def inpaint_image(image, mask):
    return cv2.inpaint(image, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

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

# Another function to fill the stains
def nearestBoundaryPixelFill(image, mask):
    # Copy the input image to avoid modifying the original
    resultant_image = image.copy()
    # Getting info on boundary pixels
    mask_boundary = d(mask)-mask
    boundary_indices = np.where(mask_boundary == 255)
    boundary_values = resultant_image[boundary_indices]
    # All the pixels that are required to filled are found
    masked_indices = np.where(mask == 255) 
    for x, y in zip(*masked_indices):
        # Compute distances to all boundary pixels
        distances = np.sqrt((boundary_indices[1] - y)**2 + (boundary_indices[0] - x)**2)
        # CLosest pixel is found so use it's value
        closest_ind = np.argmin(distances)
        resultant_image[x,y] = boundary_values[closest_ind]
    return resultant_image

#Fill gaps in the image based on custom approach binary search fill
def BinarySearchFill(img, mask):
    filled = img.copy()
    rows_to_check = np.unique(np.where(mask == 255)[0])

    for row in rows_to_check:
        cols_to_fill = np.where(mask[row, :] == 255)[0]
        if len(cols_to_fill) == 0:     #if no pixels in mask
            continue
        left_edge = cols_to_fill[0] - 1
        right_edge = cols_to_fill[-1] + 1
        left_val = filled[row, left_edge]
        right_val = filled[row, right_edge]
        #Fill pixels one at a time (midpoint-based)
        while len(cols_to_fill) > 0:
            mid = len(cols_to_fill) // 2
            target_col = cols_to_fill[mid]
            filled[row, target_col] = (left_val + right_val) // 2
            mask[row, target_col] = 0           #Remove the filled column and update mask
            cols_to_fill = np.delete(cols_to_fill, mid)
    return filled
#function for removing stains 
def stain_removal(img):
    global brush_size  

    cv2.imshow('original-image',img)  # original image is displayed
    cv2.waitKey(0)                    # press any key to go to next step

    #converting back to bgr for painting with red brush
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

        if key == ord('q'):     # press q to stop drawing and move to next step
            break
        if key == ord('+'):
            brush_size += 1
        elif key == ord('-') and brush_size > 1:
            brush_size -= 1

    # Generate mask and inpaint the image
    mask = create_mask(img)
    cv2.imshow('img-mask',mask) # binary mask is displayed
    cv2.waitKey(0)              # press any key to go to next step

    inpainted_image = inpaint_image(img, mask)    # filling the image using inpaint function
    customInpaintedImage = nearestBoundaryPixelFill(img,mask)  # filling the image using gradient filling function we wrote

    #convert color image into gray scale image
    img=cv2.cvtColor(inpainted_image,cv2.COLOR_BGR2GRAY)

    cv2.imshow('Restored Image', inpainted_image) # Finally displayed the output image
    cv2.waitKey(0)                                # Press any key to remove all the windows

    # Remove all windows
    cv2.destroyAllWindows()
    return img, customInpaintedImage
