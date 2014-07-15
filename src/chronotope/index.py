import os
from whoosh.fields import (
    SchemaClass,
    TEXT,
    ID,
)
from whoosh.index import (
    create_in,
    open_dir,
)


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
