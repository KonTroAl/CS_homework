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
import multiprocessing

logger = logging.getLogger('my_server')

timestamp = int(time.time())

users = {
    'KonTroAll': 'SpaceShip007',
    'test': 'test',
    'test2': 'test2',
    'Julia': 'SpaceShuttle007'
}

usernames_friends = ['Julia', 'test']
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
def user_authenticate(my_dict, sock):
    logger.info('start user_authenticate!')
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
        sock.send(pickle.dumps(dict_auth_response))
        return dict_auth_response
    else:
        dict_auth_response['response'] = 402
        dict_auth_response['alert'] = dict_signals[dict_auth_response['response']]
        print('error!')
        logger.info('error!')
        sock.send(pickle.dumps(dict_auth_response))
        return dict_auth_response


# Проверка присутствия пользователя
@server_log_dec
def presence_user(client, sock):
    dict_probe = {
        'action': 'probe',
        'time': timestamp
    }

    sock.send(pickle.dumps(dict_probe))

    pre_data = client.recv(1024)
    pre_data_load = pickle.loads(pre_data)
    print('Сообщение от клиента: ', pre_data_load, ', длиной ', len(pre_data), ' байт')
    return pre_data_load['action']


# Отправка сообщения другому пользователю
@server_log_dec
def message_send(my_dict, sock):
    msg_dict = {
        'time': timestamp
    }
    if list(my_dict['to'])[0].isalpha():
        for i in usernames_friends:
            if my_dict['to'] == i:
                msg_dict['response'] = 200
                msg_dict['alert'] = dict_signals[msg_dict['response']]
                print('message send!')
                logger.info('message send!')
                sock.send(pickle.dumps(msg_dict))
                return msg_dict
            else:
                msg_dict['response'] = 404
                msg_dict['alert'] = dict_signals[msg_dict['response']]
                logger.info('пользователь/чат отсутствует на сервере')
                sock.send(pickle.dumps(msg_dict))
                return msg_dict


def message_room(my_dict, sock):
    msg_dict = {
        'time': timestamp
    }
    if my_dict['to'] in room_names:
        msg_dict['response'] = 200
        msg_dict['to'] = my_dict['to']
        msg_dict['from'] = my_dict['from']
        msg_dict['message'] = my_dict['message']
        return msg_dict
    else:
        msg_dict['response'] = 404
        logger.info('пользователь/чат отсутствует на сервере')
        sock.send(pickle.dumps(msg_dict))
        return msg_dict

def message_room_send(my_dict, w):
    for val in w:
        val.send(pickle.dumps(my_dict))
    print('message send!')
    logger.info('message send!')

def read_requests(r_clients, all_clients):
    """ Чтение запросов из списка клиентов
    """
    responses = {}  # Словарь ответов сервера вида {сокет: запрос}

    for sock in r_clients:
        try:
            data = pickle.loads(sock.recv(1024))
            responses[sock] = data
        except:
            print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
            all_clients.remove(sock)

    return responses


def main():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', 8007))
    s.listen(5)
    s.settimeout(0.2)
    logger.info('start connection!')
    clients = []

    while True:
        try:
            client, addr = s.accept()
        except OSError as e:
            pass
        else:
            print("Получен запрос на соединение от %s" % str(addr))
            clients.append(client)

        finally:
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [])
            except:
                pass

            requests = read_requests(r, clients)
            if requests:
                for sock in w:
                    if sock in requests:
                        if requests[sock]['action'] == 'authenticate':
                            if user_authenticate(requests[sock], sock)['response'] == 402:
                                break
                            presence_user(sock, sock)
                            requests.clear()
                        elif requests[sock]['action'] == 'msg':
                            if requests[sock]['to'][0].isalpha():
                                message_room_send(message_send(requests[sock], sock), w)
                            message_room_send(message_room(requests[sock], sock), w)
            # for sock in w:
            #     sock.send(pickle.dumps({'action': 'quit'}))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
