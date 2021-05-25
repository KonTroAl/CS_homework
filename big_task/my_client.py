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
from threading import Thread
from queue import Queue
import multiprocessing

logger = logging.getLogger('my_client')

users = {
    'KonTroAll': 'SpaceShip007',
    'test': 'test',
    'test2': 'test2',
    'Julia': 'SpaceShuttle007'
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
def user_authenticate(s, username, password):
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

    return auth_data_loads


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
                'username': usernames_auth[0],
                'status': 'I am still here!'
            }
        }
        s.send(pickle.dumps(presence_dict))
        return presence_dict
    else:
        return 'error!'


# Отправка сообщения другому пользователю
@client_log_dec
def message_send_user(s, to, message):
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


@client_log_dec
def message_send_room(s, to, msg):
    a = True
    # global turn
    # turn = True
    print('Для выхода из комнаты введите: q')
    while a:
        # Для реализации необходимо передавать в аргументах очередь, которая была создана при
        # инициализации multiprocessing
        message = input('Enter message: ')
        if message.upper() == 'Q':
            print('Выход из чата')
            break
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

    # turn = True

def message_recv(s, msg):
    while True:
        message_room_data_load = pickle.loads(s.recv(1024))
        message_room_data = message_room_data_load.get()
        logger.info(message_room_data)
        print(f'{message_room_data["to"]} from {message_room_data["from"]}: {message_room_data["message"]}')



def main(s):
    n = 3
    while True:
        start = input('Добро пожаловать! Хотите авторизоваться? (Y / N): ')
        if start.upper() == 'Y':
            username = input('Enter your login: ')
            password = input('Enter your password: ')
            if username in usernames_auth:
                auth_dict = {
                    'time': timestamp,
                    'response': 409,
                    'message': dict_signals[409]
                }
                print(auth_dict)
            else:
                if user_authenticate(s, username, password)['response'] == 402:
                    break

            user_presence(s)

            if input("Для начала общения введите команду: 'msg', чтобы выйти введите: 'exit': ") == 'msg':
                to = input('Кому отправить сообщение: ')
                if to[0].isalpha():
                    message = input('Enter message: ')
                    message_send_user(s, to, message)
                else:
                    msg = multiprocessing.JoinableQueue()
                    msg_p = multiprocessing.Process(target=message_recv, args=(s, msg,))
                    msg_p.daemon = True
                    msg_p.start()
                    message_send_room(s, to, msg)
                    msg_p.join()

            quit_data = s.recv(1024)
            logger.info(pickle.loads(quit_data))
            usernames_auth.clear()
            print('Сообщение от сервера: ', pickle.loads(quit_data), ', длиной ', len(quit_data), ' байт \n')
        else:
            print('До свидания!')
            break


if __name__ == '__main__':
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('localhost', 8007))
        logger.info('start connection!')
        main(s)
        s.close()
    except Exception as e:
        print(e)
