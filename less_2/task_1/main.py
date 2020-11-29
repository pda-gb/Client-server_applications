"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""
import csv
import os
import re
from chardet import detect

def get_unicode_file(_file):
    """переводим файлы в utf-8"""
    with open(_file, 'rb') as file:
        content_bytes = file.read()
        detect_encoding = detect(content_bytes)['encoding']
        if detect_encoding != 'utf-8':
            content_str = content_bytes.decode(detect_encoding)

            with open(_file, 'w', encoding='utf-8') as file:
                file.write(content_str)
                file.close()

    return _file

def get_data():
    """ собираем данные из файлов и формируем список из этих данных"""
    count_files_info = 0
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = []
    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта',
               'Тип системы']
    main_data.append(headers)

    # собираем список файлов в текущей папке
    path = '.'
    files = os.listdir(path)

    for file in files:
        if re.findall('info_*', file):
            count_files_info += 1
            file = get_unicode_file(file)
            file_info = open(file)
            data_of_file = file_info.read()

            os_prod_item = re.compile(r'Изготовитель системы:\s*\S*')
            os_prod_list.append(os_prod_item.findall(data_of_file)[0]
                                .split()[2])

            os_name_item = re.compile(r'Название ОС:\s*.*')
            # maxsplit=2 - разбиение по ' ' первые два раза
            # [2:][0] берем вхождение с инд. 2, т.к. оно будет являться
            # единичным списком, то возьмем первое значеение - [0]
            os_name_list.append(os_name_item.findall(data_of_file)[0]
                                .split(maxsplit=2)[2:][0])

            os_code_item = re.compile(r'Код продукта:\s*\S*')
            os_code_list.append(os_code_item.findall(data_of_file)[0]
                                .split()[2])

            os_type_item = re.compile(r'Тип системы:\s*\S*')
            os_type_list.append(os_type_item.findall(data_of_file)[0]
                                .split()[2])

    for i in range(0, count_files_info):
        row_in_main_data = [os_prod_list[i], os_name_list[i], os_code_list[i],
                            os_type_list[i]]
        main_data.append(row_in_main_data)

    return main_data

def write_to_csv(_file):
    data_to_write = get_data()
    with open(_file, 'w', encoding='utf-8') as file_to_write:
        file_writer = csv.writer(file_to_write, quoting=csv.QUOTE_NONNUMERIC)
        file_writer.writerows(data_to_write)

write_to_csv('my_report.csv')