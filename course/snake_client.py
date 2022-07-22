from socket import *
import json
import struct
from threading import Thread

HOST = '127.0.0.1'
PORT = 21546
BUFFER_SIZE = 1024
ADDR = (HOST, PORT)

class SnakeClient(Thread):
    def __init__(self) -> None:
        super(SnakeClient, self).__init__()
        self.client_id = 'default'
        self.shadow_snake = {}

    def connect(self):
        self.tcp_client_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_client_socket.connect(ADDR)
        self.client_id = ''
        self.stop = False
        data_len = struct.unpack('i', self.tcp_client_socket.recv(4))[0]
        data = self.tcp_client_socket.recv(data_len).decode('utf-8')
        self.client_id = json.loads(data)["client-id"]

    def disconnect(self) -> None:
        self.stop = True

    def send_message(self, message) -> None:
        client_data = json.dumps({self.client_id:message}).encode('utf-8')
        client_data_length = len(client_data)
        self.tcp_client_socket.send(struct.pack('i', client_data_length))
        self.tcp_client_socket.send(client_data)
        
    def run(self) -> None:
        while not self.stop:
            data_len = struct.unpack('i', self.tcp_client_socket.recv(4))[0]
            data = self.tcp_client_socket.recv(data_len).decode('utf-8')
            if data:
                data_dic = json.loads(data)
                self.shadow_snake = data_dic
                if self.client_id in self.shadow_snake:
                    del (self.shadow_snake[self.client_id])
                    # print(self.shadow_snake)
            

    def get_competitor_snake(self):
        competitor_snake = []
        if len(self.shadow_snake.keys()) > 0:
            cods = self.shadow_snake[list(self.shadow_snake.keys())[0]]['message']
            for cod in cods:
                competitor_snake.append([cod['x'], cod['y']])
        return competitor_snake