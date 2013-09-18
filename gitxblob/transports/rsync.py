import os
import urlparse

from ..utils import call, debug
from .. import synclist


def build_rsync(url):
    return RsyncTransport(url)


class RsyncTransport(object):

    def __init__(self, url):
        self.url = url
        self.parts = urlparse.urlsplit(url)

    def get(self, digest, dst_path):
        raise NotImplementedError()

    def sync(self):
        src_dir = os.path.join(call('git rev-parse --git-dir').strip(), 'xblobs') + '/'
        dst_dir = self.parts.path.rstrip('/') + '/'
        call('rsync -avx %s %s', src_dir, dst_dir, stdout=None)
        synclist.clear()

