import unittest
import firebase_admin
from firebase_admin import firestore
import photo_capture
from photo_capture import identify_user


class TestCase(unittest.TestCase):
    def test1(self):
        message = "something"
        self.assertTrue(identify_user('imageFromDB.jpg'))

if __name__ == "__main__":
    unittest.main(verbosity=2,failfast=True)