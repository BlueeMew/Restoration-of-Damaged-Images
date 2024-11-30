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
    filled_image = image.copy()

    # Dilating the mask to increase the area of mask
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    
    # Subtracting the mask from dilated mask to obtain mask boundary pixels
    boundary_mask = cv2.dilate(mask, kernel) - mask

    # Get indices of boundary pixels
    boundary_indices = np.where(boundary_mask == 255)

    # Get pixel values of boundary pixels
    boundary_values = filled_image[boundary_indices]
    
    masked_indices = np.where(mask == 255) # All the pixels that are required to filled are found
    for y, x in zip(*masked_indices):

        # Compute distances to all boundary pixels
        distances = np.sqrt((boundary_indices[0] - y)**2 + (boundary_indices[1] - x)**2)

        # CLosest pixel is found so use it's value
        closest_ind = np.argmin(distances)
        filled_image[y, x] = boundary_values[closest_ind]

    return filled_image

# Another function to fill the stains 
def binarySearchFill(image, mask):
    filled_image = image.copy()

    rows, cols = np.where(mask==255)          #Identify rows and columns with masked areas

    #process each row in masked regions
    for row in np.unique(rows):
        # Find all masked regions in the row
        masked_indices =np.where(mask[row,:]==255)[0]       #find all masked regions in the row

        if len(masked_indices)==0:
            continue

        #finding boundary pixels
        start_idx = masked_indices[0]-1  #pixel before mask
        end_idx = masked_indices[-1]+1  #pixel after mask

        if start_idx<0 or end_idx>=filled_image.shape[1]:
            continue  # Skip regions that cannot interpolate due to boundary conditions

        #getting Boundary pixel intensities
        start_value = filled_image[row,start_idx]
        end_value = filled_image[row,end_idx]

        #filling the masked region iteratively using a binary search
        mid_indices = masked_indices
        while len(mid_indices)>0:
            mid_point = len(mid_indices)//2
            mid_idx = mid_indices[mid_point]
            
            #Compute the average of the two boundary pixels
            filled_image[row, mid_idx] = (start_value+end_value)//2

            #Update mask to exclude the filled point
            mask[row,mid_idx] =0
            
            #assigning intensities to middle indices
            left_indices = mid_indices[:mid_point]
            right_indices = mid_indices[mid_point+1:]
            
            mid_indices = np.hstack((left_indices,right_indices))
    return filled_image

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