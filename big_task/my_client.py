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
import log.client_log_config

logger = logging.getLogger('my_client')


users = {
    'KonTroAll': 'SpaceShip007'
}

usernames = ['KonTroAll']
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

authenticate = True
presence = False
user_user = True
user_all = True
my_test = False

try:

    logger.info('start connection')
    timestamp = int(time.time())
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('localhost', 8007))


    # вход на сервер
    logger.info('вход на сервер')
    welcome_data = s.recv(1024)
    print('Сообщение от сервера: ', pickle.loads(welcome_data), ', длиной ', len(welcome_data), ' байт')


    # Авторизация пользователя на сервере
    def user_authenticate(username, password):
        logger.info('start user_authenticate')
        dict_auth = {
            'action': 'authenticate',
            'time': timestamp,
            'user': {
                'user_name': username,
                'password': password
            }
        }
        s.send(pickle.dumps(dict_auth))
        data = s.recv(1024)
        load_data = pickle.loads(data)

        print('Сообщение от сервера: ', load_data, ', длиной ', len(data), ' байт')
        return load_data['response']


    for i in usernames:
        response = user_authenticate(i, users[i])
        if response == 200 or 409:
            presence = True

    # Проверка присутствия пользователя

    def user_presence():
        logger.info('start user_presence')
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
        return pickle.loads(probe_data)['action']

    if presence:
        print(user_presence())

    # Отправка сообщения другому пользователю
    def message_to_user(user_1, user_2, message):
        logger.info('start message_to_user')
        message_dict = {
            'action': 'msg',
            'time': timestamp,
            'to': user_2,
            'from': user_1,
            'encoding': 'utf-8',
            'message': message
        }
        s.send(pickle.dumps(message_dict))
        print('message send to user!')
        data_msg = s.recv(1024)
        data_msg_load = pickle.loads(data_msg)
        print('Сообщение от сервера: ', data_msg_load, ', длиной ', len(data_msg), ' байт')
        return data_msg_load['response']


    if user_user:
        message_to_user('KonTroAll', 'Julia', 'Hello world!')


    # Отправка сообщения в чат
    def message_to_all(user, room_name, message):
        logger.info('start message_to_all')
        message_dict = {
            'action': 'msg',
            'time': timestamp,
            'to': room_name,
            'from': user,
            'encoding': 'utf-8',
            'message': message
        }
        s.send(pickle.dumps(message_dict))
        print('message send!')
        data_msg = s.recv(1024)
        print('Сообщение от сервера: ', pickle.loads(data_msg), ', длиной ', len(data_msg), ' байт')
        return pickle.loads(data_msg)['response']


    if user_all:
        message_to_all('KonTroAll', '#smalltalk', 'Hello world!')

    # logout
    if authenticate:
        logger.info('logout from server')
        dict_logout = {
            'action': 'logout',
            'response': 102,
            'alert': dict_signals[102]
        }
        s.send(pickle.dumps(dict_logout))
        print('logout')

    # отключение от сервера
    quit_data = s.recv(1024)
    print('Сообщение от сервера: ', pickle.loads(quit_data), ', длиной ', len(quit_data), ' байт \n')
    logger.info('server quit')

    s.close()

except Exception as e:
    logger.critical(e)

    if my_test:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(('localhost', 8007))
        welcome_data = s.recv(1024)
        #
        # data = s.recv(1024)
        # quit_data= s.recv(1024)

