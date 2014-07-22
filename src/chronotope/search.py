import pickle
from zope.interface import implementer
from zope.component import adapter
from whoosh.qparser import QueryParser
from pyramid.security import authenticated_userid
from cone.app.interfaces import (
    IApplicationNode,
    ILiveSearch,
)
from chronotope.sql import get_session
from chronotope.index import get_index
from chronotope.model import (
    LocationRecord,
    FacilityRecord,
    OccasionRecord,
    AttachmentRecord,
)


def results_to_instances(request, results):
    instances = []
    for r in results:
        cls = pickle.loads('{0}'.format(r.get('cls')))
        uid = r.get('uid')
        instance = get_session(request).query(cls).get(uid)
        instances.append(instance)
    return instances


def search(request, query):
    index = get_index()
    parser = QueryParser('value', index.schema)
    with index.searcher() as searcher:
        query = parser.parse(query)
        results = results_to_instances(request, searcher.search(query))
    return results


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


value_types = {
    LocationRecord: 'location',
    FacilityRecord: 'facility',
    OccasionRecord: 'occasion',
    AttachmentRecord: 'attachment',
}
value_extractors = {
    LocationRecord: location_value,
    FacilityRecord: facility_value,
    OccasionRecord: occasion_value,
    AttachmentRecord: attachment_value,
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
        for record in search(request, query):
            if not authenticated and record.state in ['draft', 'declined']:
                continue
            cls = record.__class__
            result.append({
                'uid': str(record.uid),
                'value': value_extractors[cls](record),
                'type': value_types[cls],
                'icon': value_icons[cls],
            })
        return result
