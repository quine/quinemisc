#!/usr/bin/env python
"""
scapy-tracenet.py
Copyright (c) 2011, Zach Lanier <zach [-at-] n0where.org>

-----------------------------
This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; version 2
of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
-----------------------------

Wrapper script for scapy's TCP traceroute function. Takes in a file containing
destination hosts, one per line, along with an optional destination TCP port,
runs the traceroute, generates a graph using scapy's graph functionality.

I created this primarily to help w/external recon during certain parts of an
external (or, hell, even internal) network penetration test.

TODO: Add CIDR and range support; better comments
"""

from scapy import all as scapy
from optparse import OptionParser
from datetime import datetime
import sys
from mmap import mmap, MAP_PRIVATE, PROT_READ
from os import fstat
from os import geteuid

def main():
    usage = "%prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-H","--hosts",dest="opthostsfile",help="Specify hosts file")
    parser.add_option("-p","--port",dest="optdstport",help="Specify traceroute port", default="80")
    parser.add_option("-f","--file",dest="optoutfile",help="Specify graph output file (defaults to [OPTHOSTSFILE]-timestamp.svg")
    parser.add_option("-r","--resolve",dest="optresolve",action="store_true",help="Enable AS resolution",default=False)

    (options, args) = parser.parse_args()

    mandatory = ['opthostsfile']
    for o in mandatory:
        if not options.__dict__[o]:
            print "Mandatory option, OPTHOSTSFILE, is missing\n"
            parser.print_help()
            exit(-1)

    hostsfile = options.opthostsfile
    dstport = options.optdstport
    if options.optoutfile:
        outfile = options.optoutfile
    else:
        outfile = hostsfile + "-" + datetime.now().strftime("%Y%m%d%H%M%S") + ".svg"

    if options.optresolve == False:
        scapy.conf.AS_resolver=None

    tracehost(hostsfile,dstport,outfile)

def tracehost(hostsfile,dstport,outfile):
	f = file(hostsfile,mode='rt')
	fd = f.fileno()
	m = mmap(fd, fstat(fd).st_size, MAP_PRIVATE, PROT_READ)

	dsthosts=[]
	while True:
	        line = m.readline()
        	if not line: break
        	dsthosts.extend(line.split())

	res,unans = scapy.traceroute(dsthosts,dport=int(dstport))
	res.graph(type="svg",target=">"+outfile)

if __name__=='__main__':
    if geteuid() !=0:
        print "[-] This script must be run as root. Sorry..."
        sys.exit(1)
    main()
