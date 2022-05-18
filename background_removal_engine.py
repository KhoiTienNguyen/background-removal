from skimage.filters import (threshold_sauvola)
from skimage.io import imread, imsave
from skimage.color import rgb2gray
import numpy as np
import cv2

def sauvola(img, window_size, k):
    """ Receives a grayscale image and creates a mask for background removal.

    Parameters:
        img (np.ndarray): Image with shape (W, H, 3) or (W, H, 4) with dtype=uint8.
        window_size (int): window_size parameter for saulova_threshold. Must be odd
        k (float): k parameter for saulova_threshold. Must be a positive integer.

    Returns:
        mask_bool (np.ndarray): Boolean image with shape (W, H).
    """
    mask = threshold_sauvola(img, window_size=window_size, k=k)
    # Create binary mask
    mask_bool = img < mask

    return mask_bool

def contrast_and_brightness(img, contrast, brightness):
    """ Adjusts the contrast and brightness of the image.

    Parameters:
        img (np.ndarray): Image with shape (W, H, 4) or (W, H, 3) or (W, H) with dtype=uint8.
        contrast (float): The amount to adjust contrast by.
        brightness (float): The amount to adjust brightness by.

    Returns:
        img (np.ndarray): Image with same shape as input image and dtype=uint8.
    """
    img = np.int16(img)
    img = img * (contrast/127+1) - contrast + brightness
    img = np.clip(img, 0, 255)
    img = np.uint8(img)

    return img

def grayscale(img, contrast, brightness):
    """ Converts image to grayscale then increases the contrast

    Parameters:
        img (np.ndarray): Image with shape (W, H, 3) or (W, H, 4) with dtype=uint8.

    Returns:
        grayscale (np.ndarray): Image with shape (W, H) with dtype=uint8.
    """
    # Convert to grayscale
    grayscale = rgb2gray(img[:,:,:3])
    # Convert to uint8 format
    grayscale = uint8image = np.uint8(grayscale*255)
    # Increase contrast
    grayscale = contrast_and_brightness(grayscale, contrast, brightness)

    return grayscale

def remove_background(img, window_size, k, contrast, brightness):
    """ Removes background from an image. Image can be Grayscale/RGB/RGBA

    Parameters:
        img (np.ndarray): Image with shape (W, H, 4) or (W, H, 3) or (W, H) with dtype=uint8.
        window_size (int): window_size parameter for saulova_threshold. Must be odd
        k (float): k parameter for saulova_threshold. Must be a positive integer.

    Returns:
        img (np.ndarray): Image with shape (W, H, 4) with dtype=uint8.
    """
    # Convert to RGBA
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    # For grayscale images
    if len(img.shape) == 2:
        gray = contrast_and_brightness(img, contrast, brightness)
        img = img*(sauvola(gray, window_size, k))
    # For RGB or RGBA images
    else:
        gray = grayscale(img, contrast, brightness)
        img = img*(sauvola(gray, window_size, k)[:,:,np.newaxis])
    
    return img

def main():
    # Import image
    img = imread('../datasets/images/bounding/test.png')
    img = remove_background(img, 101, 0.2,127,0)
    # Save results
    imsave("../datasets/results/result.png", img)

if __name__ == "__main__":
    main()