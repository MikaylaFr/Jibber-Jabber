from http import server
import unittest
from server import Server
from server import print_log
from datetime import datetime
import io
import socket
from unittest.mock import Mock
import threading
import json
from time import sleep


class ServerSetupTests(unittest.TestCase):
    def setUp(self):
        self.test_server = Server()
    
    def test_1_print_log_message(self):
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        msg = "This is a test"
        expected_msg = time + ":  " + msg + "\n"

        with unittest.mock.patch('sys.stdout', new = io.StringIO()) as output:
            print_log(msg)
            self.assertEqual(output.getvalue(), expected_msg)
    
    def test_2_print_log_exception(self):
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        excpt = socket.error
        msg = "This is a test with exception"
        expected_msg = time + ":  " + msg + " Exception: " + str(excpt) + "\n"

        with unittest.mock.patch('sys.stdout', new=io.StringIO()) as output:
            print_log(msg, excpt)
            self.assertEqual(output.getvalue(), expected_msg)

    def test_3_set_port(self):
        test_port = 5000
        self.test_server.set_port(test_port)
        self.assertEqual(self.test_server.port, test_port)

    def test_4_set_ip(self):
        test_ip = "10.5.0.2"
        self.test_server.set_ip()
        self.assertEqual(test_ip, self.test_server.ip_address)

    def test_5_set_ip_default(self):
        self.test_server.set_ip(True)
        self.assertEqual("127.0.0.1", self.test_server.ip_address)

    def test_6_create_server_socket(self):
        self.test_server.set_ip(True)
        self.test_server.set_port(1234)
        self.test_server.create_server_socket()
        self.assertIsInstance(self.test_server.server_socket, socket.socket)
        self.test_server.server_socket.close()

class ServerAcceptConnectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print("Setting up class")
        cls.server = Server()
        cls.server.set_port(1234)
        cls.server.set_ip(True)
        cls.server.create_server_socket()
        cls.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def test_7_accept_connection(self):
        print("starting test 7")
        thread = threading.Thread(target=self.server.accept_connection, args=(True,))
        thread.start()
        self.assertEqual(None, self.client.connect((self.server.ip_address, self.server.port)))
    
    @classmethod
    def tearDownClass(self) -> None:
        self.client.close()
        self.server.server_socket.close()
        #self.server.test_client.close()

class ServerClientInitComms(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        print("Setting up comms class")
        cls.server = Server()
        cls.server.set_port(1234)
        cls.server.set_ip(True)
        cls.server.create_server_socket()

        print("Connecting client and server")
        cls.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.thread = threading.Thread(target=cls.server.accept_connection, args=(True,))
        cls.thread.start()
        cls.client.connect((cls.server.ip_address, cls.server.port))

    def test_8_send_request(self):
        print("Starting test 8")
        def client_recv_thread(self):
            buffer = self.client.recv(1024).decode("utf-8")
            #self.client_recv_buffer = json.loads(buffer)
            #print(self.client_recv_buffer)
            expected = '{"type": "REQ", "request": "testing"}'
            try:
                self.assertEqual(buffer, expected)
            except:
                print("fail")
        thread = threading.Thread(target=client_recv_thread, args=(self,))
        thread.start()
        # Give moment for client to start listening
        sleep(0.05)
        self.server.send_request(self.server.test_client, "testing")
        
        
        
    def test_9_request_username(self):
        def client_response():
            print("Waiting to receive message from server")
            server_req = self.client.recv(1024).decode("utf-8")
            print("Recd something")
            expected = '{"type": "REQ", "request": "username"}'
            self.assertEqual(server_req, expected)
            self.client.send("Testy Test".encode("utf-8"))
        thread = threading.Thread(target=client_response)
        thread.start()
        # Give moment for client to start listening
        sleep(0.1)
        print("Sending request")
        self.assertEqual(self.server.request_username(self.client, True).decode("utf-8"), "Testy Test")

    @classmethod
    def tearDownClass(self) -> None:
        self.client.close()
        self.server.server_socket.close()
        self.server.test_client.close()

# Load tests in order
def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    test_cases = [ServerSetupTests, ServerAcceptConnectionTests, ServerClientInitComms]
    for test_case in test_cases:
        tests = loader.loadTestsFromTestCase(test_case)
        suite.addTests(tests)
    return suite

if __name__ == "__main__":
    unittest.main(verbosity=2,failfast=True)