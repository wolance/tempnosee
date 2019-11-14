#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import signal
import pyuv

a = 0

def on_read(handle, ip_port, flags, data, error):
    global a
    a = a + 1
    if data is not None:
        dstdata = ' %s(udp:%d) ' % (data, a)
        print(dstdata)
        handle.send(ip_port,dstdata)

def signal_cb(handle, signum):
    signal_h.close()
    udpserver.close()
    [c.close() for c in clients]
    tcpserver.close()
    exit(1)



def tcp_on_read(client, data, error):
    if data is None:
        client.close()
        clients.remove(client)
        return
    global a
    a = a + 1
    dstdata = ' %s(tcp:%d) ' % (data, a)
    print(dstdata)
    client.write(dstdata)

def tcp_on_connection(server, error):
    client = pyuv.TCP(server.loop)
    server.accept(client)
    clients.append(client)
    print(str(client.getpeername()))
    client.start_read(tcp_on_read)



print("PyUV version %s" % pyuv.__version__)

loop = pyuv.Loop.default_loop()

udpserver = pyuv.UDP(loop)
udpserver.bind(("0.0.0.0", 17056))
udpserver.start_recv(on_read)

signal_h = pyuv.Signal(loop)

signal_h.start(signal_cb, signal.SIGINT)

clients = []
tcpserver = pyuv.TCP(loop)
tcpserver.bind(("0.0.0.0", 17057))
tcpserver.listen(tcp_on_connection)

signal_h.start(signal_cb, signal.SIGINT)

loop.run()

print("Stopped!")
