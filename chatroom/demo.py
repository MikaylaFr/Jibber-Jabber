from server import Server
from client import Client
from time import sleep
import signal


class Demo:
    def __init__(self) -> None:
        self.server = None
        self.client = None

    def main(self):
        print("Jibber jabber chat room demo")
        choice = input("What would you like to do?\n1. Start a chatroom\n2. Join to a chatroom\n")
        # Make server then start client
        if choice == '1':
            choice = input("Local IP?\n1. Yes-Uses local ip\n2. Uses public IP\n")
            if choice == "1":
                self.server = Server.start_server(True)
            else:
                self.server = Server.start_server()
            print(f"Server started on IP: {self.server.ip_address} on port {self.server.port}")
            username = input("Enter username:  ")
            self.client = Client.start_client(self.server.ip_address, self.server.port, username)
        #Start client
        else:
            connect_ip = input("Server IP: ")
            connect_port = int(input("Server Port: "))
            username = input("Enter your username: ")
            self.client = Client.start_client(connect_ip, connect_port, username)

    def signal_handler(self, signum, frame):
        if self.server:
            self.server.close()
        if self.client:
            self.client.close()
        exit(0)

if __name__=="__main__":
    demo = Demo()
    # Register handler
    signal.signal(signal.SIGINT, demo.signal_handler)
    demo.main()