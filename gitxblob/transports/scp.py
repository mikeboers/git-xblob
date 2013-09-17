import os
import urlparse

from ..utils import call, debug


def build_scp(url):
    return ScpTransport(url)


class ScpTransport(object):

    def __init__(self, url):
        self.url = url
        self.parts = urlparse.urlsplit(url)

    def get(self, digest, dst_path):
        remote_path = os.path.join(self.parts.path, digest[:2], digest[2:])
        debug('downloading %s' % remote_path)
        call('scp %s %s', remote_path, dst_path)

    def put(self, digest, src_path):
        host, path = self.parts.path.split(':')
        path = path.rstrip('/')
        remote_path = '%s:%s/%s/%s' % (host, path, digest[:2], digest[2:])
        debug('uploading to %s', remote_path)
        call(
            "ssh %s '"
            "cd %s; "
            "mkdir -p %s; "
            "cat > %s; "
            "chmod a+r %s'",
            host, path, digest[:2],
            '%s/%s' % (digest[:2], digest[2:]),
            '%s/%s' % (digest[:2], digest[2:]),
            stdin=open(src_path),
        )
        return remote_path

