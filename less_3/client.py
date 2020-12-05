import json
import socket
import sys
import time

from less_3.common.utils import send_message, get_message
from less_3.common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR


def create_massage_a_presence(_account='Guest'):
    """
    Создаёт сообщение о присутствии клиента в сети, по умолчанию c аккантом -
    Гость.
    """
    _message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: _account
        }
    }
    return _message


def parsing_response(_server_response):
    """разбор ответа сервера"""

    if RESPONSE in _server_response:
        if _server_response[RESPONSE] == 200:
            return 'code : 200. OK, you are connected.'
        return f'code : {_server_response[RESPONSE]}. Error:' \
               f'{_server_response[ERROR]}'
    raise ValueError


def main():
    # запуск клиента с заданными параметрами или по дефолту.
    # пример: client.py -a XXX.XXX.XXX.XXX -p XXXX
    # с помощью sys.argv парсим параметры по ключам
    #  -a XXX.XXX.XXX.XXX
    try:
        if '-a' in sys.argv:
            ip_for_server_connect = int(sys.argv[sys.argv.index
                                                 ('-a') + 1])
        else:
            ip_for_server_connect = DEFAULT_IP_ADDRESS
        #  --- заготовка ---
        # port_for_client_connect, ip_for_client_connect = \
        # find_connections_parameters(client)
    except IndexError:
        print('После ключа -а не указан номер ip для подключения к серверу')
        sys.exit(1)
    #  -p XXXX
    try:
        if '-p' in sys.argv:
            port_for_server_connect = int(sys.argv[sys.argv.index
                                                   ('-p') + 1])
            if 1024 > port_for_server_connect or port_for_server_connect > \
                    65535:
                raise ValueError
        else:
            port_for_server_connect = DEFAULT_PORT
    except IndexError:
        print('После ключа -р не указан номер порта для подключения к серверу')
        sys.exit(1)
    except ValueError:
        print('Порт д.б. в диапазоне 1024-65535')
        sys.exit(1)

    # создаём сокет, соединяемся
    server_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_connect.connect((ip_for_server_connect, port_for_server_connect))

    # создаём и отправляем сообщение о присутствии серверу
    message_to_server = create_massage_a_presence()
    send_message(server_connect, message_to_server)

    try:
        response_of_server = parsing_response(get_message(server_connect))
        print(response_of_server)
    except(ValueError, json.JSONDecodeError):
        print('Непрвильные данные/Не удалось декодировать данные.')


if __name__ == '__main__':
    main()
