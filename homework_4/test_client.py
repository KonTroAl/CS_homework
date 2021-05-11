import unittest
from big_task.my_client import user_authenticate, message_to_user, message_to_all, user_presence




class TestClient(unittest.TestCase):

    # для прохождения всех тестов поменять assertNotEqual на assertEqual

    def test_user_reauth(self):
        self.assertNotEqual(user_authenticate('KonTroAll', 'SpaceShip007'), 409)

    def test_user_presence(self):
        self.assertEqual(user_presence(), 'probe')

    def test_user_to_user_message(self):
        self.assertEqual(message_to_user('KonTroAll', 'Julia', 'Hello world!'), 200)

    def test_user_to_all_message(self):
        self.assertEqual(message_to_all('KonTroAll', '#smalltalk', 'Hello world!'), 200)


if __name__ == "__main__":
    unittest.main()