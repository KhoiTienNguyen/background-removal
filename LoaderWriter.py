import numpy as np
import skimage
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

def load_image(image_path, mode):
    """Load <image_path> as a ndarray with shape (width, height, 3).
    Only support rgb format.

    Parameters:
        image_path (str): Load <image path>. The image should be in RGB or RGBA.
        mode (str): A flag regarding how to load the image. For now it only supports rgb
    Returns:
        np.ndarray: Load image with shape (W, H, 3) with dtype=uint8. The channel order is RGB. 
    Exception:
        TypeError: Do not try to load a grey scale image.
    """
    if mode == 'rgb':
        image_rgb = skimage.io.imread(image_path)
        image_rgb = load_check(image_rgb)
        return image_rgb
    elif mode == "bgr_cv":
        image_bgr = cv2.imread(image_path, cv2.IMREAD_COLOR)
        image_bgr = load_check(image_bgr)
        return image_bgr
    else:
        raise NotImplementedError("Try do load image with invalid mode: {}".format(mode))

def write_image(image_path, image, mode):
    """Write <image> to <args.output_path> with a new name. <image name without its filetype><args.output_postfix>.<filetype>

    This function convert RGB to BGR and use opencv to write the image.
    Sklearn package runs significantly slower than opencv.
    Make sure the image is in RGB order!

    Parameters:
        image (np.ndarray): The output image with shape (W, H, 3) with dtype=uint8. The channel order is RGB. 
        image_name (str): the image_name from the loader function.
        args (argparse.Namespace): A namespace with arguments: <output_path>, <output_postfix>
    Returns:
        None
    """
    if mode == "rgb":
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    elif mode == "bgr_cv":
        pass
    else:
        raise NotImplementedError("Try do load image with invalid mode: {}".format(mode))
    cv2.imwrite(image_path, image)

if __name__ == "__main__":
    image_path = "./datasets/images/Image - 040.png"
    image_bgr = load_image(image_path, mode='bgr_cv')
    image_rgb = load_image(image_path, mode='rgb')
    diff = np.mean(np.abs(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB) - image_rgb))
    print (image_bgr.shape, image_bgr.dtype)
    print (image_rgb.shape, image_rgb.dtype)
    print (diff)
    print ("pass")

    write_image("./tmp.png", image_bgr, mode='bgr_cv')