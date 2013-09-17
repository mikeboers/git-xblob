import re
import sys
import os

from ..utils import git, makedirs, chunked, copy_file_obj


def run_smudge(args):


    content = sys.stdin.read(1024)
    m = re.match(r'^git-xblob: ([\da-f]+)\s*$', content)

    # Pass it through if it doesn't match.
    if not m:
        sys.stdout.write(content)
        copy_file_obj(sys.stdin, sys.stdout)
        return

    digest = m.group(1).lower()
    git_path = git('rev-parse', '--git-dir').strip()
    xblob_path = os.path.join(git_path, 'xblobs', digest[:2], digest[2:])

    if not os.path.exists(xblob_path):

        print >> sys.stderr, 'git-xblob: getting', digest
        
        makedirs(os.path.dirname(xblob_path))

        raw_get_uri = subprocess.check_output(['git', 'config', 'xblob.get']).strip()
        get_uri = urlparse.urlsplit(raw_get_uri)

        '''
        >>> urlsplit('http://files.mikeboers.com/xblob-sandbox')
        SplitResult(scheme='http', netloc='files.mikeboers.com', path='/xblob-sandbox', query='', fragment='')
        '''
        if get_uri.scheme in ('http', 'https'):

            xblob_url = '%s/%s/%s' % (raw_get_uri.strip('/'), digest[:2], digest[2:])

            response = urllib.urlopen(xblob_url)
            if response.getcode() != 200:
                print >> sys.stderr, 'HTTP %s from %s' % (response.getcode(), xblob_url)
                return 3

            with open(xblob_path, 'w') as fh:
                copy_file_obj(response, fh)

        else:
            print >> sys.stderr, 'unknown xblob.get scheme:', raw_get_uri

    with open(xblob_path) as fh:
        copy_file_obj(fh, sys.stdout)

