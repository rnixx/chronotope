import pickle
from whoosh.qparser import QueryParser
from chronotope.sql import get_session
from chronotope.index import get_index


def results_to_instances(request, results):
    instances = []
    for r in results:
        cls = pickle.loads('{0}'.format(r.get('cls')))
        uid = r.get('uid')
        instance = get_session(request).query(cls).get(uid)
        instances.append(instance)
    return instances


def fulltext_search(request, query):
    index = get_index()
    parser = QueryParser('value', index.schema)
    with index.searcher() as searcher:
        query = parser.parse(query)
        results = results_to_instances(request, searcher.search(query))
    return results
