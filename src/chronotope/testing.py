from cone.sql.testing import SQLLayer
import os
import pyramid_zcml


class ChronotopeLayer(SQLLayer):

    def make_app(self, **kw):
        kw['chronotope.index.dir'] = os.path.join(self.tempdir, 'index')
        kw['chronotope.settings.path'] = \
            os.path.join(self.tempdir, 'settings.xml')
        super(ChronotopeLayer, self).make_app(**kw)

    def setUp(self, args=None):
        pyramid_zcml.zcml_configure('configure.zcml', 'chronotope')
        super(ChronotopeLayer, self).setUp()
