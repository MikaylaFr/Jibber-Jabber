import os
import cv2
import numpy

# initialize camera
cam = cv2.VideoCapture(0)

cv2.namedWindow('Jibber-Jabber login')

# read input using the camera
result, image = cam.read()

# print(result)
img_counter = 0

if result:
    # show image
    cv2.imshow("person", image)

    # save the image
    cv2.imwrite("person.png", image)

    # show image for 5 seconds
    cv2.waitKey(5000)
    cv2.destroyWindow("person")

    #
else:
    print("No image detected.")

cam.release()

# cam.destroyAllWindows()
