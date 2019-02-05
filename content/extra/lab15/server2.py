import socket
import threading
import time

text = '''
\x1b[40m\x1b[1m\x1b[31m       Поздравляю с решением второй задачи.\x1b[0m\x1b[37m

  Вам необходимо получить секретный код из программы на этом сервере и порте 9003.
  Как? Изучите сервер сами.
\x1b[0m\x00'''

def communicate(addr, port):
    print('send to', addr, port)
    sock = socket.socket()
    sock.connect((addr, port))

    sock.send('HELLO'.encode())
    data = sock.recv(1024)
    with open('static/2.txt','a') as f:
        tmp = str(time.ctime()) + ' connected: ' + str(addr) + ' ' + data.decode("utf8")
        f.write(tmp)
        f.write("\n")
    sock.send(text.encode())
    conn.close()


sock = socket.socket()
sock.bind(('', 9001))
sock.listen(40)

while True:
    conn, addr = sock.accept()
    print('serv2', addr)
    data = conn.recv(1024)
    data = data.decode('utf8')
    print(data)
    try:
        addr1, port = data.split('\n')
    except:
        conn.send(b'Error\n\x00')
    my_thread = threading.Thread(target=communicate, args=(addr[0], int(port)))
    my_thread.start()
