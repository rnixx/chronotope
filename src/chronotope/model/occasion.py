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
from chronotope.model import FacilityRecord


_ = TranslationStringFactory('chronotope')


occasion_facility_references = Table(
        'occasion_facility_references', Base.metadata,
    Column('occasion_uid', GUID, ForeignKey('occasion.uid')),
    Column('facility_uid', GUID, ForeignKey('facility.uid'))
)


class OccasionRecord(Base):
    __tablename__ = 'occasion'
    uid = Column(GUID, primary_key=True)
    creator = Column(String)
    created = Column(DateTime)
    modified = Column(DateTime)
    title = Column(String)
    description = Column(String)
    duration_from = Column(DateTime)
    duration_to = Column(DateTime)
    facility = relationship(
        FacilityRecord,
        secondary=occasion_facility_references,
        backref='occasion')


class OccasionAttributes(SQLRowNodeAttributes):
    _keys = ['uid', 'creator', 'created', 'modified',
             'title', 'description', 'duration_from', 'duration_to',
             'facility']


class Occasion(SQLRowNode):
    node_info_name = 'occasion'

    def record_factory(self):
        return OccasionRecord()

    def attributes_factory(self, name, parent):
        return OccasionAttributes(name, parent, self.record)

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
        md.title = _('occasion_label', default='Occasion')
        md.description = _('occasion_description', default='An Occasion')
        return md


info = NodeInfo()
info.title = _('occasion_label', default='Occasion')
info.description = _('occasion_description', default='An Occasion')
info.node = Occasion
info.addables = []
info.icon = 'icon-calendar'
registerNodeInfo('occasion', info)


class Occasions(SQLTableNode):
    node_info_name = 'occasions'
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
        md.description = \
            _('occasions_description', default='Container for Occasions')
        return md


info = NodeInfo()
info.title = _('occasions_label', default='Occasions')
info.description = \
    _('occasions_description', default='Container for Occasions')
info.node = Occasions
info.addables = ['occasion']
info.icon = 'icon-folder-open'
registerNodeInfo('occasions', info)
