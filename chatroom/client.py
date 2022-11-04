import threading
import socket
import json

class Client:
    def __init__(self)->None:
        self.socket = None
        self.buffer_size = 1024
        self.write_thread = None
        self.read_thread = None
        self.username = None

    # TODO Will be more fleshed out when introducting Gui
    def print_message(self, msg:str, user:str=None):
        if user == "self":
            pass
        elif user:
            print(user + ":  " + msg)
        else:
            print(msg)
        # Append sent message to text area

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
                print("Lost connection to server...")
                self.socket.close()
                break
            self.handle_message(message)

    def listen_user_input(self):
        self.print_message("Connected. Begin chatting...")
        while True:
            try:
                chat = input()
            except:
                break
            self.send_message_to_server(chat)
            self.print_message(chat, "self")

    @classmethod
    def start_client(cls, ip:str, port:1234, user:str):
        new_client = cls()
        new_client.set_username(user)
        new_client.connect_to_server(ip, port)
        # Make daemon process?
        new_client.listen_server_thread = threading.Thread(target=new_client.listen_to_server)
        new_client.listen_server_thread.daemon = True
        new_client.listen_server_thread.start()
        new_client.listen_user_input()
        return new_client

    def close_client(self):
        self.socket.close()
        self.listen_server_thread.daemon = True
