import numpy as np
from skimage.io import imread, imsave
import cv2

def load_check(img):
    """Check the image has three channels and uint8 dtype.
    """
    if img.dtype != np.uint8:
        raise TypeError("load_image should return dtype=uint8. Got an image {} with dtype {}".format(image_path, image_rgb.dtype))
    if img.ndim == 3:
        img = img[..., :3] # Remove the alpha channel
    else:
        raise TypeError("load_image only supports rgb format. Got an image {} with shape {}".format(image_path, image_rgb.shape))
    return img

def load_image(image_path, mode='bgr_cv'):
    """Load <image_path> as a ndarray with shape (width, height, 3).
    Only support BGR

    Parameters:
        image_path (str): Load <image path>. The image should be in RGB or RGBA.
        mode (str): A flag regarding how to load the image. For now it only supports <bgr_cv>
    Returns:
        np.ndarray: Load image with shape (W, H, 3) with dtype=uint8. The channel order is RGB. 
    Exception:
        TypeError: Do not try to load a grey scale image.
    """
    if mode == 'rgb':
        # Use skimage
        img = imread(image_path)
        return img
    elif mode == "bgr_cv":
        image_bgr = cv2.imread(image_path, cv2.IMREAD_COLOR)
        image_bgr = load_check(image_bgr)
        return image_bgr
    else:
        raise NotImplementedError("Try do load image with invalid mode: {}".format(mode))

def write_image(image_path, image, mode='bgr_cv'):
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
    if mode == "rgb":
        # Conver RGB to BGR, need to do this step if you use sklearn to load image.
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        pass
    elif mode == "bgr_cv":
        # It's already in bgr
        pass
    else:
        raise NotImplementedError("Try do load image with invalid mode: {}".format(mode))

    imsave(image_path, image)

if __name__ == "__main__":
    image_path = "Image - 040.png"
    image_bgr = load_image(image_path, mode='bgr_cv')
    image_rgb = load_image(image_path, mode='rgb')
    diff = np.mean(np.abs(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB) - image_rgb))
    print (image_bgr.shape, image_bgr.dtype)
    print (image_rgb.shape, image_rgb.dtype)
    print (diff)
    print ("pass")

    write_image("./tmp.png", image_rgb, mode='bgr_cv')