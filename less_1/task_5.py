import platform
import subprocess

import chardet

words = ['yandex.ru', 'youtube.com']
args = ['ping', ]

# для linux нужно явно указать количество запроса, иначе зациклится
os_name = platform.system()
if os_name == 'Linux':
    args.append('-c 10')
if os_name != 'Linux' and os_name != 'Windows':
    os_name = platform.mac_ver()
    if os_name:
        args.append('-n 10')

for itm in words:
    args.append(itm)
    ping_host = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in ping_host.stdout:
        result = chardet.detect(line)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))
    args.pop()
