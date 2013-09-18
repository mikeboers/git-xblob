import errno
import os

from .utils import call


def _path():
    return os.path.join(call('git rev-parse --git-dir').strip(), 'info', 'xblobs_to_sync')


def append(digest):
    with open(_path(), 'a') as fh:
        fh.write('%s\n' % digest)


def iter():
    try:
        fh = open(_path(), 'r')
    except IOError:
        return
    with fh:
        for line in fh:
            yield line.strip()


def clear():
    try:
        os.unlink(_path())
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

