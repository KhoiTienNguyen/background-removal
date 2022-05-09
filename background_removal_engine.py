from skimage.filters import (threshold_sauvola)
from skimage.io import imread, imsave
from skimage.color import rgb2gray
import numpy as np
import cv2
import skimage.exposure

def remove_border(img):
    # convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

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

def background_removal(img, window_size, k, r):
    # Turn image to grayscale
    grayscale = rgb2gray(img[:,:,:3])
    # Remove background
    mask = threshold_sauvola(grayscale, window_size=window_size, k=k, r=r)
    # imsave("../datasets/results/Image - 040 threshold.png", mask)
    mask_bool = mask < 0.57
    mask_bool = mask_bool.astype(int)
    imsave("../datasets/results/Image - 040 maskbool.png", mask_bool)
    # transparent = np.zeros((img.shape[0], img.shape[1], 4), dtype=np.uint8)
    # transparent[:,:,0:3] = img[:,:,:3]
    # transparent[:, :, 3] = mask_bool[:,:,np.newaxis]
    # result = img
    # result = cvtColor(result, COLOR_BGR2BGRA)
    # print(img.shape)
    # img[:, :, 3] = mask
    result = img*mask_bool[:,:,np.newaxis]
    # img[:,:,3] = mask
    # res = bitwise_and(img,img,mask = mask)
    # Convert to uint8
    # output = (combined*255).astype(np.uint8)

    return result

def main():
    # Import image
    img = imread('../datasets/images/Image - 040.png')
    img = remove_border(img)
    # img = remove_border(img)
    img = background_removal(img, 7, 0.05, None)
    # img = remove_border(img)
    # img = background_removal(img, 15, 0.05, None)
    # Return image with removed background
    imsave("../datasets/results/cropped.png", img)
    # imsave("../datasets/results/cropped.png", result)
    # imwrite('../datasets/results/Image - 040 BR.png', result)

if __name__ == "__main__":
    main()

# import cv2
# import numpy as np

# # load image
# # img = cv2.imread('../datasets/images/Image - 040.png')
# img = cv2.imread('../datasets/images/cropped.png')

# # convert to graky
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # threshold input image as mask
# mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]

# # negate mask
# mask = 255 - mask

# # apply morphology to remove isolated extraneous noise
# # use borderconstant of black since foreground touches the edges
# kernel = np.ones((3,3), np.uint8)
# mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
# mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# # anti-alias the mask -- blur then stretch
# # blur alpha channel
# mask = cv2.GaussianBlur(mask, (0,0), sigmaX=2, sigmaY=2, borderType = cv2.BORDER_DEFAULT)

# # linear stretch so that 127.5 goes to 0, but 255 stays 255
# mask = (2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)

# # put mask into alpha channel
# result = img.copy()
# result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
# result[:, :, 3] = mask

# # save resulting masked image
# cv2.imwrite('../datasets/results/Image - 040 BR.png', result)

# # if __name__ == "__main__":
# #     main()