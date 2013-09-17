import tempfile
import hashlib
import shutil
import sys
import os
import subprocess

from ..utils import call, git, makedirs, chunked, debug, CallError, stderr
from ..transports import get_transport


def run_clean(args):

    src_path = args[0] if args else None
    if src_path is not None:
        debug('clean %s', src_path)

    # Save the contents to a temporary file, and hash it as we go.
    hash_ = hashlib.sha1()
    for chunk in chunked(sys.stdin):
        hash_.update(chunk)
    digest = hash_.hexdigest().lower()

    # Save the content into .git/xblobs
    git_path = git('rev-parse --git-dir').strip()
    xblob_path = os.path.join(git_path, 'xblobs', digest[:2], digest[2:])

    if src_path is not None and not os.path.exists(xblob_path):

        # "PUT" it before placing into local xblobs, as we use the existence
        # in local xblobs to signal existence in remote store.

        try:
            put_url = call('git config xblob.put').strip()
        except CallError:
            stderr('Please set `git config xblob.put`.')
            return 1

        transport = get_transport(put_url)
        transport.put(digest, src_path)

        makedirs(os.path.dirname(xblob_path))
        shutil.copyfile(src_path, xblob_path)

    print 'git-xblob:', digest
