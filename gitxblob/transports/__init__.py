import re


def get_transport(url):

    m = re.match(r'^(\w+)(?:$|:)', url)
    if not m:
        raise ValueError('bad transport url; got %r' % url)

    scheme = m.group(1)

    try:
        mod = __import__('gitxblob.transports.%s' % scheme, fromlist=['.'])
    except ImportError:
        raise ValueError('could not find transport %r' % scheme)


    factory = getattr(mod, 'build_%s' % scheme, None)
    if not factory:
        raise ValueError('could not find transport factory for %r' % scheme)

    return factory(url)

