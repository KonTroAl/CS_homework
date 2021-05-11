import unittest
import time
from big_task.my_server import presence_user, authenticate_user, message_to_user, message_to_all

timestamp = int(time.time())


class TestClient(unittest.TestCase):

    # для прохождения всех тестов поменять assertNotEqual на assertEqual

    def test_user_authenticate(self):
        dict_auth_test = {
            'action': 'authenticate',
            'time': timestamp,
            'user': {
                'user_name': 'KonTroAll',
                'password': 'SpaceShip007'
            }
        }
        self.assertNotEqual(authenticate_user(dict_auth_test), 'authenticate completed!')

    def test_user_presence(self):
        presence_dict = {
            'action': 'presence',
            'time': timestamp,
            'type': 'status',
            'user': {
                'username': 'KonTroAll',
                'status': 'I am still here!'
            }
        }
        self.assertNotEqual(presence_user(presence_dict), 'presence')

    def test_message_to_user(self):
        message_dict = {
            'action': 'msg',
            'time': timestamp,
            'to': 'Julia',
            'from': 'KonTroAll',
            'encoding': 'utf-8',
            'message': 'Hello world!'
        }
        self.assertNotEqual(message_to_user(message_dict), 'OOK!')

    def test_message_to_all(self):
        message_dict = {
            'action': 'msg',
            'time': timestamp,
            'to': '#smalltalk',
            'from': 'KonTroAll',
            'encoding': 'utf-8',
            'message': 'Hello world!'
        }
        self.assertNotEqual(message_to_all(message_dict), 'OOK!')


if __name__ == "__main__":
    unittest.main()
