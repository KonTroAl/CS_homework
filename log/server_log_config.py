import logging

logging.basicConfig(
    filename='client.log',
    format='%(asctime)s-10s %(levelname) %(module)s %(message)s',
    level=logging.INFO
)

server_log = logging.getLogger('my_server')

# Создание обработчкиов
server_hand = logging.FileHandler('my_client.log', encoding='utf-8')
server_hand.setLevel(logging.INFO)

server_log.addHandler(server_hand)
