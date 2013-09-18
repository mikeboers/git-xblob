import errno
import os
import re
import shlex
import subprocess
import sys


_config = {}

def config(key, *values):
    "Memoized git config accessor."

    if not values:

        # From the cache.
        try:
            return _config[key]
        except KeyError:
            pass

        try:
            _config[key] = value = call('git config %s', key).strip()
        except CallError:
            _config[key] = value = None
        return value

    else:

        call('git config --replace-all %s %s', key, values[0])
        _config[key] = values[0]


def stderr(*args):
    sys.stderr.write(' '.join(str(x) for x in args) + '\n')


def debug(msg, *args):
    if not config('xblob.debug'):
        return
    if args:
        msg = msg % args
    sys.stderr.write('git-xblob(%d): %s\n' % (os.getpid(), msg))


def call(command, *args, **kwargs):

    command = shlex.split(command)
    if args:
        args = list(args)
        for i, chunk in enumerate(command):
            command[i] = re.sub(r'%s', lambda m: args.pop(0), chunk)

    # debug('utils.call: %r', command)

    if 'stdout' in kwargs and kwargs['stdout'] is None:
        return subprocess.call(command, **kwargs)
    else:
        return subprocess.check_output(command, **kwargs)


CallError = subprocess.CalledProcessError


def git(command, *args, **kwargs):
    return call('git ' + command, *args, **kwargs)


def makedirs(path):
    """Wrapper around os.makedirs which does not fail if the directory exists."""
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def chunked(fh, size=2**14):
    while True:
        chunk = fh.read(size)
        if not chunk:
            return
        yield chunk


def copy_file_obj(src, dst, size=2**14):
    for chunk in chunked(src, size):
        dst.write(chunk)

