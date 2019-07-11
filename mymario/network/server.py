import socket
import ast


class Server:
    def __init__(self, port=12334):
        self.socket = socket.socket()
        self.socket.bind(('', port))
        self.clients = []

    @staticmethod
    def new_client(c, addr):
        return {'c': c, 'addr': addr}

    def host(self):
        self.socket.listen(5)
        c, addr = self.socket.accept()
        print('Got connection from', addr)
        c.send(b'Connection accepted')
        self.clients.append(self.new_client(c, addr))
        return self.clients[-1]

    @staticmethod
    def send_config(self, client, config):
        client.send(config.encode())

    @staticmethod
    def start_game(self, client):
        client.send("{start_game: True}".encode())

    def receive(self):
        data = self.receive_dict_data()
        return data

    def send(self, data):
        [self.send_dict_data(data, client["c"]) for client in self.clients]

    def receive_dict_data(self):
        data = self.clients[0]["c"].recv(1024)
        data = ast.literal_eval(data.decode())
        return data

    def send_dict_data(self, data, client):
        client.send(str(data).encode())

    def shut_down(self):
        [client["c"].close() for client in self.clients]
        self.socket.close()


