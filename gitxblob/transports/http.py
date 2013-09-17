import os
import urllib
import urlparse

from ..utils import call, debug, copy_file_obj


def build_http(url):
    return HttpTransport(url)


class HttpTransport(object):

    def __init__(self, url):
        self.url = url
        self.parts = urlparse.urlsplit(url)

    def get(self, digest, dst_path):

        remote_path = os.path.join(self.parts.path, digest[:2], digest[2:])
        xblob_url = os.path.join(self.url, digest[:2], digest[2:])

        debug('downloading %s', xblob_url)
        
        response = urllib.urlopen(xblob_url)
        if response.getcode() != 200:
            raise RuntimeError('HTTP %s from %s' % (response.getcode(), xblob_url))

        with open(dst_path, 'w') as fh:
            copy_file_obj(response, fh)

        return xblob_url


    def put(self, digest, src_path):
        raise NotImplementedError('http PUT')

