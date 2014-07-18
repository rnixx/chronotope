from pyramid.view import view_config
from cone.tile import Tile
from chronotope.model.category import search_categories


CATEGORY_LIMIT = 100


@view_config(name='chronotope.category',
             accept='application/json',
             renderer='json')
def json_category(model, request):
    term = request.params['q']
    categories = list()
    for category in search_categories(request, term, limit=CATEGORY_LIMIT):
        categories.append({
            'id': str(category.uid),
            'text': category.name,
        })
    if not categories:
        term = term.replace(',', ' ')
        categories.append({
            'id': term,
            'text': term,
        })
    return categories


class CategoriesTile(Tile):

    @property
    def categories(self):
        categories = self.model.attrs['category']
        return [it.name for it in categories]
