import json
import socket
import sys

from less_3.common.utils import get_message, control_of_protocol_compliance, send_message
from less_3.common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS,\
    MAX_CONNECTIONS



def main():
    # запуск сервера с заданными параметрами или по дефолту.
    # пример: server.py -p XXXX -a XXX.XXX.XXX.XXX
    # с помощью sys.argv парсим параметры по ключам
    #  -p XXXX
    try:
        if '-p' in sys.argv:
            port_for_client_connect = int(sys.argv[sys.argv.index('-p') + 1])
            if 1024 > port_for_client_connect or port_for_client_connect > \
                    65535:
                raise ValueError
        else:
            port_for_client_connect = DEFAULT_PORT
    except IndexError:
        print('После ключа -р не указан номер порта для подключения клиента')
        sys.exit(1)
    except ValueError:
        print('Порт д.б. в диапазоне 1024-65535')
        sys.exit(1)
    #  -a XXX.XXX.XXX.XXX
    try:
        if '-a' in sys.argv:
            ip_for_client_connect = int(sys.argv[sys.argv.index('-a') + 1])
        else:
            ip_for_client_connect = DEFAULT_IP_ADDRESS
    except IndexError:
        print('После ключа -а не указан номер ip для подключения клиента')
        sys.exit(1)

    # создаём сокет, соединяемся, слушаем
    client_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_connect.bind((ip_for_client_connect, port_for_client_connect))
    client_connect.listen(MAX_CONNECTIONS)

    while True:
        # подключение клиента
        client, address_of_client = client_connect.accept()
        try:
            # приём сообщения
            message_of_client = get_message(client_connect)
            print(f'приято сообщение от клиента:{message_of_client}\n')
            #  и проверка его на соответствие протоколу JIM
            response_to_client = control_of_protocol_compliance(
                message_of_client)
            # сообщаем клиенту результат
            send_message(client, response_to_client)
            client.close()
        except(ValueError, json.JSONDecodeError):
            print(f'Некорректное сообщение  от клиента [{address_of_client}]')
            client.close()

if __name__ == 'main':
    main()