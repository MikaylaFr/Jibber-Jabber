import os
import cv2
import face_recognition

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
        #confirms there is a face in the photo taken:
        try:
            userEncoding = face_recognition.face_encodings(image)[0]
        except IndexError as e:
            print(e)
            return False
        # save the image
        cv2.imwrite("person.jpg", image)

        # show image for 5 seconds
        cv2.waitKey(5000)
        # exit window
        cv2.destroyWindow("person")

        #
    else:
        print("No image detected.")
        return False

    # exits the camera
    cam.release()
    return True

# identify_user function compares saved image from user database 
# to new image
def identify_user(knownImage):
    knownImage = face_recognition.load_image_file(knownImage)

    # take photo to compare to saved photo
    # 0 refers to the camera number, most people only have one camera
    cam = cv2.VideoCapture(0)
    cv2.namedWindow('Jibber-Jabber login')
    result, image = cam.read()

    cv2.imshow('unknown image', image)

    cv2.waitKey(3000)
    cv2.destroyWindow('unknown image')

    if result:
        unknownImage = image
    else:
        print('no image detected')
    
    # photo must be encoded to be compared   
    try:
        userEncoding = face_recognition.face_encodings(knownImage)[0]
    #prevents index out of range error if no face is in the photo
    except IndexError as e:
        print(e)
        return False
    try:
        unknownEncoding = face_recognition.face_encodings(unknownImage)[0]
    except IndexError as e:
        print(e)
        return False

    comparison = face_recognition.compare_faces([userEncoding], unknownEncoding)
    print("Result: ", comparison)
    if comparison[0] == True:
        return True
    else:
        return False


# converts photo to byte array for db storage
def convert_to_byte_array(image):
    with open(image, 'rb') as f:
        imageBlob = f.read()
    return imageBlob

# converts blob back to image
def convert_to_image(blob):
    with open('imageFromDB.jpg', 'wb') as fh:
        image = fh.write(blob)
    return image
    


#print(convertToByteArray('person.jpg'))

#identify_user('person.png')
