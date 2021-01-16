import inspect
import json
import socket
import sys
import time
import traceback
from argparse import ArgumentParser
from logging import getLogger

# import less_7.log.configs.client_log_config - должна быть для
# инициализации логирования
import less_7.log.configs.client_log_config

from less_7.common.utils import send_message, get_message
from less_7.common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, ACTION, \
    PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, MESSAGE, SENDER, \
    MESSAGE_TEXT
from less_7.errors import EmptyOrFailDataRecv

# Инициализация логирования клиента.
LOGGER = getLogger('client')


# декоратор на функции
def log(decorated_func):
    """Декоратор - пример использования для дебаг-логирования функций"""

    def log_wrap(*args, **kwargs):
        """Обертка"""
        result = decorated_func(*args, **kwargs)
        LOGGER.debug(f'\n+ + +\n__doc__: {decorated_func.__doc__}\n+ + +\n'
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
def parsing_response_of_presence(_server_response):
    """Разбор ответа сервера на сообщение о присутствии клиента в сети"""

    # LOGGER.debug(f'разбор ответа сервера: {_server_response}')
    # Проверка на сообщение о присутствии
    if RESPONSE in _server_response:
        if _server_response[RESPONSE] == 200:
            return 'code : 200. OK, you are connected.'
        return f'code :{_server_response[RESPONSE]}. Error: ' \
               f'{_server_response[ERROR]}'
    raise ValueError


@log
def parsing_response_of_users_message(_server_response):
    """Разбор ответа сервера на сообщение от пользователя"""
    # Проверка на сообщение от клиента
    if ACTION in _server_response and _server_response[ACTION] == MESSAGE \
            and MESSAGE_TEXT in _server_response and TIME in _server_response:
        # отдаём текс сообщения
        return _server_response[MESSAGE_TEXT]

    raise ValueError


@log
def find_connections_parameters():
    """
    Функция парсер. Запуск клиента с заданными параметрами или по дефолту.
    пример: client.py -a XXX.XXX.XXX.XXX -p XXXX -m listen/sender

    """

    find_parameters = ArgumentParser()
    # добавляем в класс аргументы-параметры по ключам
    find_parameters.add_argument('-a', '--address', default=DEFAULT_IP_ADDRESS,
                                 nargs='?', dest='a')
    find_parameters.add_argument('-p', '--port', default=DEFAULT_PORT,
                                 type=int, nargs='?', dest='p')
    find_parameters.add_argument('-m', '--mode', default='listen', nargs='?',
                                 dest='m')
    # парсим начиная после первого элемента(client.py)
    parameters = find_parameters.parse_args(sys.argv[1:])
    ip_for_server_connect = parameters.a
    port_for_server_connect = parameters.p
    mode_client = parameters.m
    if 1024 > port_for_server_connect or port_for_server_connect > 65535:
        print('Порт д.б. в диапазоне 1024-65535')
        LOGGER.critical(f'Запуск клиента с портом {port_for_server_connect} '
                        f'недопустимо. Порт д.б. в диапазоне 1024-65535.')
        sys.exit(1)
    return ip_for_server_connect, port_for_server_connect, mode_client


@log
def get_users_message(user_msg_from_server):
    """
    Проверка сообщений от пользователей, приходящих с сервера, на
    соответствие протоколу JIM.
    """
    if ACTION in user_msg_from_server and user_msg_from_server[ACTION] == \
            MESSAGE and SENDER in user_msg_from_server and MESSAGE_TEXT in \
            user_msg_from_server:
        LOGGER.debug(f'\nПолучено сообщение:'
                     f'{user_msg_from_server[MESSAGE_TEXT]}\n'
                     f' от пользователя:{user_msg_from_server[SENDER]}\n'
                     f'отправлено в {user_msg_from_server[TIME]}\n'
                     f'получено через '
                     f'{time.time() - user_msg_from_server[TIME]} сек.')
        print(f'От:{user_msg_from_server[SENDER]} \n'
              f'сообщение:{user_msg_from_server[MESSAGE_TEXT]}\n'
              f'отправлено в {user_msg_from_server[TIME]}')


@log
def create_users_message(sock_of_conn, account='Guest'):
    """
    Функция заправшивает текст сообщения пользователя для отправки, формирует
    словарь для отправки на сервер. При вводе exit, завершает работу
    приложения.
    :param sock_of_conn:
    :param account:
    :return: dict
    """
    text_msg = input('Напишите своё сообщение или \'exit\' для закрытия '
                     'приложения:\n')
    if text_msg == 'exit':
        LOGGER.info('Пользователь завершил работу приложения по команде exit.')
        sock_of_conn.close()
        sys.exit(0)

    message_to_server = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account,
        MESSAGE_TEXT: text_msg
    }
    return message_to_server


def main():
    # запуск клиента с заданными параметрами или по дефолту.
    ip_for_server_connect, port_for_server_connect, mode_client = \
        find_connections_parameters()
    LOGGER.info(f'Запущен клиент с параметрами: {ip_for_server_connect} '
                f'{port_for_server_connect}, в режиме {mode_client}.')
    print(f'Запущен клиент с параметрами: {ip_for_server_connect} '
          f'{port_for_server_connect}, в режиме {mode_client}.')

    try:
        # создаём сокет, соединяемся
        server_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_connect.connect((ip_for_server_connect,
                                port_for_server_connect))
        LOGGER.debug(f'создаём сокет, соединяемся c сервером: '
                     f'{(ip_for_server_connect, port_for_server_connect)}')
        print(f'Соединение c сервером: '
              f'{(ip_for_server_connect, port_for_server_connect)} '
              f'установлено.')

        # создаём и отправляем сообщение о присутствии серверу
        message_to_server = create_massage_a_presence()
        send_message(server_connect, message_to_server)
        LOGGER.debug(f'создаём и отправляем сообщение о присутствии серверу: '
                     f'{message_to_server}')
        # Получаем сообщения от сервера
        response_of_server = parsing_response_of_presence(get_message(
            server_connect))
        LOGGER.debug(f'Ответ сервера на отправку сообщения о присутствии:'
                     f'{response_of_server}')
        print(f'Ответ сервера: {response_of_server}')
    except json.JSONDecodeError:
        print('Не удалось декодировать данные.')
        LOGGER.critical('Не удалось декодировать данные.')
    except EmptyOrFailDataRecv:
        LOGGER.error('Из сокета получено пустое или неправильное сообщение')
    else:
        # Если есть связь с сервером и удался обмен данными о присутствии,
        # то можем начать обмениваться сообщениями (основной цикл работы).

        if mode_client == 'listen':
            print('++++ Приложение в режиме приёма сообщения. ++++')
        if mode_client == 'sender':
            print('==== Приложение в режиме отправки сообщения. ====')

        while True:
            # Приём
            if mode_client == 'listen':
                try:
                    get_users_message(get_message(server_connect))
                    # input('Нажмите Enter для выхода!')
                except (ConnectionError, ConnectionResetError,
                        ConnectionRefusedError, ConnectionAbortedError):
                    LOGGER.error(f'Потеря связи! Сервер '
                                 f'{server_connect.getpeername()} '
                                 f'не доступен.')
                    sys.exit(1)

            # Передача
            if mode_client == 'sender':
                try:
                    send_message(server_connect,
                                 create_users_message(server_connect))
                except (ConnectionError, ConnectionResetError,
                        ConnectionRefusedError, ConnectionAbortedError):
                    LOGGER.error(f'Потеря связи! Сервер '
                                 f'{server_connect.getpeername()} '
                                 f'не доступен.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
