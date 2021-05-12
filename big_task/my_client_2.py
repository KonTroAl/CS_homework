from socket import socket, AF_INET, SOCK_STREAM
import time
import pickle

timestamp = int(time.time())
s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 8007))

welcome_data = s.recv(1024)
print('Сообщение от сервера: ', pickle.loads(welcome_data), ', длиной ', len(welcome_data), ' байт')

quit_data = s.recv(1024)
print('Сообщение от сервера: ', pickle.loads(quit_data), ', длиной ', len(quit_data), ' байт \n')
