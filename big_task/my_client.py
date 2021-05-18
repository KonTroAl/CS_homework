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
from functools import wraps
import datetime

logger = logging.getLogger('my_client')

users = {
    'KonTroAll': 'SpaceShip007'
}

usernames_auth = []
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


# Авторизация пользователя на сервере
@client_log_dec
def user_authenticate(s):
    username = input('Enter your login: ')
    password = input('Enter your password: ')
    logger.info('start user_authenticate!')
    dict_auth = {
        'action': 'authenticate',
        'time': timestamp,
        'user': {
            'user_name': username,
            'password': password
        }
    }
    s.send(pickle.dumps(dict_auth))
    auth_data = s.recv(1024)
    auth_data_loads = pickle.loads(auth_data)
    if auth_data_loads['response'] == 200:
        usernames_auth.append(username)
    logger.info(auth_data_loads)
    print('Сообщение от сервера: ', pickle.loads(auth_data), ', длиной ', len(auth_data), ' байт')

    return dict_auth


# Проверка присутствия пользователя
@client_log_dec
def user_presence(s):
    logger.info('start user_presence!')
    pre_data = s.recv(1024)
    pre_data_load = pickle.loads(pre_data)
    if pre_data_load['action'] == 'probe':
        presence_dict = {
            'action': 'presence',
            'time': timestamp,
            'type': 'status',
            'user': {
                'username': 'KonTroAll',
                'status': 'I am still here!'
            }
        }
        s.send(pickle.dumps(presence_dict))
        return presence_dict
    else:
        return 'error!'


# Отправка сообщения другому пользователю
@client_log_dec
def message_send(s):
    user_choice = input("Для начала общения введите команду: 'msg', чтобы выйти введите: 'exit'")
    if user_choice == 'msg':
        to = input('Кому отправить сообщение: ')
        message = input('Enter message: ')
        logger.info('start message_to_user!')
        message_dict = {
            'action': 'msg',
            'time': timestamp,
            'to': to,
            'from': usernames_auth[0],
            'encoding': 'utf-8',
            'message': message
        }
        s.send(pickle.dumps(message_dict))
        message_user_data = s.recv(1024)
        logger.info(pickle.loads(message_user_data))
        print('Сообщение от сервера: ', pickle.loads(message_user_data), ', длиной ', len(message_user_data), ' байт')
        return message_dict
    elif user_choice == 'exit':
        return False
    else:
        return "Для начала общения введите команду: 'msg', чтобы выйти введите: 'exit': "


def user_activity(s):
    while True:
        if len(usernames_auth) == 0:
            welcome_data = s.recv(1024)
            logger.info(pickle.loads(welcome_data))
            print('Сообщение от сервера: ', pickle.loads(welcome_data), ', длиной ', len(welcome_data), ' байт')
            user_authenticate(s)

        if len(usernames_auth) == 0:
            break

        user_presence(s)
        while message_send(s):
            message_send(s)

        quit_data = s.recv(1024)
        logger.info(pickle.loads(quit_data))
        print('Сообщение от сервера: ', pickle.loads(quit_data), ', длиной ', len(quit_data), ' байт \n')


if __name__ == '__main__':
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('localhost', 8007))
    logger.info('start connection!')
    user_activity(s)
    s.close()
