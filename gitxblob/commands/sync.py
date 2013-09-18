from ..utils import config
from ..transports import get_transport


def run_sync(args):

    url = config('xblob.sync')
    if not url:
        stderr('Please set `git config xblob.sync`.')
        return 1

    transport = get_transport(url)
    transport.sync()
