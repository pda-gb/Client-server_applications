import json
import unittest

from less_4.common.variables import ENCODING


class DummySocket:
    """тестовый сокет - заглушка"""

    def __init__(self, test_obj):



    def send_message(self, _message_dict):
        """Кодирует в байты и отправляет сообщение"""

        message_as_json = json.dumps(self.test_obj)
        message_as_byte = message_as_json.encode(ENCODING)
        self.send(message_as_byte)

### === тест ещё не сделан ===