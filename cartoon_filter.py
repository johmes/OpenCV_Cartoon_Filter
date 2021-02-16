# Author Johannes Mensalo
# Computer vision based cartoon filter made by using OpenCV
# Credits Johannes Mensalo
import cv2
import numpy as numpy
import ctypes
from time import strftime

# Get screen height
user32 = ctypes.windll.user32
screen_heigth = user32.GetSystemMetrics(1)
img_timestamp = 0

# Capture video from users camera 
#cam = cv2.VideoCapture(0)
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Change resolution if needed
def scale_image(width,height):
    cam.set(3, width)
    cam.set(4, height)
# scale video to desired resolution
scale_image(480,360)

# Main loop
while(True):
    rect, img = cam.read()

    if not rect:
        print("failed to grab frame")
        break

    # Flip image vertically
    img = cv2.flip(img, 1)

    # Stylization of image. May drop the frame rate significantly.
    #grayImage = cv2.stylization(img, sigma_s = 90, sigma_r = 0.4)
    # Converting to gray scale
    grayImage = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Reduce image noise
    blurImage = cv2.GaussianBlur(grayImage, (5,5), 0) 
    # Sharpening
    edgeImage = cv2.Laplacian(blurImage, -1, ksize = 5)
    edgeImage = 255 - edgeImage
    edgeImage = cv2.edgePreservingFilter(edgeImage, flags=1, sigma_s=60, sigma_r=0.6) 
    # You can use one of the 'edges' thresholds or try both
    #edges = cv2.adaptiveThreshold(edgeImage, 5, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 7)
    otsu_threshold, edges = cv2.threshold(edgeImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


    # Color
    colorImage = cv2.bilateralFilter(img, 9, 250, 250)

    # Combine colorImage and edges to one image
    output = cv2.bitwise_and(colorImage, colorImage, mask=edges)

    # Display original image and one with filter on.
    cv2.imshow('Cartoon Filter', output)
    cv2.imshow('Original', img)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        break
    elif k%256 == 32:
        # if SPACE pressed then take picture with filter and without
        # Create unique timestamp for every picture
        img_timestamp = strftime("%H%M%S%Y%m%d")
        img_name = "filter_img_{}.png".format(img_timestamp)
        img_name_original = "filter_original_img_{}.png".format(img_timestamp)
        # Create the image
        cv2.imwrite(img_name, output)
        cv2.imwrite(img_name_original, img)
        print("Picture {} is saved!".format(img_name))
        print("Picture {} is saved!".format(img_name_original))
        savedImage = cv2.imread(img_name)
        cv2.imshow(img_name, savedImage)
    # elif cv2.getWindowProperty('Cartoon Filter', cv2.WND_PROP_VISIBLE) < 1:
    #     #'X' pressed
    #     cv2.destroyWindow('Cartoon Filter')

# Release camera from 'duty'
cam.release()
# Close all windows
cv2.destroyAllWindows()
