from chronotope.index import get_index
from chronotope.utils import get_submitter
from cone.sql import get_session
from pyramid.security import authenticated_userid
from whoosh.qparser import QueryParser
import pickle


def results_to_instances(request, results):
    instances = []
    for r in results:
        cls = pickle.loads('{0}'.format(r.get('cls')))
        uid = r.get('uid')
        instance = get_session(request).query(cls).get(uid)
        instances.append(instance)
    return instances


def fulltext_search(request, query, limit):
    # query index
    index = get_index()
    parser = QueryParser('value', index.schema)
    with index.searcher() as searcher:
        query = parser.parse(query)
        results = searcher.search(query, limit=limit)
        results = results_to_instances(request, results)

    # helper for limit
    def limited(res):
        if limit is not None:
            return res[:limit]
        return res

    # if authenticated, return all draft and published results
    authenticated = bool(authenticated_userid(request))
    if authenticated:
        return limited(
            [res for res in results if res.state in ['draft', 'published']])
    # check for submitter
    submitter = get_submitter(request)
    if submitter:
        return limited(
            [res for res in results if res.state == 'published' \
                or (res.state == 'draft' and submitter == res.submitter)])
    # return only public results
    return limited([res for res in results if res.state == 'published'])
