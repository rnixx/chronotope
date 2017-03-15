from chronotope.index import get_index
from chronotope.publication import publication_state_acls
from cone.app.workflow import WorkflowACL
from cone.app.workflow import WorkflowState
from cone.sql import metadata
from cone.sql import sql_session_setup
from plumber import finalize
from pyramid.i18n import TranslationStringFactory
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
import pickle


_ = TranslationStringFactory('chronotope')


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


@sql_session_setup
def bind_session_listeners(session):
    event.listen(session, 'after_flush', update_indexes)


SQLBase = declarative_base(
    cls=IndexingBase,
    metadata=metadata
)


class PublicationWorkflowBehavior(WorkflowState, WorkflowACL):
    workflow_name = finalize('publication')
    state_acls = finalize(publication_state_acls)

    @finalize
    @property
    def workflow_tsf(self):
        return _
