import uuid
from plumber import (
    plumber,
    plumb,
    default,
    Behavior,
)
from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config
from cone.tile import (
    tile,
    Tile,
)
from cone.app.utils import (
    add_creation_metadata,
    update_creation_metadata,
)
from cone.app.browser.layout import ProtectedContentTile
from cone.app.browser.form import (
    Form,
    YAMLForm,
)
from cone.app.browser.authoring import (
    AddBehavior,
    EditBehavior,
)
from chronotope.model.occasion import (
    Occasion,
    occasions_by_uid,
    search_occasions,
)
from chronotope.browser.facility import FacilityReferencingForm


_ = TranslationStringFactory('chronotope')


OCCASION_LIMIT = 100


@view_config(name='chronotope.occasion',
             accept='application/json',
             renderer='json')
def json_occasion(model, request):
    term = request.params['q']
    occasions = list()
    for occasion in search_occasions(request, term, limit=OCCASION_LIMIT):
        occasions.append({
            'id': str(occasion.uid),
            'text': occasion.title,
        })
    return occasions


@tile('content', 'templates/view.pt',
      interface=Occasion, permission='view',
      strict=False)
class OccasionView(ProtectedContentTile):
    view_tile = 'occasion'


@tile('occasion', 'templates/occasion.pt',
      interface=Occasion, permission='login',
      strict=False)
class OccasionTile(Tile):
    pass


class OccasionReferencingForm(Behavior):

    @default
    @property
    def occasion_value(self):
        value = list()
        for record in self.model.attrs['occasion']:
            value.append(str(record.uid))
        return value

    @default
    def occasion_vocab(self, widget, data):
        vocab = dict()
        value = self.request.params.get(widget.dottedpath)
        if value is not None:
            records = occasions_by_uid(self.request, value.split(','))
        else:
            records = self.model.attrs['occasion']
        for record in records:
            vocab[str(record.uid)] = record.title
        return vocab

    @plumb
    def save(next_, self, widget, data):
        next_(self, widget, data)
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        # existing occasion
        existing = self.occasion_value
        # expect a list of occasion uids
        occasions = fetch('occasion')
        # remove occasions
        remove_occasions = list()
        for occasion in existing:
            if not occasion in occasions:
                remove_occasions.append(occasion)
        remove_occasions = occasions_by_uid(self.request, remove_occasions)
        for occasion in remove_occasions:
            self.model.attrs['occasion'].remove(occasion)
        # set remaining if necessary
        occasions = occasions_by_uid(self.request, occasions)
        for occasion in occasions:
            if not occasion in self.model.attrs['occasion']:
                self.model.attrs['occasion'].append(occasion)


class OccasionForm(object):
    __metaclass__ = plumber
    __plumbing__ = (
        YAMLForm,
        FacilityReferencingForm,
    )

    form_name = 'occasionform'
    form_template = 'chronotope.browser:forms/occasion.yaml'
    message_factory = _

    def save(self, widget, data):
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        attrs = self.model.attrs
        attrs['title'] = fetch('title')
        attrs['description'] = fetch('description')
        duration_from = fetch('duration_from')
        if duration_from:
            attrs['duration_from'] = duration_from
        duration_to = fetch('duration_to')
        if duration_to:
            attrs['duration_to'] = duration_to


@tile('addform', interface=Occasion, permission="add")
class OccasionAddForm(OccasionForm, Form):
    __metaclass__ = plumber
    __plumbing__ = AddBehavior

    def save(self, widget, data):
        attrs = self.model.attrs
        attrs['uid'] = uuid.uuid4()
        add_creation_metadata(self.request, attrs)
        super(OccasionAddForm, self).save(widget, data)
        self.model.parent[str(attrs['uid'])] = self.model
        self.model()


@tile('editform', interface=Occasion, permission="edit")
class OccasionEditForm(OccasionForm, Form):
    __metaclass__ = plumber
    __plumbing__ = EditBehavior

    def save(self, widget, data):
        attrs = self.model.attrs
        update_creation_metadata(self.request, attrs)
        super(OccasionEditForm, self).save(widget, data)
        self.model()
