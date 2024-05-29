import cv2 as cv
import sys

# Read, display and write an image
# read
img = cv.imread("sample_images/image.jpg")
print(img)
# display
if img is None:
    sys.exit("No image to read")
cv.imshow("Image display - ",img)
k = cv.waitKey(0)   # window displayed until the user presses some key otherwise the program closes too soon

# write
cv.imwrite("sample_images/written_image.jpg", img)


# arithmetic operatins like add, diff, etc can be performed on two or more images
#  just make sure the images are of same size otherwise resize the images

