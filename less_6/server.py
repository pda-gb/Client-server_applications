import json
import socket
import sys
import less_5.log.configs.server_log_config
from less_5.common.utils import get_message, send_message
from less_5.common.variables import DEFAULT_PORT, MAX_CONNECTIONS, ACTION, \
    PRESENCE, TIME, ACCOUNT_NAME, USER, RESPONSE, ERROR, DEFAULT_IP_ADDRESS


from logging import getLogger

# Инициализация логирования сервера.
from less_6.errors import EmptyOrFailDataRecv

LOGGER = getLogger('server')


def control_of_protocol_compliance(message_of_client):
    """
    Проверка на соответствие протоколу  сообщения от клиента.
    Возвращает результат проверки, для дальнейшей отправки клиенту.
    """
    LOGGER.debug(f'Проверка на соответствие протоколу  сообщения '
                 f'от клиента: {message_of_client}')

    if ACTION in message_of_client and message_of_client[ACTION] == PRESENCE \
            and TIME in message_of_client and type(message_of_client[TIME]) is\
            float and USER in message_of_client and \
            message_of_client[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Request is not compliance to protocol'
    }


def main():
    # запуск сервера с заданными параметрами или по дефолту.
    # пример: server.py -a XXX.XXX.XXX.XXX -p XXXX
    # с помощью sys.argv парсим параметры по ключам
    #  -a XXX.XXX.XXX.XXX
    try:
        if '-a' in sys.argv:
            ip_for_client_connect = int(sys.argv[sys.argv.index
                                                 ('-a') + 1])
        else:
            ip_for_client_connect = DEFAULT_IP_ADDRESS
        #  --- заготовка ---
        # port_for_client_connect, ip_for_client_connect = \
        # find_connections_parameters(server)
    except IndexError:
        print('После ключа -а не указан номер ip для подключения клиента')
        LOGGER.error('После ключа -а не указан номер ip для подключения '
                     'клиента')
        sys.exit(1)
    #  -p XXXX
    try:
        if '-p' in sys.argv:
            port_for_client_connect = int(sys.argv[sys.argv.index
                                                   ('-p') + 1])
            if 1024 > port_for_client_connect or port_for_client_connect > \
                    65535:
                raise ValueError
        else:
            port_for_client_connect = DEFAULT_PORT
    except IndexError:
        print('После ключа -р не указан номер порта для подключения клиента')
        LOGGER.error('После ключа -р не указан номер порта для подключения '
                     'клиента')
        sys.exit(1)
    except ValueError:
        print('Порт д.б. в диапазоне 1024-65535')
        LOGGER.critical(f'Запуск сервера с портом {port_for_client_connect} '
                        f'недопустимо. Порт д.б. в диапазоне 1024-65535.')
        sys.exit(1)

    # создаём сокет, соединяемся, слушаем
    client_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_connect.bind((ip_for_client_connect, port_for_client_connect))
    client_connect.listen(MAX_CONNECTIONS)

    while True:
        # подключение клиента
        client, address_of_client = client_connect.accept()
        LOGGER.info(f'Подключен клиент {address_of_client}')
        try:
            # приём сообщения
            message_of_client = get_message(client)
            LOGGER.debug(f'принято сообщение от клиента:{message_of_client}\n')
            # print(f'принято сообщение от клиента:{message_of_client}\n')
            #  и проверка его на соответствие протоколу JIM
            response_to_client = control_of_protocol_compliance(
                message_of_client)
            # сообщаем клиенту результат
            send_message(client, response_to_client)
            LOGGER.debug(f'сообщаем клиенту результат:{response_to_client}')
            client.close()
        except(ValueError, json.JSONDecodeError):
            print(f'Не удалось декодировать данные от клиента '
                  f'{address_of_client}')
            LOGGER.error(f'Не удалось декодировать данные от клиента '
                         f'{address_of_client}')
        except EmptyOrFailDataRecv:
            LOGGER.error('Из сокета получено пустое или неправильное '
                         'сообщение')
            client.close()


if __name__ == '__main__':
    main()
