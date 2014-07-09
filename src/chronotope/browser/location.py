import uuid
from plumber import plumber
from webob.exc import HTTPFound
from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config
from cone.tile import tile
from cone.app.utils import (
    add_creation_metadata,
    update_creation_metadata,
)
from cone.app.browser.ajax import (
    AjaxAction,
)
from cone.app.browser.form import (
    Form,
    YAMLForm,
)
from cone.app.browser.authoring import (
    AddBehavior,
    EditBehavior,
)
from cone.app.browser.utils import make_url
from chronotope.model import Location


_ = TranslationStringFactory('chronotope')


@view_config(name='chronotope.location',
             accept='application/json',
             renderer='json')
def json_location(model, request):
    return [
        {'id': 'Location1', 'text': 'Location1'},
        {'id': 'Location2', 'text': 'Location2'},
    ]


class LocationForm(object):
    __metaclass__ = plumber
    __plumbing__ = YAMLForm

    form_template = 'chronotope.browser:forms/location.yaml'
    message_factory = _

    def save(self, widget, data):
        def fetch(name):
            return data.fetch('locationform.%s' % name).extracted
        attrs = self.model.attrs
        attrs['lat'] = fetch('lat')
        attrs['lon'] = fetch('lon')
        attrs['street'] = fetch('street')
        attrs['zip'] = fetch('zip')
        attrs['city'] = fetch('city')
        attrs['country'] = fetch('country')

    def next(self, request):
        model = self.model
        tile = 'content'
        if self.request.params.get('action.locationform.cancel'):
            model = model.parent
        url = make_url(request.request, node=model)
        if self.ajax_request:
            return [
                AjaxAction(url, tile, 'inner', '#content'),
            ]
        return HTTPFound(location=url)


@tile('addform', interface=Location, permission="add")
class LocationAddForm(LocationForm, Form):
    __metaclass__ = plumber
    __plumbing__ = AddBehavior

    def save(self, widget, data):
        attrs = self.model.attrs
        add_creation_metadata(self.request, attrs)
        super(LocationAddForm, self).save(widget, data)
        self.model.parent[str(uuid.uuid4())] = self.model
        self.model()


@tile('editform', interface=Location, permission="edit")
class LocationEditForm(LocationForm, Form):
    __metaclass__ = plumber
    __plumbing__ = EditBehavior

    def save(self, widget, data):
        attrs = self.model.attrs
        update_creation_metadata(self.request, attrs)
        super(LocationEditForm, self).save(widget, data)
        self.model()
