from sqlalchemy import (
    Table,
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from node.utils import instance_property
from pyramid.i18n import TranslationStringFactory
from cone.app.model import (
    BaseNode,
    Properties,
    Metadata,
    NodeInfo,
    registerNodeInfo,
)
from chronotope.sql import (
    Base,
    GUID,
    SQLTableNode,
    SQLRowNodeAttributes,
    SQLRowNode,
)
from chronotope.model import LocationRecord


_ = TranslationStringFactory('chronotope')


facility_location_references = Table(
        'facility_location_references', Base.metadata,
    Column('facility_uid', GUID, ForeignKey('facility.uid')),
    Column('location_uid', GUID, ForeignKey('location.uid'))
)


class FacilityRecord(Base):
    __tablename__ = 'facility'
    uid = Column(GUID, primary_key=True)
    creator = Column(String)
    created = Column(DateTime)
    modified = Column(DateTime)
    title = Column(String)
    description = Column(String)
    exists_from = Column(DateTime)
    exists_to = Column(DateTime)
    #category = Column()
    location = relationship(
        LocationRecord,
        secondary=facility_location_references,
        backref='facility')


class FacilityAttributes(SQLRowNodeAttributes):
    columns = [
        'uid', 'creator', 'created', 'modified', 'title', 'description',
        'exists_from', 'exists_to', 'category', 'location',
    ]


class Facility(SQLRowNode):
    node_info_name = 'facility'

    def record_factory(self):
        return FacilityRecord()

    def attributes_factory(self, name, parent):
        return FacilityAttributes(name, parent, self.record)

    @instance_property
    def properties(self):
        props = Properties()
        props.action_up = True
        props.action_view = True
        props.action_delete = True
        return props

    @instance_property
    def metadata(self):
        md = Metadata()
        md.title = _('facility_label', default='Facility')
        md.description = _('facility_description', default='A Facility')
        return md


info = NodeInfo()
info.title = _('facility_label', default='Facility')
info.description = _('facility_description', default='A Facility')
info.node = Facility
info.addables = []
info.icon = 'icon-home'
registerNodeInfo('facility', info)


class Facilities(SQLTableNode):
    node_info_name = 'facilities'
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


info = NodeInfo()
info.title = _('facilities_label', default='Facilities')
info.description = \
    _('facilities_description', default='Container for Facilities')
info.node = Facilities
info.addables = ['facility']
info.icon = 'icon-folder-open'
registerNodeInfo('facilities', info)
