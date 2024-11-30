import cv2
import numpy as np
import matplotlib.pyplot as plt

def applyHistogramEqualization(processedImage):
    histogram = np.zeros(256, dtype=int)
    for pixel in processedImage.flatten():          #calculating frequency fo intensity values
        histogram[pixel] += 1
    
    plt.bar(range(256), histogram, color='gray', width=1)
    plt.title("Histogram of Original Image")
    plt.xlabel("Intensity Level")
    plt.ylabel("Frequency")
    plt.show()   #show the histogram of the image before histogram equilizaiton

    cdf = np.zeros_like(histogram, dtype=float)
    cdf[0] = histogram[0]
    for i in range(1, len(histogram)):          #computing the cumulative addition of the intensity levels
        cdf[i] = cdf[i-1]+histogram[i]
    
    cdfNormalized = (cdf-cdf.min())/(cdf.max()-cdf.min())*255  #getting the final intensity level my normalizing the above cumulative addition and multiplying it with 255

    equalizedImage = np.zeros_like(processedImage, dtype=np.uint8)
    for i in range(processedImage.shape[0]):
        for j in range(processedImage.shape[1]):
            equalizedImage[i, j] = int(cdfNormalized[processedImage[i, j]])    #mapping the original pixel values to equilized values

    histogramEquilized = np.zeros(256, dtype=int)
    for pixel in equalizedImage.flatten():                  #calculating frequency of equilized image
        histogramEquilized[pixel] += 1
    
    plt.bar(range(256), histogramEquilized, color='gray', width=1)
    plt.title("Histogram of Equalized Image")
    plt.xlabel("Intensity Level")
    plt.ylabel("Frequency")
    plt.show()      #show the histogram of the image after histogram equilizatioin

    return equalizedImage

def applyUnsharpMasking(processedImage):
    gaussianBlur = cv2.GaussianBlur(processedImage, (9, 9), 1.0)  #applying Guassian blurr to the image 
    processedImage = cv2.addWeighted(processedImage, 1.5, gaussianBlur, -0.5, 0) # 1.5*initial image - 0.5*blurred image to enhance edges
    return processedImage

def adjustBrightnessGamma(processedImage):
    brightness = 15
    gamma = 0.8         
    brightened = cv2.convertScaleAbs(processedImage,alpha=1,beta=brightness)    #adds constant value to all pixels
    processedImage = np.array(255*(brightened/255)**gamma,dtype='uint8')      #applys the non linear gamma equation
    return processedImage