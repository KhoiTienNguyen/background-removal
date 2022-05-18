import numpy as np
from skimage.io import imread, imsave

def load_image(image_path):
    """Load <image_path> as a ndarray with shape (width, height, 3).
    Only support loading bgr with opencv.

    Parameters:
        image_path (str): Load <image path>. The image should be in RGB or RGBA.
        mode (str): A flag regarding how to load the image. For now it only supports <bgr_cv>
    Returns:
        np.ndarray: Load image with shape (W, H, 3) with dtype=uint8. The channel order is RGB. 
    """
    img = imread(image_path)
    return img

def write_image(image_path, image):
    """Write <image> to <image_path>.

    This function convert RGB to BGR and use opencv to write the image.
    Sklearn package runs significantly slower than opencv.
    Make sure the image is in RGB order!

    Parameters:
        image (np.ndarray): The output image with shape (W, H, 3) with dtype=uint8. The channel order is RGB. 
        image_name (str): the image_name from the loader function.
        mode (str): A flag regarding how to load the image. For now it only supports <bgr_cv>
    Returns:
        None
    """
    imsave(image_path, image)