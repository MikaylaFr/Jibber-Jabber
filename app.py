# heavily sourced from: https://pythonexamples.org/python-tkinter-login-form/
# and https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter/7557028#7557028

from tkinter import *
from tkinter import ttk
from functools import partialmethod
import firebase_admin
from firebase_admin import firestore
from photo_capture import photo_capture
from validate_username import validate_username
from loginDB import setUpDatabase

class App(Tk): 
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # frames go in the container
        container = Frame(self)
        container.pack(side="top", fill = "both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight = 1)
        self.title('Jibber-Jabber')

        self.frames = {}
        #instantiating all the frames of the app
        self.frames["StartPage"] = StartPage(parent=container, controller=self)
        self.frames["Login"] = Login(parent=container, controller=self)
        self.frames["Register"] = Register(parent=container, controller = self)
        self.frames["ConfirmRegistration"] = ConfirmRegistration(parent=container, controller=self)
        self.frames["ChatEntry"] = ChatEntry(parent=container, controller=self)

        self.frames["StartPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["Login"].grid(row=0, column = 0, sticky="nsew")
        self.frames["Register"].grid(row=0, column=0, sticky="nsew")
        self.frames["ConfirmRegistration"].grid(row=0, column=0, sticky="nsew")
        self.frames["ChatEntry"].grid(row=0, column=0, sticky="nsew")

        #show the first frame when the app opens
        self.show_frame("StartPage")

        #start db
        self.startDB()

        #start DB
    def startDB(self):
        setUpDatabase()
        self.db=firestore.client()

    #db.collection('users').add({'username': 'testuser2'})

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

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
        loginButton2 = Button(self, text="Login", command=lambda: [self.validateLogin(username), controller.show_frame("ChatEntry")]).grid(row=4, column=0)
        #loginButton = Button(self, text="login").grid(row=4, column = 0)
        #controller.show_frame("Chat")
 
    def validateLogin(self, username): #also need to add photo as an argument
        # need to validate username
        print("username entered : ", username.get())
        # take photo
        photo_capture()
        # compare name of file to photo that is already saved
        # if there is no saved photo, login is not validated
        # how to validate the photo?
        return
    
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
        photoButton = Button(self, text="take photo with webcam", command=lambda: [self.photoCapture(username), 
                            controller.db.collection('users').add({'username': username.get()}),
                            controller.show_frame("ChatEntry")]).grid(row=16, column=0)

    def photoCapture(self, username):
        enteredName = username.get()
        print("username entered: ", enteredName)
        photo_capture()
        #add photo and username to database 
        #make sure 
        return

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


if __name__ == "__main__":
    app = App()
    app.mainloop()
