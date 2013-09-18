"""usage: git-xblob add <path> [...]"""

import os
import re

from ..utils import git


def bail(code=1):
    print __doc__.strip()
    exit(code)


def run_add(paths):

    if not paths:
        bail()

    missing_any = False
    for path in paths:
        if not os.path.exists(path):
            print path, 'does not exist'
            missing_any = True
    if missing_any:
        return 3

    for path in paths:

        # Add it to the attributes file.
        head, tail = os.path.split(path)

        # Clean up spaces.
        tail = re.sub(r'\s', '[[:space:]]', tail)
        
        attributes_path = os.path.join(head, '.gitattributes')
        with open(attributes_path, 'a') as fh:
            fh.write('/%s filter=xblob\n' % tail)

        # Add the file and the attributes.
        git('add -f %s', attributes_path)
        git('add -f %s', path)
        