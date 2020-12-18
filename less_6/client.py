import inspect
import json
import socket
import sys
import time
import traceback
# import less_6.log.configs.client_log_config - должна быть для
# инициализации логирования
import less_6.log.configs.client_log_config
from logging import getLogger

from less_6.common.utils import send_message, get_message
from less_6.common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, ACTION, \
    PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
from less_6.errors import EmptyOrFailDataRecv

# Инициализация логирования клиента.
LOGGER = getLogger('client')


# декоратор на функции
def log(decorated_func):
    """Декоратор - пример использования для дебаг-логирования функций"""

    def log_wrap(*args, **kwargs):
        """Обертка"""
        result = decorated_func(*args, **kwargs)
        LOGGER.debug(f'\n+ + +\nСообщение: {decorated_func.__doc__}\n+ + +\n'
                     f'Функция {decorated_func.__name__} c параметрами '
                     f'{args}, {kwargs}. \n'
                     f'Вызов из модуля {decorated_func.__module__} из '
                     f'функции '
                     f'{traceback.format_stack()[0].strip().split()[-1]}\n'
                     f'Вызов из функции {inspect.stack()[1][3]}')

        # traceback, inspect - помогают через логирование узнать имя
        # функции, модуля откуда вызвана логируемая функция.
        return result

    # для сообщения от конкретной точки для лога сначала получим описание
    # логируемой функции и передадим в качестве доп. сообщения
    log_wrap.__doc__ = decorated_func.__doc__
    return log_wrap


@log
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
    # LOGGER.debug(f'Создание сообщения о присутствии от клиента: '
    #             f'{_message}')
    return _message


@log
def parsing_response(_server_response):
    """разбор ответа сервера"""

    # LOGGER.debug(f'разбор ответа сервера: {_server_response}')
    if RESPONSE in _server_response:
        if _server_response[RESPONSE] == 200:
            return 'code : 200. OK, you are connected.'
        return f'code :{_server_response[RESPONSE]}. Error: ' \
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
        LOGGER.error('После ключа -а не указан номер ip для подключения '
                     'клиента')
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
        print('После ключа -р не указан номер порта для подключения клиента')
        LOGGER.error('После ключа -р не указан номер порта для подключения '
                     'клиента')
        sys.exit(1)
    except ValueError:
        print('Порт д.б. в диапазоне 1024-65535')
        LOGGER.critical(f'Запуск сервера с портом {port_for_server_connect} '
                        f'недопустимо. Порт д.б. в диапазоне 1024-65535.')
        sys.exit(1)

    # создаём сокет, соединяемся
    server_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_connect.connect((ip_for_server_connect, port_for_server_connect))
    LOGGER.debug(f'создаём сокет, соединяемся c сервером: '
                 f'{(ip_for_server_connect, port_for_server_connect)}')

    # создаём и отправляем сообщение о присутствии серверу
    message_to_server = create_massage_a_presence()
    send_message(server_connect, message_to_server)
    LOGGER.debug(f'создаём и отправляем сообщение о присутствии серверу: '
                 f'{message_to_server}')

    try:
        response_of_server = parsing_response(get_message(server_connect))
        print(response_of_server)
    except(ValueError, json.JSONDecodeError):
        print('Не удалось декодировать данные.')
        LOGGER.critical('Не удалось декодировать данные.')
    except EmptyOrFailDataRecv:
        LOGGER.error('Из сокета получено пустое или неправильное сообщение')


if __name__ == '__main__':
    main()
