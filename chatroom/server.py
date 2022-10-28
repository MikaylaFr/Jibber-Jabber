import threading
import socket
import sys
import select
from datetime import datetime
import json


# Resources:
# https://www.youtube.com/watch?v=sopNW98CRag

# Print to logs
# TODO Change output to file later (may not need this)
def print_log(message, exception = False):
    #f = open("logs.txt", "a")
    now = datetime.now()
    log = now.strftime("%H:%M:%S") + "  "
    log += message
    if exception:
        log += " Exception: " + exception
    print(log)
    #f.write(log)
    #f.close()

# Server Class
# Object representing the server that will receive and broadcast
# messages to all connected clients.
class Server:
    def __init__(self) -> None:
        # dict of clients represented as dict. 2D dict
        self.clients = {}
        self.buffer_size = 1024

    # Get the hosts ip address
    def set_ip_and_port(self, local, port) -> int:
        try:
            self.port = port
            if local:
                self.ip_address = "127.0.0.1"
            else:
                self.hostname = socket.gethostname()
                self.ip_address = socket.gethostbyname(self.hostname)
        except Exception:
            print_log("Error: Could not get host ip", Exception)
            return 1
                
    # Creates socket, binds socket, and sets socket to listening
    def create_server_socket(self) -> int:
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.ip_address, self.port))
            self.server_socket.listen()
            print_log("Socket created, listening on port " + self.port + ", with IP " + self.ip_address)
        except Exception:
            print_log("Error: Could not create socket", Exception)
            return 1

    def request_username(self, client_socket:any) -> any:
        if self.send_request(client_socket, "username"):
            return 1
        return client_socket.recv(self.buffer_size)

    def send_request(self, client_socket:any, request:str) -> int:
        message = {"type": "REQ","request": request}
        try:
            client_socket.send(bytes(json.dumps(message), encoding="utf-8"))
        except:
            print_log("Failed to get client's username")
            return 1

    # Listens for incoming connection. Once connection is found, requests username from the client
    # Adds all info to client dict. Creates a new thread to handle new client
    def listen_for_connections(self):
        while True:
            try:
                client_socket, address = self.server_socket.accept()
            except:
                print_log("Failed to accept connection")
                return 1
            print_log(f"New connection: {str(address)}")

            # Request username            
            client_username = self.request_username(client_socket)
            # Request for username failed, close connection and continue to listen
            if client_username == 1:
                print_log("Closing connection")
                client_socket.close()
                continue

            #Add to dict of clients
            self.clients[client_socket] = {"addr":address, "username":client_username}

            print_log(f"Username received: {client_username}")
            self.broadcast(f"{client_username} has connected...")

            # Create new thread to listen to client for incoming messages. 
            # Call handler for client connection
            thread = threading.Thread(target=self.listen_to_client, args=(client_socket, client_username))
            thread.start()

    def listen_to_client(self, client:any, username:str):
        while True:
            try:
                incoming_message = client.recv(1024)
                self.broadcast(incoming_message.decode("utf-8"), client, username)
            except:
                self.clients.pop(client)
                client.close()
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
            for curr_client in self.clients.keys():
                # Skip client that sent message
                if curr_client == client:
                    continue
                curr_client.send(bytes(json.dumps(broadcast_message), encoding="utf-8"))
        except:
            print_log("Could not send message")

    # TODO: Signal handler or variable to stop listening for connections and close server
    @classmethod
    def start_server(cls, local:bool = False, port:int = 1234)->object:
        new_server = cls()
        if new_server.set_ip_and_port(local, port) or new_server.create_server_socket():
            print_log("Could not start server!")
            return 1
        thread = threading.Thread(target=new_server.listen_for_connections, args=())
        thread.start()
        return new_server