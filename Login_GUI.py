# heavily sourced from: https://pythonexamples.org/python-tkinter-login-form/
# and https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter/7557028#7557028

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import firebase_admin
from firebase_admin import firestore
from photo_capture import photo_capture
from photo_capture import identify_user
from photo_capture import convert_to_byte_array
from photo_capture import convert_to_image
from loginDB import setUpDatabase
from loginDB import save_photo_to_firebase_storage

def LoginGuiInit(container, main_gui): 
    #instantiating all the frames of the app
    main_gui.frames["StartPage"] = StartPage(parent=container, controller=main_gui)
    main_gui.frames["Login"] = Login(parent=container, controller=main_gui)
    main_gui.frames["Register"] = Register(parent=container, controller = main_gui)
    # main_gui.frames["ConfirmRegistration"] = ConfirmRegistration(parent=container, controller=main_gui)
    # main_gui.frames["ChatEntry"] = ChatEntry(parent=container, controller=main_gui)
    main_gui.frames["StartPage"].grid(row=0, column=0, sticky="nsew")
    main_gui.frames["Login"].grid(row=0, column = 0, sticky="nsew")
    main_gui.frames["Register"].grid(row=0, column=0, sticky="nsew")
    # main_gui.frames["ConfirmRegistration"].grid(row=0, column=0, sticky="nsew")
    # main_gui.frames["ChatEntry"].grid(row=0, column=0, sticky="nsew")
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
        usernameLabel = Label(self, text="username")
        usernameLabel.grid(row=0, column=0)
        username=StringVar()
        usernameEntry = Entry(self, textvariable=username)
        usernameEntry.grid(row=0, column=1)
        #validate the login
        # login button calls validate login function
        loginButton2 = Button(self, text="Login", command=lambda: [self.validateLogin(username), self.clearText(usernameEntry)])
        loginButton2.grid(row=4, column=0)

    def clearText(self, textEntry):
        textEntry.delete(0, END)
 
    def validateLogin(self, username):
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
            messagebox.showinfo("showinfo", "username not found, going back to start page")
            self.controller.show_frame("Start_Page")
        # compare name of file to photo that is already saved
        # if there is no saved photo, login is not validated
        wasPhotoValidated = identify_user('imageFromDB.jpg')
        if wasPhotoValidated:
            print("User photo validated, login can proceed")
            self.controller.username = username.get()
            self.controller.show_frame("ChatMenu")
            return True
        else: 
            print("webcam photo does not match")
            messagebox.showinfo("showinfo", "facial recognition login failed")
            #got back to start page
            self.controller.show_frame("StartPage")
            return False
    
    
class Register(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        photoLabelText1 = "Jibber-jabber users sign in with facial recognition instead of a password. " 
        photoLabelText2 = "**By clicking register, you are consenting to Jibber-Jabber's use of your webcam"
        photoLabelText3= "and encrypted storage of your login photo."
        usernameLabel = Label(self, text="create username: ").grid(row=16, column=0, columnspan=2, sticky='SE')
        # StringVar() is an object
        #usernameValidated = 'placeholder'
        username = StringVar()
        usernameEntry = Entry(self, textvariable=username)
        usernameEntry.grid(row=16, column=2, sticky="SW")
        # access username value
        #username.set('value')
        usernameString = username.get()
        # must register the input validation thingy
        reg = self.register(self.inputValidation)
        # must configure input validation to work instantaneously on the username entry box
        usernameEntry.config(validate='key', validatecommand=(reg, '% P'))
        photoLabel1 = Label(self, text=photoLabelText1).grid(row=8, column=0, columnspan=3, sticky="NSEW")
        photoLabel2 = Label(self, text=photoLabelText2).grid(row = 28, column = 0, columnspan=3, sticky = "NSEW")
        photoLabel3 = Label(self, text=photoLabelText3).grid(row = 32, column = 0, columnspan=3, sticky='NSEW')
        photoButton = Button(self, text="register", command=lambda: [self.saveUserInDb(username), self.goToChatPage()]).grid(row=24, column=1, columnspan=2, padx=50)
    
    def clearText(self, textEntry):
        textEntry.delete(0, END)
 
    def inputValidation(self, input):
        if input == 'null':
            print('not a valid username1')
            return False
        elif input == 'NULL':
            print("not a valid un2")
            return False
        else:
            return True

    def saveUserInDb(self, username):
        #captures photo and saves it as person.jpg
        userImageCaptured = photo_capture()
        if userImageCaptured: 
            #saves person.jpg as blob
            photo = self.savePhoto()
            # save username and photo blob to db
            self.controller.db.collection('users').add({'username': username.get(), 'photo': photo})
        else:
            messagebox.showinfo("showinfo", "no face detected. facial recognition registration failed.")
            #got back to start page
            self.controller.show_frame("StartPage")
            return False

    
    def goToChatPage(self):
        self.controller.show_frame("ChatMenu")
        
    
    def savePhoto(self):
        byteImage = convert_to_byte_array('person.jpg')
        return byteImage

"""
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
"""

