#!/usr/bin/env python

from scapy import all as scapy
from optparse import OptionParser
import sys 


from os import geteuid

def main():
    usage = "%prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-H","--host",dest="dsthost",help="Specify target host")
    parser.add_option("-p","--port",dest="dstport",help="Specify traceroute port", default="80")
    parser.add_option("-f","--file",dest="dstfile",help="Specify output file")
    parser.add_option("-r","--resolve",dest="resolve",action="store_true",help="Enable AS resolution",default=False)

    (options, args) = parser.parse_args()

    dsthost = options.dsthost
    dstport = options.dstport
    dstfile = options.dstfile
    if options.resolve == False:
        scapy.conf.AS_resolver=None

    tracehost(dsthost,dstport,dstfile)


def tracehost(dsthost,dstport,dstfile):
	res,unans = scapy.traceroute(dsthost, dport=int(dstport))
	res.graph(type="svg",target=">"+dstfile)

if __name__ == '__main__':
    if geteuid() !=0:
        print "[-] This script must be run as root. Sorry..."
        sys.exit(1)
    main()
