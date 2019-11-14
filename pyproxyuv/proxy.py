#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import signal
import pyuv

CLIENT = {}
clients = []

def cudp_on_read(handle, ip_port, flags, data, error):
    if data is not None:
        print(data)
        cipport = CLIENT[handle]
        handle.send(cipport, data)


def ctcp_on_read(client, data, error):
    if data is None:
        client.close()
        clients.remove(client)
        return

    print(data)
    cli = CLIENT[client]

    cli.handle.write(data)


class UdpClient(object):
    def __init__(self, ip_port):
        self.loop = pyuv.Loop.default_loop()
        self.udp = pyuv.UDP(self.loop)
        self.udp.start_recv(cudp_on_read)
        self.ip_port = ip_port
        global CLIENT
        CLIENT.update({self.udp: ip_port})

    def sendto(self, data):
        self.udp.try_send(('127.0.0.1', 17056), data)

    ip_port = ('', 0)

    loop = None

class TcpClient(object):
    def __init__(self, ip_port):
        self.loop = pyuv.Loop.default_loop()
        self.tcp = pyuv.TCP(self.loop)
        self.ip_port = ip_port
        global CLIENT

    def on_connect(self, tcp, error):
        self.tcp.start_read(ctcp_on_read)

    def write(self, data):
        self.tcp.write(data)

    def connect(self):
        self.tcp.connect(("127.0.0.1", 17057), self.on_connect)


    ip_port = ('', 0)
    handle = None
    loop = None


def udp_on_read(handle, ip_port, flags, data, error):
    if data is not None:
        c = UdpClient(ip_port)
        c.sendto(data)


def signal_cb(handle, signum):
    signal_h.close()
    server.close()


def tcp_on_read(client, data, error):
    if data is None:
        client.close()
        clients.remove(client)
        return

    print(data)
    cipport = CLIENT[client]
    cipport.write(data)

def tcp_on_connection(server, error):
    client = pyuv.TCP(server.loop)
    server.accept(client)
    clients.append(client)
    client.start_read(tcp_on_read)

    c = TcpClient(client.getpeername())
    c.connect()
    c.handle = client

    global CLIENT
    CLIENT.update({c.handle: c})


print("PyUV version %s" % pyuv.__version__)

loop = pyuv.Loop.default_loop()

server = pyuv.UDP(loop)
server.bind(("0.0.0.0", 17046))
server.start_recv(udp_on_read)

signal_h = pyuv.Signal(loop)
signal_h.start(signal_cb, signal.SIGINT)


tcpserver = pyuv.TCP(loop)
tcpserver.bind(("0.0.0.0", 17047))
tcpserver.listen(tcp_on_connection)

loop.run()

print("Stopped!")
