#!/usr/bin/env python

from scapy import all as scapy
import sys 

from os import geteuid

def usage():
	print "Usage: " + sys.argv[0] + " host"
	sys.exit(1)

def tracehost(host):
	res,unans = scapy.traceroute(host)
	res.graph(type="svg",target=">"+host+"-traceroute.svg")

def getargs():
	argc = len(sys.argv)
	if argc != 2:
		usage()

	tracehost(sys.argv[1])

if __name__ == '__main__':
	if geteuid() !=0:
		print "This script must be run as root. Sorry..."
		sys.exit(1)
	getargs()
