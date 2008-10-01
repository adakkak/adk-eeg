#!/usr/bin/python

from __future__ import generators
import socket

PCKT_SIZE = 1024

class NsdSock(object):
    def __init__(self, sock):
        self.sock  = sock

    def role(self):
        self.sock.send("role\n")
        return self.sock.recv(PCKT_SIZE)
    
    def status(self):
        self.sock.send("status\n")
        return self.sock.recv(PCKT_SIZE)

    def eeg(self):
        self.sock.send("eeg\n")
        return self.sock.recv(PCKT_SIZE)

    def display(self):
        self.sock.send("display\n")
        return self.sock.recv(PCKT_SIZE)

    def set_header(self, data):
        self.sock.send("setheader %s\n" % data)
        return self.sock.recv(PCKT_SIZE)

    def watch(self, client):
        self.sock.send("watch %s\n" % client)
        return self.sock.recv(PCKT_SIZE)

    def recv(self):
        return self.sock.recv(PCKT_SIZE)

    def unwatch(self, client):
        self.sock.send("unwatch %s\n" % client)
        return self.sock.recv(PCKT_SIZE)

    def get_header(self, index):
        self.sock.send("getheader %s\n" % index)
        return self.sock.recv(PCKT_SIZE)

    def close(self):
        self.sock.send("close\n")
        return self.sock.recv(PCKT_SIZE)

    def hello(self):
        self.sock.send("hello\n")
        return self.sock.recv(PCKT_SIZE)

    def cmd(self):
        self.sock.send("!\n")
        return self.sock.recv(PCKT_SIZE)

class NsdReader(NsdSock):
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = ('localhost', 8336)
        self.sock.connect(addr)

        super(NsdReader, self).__init__(self.sock)

        self.display( )
        self.watch(0)

    def get_data(self):
        while 1:
            yield self.recv( ).split( )

    def parse(self, data):
        parsed_data = []
        try:
            client_index, packet_count, channel_count = data[1:4]
            samples = data[4:]
            while samples.count('!') > 0:
                parsed_data.append(self.parse(samples[samples.index('!'):]))
                samples = samples[:samples.index('!')]
            parsed_data.append({"client_index": client_index, "packet_count": packet_count, 
                                "channel_count": channel_count, "samples": samples})
    #        if len(parsed_data) == 0:
    #            return {"client_index": 0, "packet_count": 0, "channel_count": 0, "samples": []}

        except:
            pass
        return parsed_data

    def close(self):
        self.sock.close( )

if __name__ == "__main__":
    count = 0
    reader = NsdReader()

    data = []
    while count < 200:
        data += reader.parse(reader.get_data( ).next( ))
        count += 1
    for k in data:
        print k
    reader.close( )


