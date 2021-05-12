# 2. В каждом модуле выполнить настройку соответствующего логгера по следующему алгоритму:
#   a. Создание именованного логгера;
#   b. Сообщения лога должны иметь следующий формат: "<дата-время> <уровень_важности> <имя_модуля> <сообщение>";
#   c. Журналирование должно производиться в лог-файл;
#   d. На стороне сервера необходимо настроить ежедневную ротацию лог-файлов.
# 3. Реализовать применение созданных логгеров для решения двух задач:
#   a. Журналирование обработки исключений try/except. Вместо функции print() использовать журналирование и обеспечить вывод служебных сообщений в лог-файл;
#   b. Журналирование функций, исполняемых на серверной и клиентской сторонах при работе мессенджера.

import logging

logging.basicConfig(
    filename='my_client.log',
    format = "%(asctime)s %(levelname)s %(module)-10s %(message)s",
    level= logging.INFO
)

logger = logging.getLogger('my_client')

# Создание обработчкиов
# client_hand = logging.FileHandler('my_client.log', encoding='utf-8')
# client_hand.setLevel(logging.INFO)
#
# logger.addHandler(client_hand)

if __name__ == '__main__':
    # Создаем потоковый обработчик логирования (по умолчанию sys.stderr):
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    logger.addHandler(console)
    logger.info('Тестовый запуск логирования')