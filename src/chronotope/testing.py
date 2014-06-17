import tempfile
import shutil
import datetime
import pyramid_zcml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cone.app.testing import Security
from chronotope.sql import initialize_sql


class ChronotopeLayer(Security):

    def setUp(self, args=None):
        super(ChronotopeLayer, self).setUp()
        pyramid_zcml.zcml_configure('configure.zcml', 'chronotope')
        self.tempdir = tempfile.mkdtemp()
        self.init_sql()

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
        self.sql_session = maker()
