# Import socket module
import socket
import ast


class Client:
    def __init__(self):
        self.socket = socket.socket()

    def connect_to_server(self, ip="127.0.0.1", port=12334):
        self.socket.connect((ip, port))
        print(self.socket.recv(1024))
        # print("")

    def receive(self):
        return self.receive_dict_data()

    def receive_config(self):
        return self.receive_dict_data()

    def send(self, data):
        self.send_dict_data(data)

    def to_start(self):
        while True:
            data = self.receive_dict_data()
            if "start_game" in data.keys and data["start_game"]:
                return True

    def receive_dict_data(self):
        data = self.socket.recv(1024)
        data = ast.literal_eval(data.decode())
        return data

    def send_dict_data(self, data):
        self.socket.send(str(data).encode())

    def close(self):
        self.socket.close()