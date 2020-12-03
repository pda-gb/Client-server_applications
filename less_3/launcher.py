import os
import subprocess
import sys

all_servers = []
all_clients = []
work_dir = os.path.abspath(os.curdir)
while True:
    ask = input('Выход - q, запустить сервер и клиент - x, '
                'завершить работу серверов - w, завершить работу клиентов - e,'
                ' завершить все запущенные процессы - k\n')

    # выход
    if ask == 'q':
        break

    # Запуск
    elif ask == 'x':
        # выбор порта
        port = input('Укажите порт подключения (1024-65535) или оставить'
                     ' по умолчанию - d\n')
        if port == 'd':
            port = ''
        else:
            port = f'-p {port}'
        # выбор адреса
        address = input('Укажите адпес подключения (ХХХ.ХХХ.ХХХ.ХХХ) '
                        'или оставить по умолчанию - d\n')
        if address == 'd':
            address = ''
        else:
            address = f'-a {address}'
        # запуск сервера ------
        # для linux .CREATE_NEW_CONSOLE не работает
        if sys.platform == 'Windows':
            subprocess.Popen(f'python server.py {port} {address}',
                             creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            all_servers.append(subprocess.Popen(f'python server.py {port} '
                                                f'{address}', shell=True))
            # command = f'x-terminal-emulator -e {sys.executable} -c ' \
            #           f'{work_dir}/server.py {port} {address}'.split()
            # subprocess.check_call(command)
        # запуск клиента ------
        count_client = int(input('Укажите какое количество клиентов '
                                 'запустить(0-20)\n'))
        if count_client != 0:  # не запускать клиент
            for i in range(count_client):
                # для linux .CREATE_NEW_CONSOLE не работает
                if sys.platform == 'Windows':
                    subprocess.Popen(f'python client.py {port} {address}',
                                     creationflags=subprocess.
                                     CREATE_NEW_CONSOLE)
                else:
                    # subprocess.run(f'x-terminal-emulator -e {sys.executable}'
                    #                f' -c client.py {port} {address}'.split())
                    all_clients.append(subprocess.Popen(f'python client.py '
                                                        f'{port} {address}',
                                                        shell=True))
            print('готово!')
            continue
        else:
            pass
    # "убить" все сервера
    if ask == 'w' or ask == 'k':
        count = len(all_servers)
        while all_servers:
            item = all_servers.pop()
            item.kill()
        print(f'серверов \"убито\": {count}')

    # "убить" все клиенты
    if ask == 'e' or ask == 'k':
        count = len(all_clients)
        while all_clients:
            item = all_clients.pop()
            item.kill()
        print(f'клиентов \"убито\": {count}')
