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

authenticate = True
presence = False

if authenticate:
    dict_auth = {
        'action': 'authenticate',
        'time': timestamp,
        'user': {
            'user_name': 'KonTroAll',
            'password': users['KonTroAll']
        }
    }
    s.send(pickle.dumps(dict_auth))
    data = s.recv(1024)
    load_data = pickle.loads(data)
    print('Сообщение от сервера: ', load_data, ', длиной ', len(data), ' байт')
    if load_data['response'] == 200:
        presence = True

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
s.close()
