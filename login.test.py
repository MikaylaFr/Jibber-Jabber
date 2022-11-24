import unittest
import firebase_admin
from firebase_admin import firestore
from photo_capture import identify_user


class TestCase(unittest.TestCase):
    def test1(self):
        message = "something"
        self.assertTrue(identify_user('imageFromDB.jpg'))

