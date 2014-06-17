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
    SQLRowNodeAttributes,
    SQLRowNode,
)
from chronotope.model import LocationRecord


_ = TranslationStringFactory('chronotope')


facility_location_references = Table(
        'facility_location_references', Base.metadata,
    Column('facility_id', Integer, ForeignKey('facility.id')),
    Column('location_id', Integer, ForeignKey('location.id'))
)


class FacilityRecord(Base):
    __tablename__ = 'facility'
    id = Column(Integer, primary_key=True)
    uid = Column(String)
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
    _keys = ['id', 'uid', 'creator', 'created', 'modified',
             'title', 'description', 'exists_from', 'exists_to',
             'category', 'location']


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


class Facilities(BaseNode):
    node_info_name = 'facilities'

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

    def __getitem__(self, name):
        # traversal expects KeyError before looking up views.
        raise KeyError(name)

    def __setitem__(self, name, value):
        raise NotImplementedError(u'``__setitem__`` is not implemented.')

    def __delitem__(self, name):
        pass


info = NodeInfo()
info.title = _('facilities_label', default='Facilities')
info.description = \
    _('facilities_description', default='Container for Facilities')
info.node = Facilities
info.addables = ['facility']
info.icon = 'icon-folder-open'
registerNodeInfo('facilities', info)
