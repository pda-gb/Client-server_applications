w1 = 'attribute'
w2 = 'класс'
w3 = 'функция'
w4 = 'type'
words = [w1, w2, w3, w4]

for itm in words:
    try:
        print(f"[{itm}] is bytes {bytes(itm, 'ascii') }")
    except UnicodeEncodeError:
        print(f"[{itm}] невозможно записать в байтовом типе с помощью"
              f" маркировки b''")
