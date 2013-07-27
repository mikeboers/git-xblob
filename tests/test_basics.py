from . import *


class TestBasics(TestCase):

    def setUp(self):
        call(['git', 'init', self.sandbox])

    def test_tests_run(self):
        self.assert_(1)

