#!/usr/bin/env python
import sys
import socket
import subprocess

from Queue import Queue
from threading import Thread, Lock
from datetime import datetime

THREADS = 16
SCAN_FOR = "80,445,139,135,443,21,22,23,25,53,3386,8080,110,1443,1434,137"
SCAN_FOR = SCAN_FOR.replace(' ', '')
SCAN_PORTS = []
segments = SCAN_FOR.split(",")
for seg in segments:
    if '-' not in seg:
        SCAN_PORTS.append(int(seg))
    else:
        start, stop = seg.split('-')
        SCAN_PORTS += range(int(start), int(stop))
        SCAN_PORTS.append(int(stop))
SCAN_PORTS = list(set(SCAN_PORTS))

lock = Lock()

def scanhost(remoteServer):

    remoteServerIP  = socket.gethostbyname(remoteServer)

    try:
        output = []
        for port in SCAN_PORTS:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(False)
            sock.settimeout(0.2)
            result = sock.connect_ex((remoteServerIP, port))
            if result == 0:
                output.append(port)
            sock.close()

    except socket.gaierror:
        pass
    except socket.error:
        pass
    finally:
        return output

def scanner(thread_id, ip_queue, results):
    while not ip_queue.empty():
        host = ip_queue.get()
        if len(host):
            lock.acquire()
            lock.release()
            ports = scanhost(host)
            lock.acquire()
            if len(ports):
                print host , ports
            lock.release()
        ip_queue.task_done()
    lock.acquire()
    lock.release()
ip_queue = Queue()
results = ""
with open("junk.txt", "r") as ins:
        array = []
        for line in ins:
		try:
			ip_queue.put(line.strip())
			pool = []
			for thread_id in range(THREADS):
			     t = Thread(target=scanner, args=[thread_id, ip_queue, results])
			     pool.append(t)
			     t.start()

			for thread in pool:
			    thread.join()
		except:
			raise

