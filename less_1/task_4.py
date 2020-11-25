w1 = 'разработка'
w2 = 'администрирование'
w3 = 'protocol'
w4 = 'standard'
w5 = 123
w6 = True
w7 = b'\xd1\x80\xd0'
words = [w1, w2, w3, w4, w5, w6, w7]

for itm in words:
    try:
        itm_bytes = itm.encode('utf-8')
        itm_bytes_to_str = itm_bytes.decode('utf-8')
        print(f'[{itm}] in bytes [{itm_bytes}],'
              f' bytes in str[{itm_bytes_to_str}]')
    except AttributeError:
        i = words.index(itm)
        print(f'в {i+1} елементе ошибка')



