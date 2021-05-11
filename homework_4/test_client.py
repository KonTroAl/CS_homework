import unittest
from task.my_client import user_authenticate, message_to_user




class TestClient(unittest.TestCase):

    # для прохождения теста поменять assertNotEqual на assertEqual

    def test_user_reauth(self):
        self.assertNotEqual(user_authenticate('KonTroAll', 'SpaceShip007'), 409)

    def test_user_to_user_message(self):
        self.assertEqual(message_to_user('KonTroAll', 'Julia', 'Hello world!'), 200)


if __name__ == "__main__":
    unittest.main()