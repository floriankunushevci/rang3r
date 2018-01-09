#!/usr/bin/env python
import sys
import socket
import subprocess
import Queue
from threading import Thread, Lock
from datetime import datetime
import re
import os
import optparse 
parser = optparse.OptionParser()
parser.add_option('--ip',dest="question",help="test ")
opt , args = parser.parse_args()

if opt.question :
   question = (opt.question)
elif not (opt.question) :
   print("--ip option is required ")
   sys.exit()
#end ip = option

num_threads = 30
ips_q = Queue.Queue()
out_q = Queue.Queue()

ips = []
#question = raw_input("Write IP: ")
fix = ".".join(question.split('.')[0:-1]) + "."
for i in range(1,254):
  ips.append(fix+str(i))

def thread_pinger(i, q):
  """Pings hosts in queue"""
  while True:
    ip = q.get()
    args=['/bin/ping', '-c', '1', '-W', '3', str(ip)]
    p_ping = subprocess.Popen(args,
                              shell=False,
                              stdout=subprocess.PIPE)
    p_ping_out = p_ping.communicate()[0]

    if (p_ping.wait() == 0):
      search = re.search(r'rtt min/avg/max/mdev = (.*)/(.*)/(.*)/(.*) ms',
                         p_ping_out, re.M|re.I)
      ping_rtt = search.group(2)
      out_q.put(str(ip))

    q.task_done()

for i in range(num_threads):
  worker = Thread(target=thread_pinger, args=(i, ips_q))
  worker.setDaemon(True)
  worker.start()

for ip in ips:
  ips_q.put(ip)
ips_q.join()

while True:
  try:
    msg = out_q.get_nowait()
  except Queue.Empty:
    break
  with open("junk.txt", "a") as myfile:
    	myfile.write(msg + "\n")
        myfile.close()
print "-" * 30
print "Alive Hosts: "
print ""
with open("junk.txt", "r") as ins:
	array = []
	for ip in ins:
		sys.stdout.write(ip)
print "-" * 30
print "Port Open / Report: "
print ""
os.system("python files/portscan.py")
os.system("rm -rf junk.txt")
print "-" * 30
