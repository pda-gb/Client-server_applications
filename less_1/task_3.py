w1 = b'attribute'
w2 = b'класс'
w3 = b'функция'
w4 = b'type'
words = [w1, w2, w3, w4]

for itm in words:
    try:
        print(f'[{itm}] is {type(itm)}')
    except SyntaxError:
        print("невозможно записать в байтовом типе с помощью маркировки b''")
