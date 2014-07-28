import uuid
from plumber import (
    Behavior,
    plumber,
    plumb,
)
from node.utils import UNSET
from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config
from pyramid.security import authenticated_userid
from pyramid.response import Response
from yafowil.base import factory
from cone.tile import (
    tile,
    Tile,
    render_tile,
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
    AddForm,
    EditForm,
    OverlayAddForm,
    OverlayEditForm,
)
from cone.app.browser.ajax import (
    AjaxOverlay,
    AjaxEvent,
)
from cone.app.browser.utils import (
    make_url,
    make_query,
)
from chronotope.model.location import (
    Location,
    search_locations,
    location_title,
)
from chronotope.browser.references import json_references
from chronotope.browser.submitter import (
    SubmitterAccessTile,
    SubmitterAccessAddForm,
    SubmitterAccessEditForm,
)
from chronotope.browser.ux import (
    UXMixin,
    UXMixinProxy,
)
from chronotope.utils import (
    UX_IDENT,
    UX_FRONTEND,
)


_ = TranslationStringFactory('chronotope')


LOCATION_LIMIT = 100


@view_config('chronotope.location_controls')
def location_controls(model, request):
    return Response(render_tile(model, request, 'location_controls'))


@tile('location_controls', 'templates/location_controls.pt',
      permission='login', strict=False)
class LocationControls(Tile):

    @property
    def authenticated(self):
        return bool(authenticated_userid(self.request))


@view_config(name='chronotope.location',
             accept='application/json',
             renderer='json')
def json_location(model, request):
    def extract_title(record):
        return location_title(record.street, record.zip, record.city)
    return json_references(
        model, request, search_locations, LOCATION_LIMIT,
        extract_title=extract_title)


@tile('content', 'templates/view.pt',
      interface=Location, permission='view',
      strict=False)
class LocationView(ProtectedContentTile):
    view_tile = 'location'


@tile('location', 'templates/location.pt',
      interface=Location, permission='login',
      strict=False)
class LocationTile(SubmitterAccessTile, UXMixin):

    @property
    def coordinates(self):
        return {
            'lat': self.model.attrs['lat'],
            'lon': self.model.attrs['lon'],
            'zoom': 15,
        }


class CoordinatesProxy(Behavior):

    @plumb
    def prepare(_next, self):
        _next(self)
        if self.is_backend:
            return
        def fname(name):
            return '{0}.coordinates.{1}'.format(self.form_name, name)
        params = self.request.params
        coordinates = self.form['coordinates'] = factory('compound')
        coordinates['lat'] = factory('hidden', value=params[fname('lat')])
        coordinates['lon'] = factory('hidden', value=params[fname('lon')])
        coordinates['zoom'] = factory('hidden', value=params[fname('zoom')])


class LocationForm(Form, UXMixin):
    __metaclass__ = plumber
    __plumbing__ = (
        YAMLForm,
        UXMixinProxy,
        CoordinatesProxy,
    )

    form_name = 'locationform'
    form_template = 'chronotope.browser:forms/location.yaml'
    message_factory = _
    location_zoom = 15

    @property
    def coordinates_mode(self):
        return self.is_backend and 'edit' or 'skip'

    @property
    def coordinates_value(self):
        attrs = self.model.attrs
        if attrs['lat'] is not None and attrs['lon'] is not None:
            return {
                'lat': attrs['lat'],
                'lon': attrs['lon'],
                'zoom': self.location_zoom,
            }
        return UNSET

    @property
    def country_vocab(self):
        return [
            ('germany', _('germany', default=u'Germany')),
            ('austria', _('austria', default=u'Austria')),
            ('swizerland', _('swizerland', default=u'Swizerland')),
        ]

    def save(self, widget, data):
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        attrs = self.model.attrs
        coordinates = fetch('coordinates')
        if coordinates:
            attrs['lat'] = coordinates['lat']
            attrs['lon'] = coordinates['lon']
        attrs['street'] = fetch('street')
        attrs['zip'] = fetch('zip')
        attrs['city'] = fetch('city')
        attrs['country'] = fetch('country')


class LocationAdding(LocationForm):

    def save(self, widget, data):
        attrs = self.model.attrs
        attrs['uid'] = uuid.uuid4()
        add_creation_metadata(self.request, attrs)
        super(LocationAdding, self).save(widget, data)
        self.model.parent[str(attrs['uid'])] = self.model
        self.model()


class LocationEditing(LocationForm):

    def save(self, widget, data):
        attrs = self.model.attrs
        update_creation_metadata(self.request, attrs)
        super(LocationEditing, self).save(widget, data)
        self.model()


@tile('addform', interface=Location, permission="add")
class LocationAddForm(LocationAdding):
    __metaclass__ = plumber
    __plumbing__ = AddForm


@tile('editform', interface=Location, permission="edit")
class LocationEditForm(LocationEditing):
    __metaclass__ = plumber
    __plumbing__ = EditForm


@tile('overlayaddform', interface=Location, permission="add")
class LocationOverlayAddForm(LocationAdding):
    __metaclass__ = plumber
    __plumbing__ = (
        OverlayAddForm,
        SubmitterAccessAddForm,
    )

    def next(self, request):
        query = make_query(**{UX_IDENT: UX_FRONTEND})
        location_url = make_url(self.request, node=self.model, query=query)
        root_url = make_url(self.request, node=self.model.root)
        return [AjaxOverlay(action='location', target=location_url),
                AjaxEvent(root_url, 'datachanged', '#chronotope-map')]


@tile('overlayeditform', interface=Location, permission="edit")
class LocationOverlayEditForm(LocationEditing):
    __metaclass__ = plumber
    __plumbing__ = (
        OverlayEditForm,
        SubmitterAccessEditForm,
    )

    def next(self, request):
        query = make_query(**{UX_IDENT: UX_FRONTEND})
        location_url = make_url(self.request, node=self.model, query=query)
        return [AjaxOverlay(action='location', target=location_url)]
