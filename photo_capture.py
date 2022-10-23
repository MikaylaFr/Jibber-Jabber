import os
import cv2
import numpy

# photo capture function
# takes a photo with your computer's webcam
# saves it in current directory

def photo_capture():

    # initialize camera
    cam = cv2.VideoCapture(0)

    # name the popup window
    cv2.namedWindow('Jibber-Jabber login')

    # read input using the camera
    result, image = cam.read()

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

    # this print statement does not print
    # unclear when the camera releases. 
    print("camera about to release")
    cam.release()

    # cam.destroyAllWindows()

#run function
#photo_capture()
