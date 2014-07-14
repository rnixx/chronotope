from sqlalchemy import (
    Table,
    Column,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from node.utils import instance_property
from pyramid.i18n import TranslationStringFactory
from cone.app.model import (
    Properties,
    Metadata,
    node_info,
)
from chronotope.sql import (
    Base,
    GUID,
    SQLTableNode,
    SQLRowNode,
)
from chronotope.model import (
    LocationRecord,
    CategoryRecord,
)


_ = TranslationStringFactory('chronotope')


facility_location_references = Table(
        'facility_location_references', Base.metadata,
    Column('facility_uid', GUID, ForeignKey('facility.uid')),
    Column('location_uid', GUID, ForeignKey('location.uid'))
)


facility_category_references = Table(
        'facility_category_references', Base.metadata,
    Column('facility_uid', GUID, ForeignKey('facility.uid')),
    Column('category_uid', GUID, ForeignKey('category.uid'))
)


class FacilityRecord(Base):
    __tablename__ = 'facility'
    uid = Column(GUID, primary_key=True)
    creator = Column(String)
    created = Column(DateTime)
    modified = Column(DateTime)
    state = Column(String)
    title = Column(String)
    description = Column(String)
    exists_from = Column(DateTime)
    exists_to = Column(DateTime)
    category = relationship(
        CategoryRecord,
        secondary=facility_category_references,
        backref='facility')
    location = relationship(
        LocationRecord,
        secondary=facility_location_references,
        backref='facility')


@node_info(
    name='facility',
    title=_('facility_label', default='Facility'),
    description=_('facility_description', default='A Facility'),
    icon='glyphicon glyphicon-home')
class Facility(SQLRowNode):
    record_factory = FacilityRecord

    @instance_property
    def properties(self):
        props = super(Facility, self).properties
        props.action_up = True
        props.action_up_tile = 'listing'
        props.action_view = True
        props.action_edit = True
        props.action_delete = True
        return props

    @instance_property
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
    description=_('facilities_description',
                  default='Container for Facilities'),
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
        md.description = \
            _('facilities_description', default='Container for Facilities')
        return md
