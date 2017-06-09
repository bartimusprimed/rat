#!/usr/local/bin/python3

from xmlrpc import client
import socket

server_ip = socket.gethostbyname(socket.gethostname())
server_port = 4000


class RatClient():

    def __init__(self):
        self.rat_client = client.ServerProxy("http://{0}:{1}"
                                             .format(server_ip, server_port))


if __name__ == '__main__':
    rat = RatClient()
    rat.rat_client.print_name("bartimus")
