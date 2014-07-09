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
from chronotope.model import Location
from chronotope.browser import AuthoringNext


_ = TranslationStringFactory('chronotope')


@view_config(name='chronotope.location',
             accept='application/json',
             renderer='json')
def json_location(model, request):
    return [
        {'id': 'Location1-uid', 'text': 'Location1'},
        {'id': 'Location2-uid', 'text': 'Location2'},
    ]


@tile('content', 'templates/view.pt',
      interface=Location, permission='view',
      strict=False)
class LocationView(ProtectedContentTile):
    view_tile = 'location'


@tile('location', 'templates/location.pt',
      interface=Location, permission='login',
      strict=False)
class LocationTile(Tile):
    pass


class LocationForm(object):
    __metaclass__ = plumber
    __plumbing__ = YAMLForm

    form_name = 'locationform'
    form_template = 'chronotope.browser:forms/location.yaml'
    message_factory = _

    def save(self, widget, data):
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        attrs = self.model.attrs
        attrs['lat'] = fetch('lat')
        attrs['lon'] = fetch('lon')
        attrs['street'] = fetch('street')
        attrs['zip'] = fetch('zip')
        attrs['city'] = fetch('city')
        attrs['country'] = fetch('country')


@tile('addform', interface=Location, permission="add")
class LocationAddForm(LocationForm, Form):
    __metaclass__ = plumber
    __plumbing__ = (
        AddBehavior,
        AuthoringNext,
    )

    def save(self, widget, data):
        attrs = self.model.attrs
        add_creation_metadata(self.request, attrs)
        super(LocationAddForm, self).save(widget, data)
        self.model.parent[str(uuid.uuid4())] = self.model
        self.model()


@tile('editform', interface=Location, permission="edit")
class LocationEditForm(LocationForm, Form):
    __metaclass__ = plumber
    __plumbing__ = (
        EditBehavior,
        AuthoringNext,
    )

    def save(self, widget, data):
        attrs = self.model.attrs
        update_creation_metadata(self.request, attrs)
        super(LocationEditForm, self).save(widget, data)
        self.model()
