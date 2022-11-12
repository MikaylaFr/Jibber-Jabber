# heavily sourced from: https://pythonexamples.org/python-tkinter-login-form/
# and https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter/7557028#7557028

from tkinter import *
from tkinter import ttk
from functools import partialmethod
import firebase_admin
from firebase_admin import firestore
from photo_capture import photo_capture
from photo_capture import identify_user
from photo_capture import convert_to_byte_array
from photo_capture import convert_to_image
from validate_username import validate_username
from loginDB import setUpDatabase
from loginDB import save_photo_to_firebase_storage

def LoginGuiInit(container, main_gui): 
    #instantiating all the frames of the app
    main_gui.frames["StartPage"] = StartPage(parent=container, controller=main_gui)
    main_gui.frames["Login"] = Login(parent=container, controller=main_gui)
    main_gui.frames["Register"] = Register(parent=container, controller = main_gui)
    main_gui.frames["ConfirmRegistration"] = ConfirmRegistration(parent=container, controller=main_gui)
    main_gui.frames["ChatEntry"] = ChatEntry(parent=container, controller=main_gui)
    main_gui.frames["StartPage"].grid(row=0, column=0, sticky="nsew")
    main_gui.frames["Login"].grid(row=0, column = 0, sticky="nsew")
    main_gui.frames["Register"].grid(row=0, column=0, sticky="nsew")
    main_gui.frames["ConfirmRegistration"].grid(row=0, column=0, sticky="nsew")
    main_gui.frames["ChatEntry"].grid(row=0, column=0, sticky="nsew")
    #start db
    setUpDatabase()
    main_gui.db=firestore.client()

class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Jibber Jabber App")
        label.pack(side="top", fill="x", pady=10)
        #login button
        loginButton = Button(self, text="Login", command=lambda: controller.show_frame("Login"))

        #register button
        registerButton = Button(self, text="Register", command=lambda: controller.show_frame("Register"))

        loginButton.pack()
        registerButton.pack()

class Login(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller=controller
        usernameLabel = Label(self, text="username").grid(row=0, column=0)
        username=StringVar()
        usernameEntry = Entry(self, textvariable=username).grid(row=0, column=1)
        #validate the login
        # validateLogin = partial(validateLogin, username)
        # login button
        loginButton2 = Button(self, text="Login", command=lambda: [self.validateLogin(username)]).grid(row=4, column=0)
        #loginButton = Button(self, text="login").grid(row=4, column = 0)
        #controller.show_frame("Chat")
 
    def validateLogin(self, username): #also need to add photo as an argument
        # need to validate username
        print("username entered : ", username.get())
        #compare entered username to database of usernames
        if self.controller.db.collection('users').where("username", "==", username.get()).get():
            print("username found")
            # get blob associated with username
            #fetch the document from the db
            docFromDb = self.controller.db.collection('users').where("username", "==", username.get()).get()
            for doc in docFromDb:
                userDocument = doc.to_dict()
            # fetch the blob from the document fields dictionary
            blobFromDb = userDocument.get('photo')
            #print(userDocument)
            convert_to_image(blobFromDb)
        else:
            print("username not found")
        # compare name of file to photo that is already saved
        # if there is no saved photo, login is not validated
        wasPhotoValidated = identify_user('imageFromDB.jpg')
        if wasPhotoValidated:
            print("User photo validated, login can proceed")
            self.controller.username = username.get()
            self.controller.show_frame("ChatMenu")
        #return
    
    
class Register(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        usernameLabel = Label(self, text="create username").grid(row=0, column=0)
        # StringVar() is an object
        username = StringVar()
        usernameEntry = Entry(self, textvariable=username).grid(row=4, column=0)
        # access username value
        #username.set('value')
        usernameString = username.get()
        # usernameValidated is T/F
        #self.controller.db.collection('users').add({'username': 'testuser3'})
        #testButton = Button(self, text="insert into db", command=lambda: [controller.db.collection('users').add({'username': 'testuser3'})]).grid(row=8, column=0)
        usernameValidated = validate_username(usernameString)
        # validate username
        #if not usernameValidated:
        if not usernameValidated:
            print("must reenter username")
            # Figure out how to bring up a popup to tell the user to enter a new username
        photoLabel = Label(self, text="take webcam photo for facial recognition login in lieu of password").grid(row=12, column=0)
        photoButton = Button(self, text="take photo with webcam", command=lambda: [self.photoCapture(username)]).grid(row=16, column=0)
                            #controller.show_frame("ChatEntry")]).grid(row=16, column=0)
        #popup to confirm photo save
        byteImage = self.savePhoto()
        # this button saves the username and photo blob in the database
        photoSaveButton = Button(self, text="save photo", command=lambda: [controller.db.collection('users').add({'username': username.get(), 
                            'photo': byteImage}), controller.show_frame("ChatEntry")]).grid(row=20, column=0)
        testButton = Button(self, text='testing calling from function', command=lambda: [self.addToDb(byteImage)]).grid(row=24, column=0)

    def photoCapture(self, username):
        enteredName = username.get()
        print("username entered: ", enteredName)
        photo_capture()
        return
    
    def savePhoto(self):
        byteImage = convert_to_byte_array('person.jpg')
        return byteImage
    
    def addToDb(self, byteImage):
        self.controller.db.collection('users').add({'username': 'sally', 'photo': byteImage})

class ConfirmRegistration(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        #if photo was good, take user to chat page, if photo was bad, retake photo...

#this class asks if you want to log in as
class ChatEntry(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        chatLabel = Label(self, text="Jibber Jabber here").grid(row=0, column=2)
