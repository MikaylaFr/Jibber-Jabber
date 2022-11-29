import threading
import socket
import json
from tkinter import *
import tkinter.scrolledtext
from server import Server
from cryptography.fernet import Fernet

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
        create_server_button = Button(menu_frame, text="Start Server", command=lambda: controller.show_frame("StartServer"))
        connect_to_server = Button(menu_frame, text="Connect to a Server", command=lambda: controller.show_frame("ConnectToServer"))
        create_server_button.pack()
        connect_to_server.pack()
        return menu_frame

    @classmethod
    def start_server(cls, parent, controller):
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
        #if not controller.username:
            #username_label = Label(menu_frame, text="Username - Required")
            #username_label.pack()
            #username = Entry(menu_frame)
            #username.pack()
        create_server_button = Button(menu_frame, text="Start Server", command=lambda: create_server())
        create_server_button.pack()
        def create_server():
            controller.server = Server.start_server(port=int(user_port.get()), ip=user_ip.get())
            if not controller.username:
                controller.client = Client.start_client(controller=controller, ip=controller.server.ip_address, port=controller.server.port, user=controller.username)
            else:
                controller.client = Client.start_client(controller=controller, ip=controller.server.ip_address, port=controller.server.port, user=controller.username)
            controller.show_frame("ChatRoom")
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
        #if not controller.username:
            #user_name_label= Label(menu_frame, text="Username - Required")
            #user_name_label.pack()
            #user_name = Entry(menu_frame)
            #user_name.pack()
        submit_button = Button(menu_frame, text="Connect", command=lambda: create_client())
        submit_button.pack()
        cancel_button = Button(menu_frame, text="Cancel", command=lambda: controller.show_frame("ChatMenu"))
        cancel_button.pack()

        def create_client(ip:str="local", port:int=1234):
            ip=user_ip.get()
            port=int(user_port.get())
            username = controller.username
            controller.client=Client.start_client(ip=ip,controller=controller,user=username,port=port)
            controller.show_frame("ChatRoom")

        return menu_frame
    

    

    @classmethod
    def ChatRoom(cls, parent, controller):
        chat_frame = cls()
        Frame.__init__(chat_frame, parent)
        chat_frame.controller = controller
        chat_frame.config(bg="Orange")
        disconnect_button = Button(chat_frame, text="Disconnect",command=lambda: disconnect(chat_frame.controller))
        
        def disconnect(controller):
            chat_frame.text_area.delete("1.0", "end")
            controller.client.close_client()
            del controller.client
            controller.client = None
            if controller.server:
                controller.server.close_server()
                del controller.server
                controller.server = None
            controller.show_frame("ChatMenu")

        disconnect_button.grid(column=8,row=0)
        chat_label = Label(chat_frame, text="Chat Room", bg="Orange")
        chat_label.config(font=("Ubuntu", 14))
        chat_label.grid(column=2,row=0,sticky=N,columnspan=3)
        chat_frame.text_area = tkinter.scrolledtext.ScrolledText(chat_frame, font=("Ubuntu", 12), wrap=WORD)
        chat_frame.text_area.config(state="disabled")
        chat_frame.text_area.grid(row=1,column=0,columnspan=9,sticky=N,pady=10,padx=10)

        msg_label = Label(chat_frame, text="Message", bg="Orange")
        msg_label.config(font=("Ubuntu", 14))
        msg_label.grid(row=2,column=2,columnspan=3)

        chat_frame.input_area = Text(chat_frame, width=75, height=2,wrap=WORD)
        chat_frame.input_area.grid(row=3,column=0,columnspan=6,pady=10,padx=10)

        send_button = Button(chat_frame, text="Send", command=lambda: controller.client.listen_user_input())
        send_button.grid(row=3,column=8,columnspan=1)
        controller.chat_room_running = True
        return chat_frame


class Client:
    def __init__(self)->None:
        self.socket = None
        self.buffer_size = 1024
        self.write_thread = None
        self.read_thread = None
        self.username = None
        self.lock = threading.Lock()

    def print_message(self, msg:str, user:str=None):
        if self.controller.chat_room_running:
            self.lock.acquire()
            text_area = self.controller.frames["ChatRoom"].text_area
            text_area.config(state="normal")
            if user == "self":
                full_msg = "You: " + msg
            elif user:
                # Decrypt message
                msg = self.fernet_key.decrypt(msg).decode()
                full_msg = user + ":  " + msg
            else:
                full_msg = msg + '\n'
            text_area.insert('end', full_msg)
            text_area.yview('end')
            text_area.config(state="disabled")
            self.lock.release()

    def set_username(self, name:str):
        self.username = name

    def connect_to_server(self, ip:str, port:int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip,port))

    def send_message_to_server(self, msg:str):
        try:
            if type(msg) != bytes:
                self.socket.send(msg.encode("utf-8"))
            else:
                self.socket.send(msg)
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
    
    def handle_key(self, msg):
        self.encrypt_key = bytes(msg["key"], "utf-8")
        self.fernet_key = Fernet(self.encrypt_key)
    
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
        elif type_msg == "KEY":
            self.handle_key(message)

    def listen_to_server(self):
        while True:
            try:
                message = self.socket.recv(self.buffer_size).decode("utf-8")
                print("message:" + message)
                self.handle_message(message)
                print("message:" + message)
            except Exception as err:
                self.print_message(msg="Lost connection to server...", user="self")
                print(str(err))
                self.socket.close()
                self.socket = None
                break

    def listen_user_input(self):
        if self.socket:
            chat_frame = self.controller.frames["ChatRoom"]
            chat = chat_frame.input_area.get("1.0",END)
            chat_frame.input_area.delete("1.0", END)
            encrypted_chat = self.fernet_key.encrypt(bytes(chat, "utf-8"))
            self.send_message_to_server(encrypted_chat)
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
        if self.socket:
            self.socket.close()
