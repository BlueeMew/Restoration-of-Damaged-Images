import cv2
import numpy as np

def sharpen_image(image, kernel_size=3, sigma=0 , alpha=0):
    # Apply Gaussian blur to the image
    blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    
    # Sharpen the image using the unsharp masking formula
    # Adjust weights to preserve intensity levels
    sharpened = cv2.addWeighted(image, 1 + alpha, blurred, -alpha, 0)
    
    return sharpened
# defining erosion function
def e(image, k_size=(3,3)):
    kernel=np.ones(k_size,dtype=np.uint8)
    eroded_image= cv2.erode(image,kernel)
    return eroded_image
# defining dilution function
def d(image, k_size=(3,3)):
    kernel=np.ones(k_size,dtype=np.uint8)
    dilated_image= cv2.dilate(image,kernel)
    return dilated_image
# combining erosion and dilution and sharpening the result
def Nofold(image):
    nofold=np.minimum(image,d(e(e(image))))
    final=sharpen_image(nofold,sigma=0.5,alpha=1.5)
    return final    
# Example usage
def fold_removal(image):
    # Load the image (replace 'image.jpg' with your file path)
    # image = cv2.imread('folded_img.jpeg', cv2.IMREAD_GRAYSCALE)
    # Apply sharpening
    # sharpened_image = sharpen_image(image, kernel_size=3, sigma=9, alpha=1.5)
    # Removing the folds
    Final_image = Nofold(image)
    # Display results
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return Final_image