import uuid
import pickle
from plumber import plumbing
from node.behaviors import NodeAttributes
from sqlalchemy import inspect
from sqlalchemy import event
from sqlalchemy import engine_from_config
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
)
from sqlalchemy.types import (
    TypeDecorator,
    CHAR,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from pyramid.threadlocal import get_current_request
from pyramid.i18n import TranslationStringFactory
from cone.app.model import BaseNode
from cone.app.workflow import (
    WorkflowState,
    WorkflowACL,
)
from chronotope.publication import publication_state_acls
from chronotope.index import get_index


_ = TranslationStringFactory('chronotope')


###############################################################################
# sql model basics
###############################################################################

class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    http://docs.sqlalchemy.org/en/rel_0_8/core/types.html#backend-agnostic-guid-type
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value)
            else:
                # hexstring
                return "%.32x" % value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


class IndexingBase(object):
    __index_attrs__ = list()
    __index_transforms__ = dict()

    def index(self, writer):
        def transform_value(name):
            value = getattr(self, name)
            transform = self.__index_transforms__.get(name)
            if transform:
                value = transform(self, value)
            return value
        values = list()
        for attr in self.__index_attrs__:
            values.append(transform_value(attr))
        uid = u'{0}'.format(self.uid)
        cls = u'{0}'.format(pickle.dumps(self.__class__))
        value = u' '.join(values)
        writer.add_document(uid=uid, cls=cls, value=value)

    def reindex(self, writer):
        uid = u'{0}'.format(self.uid)
        writer.delete_by_term('uid', uid)
        self.index(writer)

    def deindex(self, writer):
        uid = u'{0}'.format(self.uid)
        writer.delete_by_term('uid', uid)


def update_indexes(session, flush_context):
    writer = get_index().writer()
    for i in session.new:
        i.index(writer)
    for i in session.dirty:
        i.reindex(writer)
    for i in session.deleted:
        i.deindex(writer)
    writer.commit()


def bind_session_listeners(session):
    event.listen(session, 'after_flush', update_indexes)


###############################################################################
# application node basics
###############################################################################

class SQLTableNode(BaseNode):
    record_class = None
    child_factory = None

    def __setitem__(self, name, value):
        uid = uuid.UUID(name)
        attrs = value.attrs
        if not attrs['uid']:
            attrs['uid'] = uid
        if uid != attrs['uid']:
            raise ValueError('Node name must equal Node uid.')
        if value.name is None:
            value.__name__ = name
        session = get_session(get_current_request())
        session.add(value.record)

    def __getitem__(self, name):
        # if name no UUID, raise KeyError
        try:
            uuid.UUID(name)
        except ValueError:
            raise KeyError(name)
        session = get_session(get_current_request())
        query = session.query(self.record_class)
        # always expect uid attribute as primary key
        record = query.filter(self.record_class.uid == name).first()
        if record is None:
            # traversal expects KeyError before looking up views.
            raise KeyError(name)
        return self.child_factory(name, self, record)

    def __delitem__(self, name):
        child = self[name]
        session = get_session(get_current_request())
        session.delete(child.record)

    def __iter__(self):
        session = get_session(get_current_request())
        for recid in session.query(self.record_class.uid).all():
            yield str(recid[0])

    def __call__(self):
        session = get_session(get_current_request())
        session.commit()


class SQLRowNodeAttributes(NodeAttributes):

    def __init__(self, name, parent, record):
        NodeAttributes.__init__(self, name, parent)
        self.record = record

    @property
    def _columns(self):
        return inspect(self.record.__class__).attrs.keys()

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
        return iter(self._columns)

    def __contains__(self, name):
        return name in self._columns


@plumbing(WorkflowState, WorkflowACL)
class SQLRowNode(BaseNode):
    workflow_name = 'publication'
    state_acls = publication_state_acls
    record_factory = None

    @property
    def workflow_tsf(self):
        return _

    def __init__(self, name=None, parent=None, record=None):
        self.__name__ = name
        self.__parent__ = parent
        self._new = False
        if record is None:
            self._new = True
            record = self.record_factory()
        self.record = record

    def attributes_factory(self, name, parent):
        return SQLRowNodeAttributes(name, parent, self.record)

    def __call__(self):
        session = get_session(get_current_request())
        if self._new:
            session.add(self.record)
            self._new = False
        session.commit()


###############################################################################
# initialization and WSGI
###############################################################################

SQLBase = declarative_base(cls=IndexingBase)
DBSession = scoped_session(sessionmaker())
metadata = SQLBase.metadata


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    metadata.bind = engine
    metadata.create_all(engine)


session_key = 'cone.sql.session'


def get_session(request):
    return request.environ[session_key]


class WSGISQLSession(object):
    """WSGI framework component that opens and closes a SQL session.

    Downstream applications will have the session in the environment,
    normally under the key 'cone.sql.session'.
    """

    def __init__(self, next_app, maker, session_key=session_key):
        self.next_app = next_app
        self.maker = maker
        self.session_key = session_key

    def __call__(self, environ, start_response):
        session = self.maker()
        bind_session_listeners(session)
        environ[self.session_key] = session
        try:
            result = self.next_app(environ, start_response)
            return result
        finally:
            pass


def make_app(next_app, global_conf, **local_conf):
    """Make a Session app.
    """
    from chronotope import sql
    engine = engine_from_config(local_conf, prefix='sqlalchemy.')
    sql.SQLBase.metadata.create_all(engine)
    maker = sessionmaker(bind=engine)
    sql.session_key = local_conf.get('session_key', sql.session_key)
    return WSGISQLSession(next_app, maker, sql.session_key)
