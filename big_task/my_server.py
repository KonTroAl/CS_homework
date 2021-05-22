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
    'test': 'test'
}

usernames_friends = ['Julia']
usernames_auth = []
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
def user_authenticate(my_dict, client):
    # logger.info('start user_authenticate!')
    dict_auth_response = {}
    user = my_dict['user']
    for us in users.keys():
        if us == user['user_name']:
            usernames_auth.append(us)

    if user['user_name'] in usernames_auth and users[user['user_name']] == user['password']:
        dict_auth_response['response'] = 200
        dict_auth_response['alert'] = dict_signals[dict_auth_response['response']]
        print('authenticate completed!')
        logger.info('authenticate completed!')
        client.send(pickle.dumps(dict_auth_response))
        return dict_auth_response
    else:
        dict_auth_response['response'] = 402
        dict_auth_response['alert'] = dict_signals[dict_auth_response['response']]
        print('error!')
        logger.info('error!')
        client.send(pickle.dumps(dict_auth_response))
        return dict_auth_response


# Проверка присутствия пользователя
@server_log_dec
def presence_user(client):
    dict_probe = {
        'action': 'probe',
        'time': timestamp
    }
    client.send(pickle.dumps(dict_probe))
    pre_data = client.recv(1024)
    pre_data_load = pickle.loads(pre_data)
    print('Сообщение от клиента: ', pre_data_load, ', длиной ', len(pre_data), ' байт')
    return pre_data_load['action']


# Отправка сообщения другому пользователю
@server_log_dec
def message_send(client):
    msg_data = client.recv(1024)
    msg_data_load = pickle.loads(msg_data)
    msg_dict = {
        'time': timestamp
    }
    if list(msg_data_load['to'])[0].isalpha():
        for i in usernames_friends:
            if msg_data_load['to'] == i:
                msg_dict['response'] = 200
                msg_dict['alert'] = dict_signals[msg_dict['response']]
                print('message send!')
                logger.info('message send!')
                client.send(pickle.dumps(msg_dict))
                return msg_dict
            else:
                msg_dict['response'] = 404
                msg_dict['alert'] = dict_signals[msg_dict['response']]
                logger.info('пользователь/чат отсутствует на сервере')
                client.send(pickle.dumps(msg_dict))
                return msg_dict
    else:
        for i in room_names:
            if msg_data_load['to'] == i:
                msg_dict['response'] = 200
                print('message send!')
                logger.info('message send!')
                client.send(pickle.dumps(msg_dict))
                return msg_dict
            else:
                msg_dict['response'] = 404
                logger.info('пользователь/чат отсутствует на сервере')
                client.send(pickle.dumps(msg_dict))
                return msg_dict


def main():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', 8007))
    s.listen(5)
    logger.info('start connection!')
    client, addr = s.accept()
    n = 3

    while True:
        dict_welcome = {
            'action': 'join',
            'response': 100,
            'alert': dict_signals[100]
        }
        client.send(pickle.dumps(dict_welcome))

        user_data = pickle.loads(client.recv(1024))
        if user_data['action'] == 'authenticate':
            if user_authenticate(user_data, client)['response'] == 402:
                break

        presence_user(client)
        while pickle.loads(client.recv(1024)) == 'msg':
            message_send(client)

        client.send(pickle.dumps({'action': 'quit'}))

        s.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
