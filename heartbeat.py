#!/usr/bin/python

# Given a file containing a list of IP addresses,
# send heatbeat messages and maintain a list of
# alive IP's.

import time
import sys
import socket
import signal

def signal_handler(signal, frame):
    ssock.close()
    print ''
    exit(0)

# register signal handler
signal.signal(signal.SIGINT, signal_handler)

# read IP's
addrs = []
with open(sys.argv[1]) as inf:
    for line in inf:
        addrs.append(line.strip('\n'))
myaddr = sys.argv[2]
addrs.remove(myaddr)

for i in xrange(len(addrs)):
    addrs[i] = (addrs[i][:addrs[i].find(':')],
                int(addrs[i][addrs[i].find(':')+1:]))

print myaddr
print addrs

ssock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ssock.settimeout(1)
ssock.bind((myaddr[:myaddr.find(':')], int(myaddr[myaddr.find(':')+1:])))

while 1:
    # send heartbeats
    for addr in addrs:
        ssock.sendto("beat", addr)

    # maintain list of alive processes
    procs_alive = []
    reading = 1
    while reading:
        try:
            data, addr = ssock.recvfrom(10)
            procs_alive.append(addr)
        except socket.timeout:
            reading = 0

    print procs_alive

    # sleep
    time.sleep(5)
