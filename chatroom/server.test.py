import unittest
import socket
from server import Server

class ServerTest(unittest.TestCase):
    def test_set_ip_default(self):
        server_obj = Server()
        result = server_obj.get_ip()

