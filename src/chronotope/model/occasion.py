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
    GUID,
    SQLBase,
    SQLTableNode,
    SQLRowNode,
)
from chronotope.model import FacilityRecord
from chronotope.utils import html_index_transform


_ = TranslationStringFactory('chronotope')


occasion_facility_references = Table(
        'occasion_facility_references', SQLBase.metadata,
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
    creator = Column(String)
    created = Column(DateTime)
    modified = Column(DateTime)
    state = Column(String)
    title = Column(String)
    description = Column(String)
    duration_from = Column(DateTime)
    duration_to = Column(DateTime)

    facility = relationship(
        FacilityRecord,
        secondary=occasion_facility_references,
        backref='occasion')


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
        md.description = \
            _('occasions_description', default='Container for Occasions')
        return md
