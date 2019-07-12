import socket
import ast
import datetime
import time


class Server:
    def __init__(self, port=12334):
        self.socket = socket.socket()
        self.socket.bind(('', port))
        self.header_length = 5
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
        self.synchronize_time(self.clients[-1])

        return self.clients[-1]

    def synchronize_time(self, client):
        cycles = 5
        for _ in range(cycles):
            data = self.receive()
            self.send({"epoch_time": time.time()},timestamp=False)
        # epoch_time = time.time()
        # date_time = datetime.datetime.fromtimestamp(epoch_time)
        # time_format = "%d/%m/%Y, %H:%M:%S:%f"
        # str_time = date_time.strftime(time_format)
        #
        # self.send({'epoch_time': epoch_time, 'str_time': str_time, 'time_format': time_format}, clients=[client])
        # self.socket.close()
        # exit(1)

    @staticmethod
    def send_config(self, client, config):
        client.send(config.encode())

    @staticmethod
    def start_game(self, client):
        client.send("{start_game: True}".encode())

    def receive(self):
        header = self.clients[0]["c"].recv(self.header_length)
        len_data = 0
        try:
            len_data = int(header.decode())
        except Exception as e:
            print(e, " Sorry there is some error in receiving data.")
            exit(1)
        data = self.receive_dict_data(len_data)
        return data

    def send(self, data, clients=None, timestamp=True):
        if clients is None:
            clients = self.clients
        # print(data)
        if timestamp:
            data.update({'timestamp': time.time()})
        encoded_data = str(data).encode()
        len_data = str(len(encoded_data))
        num_zeros = len(len_data)
        for i in range(self.header_length-num_zeros):
            len_data = '0' + len_data

        # print(len_data)
        # exit(1)

        for client in clients:
            client["c"].send(len_data.encode())
            client["c"].send(encoded_data)

    def receive_dict_data(self, len_data):
        data = self.clients[0]["c"].recv(len_data)
        try:
            data = ast.literal_eval(data.decode())
        except Exception as e:
            print("Sorry, there is error in parsing received data and the error is ", e)
            exit(1)
        return data

    def send_dict_data(self, data, client):
        client.send(str(data).encode())

    def shut_down(self):
        [client["c"].close() for client in self.clients]
        self.socket.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()


