import unittest
from big_task import my_client



class TestClient(unittest.TestCase):
    def test_user_auth(self):
        self.assertEqual(my_client.user_authenticate('KonTroAll', 'SpaceShip007'), '200')
