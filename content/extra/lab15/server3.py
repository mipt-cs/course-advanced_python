import math
import socket
import threading
import time
import hashlib


def code_bitstr(data, K):
    res = [0]*len(data)
    j = 0
    for i in range(len(data)):
        res[i] = data[i] ^ K[j]
        j = (j+1) % len(K)
    print(data, res)
    return bytes(res)


def communicate(conn, addr):
    g, p, A, b, B = 12523, 1234123, 234423, 9973, None
    try: 
        data = conn.recv(1024).decode('utf8')
    except:
        conn.send(b'Error\n')

    if data != "HELLO":
        conn.send('Error income message. HELLO waiting\n'.encode())
        conn.close()
        return

    conn.send('Get command (help for more information). \n'.encode())

    while True:
        data = conn.recv(1024).decode('utf8')
        if data == "help":
            conn.send('''about_dh : Информация о протоколе Диффи — Хеллмана
about_coding: Информация о методе кодировки
set [g, p, A]=<int>: Пердать информацию о ключе шифрования
get B: Получить B
connect: перейти в зашифрованный канал
exit: Выход
'''.encode())
            continue

        if data == "exit":
            conn.send('Buy\n')
            conn.close()
            return

        if data == "about_coding":
            conn.send('''  Шифрование информации происходит по следующему алгоритму:
    1. Строка \x1b[32mS\x1b[37m представляется как последовательность байт (encode)
    2. Ключ шифрования представляем как последовательность байт: 41960 → A3E8 → [E8, A3] → [163, 232] = K_bits
    3. \x1b[32mi = 0; j = 0\x1b[37m
    4. \x1b[32mS[i] → S[i] mod K_bits[i]\x1b[37m
    5. \x1b[32mi = i + 1; j = (j+2) % len(K_bits)\x1b[37m
    6. если \x1b[32mi < len(S)\x1b[37m возвращаемся к шагу 3 иначе - шифрование закончено.
'''.encode())
            continue

        if data == "about_dh":
            conn.send('''    Протокол Диффи — Хеллмана
  https://ru.wikipedia.org/wiki/Протокол_Диффи_—_Хеллмана

  Протокол Диффи — Хеллмана — криптографический протокол, позволяющий двум и более сторонам получить общий секретный ключ, используя незащищенный от прослушивания канал связи. Полученный ключ используется для шифрования дальнейшего обмена с помощью алгоритмов симметричного шифрования.
  Получение ключа шифрования K для двух пользователей происходит по следующей схеме:

         USER 1                     USER 2
    ╭───────────────╮         ╭───────────────╮
    │\x1b[32m    a, g, p    \x1b[37m│\x1b[32m  g,p,A  \x1b[37m│\x1b[32m       b       \x1b[37m│
    │               │ ──────► │               │
    │\x1b[32m A = g^a mod p \x1b[37m│         │\x1b[32m B = g^b mod p \x1b[37m│
    │               │\x1b[32m    B    \x1b[37m│               │
    │\x1b[32m K = B^a mod p \x1b[37m│ ◄────── │\x1b[32m K = A^b mod p \x1b[37m│
    ╰───────────────╯         ╰───────────────╯
'''.encode())
            continue

        if data == "get B":
            conn.send(str((g**b) % p).encode())
            continue;

        if len(data) > 6 and data[:3] == 'set':
            try:
                if data[4] == 'g':
                    g = int(data[6:])
                if data[4] == 'p':
                    p = int(data[6:])
                if data[4] == 'A':
                    A = int(data[6:])
                conn.send(b'OK\n')
            except:
                conn.send(b'Error\n')

        if data == "connect":
            K = (A ** b) % p
            K = [(K // 256**i) % 256 for i in range(int(math.log(K,256)) + 1)]
            name = "No name"
            conn.send(code_bitstr(b'Welcome to coded channel\n', K))
            while True:
                try:
                    data = conn.recv(1024)
                    if len(data) < 3:
                        conn.send(code_bitstr('''Error\n''', K))
                        conn.close()
                        return
                    data = code_bitstr(data, K).decode("utf8")
                except:
                    conn.send(b"Error coding\n")
                    conn.close()
                    return

                if data == "help":
                    conn.send(code_bitstr('''name <имя>: передать информацию о студенте
get code: Получить код
exit: Выход
'''.encode(), K))
                    continue

                if len(data) > 5 and data[:4] == name:
                    name = data[5:]
                    conn.send(code_bitstr(('Your name is ' + name + '\n').encode(), K))
                    continue

                if data == "exit":
                    conn.send(code_bitstr(b'Buy\n', K))
                    conn.close()
                    return

                if data == "get code":
                    with open('static/3.txt', 'a') as f:
                        code = hashlib.md5(name.encode()).hexdigest()
                        tmp = str(time.ctime()) + ' solved ' + name + ' > ' + code
                        f.write(tmp)
                        f.write("\n")
                    conn.send(code_bitstr.encode())


sock = socket.socket()
sock.bind(('', 9003))
sock.listen(40)

while True:
    conn, addr = sock.accept()
    my_thread = threading.Thread(target=communicate, args=(conn, addr))
    my_thread.start()
