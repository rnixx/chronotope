import uuid
from plumber import plumber
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
from chronotope.model import Occasion


_ = TranslationStringFactory('chronotope')


@view_config(name='chronotope.occasion',
             accept='application/json',
             renderer='json')
def json_occasion(model, request):
    return [
        {'id': 'Occasion1-uid', 'text': 'Occasion1'},
        {'id': 'Occasion2-uid', 'text': 'Occasion2'},
    ]


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


class OccasionForm(object):
    __metaclass__ = plumber
    __plumbing__ = YAMLForm

    form_name = 'occasionform'
    form_template = 'chronotope.browser:forms/occasion.yaml'
    message_factory = _

    @property
    def facility_value(self):
        return ['g', 'h', 'i']

    @property
    def facility_vocab(self):
        return {
            'g': 'Label g',
            'h': 'Label h',
            'i': 'Label i',
        }

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
        print fetch('facility')
        #attrs['facility'] = fetch('facility')


@tile('addform', interface=Occasion, permission="add")
class OccasionAddForm(OccasionForm, Form):
    __metaclass__ = plumber
    __plumbing__ = AddBehavior

    def save(self, widget, data):
        attrs = self.model.attrs
        add_creation_metadata(self.request, attrs)
        super(OccasionAddForm, self).save(widget, data)
        self.model.parent[str(uuid.uuid4())] = self.model
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
