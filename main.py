#from Login_GUI import LoginGuiInit
from tkinter import *
import sys
sys.path.append('chatroom')
from chatroom import client, server

class Gui(Tk):
    def __init__(self, admin_login=False):
        self.server, self.client, self.username, self.chat_room_running = None, None, None, False
        Tk.__init__(self)
        # frames go in the container
        self.container = Frame(self)
        self.container.pack(side="top", fill = "both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight = 1)
        self.title('Jibber-Jabber')
        self.frames = {}
        client.ChatGuiInit(container=self.container, main_gui=self)
        
        #self.frames["ChatRoom"]
        if not admin_login:
            #LoginGuiInit(container=container, main_gui=self)
            # self.frames.update(login_frames)
            # self.db = database
            #self.show_frame("StartPage")
            pass
        else:
            self.show_frame("ChatMenu")
        
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
    def onClose(self):
        if self.server:
            self.server.close_server()
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        app = Gui(True)
    else:
        app = Gui()
    app.protocol("WM_DELETE_WINDOW", app.onClose)
    app.mainloop()
