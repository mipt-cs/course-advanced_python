import socket
import threading
import time

text = '''\x1b[1m\x1b[31mПоздравляю с решением первой задачи.\x1b[0m\x1b[37m

  Теперь Вам необходимо написать сервер.
  Для регистрации вашей программы как сервера, необходимо сообщить системе какой порт вы хотите использовать (метод \x1b[32msock.bind((<ip_address>, <port>))\x1b[37m), после чего начать его прослушивать (метод \x1b[32msock.listen(<max connection numbers>)\x1b[37m) и принять информацию о соединении (connection) и адресе (address) методом  sock.accept() (возвращает кортеж).
  В отличии от клиента - сервер сначала должен получить сообщение на соединение (\x1b[32mconnection.recv(<length>)\x1b[37m) и только потом отправить сообщение (\x1b[32mconnection.send(<bin str>)\x1b[37m)
  Задача: написать сервер, который получит на вход текст следующей задачи и ответит информацией о студенте.
  Сообщить информацию о сервере необходимо в формате \x1b[33m"<ip_address>\\n<port>"\x1b[37m в сообщении данному серверу на порт 9001."
\x00'''

def communicate(conn, addr):

    data = conn.recv(1024)
    with open('static/1.txt','a') as f:
        tmp = str(time.ctime()) + ' connected: ' + str(addr) + ' ' + data.decode("utf8")
        f.write(tmp)
        f.write('\n')
    conn.send(text.encode())

    conn.close()


sock = socket.socket()
sock.bind(('', 9000))
sock.listen(40)

while True:
    conn, addr = sock.accept()
    my_thread = threading.Thread(target=communicate, args=(conn, addr))
    my_thread.start()
