import gzip


class Simple_server:
    def __init__(self, sock):
        self.sock = sock

    def send(self, message):
        if isinstance(message, str):
            message = message.encode()
        self.sock.send(message)

    def recv(self, size=10000):
        message = self.sock.recv(size)
        if isinstance(message, bytes):
            message = message.decode("utf8")
        return message


class Coded_server:
    @staticmethod
    def code_bitstr(data, K):
        res = [0] * len(data)
        j = 0
        for i in range(len(data)):
            res[i] = data[i] ^ K[j]
            j = (j + 1) % len(K)
        print(data, res)
        return bytes(res)

    def __init__(self, sock, K):
        self.sock = sock

    def send(self, message):
        if isinstance(message, str):
            message = message.encode()
        self.sock.send(Coded_server.code_bitstr(message, self.K))

    def recv(self, size=10000):
        message = self.sock.recv(size)
        if isinstance(message, bytes):
            message = message.decode("utf8")
        return Coded_server.code_bitstr(message, self.K)


class ZippedServer:
    def __init__(self, sock, K):
        self.sock = sock

    def send(self, message):
        if isinstance(message, str):
            message = message.encode()
        self.sock.send(gzip.compress(message))

    def recv(self, size=10000):
        message = self.sock.recv(size)
        if isinstance(message, str):
            message = message.encode()
        message = gzip.decompress(self.sock.recv(size))
        return message.decode("utf8")


