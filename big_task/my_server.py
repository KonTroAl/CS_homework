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
    'KonTroAll': 'SpaceShip007'
}
presence = False

while True:
    client, addr = s.accept()
    data = client.recv(1024)
    client_data = pickle.loads(data)


    if client_data['action'] == 'authenticate':
        user = client_data['user']
        for us, pas in users.items():
            for val in user.values():
                if us == val and pas == user['password']:
                    dict_auth_response = {
                        'response': 200,
                        'alert': 'authenticate completed!'
                    }
                    print('authenticate completed!')
                    presence = True
                    client.send(pickle.dumps(dict_auth_response))
                    break
                else:
                    dict_auth_response = {
                        'response': 402,
                        'error': 'This could be "wrong password" or "no account with that name"'
                    }
                    print('error!')
                    client.send(pickle.dumps(dict_auth_response))
                    break

    if presence:
        dict_probe = {
            'action': 'probe',
            'time': timestamp
        }
        client.send(pickle.dumps(dict_probe))

    client.send(pickle.dumps({'action': 'close'}))
    client.close()

