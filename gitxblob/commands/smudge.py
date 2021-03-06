import re
import sys
import os

from ..utils import call, git, makedirs, chunked, copy_file_obj, debug, CallError, stderr
from ..transports import get_transport


def run_smudge(args):

    if args:
        debug('smudge %s', args[0])

    content = sys.stdin.read(1024)
    m = re.match(r'^git-xblob: ([\da-f]+)\s*$', content)

    # Pass it through if it doesn't match.
    if not m:
        sys.stdout.write(content)
        copy_file_obj(sys.stdin, sys.stdout)
        return

    digest = m.group(1).lower()
    git_path = git('rev-parse --git-dir').strip()
    xblob_path = os.path.join(git_path, 'xblobs', digest[:2], digest[2:])

    if not os.path.exists(xblob_path):

        makedirs(os.path.dirname(xblob_path))
        
        get_url = config('xblob.get')
        if not get_url:
            stderr('Please set `git config xblob.get <url>`.')
            return 1
        transport = get_transport(get_uri)
        transport.get(digest, xblob_path)


    with open(xblob_path) as fh:
        copy_file_obj(fh, sys.stdout)

