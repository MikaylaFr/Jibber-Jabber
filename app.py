# heavily sourced from: https://pythonexamples.org/python-tkinter-login-form/
# and https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter/7557028#7557028

from tkinter import *
from tkinter import ttk
from functools import partialmethod
from photo_capture import photo_capture

class App(Tk): 
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # frames go in the container
        container = Frame(self)
        container.pack(side="top", fill = "both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}
        self.frames["StartPage"] = StartPage(parent=container, controller=self)
        self.frames["Login"] = Login(parent=container, controller=self)
        self.frames["Register"] = Register(parent=container, controller = self)
        self.frames["ConfirmRegistration"] = ConfirmRegistration(parent=container, controller=self)
        self.frames["Chat"] = Chat(parent=container, controller=self)

        self.frames["StartPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["Login"].grid(row=0, column = 0, sticky="nsew")
        self.frames["Register"].grid(row=0, column=0, sticky="nsew")
        self.frames["ConfirmRegistration"].grid(row=0, column=0, sticky="nsew")
        self.frames["Chat"].grid(row=0, column=0, sticky="nsew")

        #show the first frame when the app opens
        self.show_frame("StartPage")

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
        loginButton2 = Button(self, text="Login", command=lambda: [self.validateLogin(username), controller.show_frame("Chat")]).grid(row=4, column=0)
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
        username = StringVar()
        usernameEntry = Entry(self, textvariable=username).grid(row=4, column=0)
        photoLabel = Label(self, text="take webcam photo for facial recognition login in lieu of password").grid(row=8, column=0)
        photoButton = Button(self, text="take photo with webcam", command=lambda: [self.photoCapture(username), controller.show_frame("Chat")]).grid(row=12, column=0)

    def photoCapture(self, username):
        print("username entered: ", username.get())
        photo_capture()
        return

class ConfirmRegistration(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        #if photo was good, take user to chat page, if photo was bad, retake photo...

class Chat(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        chatLabel = Label(self, text="Jibber Jabber here").grid(row=0, column=2)


if __name__ == "__main__":
    app = App()
    app.mainloop()
