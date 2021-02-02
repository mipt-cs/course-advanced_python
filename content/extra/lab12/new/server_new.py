import socket
from problems import BaseProblem
import time
from myservers import Simple_server

results = {}


def dump():
    global results
    data = ['<table>']
    for i in results:
        data.append('<tr><td>')
        data.append(i)
        data.append('</td><td>')
        data.append(results[i]['name'])
        data.append('</td><td>')
        data.append(results[i]['group'])
        data.append('</td><td>')
        data.append(results[i]['ip'])
        data.append('</td><td>')
        data.append(results[i]['time'])
        data.append('</td><td>')
        data.append(results[i]['secret'])
        data.append('</td></tr>')

    data.append('</table>')
    data = ''.join(data)

    open('/var/www/html/index.html', 'w').write(data)


def communicate(conn, addr):
    global results
    server = Simple_server(conn)
    server.send("Привет. Введите имя задачи: ")
    data = server.recv()

    if data == 'Register':
        server.send("Введите ваш логин: ")
        login = server.recv()
        if login in results:
            server.send(f'{login} уже существует')
            return
        server.send("Введите ФИО: ")
        name = server.recv()
        server.send("Введите вашу группу: ")
        group = server.recv()
        data[login] = {
            'name': name,
            'group': group,
            'ip': addr,
            'time': time.ctime(),
            'secret': "None"
        }
        dump()
        server.send('Спасибо. Переподсоединитесь к серверу и решите следующую задачу - "Get secret key"')
        return

    if data == 'Get secret key':
        server.send('Введите Ваш логин: ')
        login = server.recv()
        if login not in results:
            server.send(f'{login} не найден')
            return

        problem = BaseProblem(server, results)
        while server is not None:
            server.send("Введите Ваш запрос: (help для помощи)")
            query = server.recv()
            server, problem = problem.proced(query)

        dump()
        return

    server.send("Неизвестное имя задачи. Проверьте ")

sock = socket.socket()
sock.bind(('', 9000))
sock.listen(40)

while True:
    conn, addr = sock.accept()
    my_thread = threading.Thread(target=communicate, args=(conn, addr))
    my_thread.start()
