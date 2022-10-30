from server import Server
from client import Client
from time import sleep

def main():
    # For testing
    choice = input("What you want?\n1. Server\n2. Client\n")
    if choice == "1":
        serv = Server.start_server(True)
    else:
        user_name = input("Whats your name?\n")
        client = Client.start_client("127.0.0.1", user_name)
    while True:
        #This should be replaced once GUI is initiated, since gui always loops
        sleep(5000)

if __name__=="__main__":
    main()