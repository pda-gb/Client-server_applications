"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""
import yaml

include_list = ['qwe', 'asd', 'zxc', 'йцу']
int_number = 22
include_dict = {'qqq': '12 \u20BD', 'www': '23 \u20BD', 'eee': '34 \u20BD'}
dict_data = {'1key': include_list, '2key': int_number, '3key': include_dict}

with open('my_file.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(dict_data, file, default_flow_style=False, allow_unicode=True)

with open('my_file.yaml', 'r', encoding="utf-8") as file:
    data_from_file = yaml.load(file)

if dict_data == data_from_file:
    print('verify is OK!')
else:
    print('The file was written with an error !!!')
