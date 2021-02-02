from myservers import Simple_server, Coded_server, ZippedServer
import pickle
import textes
import abc


class AbstractProblem(abc.ABC):
    def __init__(self, server, results, login):
        self.server = server
        self.results = results
        self.login = login

    @abc.abstractclassmethod
    def proced(self, data):
        pass


class BaseProblem(AbstractProblem):
    def proced(self, data):
        if data == 'help':
            self.server.send(textes.base_help)
        elif data == 'about':
            self.server.send(textes.base_about)
        elif data == 'next':
            server = ZippedServer(self.server)
            return server, DHProblem(server, self.results)
        else:
            self.server.send('Неизвестная комманда')

        return self.server, self


class DHProblem(AbstractProblem):
    def __init__(self, server, results, login):
        super(DHProblem, self).__init__(server, result, login)
        self.data = {'g': 123123, 'p': 12397983, 'A': 907072379, 'b': 9973}

    def proced(self, data):
        if data == 'help':
            self.server.send(textes.dh_help)
        elif data == 'about':
            self.server.send(textes.dh_about)
        elif data == 'about_dh':
            self.server.send(textes.dh_about_dh)
        elif data == 'about_coding':
            self.server.send(textes.dh_about_coding)
        elif data == 'set':
            self.server.send('"Запиклите" словарь {"g":value, "p":value, "A":value} методом pickle.dumps() и передайте')
            try:
                data = self.server.recv()
                data = pickle.loads(data)
                self.data['g'] = data['g']
                self.data['p'] = data['p']
                self.data['A'] = data['A']
            except Exception as e:
                self.server.send(f"ERROR {e}")
                return None, self
        elif data == 'get':
            try:
                B = (self.data['g'] ** self.data['b']) % self.data['p']
                self.server.send(pickle.dumps(B))
            except Exception as e:
                self.server.send(f"ERROR {e}")
                return None, self
        elif data == 'connect':
            K = (self.data['A'] ** self.data['b']) % self.data['p']
            server = Coded_server(self.server, K)
            return server, DHProblem(server, self.results)
        else:
            self.server.send('Неизвестная комманда')

        return self.server, self


class CodedProblem(AbstractProblem):

    def proced(self, data):
        if data == 'help':
            self.server.send(textes.coded_help)
        if data == 'get_code':
            res = hashlib.md5(self.login.encode()).hexdigest()
            results[self.login]['secret'] = results
            self.server.send(res)
            return None, self
        else:
            self.server.send('Неизвестная комманда')

        return self.server, self
