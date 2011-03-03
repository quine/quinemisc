#!/usr/bin/env python

from scapy import all as scapy
from optparse import OptionParser
import sys
from mmap import mmap, MAP_PRIVATE, PROT_READ
from os import fstat
from os import geteuid

def main():
    usage = "%prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-H","--hosts",dest="dsthostsfile",help="Specify hosts file")
    parser.add_option("-p","--port",dest="dstport",help="Specify traceroute port", default="80")
    parser.add_option("-f","--file",dest="dstfile",help="")
    parser.add_option("-r","--resolve",dest="resolve",action="store_true",help="Enable AS resolution",default=False)

    (options, args) = parser.parse_args()

    dsthostsfile = options.dsthostsfile
    dstport = options.dstport
    dstfile = options.dstfile
    if options.resolve == False:
        scapy.conf.AS_resolver=None

    tracehost(dsthostsfile,dstport,dstfile)

def tracehost(dsthostsfile,dstport,dstfile):
	f = file(dsthostsfile,mode='rt')
	fd = f.fileno()
	m = mmap(fd, fstat(fd).st_size, MAP_PRIVATE, PROT_READ)

	dsthosts=[]
	while True:
	        line = m.readline()
        	if not line: break
        	dsthosts.extend(line.split())

	res,unans = scapy.traceroute(dsthosts,dport=int(dstport))
	res.graph(type="svg",target=">"+dstfile)

#	for thost in thosts:
#        	res1,unans1 = scapy.traceroute(thost)
#        	res1.graph(type="ps",target=">/tmp/"+cust+"-traceroute-"+thost)

if __name__=='__main__':
    if geteuid() !=0:
        print "[-] This script must be run as root. Sorry..."
        sys.exit(1)
    main()
