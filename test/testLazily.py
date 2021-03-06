
# -*- coding: utf-8 -*-

# Test the lazy import module lazily.

__all__ = ('Tests',)
__version__ = '18.11.12'

from base import TestsBase, ismacOS, isNix, isPython37, isWindows, PythonX
from pygeodesy import lazily, __all__ as _all_

import os

_cmd = PythonX + " -c 'from pygeodesy import lazily, R_M, LimitError; " \
                      "import sys; " \
                      "sys.exit(0 if lazily.isLazy == %s else 1)'"
if ismacOS or isNix:
    _env_cmd = 'env %s ' + _cmd + ' >>/dev/null'
elif isWindows:  # XXX UNTESTED
    _env_cmd = 'set %s;' + _cmd
else:
    _env_cmd = None


class Tests(TestsBase):

    def testLazily(self):

        z = lazily.isLazy
        self.test('isLazy', z, z)
        if not z:
            for a, m in lazily._all_missing2(_all_):
                self.test('missing in %s' % (a,), m or None, None)

        # simple lazy_import enable tests
        self.test('cmd', _cmd, _cmd)
        if _env_cmd:
            for z in range(5):
                e = 'PYGEODESY_LAZY_IMPORT=%s' % (z,)
                c = _env_cmd % (e, z if isPython37 else None)
                self.test(e, os.system(c), 0)
        else:
            self.skip('no _env_cmd')


if __name__ == '__main__':

    t = Tests(__file__, __version__)
    t.testLazily()
    t.results()
    t.exit()
