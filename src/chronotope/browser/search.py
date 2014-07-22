from zope.interface import implementer
from zope.component import adapter
from pyramid.security import authenticated_userid
from cone.app.interfaces import (
    IApplicationNode,
    ILiveSearch,
)
from cone.app.browser.utils import (
    make_url,
    make_query,
)
from chronotope.model import (
    LocationRecord,
    FacilityRecord,
    OccasionRecord,
    AttachmentRecord,
)
from chronotope.search import fulltext_search
from chronotope.utils import (
    UX_IDENT,
    UX_FRONTEND,
)


###############################################################################
# livesearch
###############################################################################

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
        authenticated = bool(authenticated_userid(request))
        result = list()
        for record in fulltext_search(request, query):
            if not authenticated and record.state in ['draft', 'declined']:
                continue
            cls = record.__class__
            uid = str(record.uid)
            value_action = value_actions[cls]
            query = make_query(**{UX_IDENT: UX_FRONTEND})
            target = make_url(request,
                              path=[value_containers[cls], uid],
                              query=query)
            suggestion = {
                'uid': uid,
                'value': value_extractors[cls](record),
                'action': value_action,
                'target': target,
                'icon': value_icons[cls],
            }
            if value_action == 'location':
                suggestion['lat'] = record.lat
                suggestion['lon'] = record.lon
            result.append(suggestion)
        return result
