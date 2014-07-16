from plumber import (
    plumb,
    default,
    Behavior,
)
from pyramid.view import view_config
from chronotope.model.category import (
    add_category,
    category_by_name,
    categories_by_uid,
    search_categories,
)


CATEGORY_LIMIT = 100
CATEGORY_NEW_MARKER = '__new__'


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
        categories.append({
            'id': '{0}{1}'.format(CATEGORY_NEW_MARKER, term),
            'text': term,
        })
    return categories


class CategoryReferencingForm(Behavior):

    @default
    @property
    def category_value(self):
        value = list()
        for record in self.model.attrs['category']:
            value.append(str(record.uid))
        return value

    @default
    @property
    def category_vocab(self):
        vocab = dict()
        for record in self.model.attrs['category']:
            vocab[str(record.uid)] = record.name
        return vocab

    @plumb
    def save(next_, self, widget, data):
        next_(self, widget, data)
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        # existing categories
        existing = self.category_value
        # expect a list of category uids, newly added categories consists of
        # ``CATEGORY_NEW_MARKER`` prefix followed by the value.
        categories = fetch('category')
        # new categories
        new_categories = list()
        for category in categories:
            if category[:len(CATEGORY_NEW_MARKER)] == CATEGORY_NEW_MARKER:
                name = category[len(CATEGORY_NEW_MARKER):]
                # try to get by name, possibly added by others in meantime
                cat = category_by_name(self.request, name)
                if not cat:
                    cat = add_category(self.request, name)
                new_categories.append(cat)
        for category in new_categories:
            self.model.attrs['category'].append(category)
        # reduce categories
        categories = [cat for cat in categories \
                      if cat[:len(CATEGORY_NEW_MARKER)] != CATEGORY_NEW_MARKER]
        # remove categories
        remove_categories = list()
        for category in existing:
            if not category in categories:
                remove_categories.append(category)
        remove_categories = categories_by_uid(self.request, remove_categories)
        for category in remove_categories:
            self.model.attrs['category'].remove(category)
        # set remaining if necessary
        categories = categories_by_uid(self.request, categories)
        for category in categories:
            if not category in self.model.attrs['category']:
                self.model.attrs['category'].append(category)
