import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_histogram_equalization(processed_img, window_width, window_height):
    # Step 1: Compute the histogram
    print(processed_img.flatten)
    hist, bins = np.histogram(processed_img.flatten(), bins=256, range=[0, 256])
    
    plt.hist(processed_img.flatten(), bins=256, range=[0, 256], color='gray')
    plt.title("histogram of image")
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.show()

    # Step 2: Compute the cumulative distribution function (CDF)
    cdf = hist.cumsum()
    cdf_normalized = cdf * (255 / cdf[-1])  # Normalize to the range [0, 255]
    
    # Step 3: Map the original pixel values to equalized values
    equalized_image = np.interp(processed_img.flatten(), bins[:-1], cdf_normalized).reshape(processed_img.shape)
    
    return equalized_image.astype(np.uint8)

def apply_unsharp_masking(processed_img, window_width, window_height):
    if processed_img is not None:
        gaussian_blur = cv2.GaussianBlur(processed_img, (9, 9), 10.0)
        processed_img = cv2.addWeighted(processed_img, 1.5, gaussian_blur, -0.5, 0)
    return processed_img

def adjust_brightness_gamma(processed_img, window_width, window_height):
    if processed_img is not None:
        brightness = 30
        gamma = 1.2
        bright_img = cv2.convertScaleAbs(processed_img, alpha=1, beta=brightness)
        processed_img = np.array(255 * (bright_img / 255) ** gamma, dtype='uint8')
    return processed_img