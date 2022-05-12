from skimage.filters import (threshold_sauvola)
from skimage.io import imread, imsave
from skimage.color import rgb2gray
import skimage.exposure
import numpy as np
import cv2
# from PIL import Image, ImageEnhance 

def remove_border(img):
    # convert to gray
    gray = img if len(img.shape) == 2 else cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # threshold
    thresh = cv2.threshold(gray, 11, 255, cv2.THRESH_BINARY)[1]
    # apply morphology to clean small spots
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, borderType=cv2.BORDER_CONSTANT, borderValue=0)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel, borderType=cv2.BORDER_CONSTANT, borderValue=0)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    morph = cv2.morphologyEx(morph, cv2.MORPH_ERODE, kernel, borderType=cv2.BORDER_CONSTANT, borderValue=0)
    # get external contour
    contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    big_contour = max(contours, key=cv2.contourArea)
    # draw white filled contour on black background as mas
    contour = np.zeros_like(gray)
    cv2.drawContours(contour, [big_contour], 0, 255, -1)
    # blur dilate image
    blur = cv2.GaussianBlur(contour, (5,5), sigmaX=0, sigmaY=0, borderType = cv2.BORDER_DEFAULT)
    # stretch so that 255 -> 255 and 127.5 -> 0
    mask = skimage.exposure.rescale_intensity(blur, in_range=(127.5,255), out_range=(0,255))
    # put mask into alpha channel of input
    result = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    result[:,:,3] = mask

    return result

def binary_threshold(img, threshold):
    # Binarization
    _, binarized = cv2.threshold(img, threshold , 255, cv2.THRESH_BINARY)
    mask_bool = binarized[:,:] < 50
    return mask_bool

def sauvola(img, window_size, k, r):
    mask = threshold_sauvola(img, window_size=window_size, k=k, r=r)
    # Create binary mask
    mask_bool = img < mask

    return mask_bool

def contrast_and_brightness(img, contrast, brightness):
    img = np.int16(img)
    img = img * (contrast/127+1) - contrast + brightness
    img = np.clip(img, 0, 255)
    img = np.uint8(img)

    return img

def scan(img):
    gray = img if len(img.shape) == 2 else cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = contrast_and_brightness(gray, 127, 0)
    # do adaptive threshold on gray image
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 10)
    # make background of input white where thresh is white
    result = img.copy()
    result[thresh==255] = (255,255,255,0)

    return result

def grayscale(img):
    # Convert to grayscale
    grayscale = rgb2gray(img[:,:,:3])
    # Convert to uint8 format
    grayscale = uint8image = np.uint8(grayscale*255)
    # Increase contrast
    grayscale = contrast_and_brightness(grayscale, 127, 0)

    return grayscale

def remove_background(img, window_size, k, r=None):
    # Remove black border
    img = remove_border(img)
    # For grayscale images
    if len(img.shape) == 2:
        gray = contrast_and_brightness(img, 127, 0)
        img = img*(sauvola(gray, window_size, k, r))
    # For RGB or RGBA images
    else:
        gray = grayscale(img)
        img = img*(sauvola(gray, window_size, k, r)[:,:,np.newaxis])
    
    return img

def main():
    # Import image
    img = imread('../datasets/images/SEILS/alberti_dalmio_A.jpg')
    img = remove_background(img, window_size, k, r=None)
    # Save results
    imsave("../datasets/results/result.png", img)

if __name__ == "__main__":
    main()