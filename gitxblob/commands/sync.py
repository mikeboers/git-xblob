import os
import subprocess
import urlparse

from ..utils import git


def run_sync(args):

    git_path = git('rev-parse --git-dir').strip()
    xblob_dir = os.path.join(git_path, 'xblobs')

    raw_put_uri = git('config xblob.put').strip()
    put_uri = urlparse.urlsplit(raw_put_uri)

    # urlsplit('scp:mikeboers.com:/srv/mikeboers.com/files/xblob-sandbox')
    # SplitResult(scheme='scp', netloc='', path='mikeboers.com:/srv/mikeboers.com/files/xblob-sandbox', query='', fragment='')    '''
    
    if put_uri.scheme == 'rsync':
        subprocess.call(['rsync', '-avx', 
            xblob_dir.rstrip('/') + '/',
            put_uri.path.rstrip('/') + '/',
        ])

    else:
        print 'unknown xblob.put scheme:', raw_put_uri