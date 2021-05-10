import unittest
from big_task import my_client

users = {
    'KonTroAll': 'SpaceShip007'
}

usernames = ['KonTroAll']

user_auth = False


class TestClient(unittest.TestCase):

    # для прохождения теста поменять assertNotEqual на assertEqual

    def test_user_reauth(self):
        self.assertNotEqual(my_client.user_authenticate('KonTroAll', 'SpaceShip007'), 409)

    def test_user_to_user_message(self):
        self.assertEqual(my_client.message_to_user('KonTroAll', 'Julia', 'Hello world!'), 200)
