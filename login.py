# heavily sourced from: https://pythonexamples.org/python-tkinter-login-form/

from tkinter import *
from functools import partial

def validateLogin(username, photo):
    # need to validate username
    print("username entered : ", username.get())
    # how to validate the photo?
    return

# window
tkWindow = Tk()
tkWindow.geometry('400x150')
tkWindow.title('Jibber-Jabber User Login')

#username label and text entry box
usernameLabel = Label(tkWindow, text="username").grid(row=0, column=0)
username=StringVar()
usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)

validateLogin = partial(validateLogin, username)

#login button
loginButton = Button(tkWindow, text="Login", command=validateLogin).grid(row=4, column=0)

tkWindow.mainloop()