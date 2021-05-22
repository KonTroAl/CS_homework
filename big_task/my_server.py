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
import select

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
def user_authenticate(my_dict, w):
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
        for client in w:
            client.send(pickle.dumps(dict_auth_response))
            return dict_auth_response
    else:
        dict_auth_response['response'] = 402
        dict_auth_response['alert'] = dict_signals[dict_auth_response['response']]
        print('error!')
        logger.info('error!')
        for client in w:
            client.send(pickle.dumps(dict_auth_response))
            return dict_auth_response


# Проверка присутствия пользователя
@server_log_dec
def presence_user(client, w):
    dict_probe = {
        'action': 'probe',
        'time': timestamp
    }
    for sock in w:
        sock.send(pickle.dumps(dict_probe))

    pre_data = client.recv(1024)
    pre_data_load = pickle.loads(pre_data)
    print('Сообщение от клиента: ', pre_data_load, ', длиной ', len(pre_data), ' байт')
    return pre_data_load['action']


# Отправка сообщения другому пользователю
@server_log_dec
def message_send(client, w):
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
                for sock in w:
                    sock.send(pickle.dumps(msg_dict))
                    return msg_dict
            else:
                msg_dict['response'] = 404
                msg_dict['alert'] = dict_signals[msg_dict['response']]
                logger.info('пользователь/чат отсутствует на сервере')
                for sock in w:
                    sock.send(pickle.dumps(msg_dict))
                    return msg_dict
    else:
        for i in room_names:
            if msg_data_load['to'] == i:
                msg_dict['response'] = 200
                print('message send!')
                logger.info('message send!')
                for sock in w:
                    sock.send(pickle.dumps(msg_dict))
                    return msg_dict
            else:
                msg_dict['response'] = 404
                logger.info('пользователь/чат отсутствует на сервере')
                for sock in w:
                    sock.send(pickle.dumps(msg_dict))
                    return msg_dict


def read_requests(r_clients, all_clients):
    """ Чтение запросов из списка клиентов
    """
    responses = {}  # Словарь ответов сервера вида {сокет: запрос}

    for sock in r_clients:
        try:
            data = pickle.loads(sock.recv(1024))
            responses[sock] = data
            print(responses[sock])
            return data
        except:
            print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
            all_clients.remove(sock)


def main():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', 8007))
    s.listen(5)
    s.setblocking(False)
    logger.info('start connection!')
    clients = []

    n = 3

    while True:
        try:
            client, addr = s.accept()
        except OSError as e:
            pass
        else:
            print("Получен запрос на соединение от %s" % str(addr))
            clients.append(client)

            dict_welcome = {
                'action': 'join',
                'response': 100,
                'alert': dict_signals[100]
            }

            client.send(pickle.dumps(dict_welcome))
        finally:
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [])
            except:
                pass

            for sock in r:
                user_data = pickle.loads(sock.recv(1024))
                if user_data is None:
                    print('wait user request')
                elif user_data['action'] == 'authenticate':
                    if user_authenticate(user_data, w)['response'] == 402:
                        break

                presence_user(sock, w)

                user_message = pickle.loads(sock.recv(1024))
                if user_data is None:
                    print('wait user request')
                else:
                    while user_message == 'msg':
                        message_send(sock, w)

            # for sock in w:
            #     sock.send(pickle.dumps({'action': 'quit'}))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
