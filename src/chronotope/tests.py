import doctest
import interlude
import pprint
import unittest2 as unittest
from plone.testing import layered
from chronotope import testing


optionflags = doctest.NORMALIZE_WHITESPACE | \
              doctest.ELLIPSIS | \
              doctest.REPORT_ONLY_FIRST_FAILURE
layer = testing.ChronotopeLayer()


TESTFILES = [
    'model/chronotope.rst',
    'model/location.rst',
    'model/facility.rst',
    'model/occasion.rst',
    'model/attachment.rst',
]


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                testfile,
                globs={'interact': interlude.interact,
                       'pprint': pprint.pprint,
                       'pp': pprint.pprint,
                       },
                optionflags=optionflags,
                ),
            layer=layer,
            )
        for testfile in TESTFILES
        ])
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')                 #pragma NO COVERAGE
