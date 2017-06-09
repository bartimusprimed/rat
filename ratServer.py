#!/usr/local/bin/python3

from xmlrpc import server
import socket

server_ip = socket.gethostbyname(socket.gethostname())
server_port = 4000

class RatServer:

    def __init__(self):
        self.rat_server = server.SimpleXMLRPCServer((server_ip, server_port))

    def print_name(self, name):
        print(name)
        return name

if __name__ == '__main__':
    rat = RatServer()
    rat.rat_server.register_function(rat.print_name, "print_name")
    rat.rat_server.serve_forever()
