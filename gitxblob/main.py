"""
usage: git xblob init
   or: git xblob add <path> [...]
   or: git xblob sync
"""

import re
import sys
from optparse import OptionParser


def bail(code=1):
    print __doc__.strip()
    exit(code)


def main():

    if len(sys.argv) == 1:
        bail(1)

    command_name = sys.argv[1]
    if not re.match(r'^\w+$', command_name):
        bail(2)

    try:
        command_mod = __import__('gitxblob.commands.%s' % command_name, fromlist=['.'])
    except ImportError:
        bail(3)

    command_func = getattr(command_mod, 'run_%s' % command_name, None)
    if not command_func:
        bail(4)

    exit(command_func(sys.argv[2:]) or 0)


def main_init():
    print 'git xblob init: not implemented'
    exit(2)
