# Функции клиента:
#     - сформировать presence-сообщение;
#     - отправить сообщение серверу;
#     - получить ответ сервера;
#     - разобрать сообщение сервера;
#     - параметры командной строки скрипта client.py <addr> [<port>]:
#         * addr — ip-адрес сервера;
#         * port — tcp-порт на сервере, по умолчанию 7777.


from socket import socket, AF_INET, SOCK_STREAM
import time
import pickle
import logging
import log.client_log_config
from functools import wraps
import datetime

logger = logging.getLogger('my_client')

users = {
    'KonTroAll': 'SpaceShip007'
}

usernames = ['KonTroAll']
room_names = ['#smalltalk']

dict_signals = {
    100: 'welcome!',
    101: 'do not come here!',
    102: 'logout',
    200: 'OOK!',
    201: 'created',
    202: 'accepted',
    400: 'неправильный запрос/JSON-объект',
    401: 'не авторизован',
    402: 'неправильный логин/пароль',
    403: 'пользователь заблокирован',
    404: 'пользователь/чат отсутствует на сервере',
    409: 'уже имеется подключение с указанным логином',
    410: 'адресат существует, но недоступен (offline)',
    500: 'ошибка сервера'
}

authenticate = True
test = True

timestamp = int(time.time())


# декоратор
def client_log_dec(func):
    @wraps(func)
    def call(*args, **kwargs):
        res = func(*args, **kwargs)
        logger.info(f'{datetime.datetime.now()} Call {func.__name__}: {args}, {kwargs}')
        return res

    return call


def mockable(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__ + '_mock' if test == True else func.__name__
        print(func_name)
        result = func_name(*args, **kwargs)
        logger.info(f'{datetime.datetime.now()} Call {func.__name__}: {args}, {kwargs}')
        return result

    return wrapper


# Авторизация пользователя на сервере
@mockable
@client_log_dec
def user_authenticate(username, password):
    logger.info('start user_authenticate!')
    dict_auth = {
        'action': 'authenticate',
        'time': timestamp,
        'user': {
            'user_name': username,
            'password': password
        }
    }
    return dict_auth


def user_authenticate_mock():
    logger.info('start user_authenticate!')
    dict_auth = {
        'action': 'authenticate',
        'time': timestamp,
        'user': {
            'user_name': 'KonTroAll',
            'password': 'SpaceShip007'
        }
    }
    return dict_auth


# Проверка присутствия пользователя
@client_log_dec
def user_presence(my_dict):
    logger.info('start user_presence!')
    if my_dict['action'] == 'probe':
        presence_dict = {
            'action': 'presence',
            'time': timestamp,
            'type': 'status',
            'user': {
                'username': 'KonTroAll',
                'status': 'I am still here!'
            }
        }
        return presence_dict
    else:
        return 'error!'


# Отправка сообщения другому пользователю
@client_log_dec
def message_to_user(user_1, user_2, message):
    logger.info('start message_to_user!')
    message_dict = {
        'action': 'msg',
        'time': timestamp,
        'to': user_2,
        'from': user_1,
        'encoding': 'utf-8',
        'message': message
    }
    return message_dict


# Отправка сообщения в чат
@client_log_dec
def message_to_all(user, room_name, message):
    logger.info('start message_to_all!')
    message_dict = {
        'action': 'msg',
        'time': timestamp,
        'to': room_name,
        'from': user,
        'encoding': 'utf-8',
        'message': message
    }
    return message_dict


if __name__ == '__main__':
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('localhost', 8007))
    logger.info('start connection!')

    # вход на сервер
    welcome_data = s.recv(1024)
    logger.info(pickle.loads(welcome_data))
    print('Сообщение от сервера: ', pickle.loads(welcome_data), ', длиной ', len(welcome_data), ' байт')

    # Авторизация пользователя на сервере
    a = user_authenticate('KonTroAll', 'SpaceShip007')
    s.send(pickle.dumps(a))
    auth_data = s.recv(1024)
    auth_data_loads = pickle.loads(auth_data)
    logger.info(auth_data_loads)
    print('Сообщение от сервера: ', pickle.loads(auth_data), ', длиной ', len(auth_data), ' байт')

    if auth_data_loads['response'] == 200 or 409:
        # проверка присутствия
        pre_data = s.recv(1024)
        logger.info(pickle.loads(pre_data))
        print('Сообщение от сервера: ', pickle.loads(pre_data), ', длиной ', len(pre_data), ' байт')
        s.send(pickle.dumps(user_presence(pickle.loads(pre_data))))

        # отправка сообщения пользователю
        s.send(pickle.dumps(message_to_user('KonTroAll', 'Julia', 'Hello world!')))
        message_user_data = s.recv(1024)
        logger.info(pickle.loads(message_user_data))
        print('Сообщение от сервера: ', pickle.loads(message_user_data), ', длиной ', len(message_user_data), ' байт')

        # отправка сообщения в чат
        s.send(pickle.dumps(message_to_all('KonTroAll', '#smalltalk', 'Hello world!')))
        message_room_data = s.recv(1024)
        logger.info(pickle.loads(message_room_data))
        print('Сообщение от сервера: ', pickle.loads(message_room_data), ', длиной ', len(message_room_data), ' байт')

        # logout
        logger.info('start logout!')
        dict_logout = {
            'action': 'logout',
            'response': 102,
            'alert': dict_signals[102]
        }
        s.send(pickle.dumps(dict_logout))
    else:
        print('Error!')

    # отключение от сервера
    quit_data = s.recv(1024)
    logger.info(pickle.loads(quit_data))
    print('Сообщение от сервера: ', pickle.loads(quit_data), ', длиной ', len(quit_data), ' байт \n')
    s.close()
