# -*- coding: utf-8 -*-
from chronotope.sql import GUID
from chronotope.sql import SQLBase
from chronotope.sql import SQLRowNode
from chronotope.sql import SQLTableNode
from chronotope.sql import get_session
from chronotope.utils import ensure_uuid
from cone.app.model import Metadata
from cone.app.model import Properties
from cone.app.model import node_info
from node.utils import instance_property
from pyramid.i18n import TranslationStringFactory
from pyramid.i18n import get_localizer
from pyramid.threadlocal import get_current_request
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import or_


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


def search_locations(request, term, state=[], submitter=None, limit=None):
    session = get_session(request)
    query = session.query(LocationRecord)
    query = query.filter(or_(LocationRecord.street.like(u'%{0}%'.format(term)),
                             LocationRecord.zip.like(u'%{0}%'.format(term)),
                             LocationRecord.city.like(u'%{0}%'.format(term)),
                             LocationRecord.lat.like(u'%{0}%'.format(term)),
                             LocationRecord.lon.like(u'%{0}%'.format(term))))
    if state:
        query = query.filter(LocationRecord.state.in_(state))
    if submitter:
        query = query.filter(LocationRecord.submitter == submitter)
    query = query.order_by(LocationRecord.city)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


def locations_in_bounds(request, north, south, west, east,
                        state=[], submitter=None, limit=None):
    session = get_session(request)
    query = session.query(LocationRecord)\
                   .filter(LocationRecord.lon.between(west, east))\
                   .filter(LocationRecord.lat.between(south, north))
    if state:
        query = query.filter(LocationRecord.state.in_(state))
    if submitter:
        query = query.filter(LocationRecord.submitter == submitter)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


north = _('north', default='N')
south = _('south', default='S')
west = _('west', default='W')
east = _('east', default='E')


def location_title(request, street, zip_, city, lat, lon):
    if not street and not zip_ and not city:
        localizer = get_localizer(request)
        lon_dir = localizer.translate(lon >= 0 and east or west)
        lat_dir = localizer.translate(lat >= 0 and north or south)
        return u'{0}° {1} / {2}° {3}'.format(
            abs(lat), lat_dir, abs(lon), lon_dir
        )
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

    @property
    def metadata(self):
        md = Metadata()
        md.title = location_title(
            get_current_request(),
            self.attrs['street'],
            self.attrs['zip'],
            self.attrs['city'],
            self.attrs['lat'],
            self.attrs['lon'])
        md.creator = self.attrs['creator']
        md.created = self.attrs['created']
        md.modified = self.attrs['modified']
        return md


@node_info(
    name='locations',
    title=_('locations_label', default='Locations'),
    description=_(
        'locations_description',
        default='Container for Locations'
    ),
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
        md.description = _(
            'locations_description',
            default='Container for Locations'
        )
        return md
