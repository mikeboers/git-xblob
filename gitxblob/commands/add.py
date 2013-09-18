"""usage: git-xblob add <path> [...]"""

import os
import re
from optparse import OptionParser

from ..utils import git, call


def bail(code=1):
    print __doc__.strip()
    exit(code)


def run_add(args):

    opt_parser = OptionParser()
    opt_parser.add_option('-g', '--glob', action='store_true')
    opts, args = opt_parser.parse_args(args)

    if not args:
        bail()

    if not opts.glob:
        missing_any = False
        for path in args:
            if not os.path.exists(path):
                print path, 'does not exist'
                missing_any = True
        if missing_any:
            return 3

    for path in args:

        if opts.glob:
            dir_ = ''
            pattern = path
        else:
            dir_, pattern = os.path.split(path)
            pattern = '/' + pattern

        # Clean up spaces.
        pattern = re.sub(r'\s', '[[:space:]]', pattern)
        
        if opts.glob or 'filter: xblob' not in call('git check-attr filter %s', path):

            attributes_path = os.path.join(dir_, '.gitattributes')
            with open(attributes_path, 'a') as fh:
                fh.write('%s filter=xblob\n' % pattern)

            git('add -f %s', attributes_path)

            if not opts.glob:
                git('add -f %s', path)
            