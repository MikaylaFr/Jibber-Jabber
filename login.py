# heavily sourced from: https://pythonexamples.org/python-tkinter-login-form/

from tkinter import *
from tkinter import ttk
from functools import partial
from photo_capture import photo_capture


def login():
    def validateLogin(username): #also need to add photo as an argument
        # need to validate username
        print("username entered : ", username.get())
        # how to validate the photo?
        
        return

    # window
    tkWindow = Tk()
    tkWindow.geometry('800x800')
    tkWindow.title('Jibber-Jabber User Login')

    # username label and text entry box
    usernameLabel = Label(tkWindow, text="username").grid(row=0, column=0)
    username=StringVar()
    usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)

    # partial funciton doesn't seem to be doing anything special since we called all the args?
    # validateLogin = partial(validateLogin, username)
    validateLogin = validateLogin(username)

    # login button
    loginButton = Button(tkWindow, text="Login", command=validateLogin).grid(row=4, column=0)

    # register button
    registerButton = Button(tkWindow, text="Create Account").grid(row=10, column=0)
    tkWindow.mainloop() 

login()
