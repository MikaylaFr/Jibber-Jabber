import os
import cv2
import face_recognition
import base64

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
        cv2.imwrite("person.jpg", image)

        # show image for 5 seconds
        cv2.waitKey(5000)
        # exit window
        cv2.destroyWindow("person")

        #
    else:
        print("No image detected.")

    # exits the camera
    cam.release()

def identify_user(knownImage):
    knownImage = face_recognition.load_image_file(knownImage)

    # take photo to compare to saved photo
    # 0 refers to the camera number, most people only have one camera
    cam = cv2.VideoCapture(0)
    cv2.namedWindow('Jibber-Jabber login')
    result, image = cam.read()

    cv2.imshow('unknown image', image)

    cv2.waitKey(3000)

    if result:
        unknownImage = image
    else:
        print('no image detected')
    
    # photo must be encoded to be compared   
    userEncoding = face_recognition.face_encodings(knownImage)[0]
    unknownEncoding = face_recognition.face_encodings(unknownImage)[0]

    comparison = face_recognition.compare_faces([userEncoding], unknownEncoding)
    print("Result: ", comparison)


# converts photo to byte array for db storage
def convert_to_byte_array(image):
    with open(image, 'rb') as f:
        imageBlob = f.read()
    return imageBlob

def convert_to_image(blob):
    with open('imageFromDB.jpg', 'wb') as fh:
        image = fh.write(base64.decodebytes(blob))
    return image

#print(convertToByteArray('person.jpg'))

#identify_user('person.png')
