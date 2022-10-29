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
        cls.server = Server()
        cls.server.set_port(1234)
        cls.server.set_ip(True)
        cls.server.create_server_socket()
        cls.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def test_7_accept_connection(self):
        thread = threading.Thread(target=self.server.accept_connection, args=(True,))
        thread.start()
        self.assertEqual(None, self.client.connect((self.server.ip_address, self.server.port)))
    
    @classmethod
    def tearDown(self) -> None:
        self.client.close()
        self.server.server_socket.close()
        self.server.test_client.close()

class ServerClientInitComms(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = Server()
        cls.server.set_port(1234)
        cls.server.set_ip(True)
        cls.server.create_server_socket()

        cls.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.thread = threading.Thread(target=cls.server.accept_connection, args=(True,))
        cls.thread.start()
        cls.client.connect((cls.server.ip_address, cls.server.port))
        cls.client_rcv_buffer = None

    def test_8_send_request(self):
        def client_recv_thread(self):
            buffer = self.client.recv(1024).decode("utf-8")
            self.client_rcv_buffer = json.loads(buffer)
        thread = threading.Thread(target=client_recv_thread, args=(self,))
        thread.start()
        self.assertEqual(None, self.server.send_request(self.server.test_client, "testing"))
        expected = {"type": "REQ", "request": "testing"}
        self.assertEqual(self.client_rcv_buffer, expected)
        

    @classmethod
    def tearDown(self) -> None:
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