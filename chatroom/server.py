import threading
import socket
from datetime import datetime
import json
from cryptography.fernet import Fernet
import time


# Resources:
# https://www.youtube.com/watch?v=sopNW98CRag

# Print to logs
# TODO Change output to file later (may not need this)
def print_log(message, exception:Exception = None) -> str:
    f = open("logs.txt", "a")
    now = datetime.now()
    log = "Server: "
    log += now.strftime("%H:%M:%S") + ":  "
    log += message
    if exception:
        log += " Exception: " + str(exception)
    print(log)
    f.write(log + '\n')
    f.close()

# Server Class
# Object representing the server that will receive and broadcast
# messages to all connected clients.
class Server:
    def __init__(self) -> None:
        # dict of clients represented as dict. 2D dict
        self.clients = {}
        self.buffer_size = 1024
        self.ip_address = None
        self.port = None
        self.hostname = None
        self.server_socket = None
        self.test_client = None
        self.client_listen_threads = []
        self.listen_connections_thread = None
        self.lock = threading.Lock()

    # Get the hosts ip address
    def set_ip(self, ip:str = None):
        self.ip_address = ip
   
    # Set port
    def set_port(self, port:int):
        self.port = port

    # Creates socket, binds socket, and sets socket to listening
    def create_server_socket(self) -> int:
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.ip_address, self.port))
            self.server_socket.listen()
            print_log("Socket created, listening on port " + str(self.port) + ", with IP " + self.ip_address)
        except Exception as err:
            print_log("Error: Could not create socket", err)
            return 1

    def request_username(self, client_socket:any, test:bool = False) -> any:
        print_log("Requesting username")
        # Since we have to call accept_connection via a new thread, we are not able to 
        # get the new client socket created in accept() from the thread in the test unit
        if test:
            client_socket = self.test_client
        if self.send_request(client_socket, "username"):
            return 1
        return client_socket.recv(self.buffer_size).decode("utf-8")

    def send_request(self, client_socket:any, request:str) -> int:
        message = {"type": "REQ","request": request}
        try:
            client_socket.send(bytes(json.dumps(message), encoding="utf-8"))
        except Exception as err:
            print_log("Failed to send request", err)
            return 1
        
    def send_key(self, client_socket:any):
        message = {"type": "KEY","key":self.key.decode("utf-8")}
        try:
            print_log("Sending key")
            client_socket.send(bytes(json.dumps(message), encoding="utf-8"))
            time.sleep(0.1)
        except Exception as err:
            print_log("Failed to send key", err)
            return 1

    def accept_connection(self, test:bool=False) -> tuple:
        try:
            client_socket, address = self.server_socket.accept()
            print_log(f"New connection: {str(address)}")
            return (client_socket, address)
        except Exception as err:
            print_log("\nFailed to accept connection. Socket could be closed", err)
            return err
            
        # Because testing this indiv function, need to clean up within the thread
        if test:
            self.test_client = client_socket
            return (client_socket, address)
        
    # Listens for incoming connection. Once connection is found, requests username from the client
    # Adds all info to client dict. Creates a new thread to handle new client
    def listen_for_connections(self, test:bool=False):
        while True:
            try:
                client_socket, address = self.accept_connection()
            except TypeError:
                #Socket is closed
                break
            # Request username            
            client_username = self.request_username(client_socket)
            # Request for username failed, close connection and continue to listen
            if client_username == 1:
                print_log("Closing connection")
                client_socket.close()
                break
            
            self.send_key(client_socket=client_socket)
            #Add to dict of clients
            self.lock.acquire()
            self.clients[client_socket] = {"addr":address, "username":client_username}
            self.lock.release()
            if len(self.clients) == 1:
                self.broadcast(f"Chatroom created with IP {self.ip_address} on port {self.port}")

            print_log(f"Username received: {client_username}")
            self.broadcast(f"{client_username} has connected...")

            # Create new thread to listen to client for incoming messages. 
            # Call handler for client connection
            thread = threading.Thread(target=self.listen_for_client_message, args=(client_socket, client_username))
            thread.daemon = True
            thread.start()
            self.client_listen_threads.append(thread)

    def listen_for_client_message(self, client:any, username:str, test:bool=False):
        while True:
            if test:
                client = self.test_client
            try:
                incoming_message = client.recv(4096)
                self.broadcast(incoming_message.decode("utf-8"), client, username)
            except:
                self.lock.acquire()
                self.clients.pop(client)
                self.lock.release()
                client.close()
                self.broadcast(f"{username} has left the chat...")
                break
            
            if test:
                break

    # Send message to all clients. Encode default is UTF-8
    def broadcast(self, message:str, client:any=None, username:str=""):
        # Construct JSON to send
        broadcast_message = {}
        if client == None:
            broadcast_message["type"] = "STAT"
        else:
            broadcast_message["type"] = "CHAT"
            broadcast_message["user"] = username
        broadcast_message["msg"] = message

        try:
            self.lock.acquire()
            for curr_client in self.clients.keys():
                # Skip client that sent message
                if curr_client == client:
                    continue
                curr_client.send(bytes(json.dumps(broadcast_message), encoding="utf-8"))
            self.lock.release()
        except Exception as err:
            print_log("Could not send message", err)
            self.lock.release()

    def create_key(self):
        self.key = Fernet.generate_key()

    @classmethod
    def start_server(cls, port:int, ip:str)->object:
        new_server = cls()
        new_server.set_port(port)
        if new_server.set_ip(ip) or new_server.set_port(port) or new_server.create_server_socket():
            print_log("Could not start server!")
            return 1
        new_server.create_key()
        new_server.listen_connections_thread = threading.Thread(target=new_server.listen_for_connections, args=())
        new_server.listen_connections_thread.daemon = True
        new_server.listen_connections_thread.start()
        return new_server

    def close_server(self):
        print_log("Shutting down...")
        self.server_socket.close()
        self.broadcast("Server is shutting down...")
        self.lock.acquire()
        for client in self.clients.keys():
            client.close()
        self.lock.release()

