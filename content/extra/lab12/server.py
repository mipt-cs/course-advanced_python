import socket
import threading
import time

text = '''\033[1m\033[34mПоздравляю с решением первой задачи.\033[0m\033[37m

  Теперь Вам необходимо написать сервер.

  Для регистрации вашей программы как сервера, необходимо сообщить системе какой порт вы хотите использовать (метод \033[32msock.bind((<ip_address>, <port>))\033[37m), после чего начать его прослушивать (метод \033[32msock.listen(<max connection numbers>)\033[37m) и принять информацию о соединении (connection) и адресе (address) методом  sock.accept() (возвращает кортеж).

  В отличии от клиента - сервер сначала должен получить сообщение на соединение (\033[32mconnection.recv(<length>)\033[37m) и только потом отправить сообщение (\033[32mconnection.send(<bin str>)\033[37m)

  \033[34mЗадача:\033[0m написать сервер, который получит на вход текст следующей задачи и ответит информацией о студенте.

  Сообщить информацию о сервере необходимо в формате \033[33mf"{ip_address}\\n{port}"\033[37m в сообщении данному серверу на порт 9001.

  Ip адрес можно узнать по "hostname -I" или "ip addr" или "ifconfig" (что заработает в Linux); ipconfig (в windows)

  \033[1m\033[31mЗадачу можно сдать, если Ваш ip адресс имеет вид 10.55.x.x. Иначе спрашивайте преподавателя.\033[0m
\000'''

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
