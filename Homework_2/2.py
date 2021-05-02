# 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
# Написать скрипт, автоматизирующий его заполнение данными.
import json


# a. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date).
# Функция должна предусматривать запись данных в виде словаря в файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;

def write_order_to_json():
    item = "iphone"
    quantity = 5
    # цена указана в рублях
    price = 120000
    buyer = "Troshenkin_KA"
    date = "02.05.2021"

    dict_to_json = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date
    }
    with open('orders.json', 'w') as f:
        json.dump(dict_to_json, f, indent=4)

# b. Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.

write_order_to_json()

with open('orders.json') as f:
    print(f.read())