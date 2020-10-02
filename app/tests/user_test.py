import unittest
from app.models import User


class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.user = User(password="0000")

    def test_password_setter(self):
        self.assertTrue(self.user.password_hash is not None)

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.user.password

    def test_password_verification(self):
        self.assertTrue(self.user.verify_password('1111111'))