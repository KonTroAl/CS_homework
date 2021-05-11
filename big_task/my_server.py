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

s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 8007))
s.listen(5)
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

authenticate = True
presence = False
user_user = True
user_all = False
my_test = True

while True:
    client, addr = s.accept()

    # вход на сервер
    dict_welcome = {
        'action': 'join',
        'response': 100,
        'alert': dict_signals[100]
    }
    client.send(pickle.dumps(dict_welcome))

    # Авторизация пользователя на сервере
    if authenticate:
        data = client.recv(1024)
        client_data = pickle.loads(data)

        if client_data['action'] == 'authenticate' and presence == False:
            user = client_data['user']
            for us, pas in users.items():
                for val in user.values():
                    if us == val and pas == user['password']:
                        dict_auth_response = {
                            'response': 200,
                            'alert': dict_signals[200]
                        }
                        print('authenticate completed!')
                        client.send(pickle.dumps(dict_auth_response))
                        presence = True
                        break
                    else:
                        dict_auth_response = {
                            'response': 402,
                            'error': dict_signals[402]
                        }
                        print('error!')
                        client.send(pickle.dumps(dict_auth_response))
                        break
        else:
            dict_auth_response = {
                'response': 409,
                'error': dict_signals[409]
            }
            print('Someone is already connected with the given user name!')
            presence = True
            signal_409 = True
            client.send(pickle.dumps(dict_auth_response))


    # Проверка присутствия пользователя
    def presence_user():
        dict_probe = {
            'action': 'probe',
            'time': timestamp
        }
        client.send(pickle.dumps(dict_probe))
        presence_data = client.recv(1024)
        print('Сообщение от клиента: ', pickle.loads(presence_data), ', длиной ', len(presence_data), ' байт')
        return dict_probe['action']


    if presence:
        presence_user()

    # Отправка сообщения другому пользователю
    if user_user:
        if authenticate:
            msg_data = pickle.loads(client.recv(1024))
            if msg_data['action'] == 'msg':
                if list(msg_data['to'])[0].isalpha():
                    for i in usernames_friends:
                        if msg_data['to'] == i:
                            msg_dict = {
                                'response': 200,
                                'time': timestamp,
                                'alert': dict_signals[200]
                            }
                            client.send(pickle.dumps(msg_dict))
                        else:
                            msg_dict = {
                                'response': 404,
                                'time': timestamp,
                                'alert': dict_signals[404]
                            }
                            client.send(pickle.dumps(msg_dict))
        else:
            msg_data = pickle.loads(client.recv(1024))
            dict_not_auth = {
                'response': 401,
                'alert': dict_signals[401]
            }
            client.send(pickle.dumps(dict_not_auth))

    # Отправка сообщения в чат
    if user_all:
        if authenticate:
            msg_for_room_data = pickle.loads(client.recv(1024))
            if msg_for_room_data['action'] == 'msg':
                for i in room_names:
                    if i == msg_for_room_data['to']:
                        room_dict = {
                            'response': 200,
                            'time': timestamp,
                            'alert': dict_signals[200]
                        }
                        client.send(pickle.dumps(room_dict))
                    else:
                        room_dict = {
                            'response': 404,
                            'time': timestamp,
                            'alert': dict_signals[404]
                        }
                        client.send(pickle.dumps(room_dict))
        else:
            msg_for_room_data = pickle.loads(client.recv(1024))
            dict_not_auth = {
                'response': 401,
                'alert': dict_signals[401]
            }
            client.send(pickle.dumps(dict_not_auth))

    # logout
    if authenticate:
        print(pickle.loads(client.recv(1024)))

    # отключение от сервера
    client.send(pickle.dumps({'action': 'quit'}))

    client.close()
