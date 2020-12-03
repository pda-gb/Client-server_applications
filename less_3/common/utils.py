"""Утилиты"""
import json
import sys

from less_3.common.variables import MAX_PACKAGE_LENGTH, ENCODING


def get_message(_sock):
    """
    Приём сообщения, декодирование из байт, если ошибка, выдать текст ошибки
    """

    response_as_byte = _sock.recv(MAX_PACKAGE_LENGTH)
    if isinstance(response_as_byte, bytes):
        response_as_json = response_as_byte.decode(ENCODING)
        response = json.loads(response_as_json)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message(_sock, _message_dict):
    """Кодирует в байты и отправляет сообщение"""

    message_as_json = json.dumps(_message_dict)
    message_as_byte = message_as_json.encode(ENCODING)
    _sock.send(message_as_byte)


# def find_connections_parameters(_str):
#     """
#     Ищет ключи в коммандной строке запуска приложения, которым задаётся
#     порт и адресс подключения
#     _str - указывает для какого приложения(server/client)
#     """
#     key_port = ''
#     key_address = ''
#     if '-p' in sys.argv:
#         key_port = '-p'
#         port = int(sys.argv[sys.argv.index(key_port) + 1])
#     if '--port' in sys.argv:
#         key_port = '--port'
#         port = int(sys.argv[sys.argv.index(key_port) + 1])
#
#     if '-a' in sys.argv:
#         key_address = '-a'
#         address = int(sys.argv[sys.argv.index(key_address) + 1])
#     if '--address' in sys.argv:
#         key_address = '--address'
#         address = int(sys.argv[sys.argv.index(key_address) + 1])
#
#     # если не найдено, то поумолчанию
#     port = DEFAULT_PORT
#     if _str == 'server':
#         address = DEFAULT_IP_ADDRESS_FOR_LISTEN
#     if _str == 'client':
#         address = DEFAULT_IP_ADDRESS
#     return {'port': port, 'address': address}
