# 1. Задание на закрепление знаний по модулю CSV.
#    Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt
#    и формирующий новый «отчетный» файл в формате CSV.

#  a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными,
#  их открытие и считывание данных. В этой функции из считанных данных необходимо с помощью регулярных выражений
#  извлечь значения параметров «Изготовитель системы»,  «Название ОС», «Код продукта», «Тип системы».
#  Значения каждого параметра поместить в соответствующий список.
#  Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list.
#  В этой же функции создать главный список для хранения данных отчета — например,
#  main_data — и поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС»,
#  «Код продукта», «Тип системы». Значения для этих столбцов также оформить в виде списка
#  и поместить в файл main_data (также для каждого файла);

import csv

files = ['info_1.txt', 'info_2.txt', 'info_3.txt']


def get_data():
    # headers
    headers = []
    # Изготовитель системы
    os_prod_list = []
    # Название ОС
    os_name_list = []
    # Код продукта
    os_code_list = []
    # Тип системы
    os_type_list = []
    my_dict = {}
    main_data = [headers]

    for file in files:
        with open(file) as f:
            onstring = f.read().split("\n")[:-1]
            for i in onstring:
                my_list = i.split(':', maxsplit=1)
                for val in range(len(my_list) - 1):
                    my_dict[my_list[val]] = ' '.join(my_list[val + 1].split())
        for key, val in my_dict.items():
            if key == 'Изготовитель системы':
                os_prod_list.append(val)
            elif key == 'Название ОС':
                os_name_list.append(val)
            elif key == 'Код продукта':
                os_code_list.append(val)
            elif key == 'Тип системы':
                os_type_list.append(val)

    for key, val in my_dict.items():
        if key == 'Изготовитель системы':
            headers.append(key)
        elif key == 'Название ОС':
            headers.append(key)
        elif key == 'Код продукта':
            headers.append(key)
        elif key == 'Тип системы':
            headers.append(key)

    for i in range(len(files)):
        file_info = [os_name_list[i], os_code_list[i], os_prod_list[i], os_type_list[i]]
        main_data.append(file_info)

    return main_data


#  b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение
#  данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;

def write_to_csv():
    with open('main_data.csv', 'w') as file:
        file_writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        file_writer.writerows(get_data())


#  c. Проверить работу программы через вызов функции write_to_csv().

write_to_csv()

with open('main_data.csv') as f:
    print(f.read())
