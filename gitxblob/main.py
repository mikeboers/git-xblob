"""
usage: git xblob init [--get <url>] [--put <url>] [.]
   or: git xblob add <path> [...]
   or: git xblob fetch [-r]
   or: git xblob push
"""

import sys
from optparse import OptionParser


def main():
    if len(sys.argv) == 1:
        print __doc__.strip()
        exit(1)
    command_name = sys.argv[1]
    command_func = globals().get('main_' + command_name)
    if not command_func:
        print __doc__.strip()
        exit(1)
    command_func()


def main_init():
    print 'git xblob init: not implemented'
    exit(2)
