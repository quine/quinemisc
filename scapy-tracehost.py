#!/usr/bin/env python
"""
scapy-tracehost.py
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

Wrapper script for scapy's TCP traceroute function. Takes in a single
destination hosts along with an optional destination TCP port, runs the
traceroute, generates a graph using scapy's graph functionality.

I created this primarily to help w/external recon during certain parts of an
external (or, hell, even internal) network penetration test.

TODO: better comments; possible merge w/scapy-tracenet.py
"""

from scapy import all as scapy
from optparse import OptionParser
from datetime import datetime
import sys 


from os import geteuid

def main():
    usage = "%prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-H","--host",dest="opthost",help="Specify target host")
    parser.add_option("-p","--port",dest="optdstport",help="Specify traceroute port", default="80")
    parser.add_option("-f","--file",dest="optoutfile",help="Specify graph output file (defaults to [OPTHOSTSFILE]-TIMESTAMP.svg")
    parser.add_option("-r","--resolve",dest="resolve",action="store_true",help="Enable AS resolution",default=False)

    (options, args) = parser.parse_args()

    mandatory = ['opthost']
    for o in mandatory:
        if not options.__dict__[o]:
            print "Mandatory option, OPTHOST, is missing\n"
            parser.print_help()
            exit(-1)

    host = options.opthost
    dstport = options.optdstport
    if options.optoutfile:
        outfile = options.optoutfile
    else:
        outfile = host + "-" + datetime.now().strftime("%Y%m%d%H%M%S") + ".svg"

    if options.resolve == False:
        scapy.conf.AS_resolver=None

    tracehost(host,dstport,outfile)


def tracehost(host,dstport,outfile):
	res,unans = scapy.traceroute(host, dport=int(dstport))
	res.graph(type="svg",target=">"+outfile)

if __name__ == '__main__':
    if geteuid() !=0:
        print "[-] This script must be run as root. Sorry..."
        sys.exit(1)
    main()
