import os
import tempfile
import shutil
import pyramid_zcml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cone.app.testing import Security
from chronotope.sql import (
    initialize_sql,
    bind_session_listeners,
)


class ChronotopeLayer(Security):

    def make_app(self, **kw):
        dummy_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        kw['chronotope.recaptcha.public_key'] = dummy_key
        kw['chronotope.recaptcha.private_key'] = dummy_key
        kw['chronotope.index.dir'] = os.path.join(self.tempdir, 'index')
        super(ChronotopeLayer, self).make_app(**kw)

    def setUp(self, args=None):
        self.tempdir = tempfile.mkdtemp()
        super(ChronotopeLayer, self).setUp()
        pyramid_zcml.zcml_configure('configure.zcml', 'chronotope')
        self.init_sql()
        self.new_request()

    def tearDown(self):
        super(ChronotopeLayer, self).tearDown()
        shutil.rmtree(self.tempdir)

    def new_request(self):
        request = super(ChronotopeLayer, self).new_request()
        request.environ['cone.sql.session'] = self.sql_session
        return request

    def init_sql(self):
        engine = create_engine('sqlite:///:memory:', echo=False)
        initialize_sql(engine)
        maker = sessionmaker(bind=engine)
        session = maker()
        bind_session_listeners(session)
        self.sql_session = session
