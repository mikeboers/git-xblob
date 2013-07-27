import datetime
import errno
import os
import unittest
from subprocess import call, check_call


start_time = datetime.datetime.utcnow()


class TestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)
        self._sandbox = None

    @property
    def sandbox(self):
        if self._sandbox is None:
            self._sandbox = os.path.abspath(os.path.join(
                __file__, '..', 'sandbox', start_time.isoformat('T'), self.__class__.__name__,
            ))
            try:
                os.makedirs(self._sandbox)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        return self._sandbox
