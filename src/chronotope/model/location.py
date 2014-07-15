from sqlalchemy import (
    Column,
    Float,
    String,
    DateTime,
)
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


_ = TranslationStringFactory('chronotope')


class LocationRecord(Base):
    __tablename__ = 'location'
    __index_attrs__ = ['street', 'zip', 'city']

    uid = Column(GUID, primary_key=True)
    creator = Column(String)
    created = Column(DateTime)
    modified = Column(DateTime)
    state = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    street = Column(String)
    zip = Column(String)
    city = Column(String)
    country = Column(String)


@node_info(
    name='location',
    title=_('location_label', default='Location'),
    description=_('location_description', default='A location'),
    icon='glyphicon glyphicon-map-marker')
class Location(SQLRowNode):
    record_factory = LocationRecord

    @instance_property
    def properties(self):
        props = super(Location, self).properties
        props.action_up = True
        props.action_up_tile = 'listing'
        props.action_view = True
        props.action_edit = True
        props.action_delete = True
        return props

    @instance_property
    def metadata(self):
        md = Metadata()
        md.title = u'{0} {1} {2}'.format(self.attrs['street'],
                                         self.attrs['zip'],
                                         self.attrs['city'])
        md.creator = self.attrs['creator']
        md.created = self.attrs['created']
        md.modified = self.attrs['modified']
        return md


@node_info(
    name='locations',
    title=_('locations_label', default='Locations'),
    description=_('locations_description',
                  default='Container for Locations'),
    icon='glyphicon glyphicon-globe',
    addables=['location'])
class Locations(SQLTableNode):
    record_class = LocationRecord
    child_factory = Location

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
        md.title = _('locations_label', default='Locations')
        md.description = \
            _('locations_description', default='Container for Locations')
        return md
