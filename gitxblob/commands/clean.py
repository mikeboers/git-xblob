import tempfile
import hashlib
import shutil
import sys
import os
import subprocess

from ..utils import call, git, makedirs, chunked, debug, CallError, stderr
from ..transports import get_transport
from .. import synclist


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
        stderr('New xblob; remember to `git xblob sync` before pushing.')
        synclist.append(digest)
        makedirs(os.path.dirname(xblob_path))
        shutil.copyfile(src_path, xblob_path)

    print 'git-xblob:', digest
