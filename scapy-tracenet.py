#!/usr/bin/env python

from scapy import all as scapy
import sys 

from mmap import mmap, MAP_PRIVATE, PROT_READ
from os import fstat
from os import geteuid

def usage():
	print "Usage: " + sys.argv[0] + " customer hostfile"
	sys.exit(1)

def tracehost(customer, thostsfile):
	f = file(thostsfile,mode='rt')
	fd = f.fileno()
	m = mmap(fd, fstat(fd).st_size, MAP_PRIVATE, PROT_READ)

	thosts=[]
	while True:
	        line = m.readline()
        	if not line: break
        	thosts.extend(line.split())

	res,unans = scapy.traceroute(thosts)
	res.graph(type="svg",target=">" +customer+"-traceroute.svg")

#	for thost in thosts:
#        	res1,unans1 = scapy.traceroute(thost)
#        	res1.graph(type="ps",target=">/tmp/"+cust+"-traceroute-"+thost)

def getargs():
	argc = len(sys.argv)
	if argc != 3:
		usage()

	tracehost(sys.argv[1],sys.argv[2])

if __name__ == '__main__':
	if geteuid() !=0:
		print "This script must be run as root. Sorry..."
		sys.exit(1)
	getargs()
