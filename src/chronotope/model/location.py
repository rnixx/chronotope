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


_ = TranslationStringFactory('chronotope')


class LocationRecord(Base):
    __tablename__ = 'location'
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


class LocationAttributes(SQLRowNodeAttributes):
    columns = [
        'uid', 'creator', 'created', 'modified', 'state',
        'lat', 'lon', 'street', 'zip', 'city', 'country',
    ]


class Location(SQLRowNode):
    node_info_name = 'location'

    def record_factory(self):
        return LocationRecord()

    def attributes_factory(self, name, parent):
        return LocationAttributes(name, parent, self.record)

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


info = NodeInfo()
info.title = _('location_label', default='Location')
info.description = _('location_description', default='A location')
info.node = Location
info.addables = []
info.icon = 'glyphicon glyphicon-map-marker'
registerNodeInfo('location', info)


class Locations(SQLTableNode):
    node_info_name = 'locations'
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


info = NodeInfo()
info.title = _('locations_label', default='Locations')
info.description = \
    _('locations_description', default='Container for Locations')
info.node = Locations
info.addables = ['location']
info.icon = 'glyphicon glyphicon-globe'
registerNodeInfo('locations', info)
