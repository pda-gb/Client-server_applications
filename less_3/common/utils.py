"""Утилиты"""
import json

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
