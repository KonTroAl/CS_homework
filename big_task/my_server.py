# Функции сервера:
#     - принимает сообщение клиента;
#     - формирует ответ клиенту;
#     - отправляет ответ клиенту;
#     - имеет параметры командной строки:
#         * -p <port> — TCP-порт для работы (по умолчанию использует 7777);
#         * -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).


from socket import *
import time
import pickle

s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 8007))
s.listen(5)
timestamp = int(time.time())

users = {
    'KonTroAll': 'SpaceShip007',
    'Julia': 'SpaceShuttle008'
}

usernames = ['KonTroAll', 'Julia']

dict_signals = {
    100: 'welckome!',
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

presence = False

while True:
    client, addr = s.accept()
    data = client.recv(1024)
    client_data = pickle.loads(data)
    num_users = len(usernames)

    if client_data['action'] == 'authenticate' and presence == False:
        user = client_data['user']
        for us, pas in users.items():
            for val in user.values():
                if us == val and pas == user['password']:
                    dict_auth_response = {
                        'response': 200,
                        'alert': 'authenticate completed!'
                    }
                    print('authenticate completed!')
                    client.send(pickle.dumps(dict_auth_response))
                    num_users = num_users - 1
                    if num_users > 0:
                        presence = True
                    break
                else:
                    dict_auth_response = {
                        'response': 402,
                        'error': 'This could be "wrong password" or "no account with that name"'
                    }
                    print('error!')
                    client.send(pickle.dumps(dict_auth_response))
                    break
    else:
        dict_auth_response = {
            'response': 409,
            'error': 'Someone is already connected with the given user name'
        }
        print('error!')
        client.send(pickle.dumps(dict_auth_response))

    if presence:
        dict_probe = {
            'action': 'probe',
            'time': timestamp
        }
        client.send(pickle.dumps(dict_probe))
        presence_data = client.recv(1024)
        print('Сообщение от клиента: ', pickle.loads(presence_data), ', длиной ', len(presence_data), ' байт')

    client.send(pickle.dumps({'action': 'quit'}))
    client.close()
