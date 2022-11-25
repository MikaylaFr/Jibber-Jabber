import unittest
import photo_capture
from photo_capture import identify_user
from photo_capture import convert_to_byte_array
from photo_capture import convert_to_image


class PhotoTestCase(unittest.TestCase):
    def test1(self):
        self.assertTrue(identify_user('imageFromDB.jpg'))

    def test2(self):
        self.assertIsInstance(convert_to_byte_array('person.jpg'), bytes)

    def test3(self):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)