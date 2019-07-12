# Import socket module
import socket
import ast
import time
import datetime
from statistics import mean

class Client:
    def __init__(self):
        self.socket = socket.socket()
        self.header_length = 5 
        self.time_diff = 0

    def connect_to_server(self, ip="10.42.0.228", port=12334):
        self.socket.connect((ip, port))
        print(self.socket.recv(19))
        self.synchronize_time()
        # print("")

    def synchronize_time(self):
        rtp = []
        csd = []
        cycles = 5
        for i in range(cycles):
            sent_time = time.time()
            self.send({'epoch_time': sent_time})
            data = self.receive()
            received_time = time.time()
            rtp.append(received_time - sent_time)
            csd.append(sent_time - data["epoch_time"]) 
            print('\r', "rtp: ", rtp[-1], "csd: ", csd[-1])
        # data = self.receive()
        # server_time = datetime.datetime.strptime(data["str_time"], data["time_format"])
        # self.time_diff = server_time.timestamp() - data["epoch_time"]
        # print(self.time_diff)
        print("Mean_rtp: ", mean(rtp), "Mean_csd: ",mean(csd))
        self.time_diff = mean(csd) - mean(rtp) / 2
        print('\r', self.time_diff)
        # self.socket.close()
        # exit(1)
        # epoch_time = time.time()
        # date__time = datetime.datetime.fromtimestamp(epoch_time)
        # str_time = date__time.strftime("%d/%m/%Y, %H:%M:%S:%f")



    def receive(self):
        header = self.socket.recv(self.header_length)
        try:
            len_data = int(header)
        except Exception as e:
            print(e, " Sorry there is some error in receiving data.")
            exit(1)

        return self.receive_dict_data(len_data)

    def receive_config(self):
        return self.receive_dict_data()

    def send(self, data):
        encoded_data = str(data).encode()
        len_data = str(len(encoded_data))
        num_zeros = len(len_data)
        for _ in range(self.header_length-num_zeros):
            len_data = '0' + len_data
        # print(len_data)
        # exit(1)
        self.socket.send(len_data.encode())
        # self.send_dict_data(data)
        self.socket.send(encoded_data)

    def to_start(self):
        while True:
            data = self.receive_dict_data()
            if "start_game" in data.keys and data["start_game"]:
                return True

    def receive_dict_data(self, len_data):
        data = self.socket.recv(len_data)
        try:
            data = ast.literal_eval(data.decode())
        except Exception as e:
            print("Sorry, there is error in parsing received data and the error is ", e)
            exit(1)
        return data

    def send_dict_data(self, data):
        self.socket.send(str(data).encode())

    def close(self):
        self.socket.close()