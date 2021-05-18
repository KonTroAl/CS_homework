# Функции сервера:
#     - принимает сообщение клиента;
#     - формирует ответ клиенту;
#     - отправляет ответ клиенту;
#     - имеет параметры командной строки:
#         * -p <port> — TCP-порт для работы (по умолчанию использует 7777);
#         * -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).


from socket import socket, AF_INET, SOCK_STREAM
import time
import pickle
import logging
from functools import wraps
import datetime

logger = logging.getLogger('my_server')

timestamp = int(time.time())

users = {
    'KonTroAll': 'SpaceShip007',
}

usernames_friends = ['Julia']
room_names = ['#smalltalk']

dict_signals = {
    100: 'welcome!',
    101: 'do not come here!',
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




def server_log_dec(func):
    @wraps(func)
    def call(*args, **kwargs):
        res = func(*args, **kwargs)
        logger.info(f'{datetime.datetime.now()} Call {func.__name__}: {args}, {kwargs}')
        return res

    return call


# Авторизация пользователя на сервере
@server_log_dec
def user_authenticate(client):
    # logger.info('start user_authenticate!')
    auth_data = client.recv(1024)
    auth_data_load = pickle.loads(auth_data)
    if auth_data_load['action'] == 'authenticate':
        user = auth_data_load['user']
        for us, pas in users.items():
            for val in user.values():
                if us == val and pas == user['password']:
                    dict_auth_response = {
                        'response': 200,
                        'alert': dict_signals[200]
                    }
                    print('authenticate completed!')
                    logger.info('authenticate completed!')
                    return dict_auth_response
                else:
                    dict_auth_response = {
                        'response': 402,
                        'error': dict_signals[402]
                    }
                    print('error!')
                    logger.info('error!')
                    return dict_auth_response
    # else:
    #     dict_auth_response = {
    #         'response': 409,
    #         'error': dict_signals[409]
    #     }
    #     print('Someone is already connected with the given user name!')
    #     return dict_auth_response


# Проверка присутствия пользователя
@server_log_dec
def presence_user(my_dict):
    # logger.info('start presence_user!')
    print('Сообщение от клиента: ', my_dict, ', длиной ', len(my_dict), ' байт')
    return my_dict['action']


# Отправка сообщения другому пользователю
@server_log_dec
def message_to_user(my_dict):
    # logger.info('start message_to_user!')
    if my_dict['action'] == 'msg':
        if list(my_dict['to'])[0].isalpha():
            for i in usernames_friends:
                if my_dict['to'] == i:
                    msg_dict = {
                        'response': 200,
                        'time': timestamp,
                        'alert': dict_signals[200]
                    }
                    print('message send!')
                    logger.info('message send!')
                    return msg_dict
                else:
                    msg_dict = {
                        'response': 404,
                        'time': timestamp,
                        'alert': dict_signals[404]
                    }
                    logger.info('пользователь/чат отсутствует на сервере')
                    return msg_dict


# Отправка сообщения в чат
@server_log_dec
def message_to_room(my_dict):
    # logger.info('start message_to_room!')
    if my_dict['action'] == 'msg':
        for i in room_names:
            if i == my_dict['to']:
                room_dict = {
                    'response': 200,
                    'time': timestamp,
                    'alert': dict_signals[200]
                }
                print('message send!')
                logger.info('message send!')
                return room_dict
            else:
                room_dict = {
                    'response': 404,
                    'time': timestamp,
                    'alert': dict_signals[404]
                }
                logger.info('пользователь/чат отсутствует на сервере')
                return room_dict


def user_activity(s):
    auth = False
    while True:
        client, addr = s.accept()
        dict_welcome = {
            'action': 'join',
            'response': 100,
            'alert': dict_signals[100]
        }
        client.send(pickle.dumps(dict_welcome))

        user_authenticate(client)

        if user_authenticate(client)['response'] == 200 or 409:
            auth = True

        client.close()

if __name__ == '__main__':
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', 8007))
    s.listen(5)
    logger.info('start connection!')
    user_activity(s)






