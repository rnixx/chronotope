from chronotope.model.base import PublicationWorkflowBehavior
from chronotope.model.base import SQLBase
from chronotope.model.category import CategoryRecord
from chronotope.model.location import LocationRecord
from chronotope.utils import ensure_uuid
from chronotope.utils import html_index_transform
from cone.app.model import Metadata
from cone.app.model import Properties
from cone.app.model import node_info
from cone.sql import get_session
from cone.sql import metadata
from cone.sql.model import GUID
from cone.sql.model import SQLRowNode
from cone.sql.model import SQLTableNode
from node.utils import instance_property
from plumber import plumbing
from pyramid.i18n import TranslationStringFactory
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship


_ = TranslationStringFactory('chronotope')


facility_location_references = Table(
    'facility_location_references',
    metadata,
    Column('facility_uid', GUID, ForeignKey('facility.uid')),
    Column('location_uid', GUID, ForeignKey('location.uid'))
)
facility_category_references = Table(
    'facility_category_references',
    metadata,
    Column('facility_uid', GUID, ForeignKey('facility.uid')),
    Column('category_uid', GUID, ForeignKey('category.uid'))
)


class FacilityRecord(SQLBase):
    __tablename__ = 'facility'
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
    exists_from = Column(String)
    exists_to = Column(String)

    category = relationship(
        CategoryRecord,
        secondary=facility_category_references,
        backref='facility')
    location = relationship(
        LocationRecord,
        secondary=facility_location_references,
        backref='facility')


def facility_by_uid(request, uid):
    session = get_session(request)
    return session.query(FacilityRecord).get(ensure_uuid(uid))


def facilities_by_uid(request, uids):
    if not uids:
        return list()
    uids = [ensure_uuid(uid) for uid in uids]
    session = get_session(request)
    return session.query(FacilityRecord)\
                  .filter(FacilityRecord.uid.in_(uids))\
                  .all()


def search_facilities(request, term, state=[], submitter=None, limit=None):
    session = get_session(request)
    query = session.query(FacilityRecord)
    query = query.filter(FacilityRecord.title.like(u'%{0}%'.format(term)))
    if state:
        query = query.filter(FacilityRecord.state.in_(state))
    if submitter:
        query = query.filter(FacilityRecord.submitter == submitter)
    query = query.order_by(FacilityRecord.title)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


@node_info(
    name='facility',
    title=_('facility_label', default='Facility'),
    description=_('facility_description', default='A Facility'),
    icon='glyphicon glyphicon-home')
@plumbing(PublicationWorkflowBehavior)
class Facility(SQLRowNode):
    record_class = FacilityRecord

    @instance_property
    def properties(self):
        props = super(Facility, self).properties
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
    name='facilities',
    title=_('facilities_label', default='Facilities'),
    description=_(
        'facilities_description',
        default='Container for Facilities'
    ),
    icon='glyphicon glyphicon-record',
    addables=['facility'])
class Facilities(SQLTableNode):
    record_class = FacilityRecord
    child_factory = Facility

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
        md.title = _('facilities_label', default='Facilities')
        md.description = _(
            'facilities_description',
            default='Container for Facilities'
        )
        return md
