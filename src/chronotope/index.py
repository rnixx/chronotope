from whoosh.fields import ID
from whoosh.fields import SchemaClass
from whoosh.fields import TEXT
from whoosh.index import create_in
from whoosh.index import open_dir
import os


class ChronotopeSchema(SchemaClass):
    value = TEXT
    uid = ID(stored=True, unique=True)
    cls = ID(stored=True)


def get_index():
    index_dir = os.environ['chronotope.index.dir']
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        index = create_in(index_dir, ChronotopeSchema)
    else:
        index = open_dir(index_dir)
    return index
