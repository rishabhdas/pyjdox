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
import sys
from lib import pyjdox


def get_doc(pyjdoxobj, filepath):
    """
    Get code documentation
    """
    mod = pydoc.importfile(filepath)
    jdata = pyjdoxobj.describe(mod, filepath)
    return jdata


def main():
    """
    Take user input and run get python doc as JSON
    """
    # Get user Input
    parser = argparse.ArgumentParser(description='pyjdox parser')
    parser.add_argument('-f', '--file', help='Pass python file')
    parser.add_argument('-d', '--dir', help='Path to library source tree')
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
            jdata = get_doc(pyjdoxobj, args.file)
            fname = '%s.json' % os.path.basename(args.file)
            fname = os.path.join(output_dir, fname)
            with open(fname, 'w') as jfile:
                json.dump(jdata, jfile)
            print("Output has been created successfully")
            print("Path: %s" % (fname))

    # Run pyjdox on source tree
    if args.dir:
        filelist = []
        output_dir = os.path.join(output_dir, os.path.basename(args.dir))
        if args.dir.startswith('~'):
            args.dir = os.path.expanduser(args.dir)
        try:
            if not os.path.exists(output_dir) or not os.path.isdir(output_dir):
                os.makedirs(output_dir)
            for folder, subs, files in os.walk(args.dir):
                for filename in files:
                    if filename.endswith('.py'):
                        filelist.append(os.path.join(folder, filename))

            for fname in filelist:
                print fname
                jdata = get_doc(pyjdoxobj, fname)
                ofloc = os.path.dirname((os.path.relpath(fname, args.dir)))
                ofloc = os.path.join(output_dir, ofloc)
                if not os.path.exists(ofloc) or not os.path.isdir(ofloc):
                    os.makedirs(ofloc)
                ofname = '%s.json' % os.path.basename(fname)
                ofname = os.path.join(ofloc, ofname)
                with open(ofname, 'w') as jfile:
                    json.dump(jdata, jfile)
                print("Output has been created successfully")
                print("Path: %s" % (output_dir))
        except Exception as e:
            print e.message
            sys.exit(1)

if __name__ == '__main__':
    main()
