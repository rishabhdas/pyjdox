#!/usr/bin/python

# Rishabh Das <rishabh5290@gmail.com>
#
# This program is a free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the license, or(at your option) any
# later version. See http://www.gnu.org/copyleft/gpl.html for the full text of
# the license.


import argparse
import ConfigParser
import os
import json
import pydoc
import inspect
from lib import pyjdox

def main():
    """ Take user input and run get python doc as JSON """
    # Get user Input
    parser = argparse.ArgumentParser(description='pyjdox parser')
    parser.add_argument('-f', '--file', help='Pass python file')
    args = parser.parse_args()
    # Create object for pyjdox
    pyjdoxobj = pyjdox.pyjdox()
    # Read configuration
    config = ConfigParser.ConfigParser()
    if os.path.isfile('config'):
        config.read('config')
        output_dir = config.get('pyjdox', 'output-dir')
    # Create output directory
    if not os.path.exists(output_dir) or not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    # Run pyjdox on user input
    if args.file:
        if args.file.startswith('~'):
            args.file = os.path.expanduser(args.file)
        if os.path.isfile(args.file):
            mod = pydoc.importfile(args.file)
            jdata = pyjdoxobj.describe(mod, args.file)
            fname = '%s.json' % os.path.basename(args.file)
            fname = os.path.join(output_dir, fname)
            with open(fname, 'w') as jfile:
                json.dump(jdata, jfile)

if __name__ == '__main__':
    main()
