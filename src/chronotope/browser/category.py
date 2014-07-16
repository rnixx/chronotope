import uuid
from plumber import (
    plumb,
    default,
    Behavior,
)
from pyramid.view import view_config
from chronotope.model.category import (
    add_category,
    delete_category,
    category_by_name,
    category_by_uid,
    categories_by_uid,
    search_categories,
)


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


class CategoryReferencingForm(Behavior):

    @default
    @property
    def category_value(self):
        value = list()
        for record in self.model.attrs['category']:
            value.append(str(record.uid))
        return value

    @default
    def category_vocab(self, widget, data):
        vocab = dict()
        value = self.request.params.get(widget.dottedpath)
        if value is not None:
            value = [it for it in value.split(',') if it]
            for category in value:
                try:
                    uid = uuid.UUID(category)
                    category = category_by_uid(self.request, uid)
                    if category:
                        vocab[str(uid)] = category.name
                except ValueError:
                    vocab[category] = category
        else:
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
            try:
                uuid.UUID(category)
            except ValueError:
                # try to get by name, possibly added by others in meantime
                cat = category_by_name(self.request, category)
                if not cat:
                    cat = add_category(self.request, category)
                new_categories.append(cat)
        for category in new_categories:
            self.model.attrs['category'].append(category)
        # reduce categories
        reduced = list()
        for cat in categories:
            try:
                uuid.UUID(cat)
                reduced.append(cat)
            except ValueError:
                pass
        # remove categories
        remove_categories = list()
        for category in existing:
            if not category in reduced:
                remove_categories.append(category)
        remove_categories = categories_by_uid(self.request, remove_categories)
        for category in remove_categories:
            self.model.attrs['category'].remove(category)
            # remove category entirely if not used any longer
            # XXX: need to adopt once other than facilities are categorized
            if not category.facility:
                delete_category(self.request, category)
        # set categories
        categories = categories_by_uid(self.request, reduced)
        for category in categories:
            if not category in self.model.attrs['category']:
                self.model.attrs['category'].append(category)
