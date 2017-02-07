#!/usr/bin/env python

import json, argparse, sys

class Parser(object):
    def __init__(self):
        self.host_list = []

    def search(self, filename, ip_addr):
        with open(filename) as data_file:
            data = json.load(data_file)
        match = [x for x in data if x['ip'] == ip_addr]
        for x in match:
            name = x['hostname'].replace("*.", "")
            self.host_list.append(name)

parser = argparse.ArgumentParser(description="""This script parses BlackSheepWall .json output
                                                and compares it to a list of in-scope ip
                                                addresses, returning in-scope FQDNs.""")
parser.add_argument("bsw_json", nargs='?', help="BlackSheepWall .json file")
parser.add_argument("scoped_hosts", nargs='?', help="List of in-scope ip addresses")
args = parser.parse_args()

parse = Parser()

if len(sys.argv) <= 2:
    parser.print_help()
    sys.exit(1)

with open(args.scoped_hosts) as ips_to_search:
    content = ips_to_search.readlines()
    content = [x.strip() for x in content]

for x in content:
    parse.search(args.bsw_json, x)

for x in set(parse.host_list):
    print x
