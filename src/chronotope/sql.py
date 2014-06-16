from node.behaviors import NodeAttributes
from sqlalchemy import (
    engine_from_config,
    MetaData,
)
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
)
from sqlalchemy.ext.declarative import declarative_base
from pyramid.threadlocal import get_current_request
from cone.app.model import BaseNode


Base = declarative_base()


DBSession = scoped_session(sessionmaker())
metadata = MetaData()


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    metadata.bind = engine
    metadata.create_all(engine)


session_key = 'cone.sql.session'


def get_session(request):
    return request.environ[session_key]


class Session(object):
    """WSGI framework component that opens and closes a SQL session.

    Downstream applications will have the session in the environment,
    normally under the key 'cone.sql.session'.
    """

    def __init__(self, next_app, maker, session_key=session_key):
        self.next_app = next_app
        self.maker = maker
        self.connection_key = session_key

    def __call__(self, environ, start_response):
        environ[self.connection_key] = self.maker()
        try:
            result = self.next_app(environ, start_response)
            return result
        finally:
            # XXX close session required?
            pass


class ReadMappingRecord(object):

    def __getitem__(self, name):
        if hasattr(self, name):
            return getattr(self, name)
        raise KeyError(name)

    def get(self, name, default=None):
        try:
            return self[name]
        except KeyError:
            return default


class SQLRowNodeAttributes(NodeAttributes):
    """Class representing attributes of an SQLNode.
    """
    _keys = list()

    def __init__(self, name, parent, record):
        NodeAttributes.__init__(self, name, parent)
        self.record = record

    def __getitem__(self, name):
        if name in self:
            return getattr(self.record, name)
        raise KeyError(name)

    def __setitem__(self, name, value):
        if name in self:
            setattr(self.record, name, value)
        else:
            raise KeyError(u'unknown attribute: %s' % name)

    def __delitem__(self):
        raise NotImplementedError

    def __iter__(self):
        return iter(self._keys)

    def __contains__(self, name):
        return name in self._keys


class SQLRowNode(BaseNode):

    def __init__(self, name=None, parent=None, record=None):
        self.__name__ = name
        self.__parent__ = parent
        self._new = False
        if record is None:
            self._new = True
            record = self.record_factory()
        self.record = record

    def record_factory(self):
        raise NotImplementedError(u"Abstract SQLRowNode does not implement "
                                  u"record_factory")

    def attributes_factory(self, name, parent):
        raise NotImplementedError(u"Abstract SQLRowNode does not implement "
                                  u"attributes_factory")

    def __call__(self):
        session = get_session(get_current_request())
        if self._new:
            session.add(self.record)
            self._new = False
        session.commit()


def make_app(next_app, global_conf, **local_conf):
    """Make a Session app.
    """
    from chronotope import sql
    engine = engine_from_config(local_conf, prefix='sqlalchemy.')
    sql.Base.metadata.create_all(engine)
    maker = sessionmaker(bind=engine)
    sql.session_key = local_conf.get('session_key', sql.session_key)
    return Session(next_app, maker, sql.session_key)
