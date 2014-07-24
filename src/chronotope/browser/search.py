import uuid
from zope.interface import implementer
from zope.component import adapter
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from cone.app.interfaces import (
    IApplicationNode,
    ILiveSearch,
)
from cone.app.browser.utils import (
    make_url,
    make_query,
)
from chronotope.sql import get_session
from chronotope.model import (
    LocationRecord,
    FacilityRecord,
    OccasionRecord,
    AttachmentRecord,
)
from chronotope.model.location import locations_in_bounds
from chronotope.search import fulltext_search
from chronotope.utils import (
    UX_IDENT,
    UX_FRONTEND,
)


SEARCH_LIMIT = 50


def location_value(record):
    return u'{0}, {1} {2}'.format(record.street, record.zip, record.city)


def facility_value(record):
    return record.title


def occasion_value(record):
    return record.title


def attachment_value(record):
    return record.title


value_extractors = {
    LocationRecord: location_value,
    FacilityRecord: facility_value,
    OccasionRecord: occasion_value,
    AttachmentRecord: attachment_value,
}
value_actions = {
    LocationRecord: 'location',
    FacilityRecord: 'facility',
    OccasionRecord: 'occasion',
    AttachmentRecord: 'attachment',
}
value_containers = {
    LocationRecord: 'locations',
    FacilityRecord: 'facilities',
    OccasionRecord: 'occasions',
    AttachmentRecord: 'attachments',
}
value_icons = {
    LocationRecord: 'glyphicon glyphicon-map-marker',
    FacilityRecord: 'glyphicon glyphicon-home',
    OccasionRecord: 'glyphicon glyphicon-star-empty',
    AttachmentRecord: 'glyphicon glyphicon-file',
}


@implementer(ILiveSearch)
@adapter(IApplicationNode)
class LiveSearch(object):

    def __init__(self, model):
        self.model = model

    def search(self, request, query):
        result = list()
        state = not authenticated_userid(request) and ['published'] or []
        for record in fulltext_search(request, query, state=state,
                                      limit=SEARCH_LIMIT):
            cls = record.__class__
            uid = str(record.uid)
            query = make_query(**{UX_IDENT: UX_FRONTEND})
            target = make_url(request,
                              path=[value_containers[cls], uid],
                              query=query)
            suggestion = {
                'uid': uid,
                'value': value_extractors[cls](record),
                'action': value_actions[cls],
                'target': target,
                'icon': value_icons[cls],
            }
            result.append(suggestion)
        return result


def extract_locations(request, record, result):
    cls = record.__class__
    if cls is LocationRecord:
        authenticated = bool(authenticated_userid(request))
        if not authenticated and record.state != 'published':
            return
        uid = str(record.uid)
        query = make_query(**{UX_IDENT: UX_FRONTEND})
        target = make_url(
            request,
            path=[value_containers[cls], uid],
            query=query,
        )
        result[uid] = {
            'value': value_extractors[cls](record),
            'action': value_actions[cls],
            'target': target,
            'lat': record.lat,
            'lon': record.lon,
        }
    elif cls is FacilityRecord:
        for location in record.location:
            extract_locations(request, location, result)
    elif cls is OccasionRecord:
        for location in record.location:
            extract_locations(request, location, result)
        for facility in record.facility:
            extract_locations(request, facility, result)
    elif cls is AttachmentRecord:
        for location in record.location:
            extract_locations(request, location, result)
        for facility in record.facility:
            extract_locations(request, facility, result)
        for occasion in record.occasion:
            extract_locations(request, occasion, result)


@view_config(name='chronotope.related_locations',
             accept='application/json',
             renderer='json')
def json_related_locations(model, request):
    uid = uuid.UUID(request.params['uid'])
    actions = dict([(v, k) for k, v in value_actions.items()])
    cls = actions[request.params['action']]
    record = get_session(request).query(cls).get(uid)
    if not record:
        return list()
    result = dict()
    extract_locations(request, record, result)
    return result.values()


@view_config(name='chronotope.search_locations',
             accept='application/json',
             renderer='json')
def json_search_locations(model, request):
    query = request.params['term']
    result = dict()
    state = not authenticated_userid(request) and ['published'] or []
    for record in fulltext_search(request, query, state=state,
                                  limit=SEARCH_LIMIT):
        extract_locations(request, record, result)
    return result.values()


@view_config(name='chronotope.locations_in_bounds',
             accept='application/json',
             renderer='json')
def json_locations_in_bounds(model, request):
    state = not authenticated_userid(request) and ['published'] or []
    records = locations_in_bounds(
        request,
        request.params['n'],
        request.params['s'],
        request.params['w'],
        request.params['e'],
        state=state
    )
    result = list()
    for record in records:
        uid = str(record.uid)
        query = make_query(**{UX_IDENT: UX_FRONTEND})
        target = make_url(
            request,
            path=[value_containers[LocationRecord], uid],
            query=query,
        )
        result.append({
            'value': value_extractors[LocationRecord](record),
            'action': value_actions[LocationRecord],
            'target': target,
            'lat': record.lat,
            'lon': record.lon,
        })
    return result
