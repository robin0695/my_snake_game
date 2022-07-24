from collections import deque
from datetime import datetime
from pydoc import cli
from socket import *
import select
import uuid
import json
import struct
import time

HOST = ''
PORT = 21546
BUFFER_SIZE = 1024
ADDR = (HOST, PORT)

class SnakeServer:

    def __init__(self) -> None:
        self.tcp_server_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_server_socket.bind(ADDR)
        self.tcp_server_socket.listen(2)
        self.tcp_server_socket.setblocking(0)

    def up(self):

        rlist = deque([self.tcp_server_socket])
        wlist = deque()
        xlist = deque()

        clients = {}
        client_data = {}
        remove_item = []

        while True:
            
            time.sleep(0.02)
            read_list, write_list, error_list = select.select(rlist, wlist, xlist)
                    
            # print(len(remove_item), len(read_list), len(write_list))
            for socket_item in read_list:
                if socket_item is self.tcp_server_socket:
                    tcp_client_socket, addr = socket_item.accept()
                    tcp_client_socket.setblocking(1)
                    rlist.append(tcp_client_socket)
                    wlist.append(tcp_client_socket)
                    
                    # genclient id and send to client.
                    client_id = str(uuid.uuid4())
                    clients[tcp_client_socket] = client_id
                    client_id_data = {'client-id': f'{client_id}'}
                    client_data_json = json.dumps(client_id_data)
                    tcp_client_socket.sendall(struct.pack('i', len(client_data_json.encode('utf-8'))))
                    tcp_client_socket.sendall(client_data_json.encode('utf-8'))

                else:
                    try:
                        data_len = struct.unpack('i', socket_item.recv(4))[0]
                        recved_len = 0
                        chunks = []
                        while recved_len < data_len:
                            chunk = socket_item.recv(data_len - recved_len)
                            if chunk == b'':
                                raise RuntimeError('socket connection broken')
                            chunks.append(chunk)
                            recved_len += len(chunk)
                            
                        if chunks:
                            data_dic = json.loads(b''.join(chunks))
                            client_data.update(data_dic)
                            print(client_data)
                    except ConnectionResetError as e:
                        print(e)
                        remove_item.append(socket_item)
            
            for it in remove_item:
                if it in read_list and it in write_list:
                    del client_data[clients[it]]
                    rlist.remove(it)
                    wlist.remove(it)

            for write_item in write_list:

                json_data = json.dumps(client_data).encode('utf-8')
                json_data_length = len(json_data)
                try:
                    write_item.sendall(struct.pack('i', json_data_length))
                    write_item.sendall(json_data)
                except ConnectionResetError as e:
                    print(e)
                    remove_item.append(write_item)

            remove_item = []

            for error_item in error_list:
                print(error_item)
            
SnakeServer().up()