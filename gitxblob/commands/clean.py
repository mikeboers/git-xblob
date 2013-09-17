import tempfile
import hashlib
import shutil
import sys
import os
import subprocess

from ..utils import git, makedirs, chunked


def run_clean(args):

    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    try:

        # Save the contents to a temporary file, and hash it as we go.
        hash_ = hashlib.sha1()
        for chunk in chunked(sys.stdin):
            hash_.update(chunk)
            tmp_file.write(chunk)
        digest = hash_.hexdigest().lower()
        tmp_file.close()

        # Save the content into .git/xblobs
        git_path = git('rev-parse --git-dir').strip()
        xblob_path = os.path.join(git_path, 'xblobs', digest[:2], digest[2:])
        if not os.path.exists(xblob_path):
            makedirs(os.path.dirname(xblob_path))
            shutil.copyfile(tmp_file.name, xblob_path)

        print 'git-xblob:', digest

    finally:
        os.unlink(tmp_file.name)