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
from chronotope.model import Facility
from chronotope.browser import AuthoringNext


_ = TranslationStringFactory('chronotope')


@view_config(name='chronotope.facility',
             accept='application/json',
             renderer='json')
def json_facility(model, request):
    return [
        {'id': 'Facility1-uid', 'text': 'Facility1'},
        {'id': 'Facility2-uid', 'text': 'Facility2'},
    ]


@tile('content', 'templates/view.pt',
      interface=Facility, permission='view',
      strict=False)
class FacilityView(ProtectedContentTile):
    view_tile = 'facility'


@tile('facility', 'templates/facility.pt',
      interface=Facility, permission='login',
      strict=False)
class FacilityTile(Tile):
    pass


class FacilityForm(object):
    __metaclass__ = plumber
    __plumbing__ = YAMLForm

    form_name = 'facilityform'
    form_template = 'chronotope.browser:forms/facility.yaml'
    message_factory = _

    @property
    def category_value(self):
        return ['a', 'b', 'c']

    @property
    def category_vocab(self):
        return {
            'a': 'Label a',
            'b': 'Label b',
            'c': 'Label c',
        }

    @property
    def location_value(self):
        return ['d', 'e', 'f']

    @property
    def location_vocab(self):
        return {
            'd': 'Label d',
            'e': 'Label e',
            'f': 'Label f',
        }

    def save(self, widget, data):
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        attrs = self.model.attrs
        attrs['title'] = fetch('title')
        attrs['description'] = fetch('description')
        attrs['exists_from'] = fetch('exists_from')
        attrs['exists_to'] = fetch('exists_to')
        print fetch('category')
        print fetch('location')
        #attrs['category'] = fetch('category')
        #attrs['location'] = fetch('location')


@tile('addform', interface=Facility, permission="add")
class FacilityAddForm(FacilityForm, Form):
    __metaclass__ = plumber
    __plumbing__ = (
        AddBehavior,
        AuthoringNext,
    )

    def save(self, widget, data):
        attrs = self.model.attrs
        add_creation_metadata(self.request, attrs)
        super(FacilityAddForm, self).save(widget, data)
        self.model.parent[str(uuid.uuid4())] = self.model
        self.model()


@tile('editform', interface=Facility, permission="edit")
class FacilityEditForm(FacilityForm, Form):
    __metaclass__ = plumber
    __plumbing__ = (
        EditBehavior,
        AuthoringNext,
    )

    def save(self, widget, data):
        attrs = self.model.attrs
        update_creation_metadata(self.request, attrs)
        super(FacilityEditForm, self).save(widget, data)
        self.model()
