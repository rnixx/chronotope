from chronotope.model.facility import FacilityRecord
from chronotope.model.location import LocationRecord
from chronotope.sql import GUID
from chronotope.sql import SQLBase
from chronotope.sql import SQLRowNode
from chronotope.sql import SQLTableNode
from chronotope.sql import get_session
from chronotope.utils import ensure_uuid
from chronotope.utils import html_index_transform
from cone.app.model import Metadata
from cone.app.model import Properties
from cone.app.model import node_info
from node.utils import instance_property
from pyramid.i18n import TranslationStringFactory
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship


_ = TranslationStringFactory('chronotope')


occasion_location_references = Table(
    'occasion_location_references',
    SQLBase.metadata,
    Column('occasion_uid', GUID, ForeignKey('occasion.uid')),
    Column('location_uid', GUID, ForeignKey('location.uid'))
)
occasion_facility_references = Table(
    'occasion_facility_references',
    SQLBase.metadata,
    Column('occasion_uid', GUID, ForeignKey('occasion.uid')),
    Column('facility_uid', GUID, ForeignKey('facility.uid'))
)


class OccasionRecord(SQLBase):
    __tablename__ = 'occasion'
    __index_attrs__ = ['title', 'description']
    __index_transforms__ = {
        'description': html_index_transform,
    }

    uid = Column(GUID, primary_key=True)
    submitter = Column(String)
    creator = Column(String)
    created = Column(DateTime)
    modified = Column(DateTime)
    state = Column(String)
    title = Column(String)
    description = Column(String)
    duration_from = Column(DateTime)
    duration_to = Column(DateTime)

    location = relationship(
        LocationRecord,
        secondary=occasion_location_references,
        backref='occasion')
    facility = relationship(
        FacilityRecord,
        secondary=occasion_facility_references,
        backref='occasion')


def occasion_by_uid(request, uid):
    session = get_session(request)
    return session.query(OccasionRecord).get(ensure_uuid(uid))


def occasions_by_uid(request, uids):
    if not uids:
        return list()
    uids = [ensure_uuid(uid) for uid in uids]
    session = get_session(request)
    return session.query(OccasionRecord)\
                  .filter(OccasionRecord.uid.in_(uids))\
                  .all()


def search_occasions(request, term, state=[], submitter=None, limit=None):
    session = get_session(request)
    query = session.query(OccasionRecord)
    query = query.filter(OccasionRecord.title.like(u'%{0}%'.format(term)))
    if state:
        query = query.filter(OccasionRecord.state.in_(state))
    if submitter:
        query = query.filter(OccasionRecord.submitter == submitter)
    query = query.order_by(OccasionRecord.title)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


@node_info(
    name='occasion',
    title=_('occasion_label', default='Occasion'),
    description=_('occasion_description', default='An Occasion'),
    icon='glyphicon glyphicon-star-empty')
class Occasion(SQLRowNode):
    record_factory = OccasionRecord

    @instance_property
    def properties(self):
        props = super(Occasion, self).properties
        props.action_up = True
        props.action_up_tile = 'listing'
        props.action_view = True
        props.action_edit = True
        props.action_delete = True
        return props

    @property
    def metadata(self):
        md = Metadata()
        md.title = self.attrs['title']
        md.description = self.attrs['description']
        md.creator = self.attrs['creator']
        md.created = self.attrs['created']
        md.modified = self.attrs['modified']
        return md


@node_info(
    name='occasions',
    title=_('occasions_label', default='Occasions'),
    description=_('occasions_description', default='Container for Occasions'),
    icon='glyphicon glyphicon-calendar',
    addables=['occasion'])
class Occasions(SQLTableNode):
    record_class = OccasionRecord
    child_factory = Occasion

    @instance_property
    def properties(self):
        props = Properties()
        props.in_navtree = True
        props.action_up = True
        props.action_up_tile = 'content'
        props.action_add = True
        props.default_content_tile = 'listing'
        return props

    @instance_property
    def metadata(self):
        md = Metadata()
        md.title = _('occasions_label', default='Occasions')
        md.description = _(
            'occasions_description',
            default='Container for Occasions'
        )
        return md
