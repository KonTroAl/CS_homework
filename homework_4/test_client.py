import unittest
from big_task import my_client

users = {
    'KonTroAll': 'SpaceShip007'
}

usernames = ['KonTroAll']


class TestClient(unittest.TestCase):

    # для прохождения теста поменять assertNotEqual на assertEqual
    def test_user_reauth(self):
        self.assertNotEqual(my_client.user_authenticate('KonTroAll', 'SpaceShip007'), 409)
