import threading
import socket
import json
from tkinter import *
import tkinter.scrolledtext
from server import Server

def ChatGuiInit(container, main_gui):
    # Instantiate chat frames
    main_gui.frames["ChatMenu"] = ChatMenu.main_menu(parent=container, controller=main_gui)
    main_gui.frames["ChatMenu"].grid(row=0, column=0, sticky="nsew")
    main_gui.frames["StartServer"] = ChatMenu.start_server(parent=container, controller=main_gui)
    main_gui.frames["StartServer"].grid(row=0, column=0, sticky="nsew")
    main_gui.frames["ConnectToServer"] = ChatMenu.connect_to_server(parent=container, controller=main_gui)
    main_gui.frames["ConnectToServer"].grid(row=0, column=0, sticky="nsew")
    main_gui.frames["ChatRoom"] = ChatMenu.ChatRoom(parent=container, controller=main_gui)
    main_gui.frames["ChatRoom"].grid(row=0, column=0, sticky="nsew")

class ChatMenu(Frame):
    @classmethod
    def main_menu(cls, parent, controller):
        menu_frame = cls()
        Frame.__init__(menu_frame, parent)
        menu_frame.controller = controller
        #login button
        create_server_button = Button(menu_frame, text="Start Server", command=lambda: controller.show_frame("StartServer"))
        #register button
        connect_to_server = Button(menu_frame, text="Connect to a Server", command=lambda: controller.show_frame("ConnectToServer"))
        create_server_button.pack()
        connect_to_server.pack()
        return menu_frame

    @classmethod
    def start_server(cls, parent, controller):
        menu_frame = cls()
        Frame.__init__(menu_frame, parent)
        menu_frame.controller = controller
        def create_server_local():
            controller.server = Server.start_server(local=True)
            if not controller.username:
                controller.show_frame("ConnectToServer")
            else:
                print(controller.server.ip_address)
                controller.client = Client.start_client(ip=controller.server.ip_address,user=controller.username, controller=controller)
                controller.show_frame("ChatRoom")
        local_ip_button = Button(menu_frame, text="Use Local IP", command=lambda: create_server_local())
        local_ip_button.pack()
        public_ip_button = Button(menu_frame, text="Use Public IP", command=lambda: create_server_public())
        public_ip_button.pack()
        #TODO Implement getting public ip
        def create_server_public():
           pass
           #controller.server = Server.start_server()  
        return menu_frame

    @classmethod
    def connect_to_server(cls, parent, controller):
        menu_frame = cls()
        Frame.__init__(menu_frame, parent)
        menu_frame.controller = controller
        user_ip_label = Label(menu_frame, text="Server's IP")
        user_ip_label.pack()
        user_ip = Entry(menu_frame)
        user_ip.insert(0, "127.0.0.1")
        user_ip.pack()
        user_port_label= Label(menu_frame, text="Server's Port")
        user_port_label.pack()
        user_port = Entry(menu_frame)
        user_port.insert(0, "1234")
        user_port.pack()
        if not controller.username:
            user_name_label= Label(menu_frame, text="Username - Required")
            user_name_label.pack()
            user_name = Entry(menu_frame)
            user_name.pack()
        submit_button = Button(menu_frame, text="Connect", command=lambda: create_client())
        submit_button.pack()
        def create_client(ip:str="local", port:int=1234):
            ip=user_ip.get()
            port=int(user_port.get())
            username = user_name.get()
            controller.client=Client.start_client(ip=ip,controller=controller,user=username,port=port)
            controller.show_frame("ChatRoom")
        return menu_frame

    # TODO Implement return to menu
    @classmethod
    def ChatRoom(cls, parent, controller):
        chat_frame = cls()
        Frame.__init__(chat_frame, parent)
        chat_frame.controller = controller
        chat_frame.config(bg="Orange")
        chat_label = Label(chat_frame, text="Chat Room", bg="Orange")
        chat_label.config(font=("Ubuntu", 14))
        chat_label.pack(padx=20, pady=5)
        chat_frame.text_area = tkinter.scrolledtext.ScrolledText(chat_frame, font=("Ubuntu", 12))
        chat_frame.text_area.pack(padx=20, pady=5)
        chat_frame.text_area.config(state="disabled")

        msg_label = Label(chat_frame, text="Message", bg="Orange")
        msg_label.config(font=("Ubuntu", 14))
        msg_label.pack(padx=20, pady=5)

        chat_frame.input_area = Entry(chat_frame, width=100)
        chat_frame.input_area.pack(padx=10,pady=5)

        send_button = Button(chat_frame, text="Send", command=lambda: controller.client.listen_user_input())
        send_button.pack()
        controller.chat_room_running = True
        return chat_frame


class Client:
    def __init__(self)->None:
        self.socket = None
        self.buffer_size = 1024
        self.write_thread = None
        self.read_thread = None
        self.username = None

    def print_message(self, msg:str, user:str=None):
        if self.controller.chat_room_running:
            text_area = self.controller.frames["ChatRoom"].text_area
            text_area.config(state="normal")
            if user == "self":
                full_msg = "You: " + msg + '\n'
            elif user:
                full_msg = user + ":  " + msg + '\n'
            else:
                full_msg = msg + '\n'
            text_area.insert('end', full_msg)
            text_area.yview('end')
            text_area.config(state="disabled")

    def set_username(self, name:str):
        self.username = name

    def connect_to_server(self, ip:str, port:int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip,port))

    def send_message_to_server(self, msg:str):
        try:
            self.socket.send(msg.encode("utf-8"))
        except Exception as err:
            print(f"Could not send message to server Exception: {err}") 

    def handle_req(self, msg):
        if msg["request"] == "username":
            self.send_message_to_server(self.username)
        else:
            print("unkown req received")
            
    def handle_stat(self, msg):
        if msg["msg"] == "Server is shutting down...":
            self.print_message(msg["msg"])
            self.close_client()
        else:
            self.print_message(msg["msg"])
    
    def handle_message(self, msg:str):
        # Convert message to dict
        message = json.loads(msg)
        type_msg = message["type"]

        if type_msg == "REQ":
            self.handle_req(message)
        elif type_msg == "STAT":
            self.handle_stat(message)
        elif type_msg == "CHAT":
            self.print_message(message["msg"], message["user"])

    def listen_to_server(self):
        while True:
            try:
                message = self.socket.recv(self.buffer_size).decode("utf-8")
            except Exception as err:
                self.print_message(msg="Lost connection to server...", user="self")
                self.socket.close()
                self.socket = None
                break
            self.handle_message(message)

    def listen_user_input(self):
        if self.socket:
            chat_frame = self.controller.frames["ChatRoom"]
            chat = chat_frame.input_area.get()
            chat_frame.input_area.delete(0, END)
            self.send_message_to_server(chat)
            self.print_message(msg=chat, user="self")

    @classmethod
    def start_client(cls, controller, ip:str, user:str, port:int = 1234):
        new_client = cls()
        new_client.controller = controller
        new_client.set_username(user)
        new_client.connect_to_server(ip, int(port))
        new_client.listen_server_thread = threading.Thread(target=new_client.listen_to_server)
        new_client.listen_server_thread.daemon = True
        new_client.listen_server_thread.start()
        return new_client

    def close_client(self):
        self.socket.close()
