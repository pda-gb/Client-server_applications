from chardet import detect

with open('test_file.txt', 'rb') as file:
    content_bytes = file.read()
    detect_encoding = detect(content_bytes)['encoding']
    print(detect_encoding)
    content_str = content_bytes.decode(detect_encoding)

with open('test_file.txt', 'w', encoding='utf-8') as file:
    file.write(content_str)
    file.close()

with open('test_file.txt', encoding='utf-8') as file:
    print(file)
    for str_file in file:
        # str_file = str_file.decode('utf-8').encode('windows-1251')
        print(str_file, end='')

