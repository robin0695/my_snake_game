from socket import *
import json
import struct
from threading import Thread
import time
HOST = '192.168.0.110'
#HOST = '127.0.0.1'
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
        print(self.client_id)

    def disconnect(self) -> None:
        self.stop = True

    def send_message(self, message) -> None:
        client_data = json.dumps({self.client_id:message}).encode('utf-8')
        client_data_length = len(client_data)
        self.tcp_client_socket.sendall(struct.pack('i', client_data_length))
        self.tcp_client_socket.sendall(client_data)
        
    def run(self) -> None:
        try:
            time.sleep(0.02)
            while not self.stop:
                data_len = struct.unpack('i', self.tcp_client_socket.recv(4))[0]
                data = self.tcp_client_socket.recv(data_len).decode('utf-8')
                if data:
                    data_dic = json.loads(data)
                    self.shadow_snake = data_dic
                    if self.client_id in self.shadow_snake:
                        del (self.shadow_snake[self.client_id])
                        # print(self.shadow_snake)
        except struct.error as e:
            print(data, e)
            pass
        except json.decoder.JSONDecodeError as ee:
            print(data, ee)
            pass
            

    def get_competitor_snake(self):
        competitor_snake = []
        if len(self.shadow_snake.keys()) > 0:
            cods = self.shadow_snake[list(self.shadow_snake.keys())[0]]['snake_body']
            for cod in cods:
                competitor_snake.append([cod['x'], cod['y']])
        return competitor_snake

    def get_competitor_food(self):
        if len(self.shadow_snake.keys()) > 0:
            cod = self.shadow_snake[list(self.shadow_snake.keys())[0]]['snake_food']
            return [cod['x'], cod['y']]

    def get_competitor_score(self):
        if len(self.shadow_snake.keys()) > 0:
            return self.shadow_snake[list(self.shadow_snake.keys())[0]]['score']