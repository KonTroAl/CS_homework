# Функции клиента:
#     - сформировать presence-сообщение;
#     - отправить сообщение серверу;
#     - получить ответ сервера;
#     - разобрать сообщение сервера;
#     - параметры командной строки скрипта client.py <addr> [<port>]:
#         * addr — ip-адрес сервера;
#         * port — tcp-порт на сервере, по умолчанию 7777.

from socket import *
import time
import pickle

timestamp = int(time.time())
s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 8007))

users = {
    'KonTroAll': 'SpaceShip007'
}

usernames = ['KonTroAll']

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

authenticate = True
presence = False
signal_409 = False
user_user = True

# Авторизация пользователя на сервере
if authenticate:
    for i in usernames:
        dict_auth = {
            'action': 'authenticate',
            'time': timestamp,
            'user': {
                'user_name': i,
                'password': users[i]
            }
        }
        s.send(pickle.dumps(dict_auth))
        data = s.recv(1024)
        load_data = pickle.loads(data)
        print('Сообщение от сервера: ', load_data, ', длиной ', len(data), ' байт')
        if load_data['response'] == 200:
            presence = True

    # Проверка сигнала 409
if signal_409:
    dict_auth = {
        'action': 'authenticate',
        'time': timestamp,
        'user': {
            'user_name': 'KonTroAll',
            'password': users['KonTroAll']
        }
    }
    s.send(pickle.dumps(dict_auth))
    data_2 = s.recv(1024)
    load_data_2 = pickle.loads(data_2)
    print('Сообщение от сервера: ', load_data_2, ', длиной ', len(data_2), ' байт')


if presence:
    probe_data = s.recv(1024)
    print('Сообщение от сервера: ', pickle.loads(probe_data), ', длиной ', len(probe_data), ' байт')
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

if user_user:
    message_dict = {
        'action': 'msg',
        'time': timestamp,
        'to': 'Julia',
        'from': 'KonTroAll',
        'encoding': 'utf-8',
        'message': 'Привет!'
    }
    s.send(pickle.dumps(message_dict))
    print('message send!')
    data_msg = s.recv(1024)
    print('Сообщение от сервера: ', pickle.loads(data_msg), ', длиной ', len(data_msg), ' байт')


quit_data = s.recv(1024)
print('Сообщение от сервера: ', pickle.loads(quit_data), ', длиной ', len(quit_data), ' байт')
s.close()
