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
    main_data = []
    # Изготовитель системы
    os_prod_list = []
    # Название ОС
    os_name_list = []
    # Код продукта
    os_code_list = []
    # Тип системы
    os_type_list = []
    my_dict = {}
    for file in files:
        with open(file) as f:
            onstring = f.read().split("\n")[:-1]
            for i in onstring:
                my_list = i.split(':', maxsplit=1)
                for val in range(len(my_list) - 1):
                    my_dict[my_list[val]] = my_list[val + 1]
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
            main_data.append(key)
        elif key == 'Название ОС':
            main_data.append(key)
        elif key == 'Код продукта':
            main_data.append(key)
        elif key == 'Тип системы':
            main_data.append(key)


    return main_data, os_code_list, os_type_list, os_name_list, os_prod_list


print(get_data())
# with open('info_1.txt') as f:
#
#     for row in f:
#         print(row)

#  b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение
#  данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;

#  c. Проверить работу программы через вызов функции write_to_csv().
