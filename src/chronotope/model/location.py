from sqlalchemy import (
    Column,
    Float,
    String,
    DateTime,
    or_,
)
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
    get_session,
)
from chronotope.utils import ensure_uuid


_ = TranslationStringFactory('chronotope')


class LocationRecord(SQLBase):
    __tablename__ = 'location'
    __index_attrs__ = ['street', 'zip', 'city']

    uid = Column(GUID, primary_key=True)
    submitter = Column(String)
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


def location_by_uid(request, uid):
    session = get_session(request)
    return session.query(LocationRecord).get(ensure_uuid(uid))


def locations_by_uid(request, uids):
    if not uids:
        return list()
    uids = [ensure_uuid(uid) for uid in uids]
    session = get_session(request)
    return session.query(LocationRecord)\
                  .filter(LocationRecord.uid.in_(uids))\
                  .all()


def search_locations(request, term, limit=None):
    session = get_session(request)
    query = session.query(LocationRecord)
    query = query.filter(or_(LocationRecord.street.like('%{0}%'.format(term)),
                             LocationRecord.zip.like('%{0}%'.format(term)),
                             LocationRecord.city.like('%{0}%'.format(term))))
    query = query.order_by(LocationRecord.city)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


def locations_in_bounds(request, north, south, west, east, limit=None):
    session = get_session(request)
    query = session.query(LocationRecord)\
                   .filter(LocationRecord.lon.between(west, east))\
                   .filter(LocationRecord.lat.between(south, north))
    if limit is not None:
        query = query.limit(limit)
    return query.all()


def location_title(street, zip_, city):
    return u'{0} {1} {2}'.format(street, zip_, city)


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
        md.title = location_title(
            self.attrs['street'], self.attrs['zip'], self.attrs['city'])
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
