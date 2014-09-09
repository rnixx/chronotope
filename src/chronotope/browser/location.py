import uuid
import urllib2
from plumber import (
    Behavior,
    plumbing,
    plumb,
    default,
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
    ContentAddForm,
    ContentEditForm,
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
from chronotope.browser.references import (
    json_references,
    FacilityReferencing,
    OccasionReferencing,
)
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
    submitter_came_from,
    get_submitter,
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
        return location_title(
            request,
            record.street,
            record.zip,
            record.city,
            record.lat,
            record.lon)
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
    def show_note(self):
        authenticated = authenticated_userid(self.request)
        if authenticated:
            return False
        submitter = get_submitter(self.request)
        if self.model.attrs['submitter'] != submitter:
            return False
        return True

    @property
    def coordinates(self):
        return {
            'lat': self.model.attrs['lat'],
            'lon': self.model.attrs['lon'],
            'zoom': 15,
        }


class CoordinatesProxy(Behavior):

    @default
    def location_picker(self, widget, data):
        map_icon = data.tag(
            'span', ' ', class_='glyphicon glyphicon-map-marker')
        pick_location = _('pick_location', default='Pick other location')
        link = data.tag('a', pick_location, class_='change_coordinates')
        return data.tag('div', map_icon, link, class_='location_picker')

    @plumb
    def prepare(_next, self):
        _next(self)
        if self.is_backend:
            return
        def fname(name):
            return '{0}.coordinates.{1}'.format(self.form_name, name)
        params = self.request.params
        coordinates = self.form['coordinates'] = factory(
            'field:label:div',
            props={
                'label': _('coordinates_label', default='Coordinates'),
                'label.class_add': 'col-sm-2',
                'div.class_add': 'col-sm-10',
            })
        coordinates['lat'] = factory(
            'div:label:text',
            value=params[fname('lat')],
            props={
                'div.class': 'inner-field',
                'label': _('lat', default='Latitude'),
                'display_proxy': True,
            },
            mode='display')
        coordinates['lon'] = factory(
            'div:label:text',
            value=params[fname('lon')],
            props={
                'div.class': 'inner-field',
                'label': _('lon', default='Longitude'),
                'display_proxy': True,
            },
            mode='display')
        coordinates['location_picker'] = factory(
            '*location_picker',
            props={
                'structural': True,
            },
            custom={
                'location_picker': {
                    'edit_renderers': [self.location_picker],
                }
            })
        coordinates['zoom'] = factory('hidden', value=params[fname('zoom')])


@plumbing(
    YAMLForm,
    UXMixinProxy,
    CoordinatesProxy,
    FacilityReferencing,
    OccasionReferencing)
class LocationForm(Form, UXMixin):
    form_name = 'locationform'
    form_template = 'chronotope.browser:forms/location.yaml'
    location_zoom = 15

    @property
    def description(self):
        return _(
            'location_form_description_text',
            default='If you know the exact address, please enter it. If not, '
                    'enter the information you know. The Captcha is required '
                    'to avoid spam'
        )

    @property
    def message_factory(self):
        return _

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
@plumbing(ContentAddForm)
class LocationAddForm(LocationAdding):
    pass


@tile('editform', interface=Location, permission="edit")
@plumbing(ContentEditForm)
class LocationEditForm(LocationEditing):
    pass


@tile('overlayaddform', interface=Location, permission="add")
@plumbing(SubmitterAccessAddForm, OverlayAddForm)
class LocationOverlayAddForm(LocationAdding):

    def next(self, request):
        came_from_url = urllib2.unquote(request.get('authoring_came_from'))
        root_url = make_url(self.request, node=self.model.root)
        if not came_from_url:
            if request.get('action.{0}.cancel'.format(self.form_name)):
                return [AjaxOverlay(close=True)]
            query = make_query(**{
                UX_IDENT: UX_FRONTEND,
            })
            url = make_url(self.request, node=self.model, query=query)
            return [AjaxOverlay(action='location', target=url),
                    AjaxEvent(root_url, 'datachanged', '#chronotope-map')]
        came_from_url += make_query(**{
            UX_IDENT: UX_FRONTEND,
            'submitter_came_from': submitter_came_from(self.request),
        })
        came_from_tile = request.get('came_from_tile')
        return [AjaxOverlay(action=came_from_tile, target=came_from_url),
                AjaxEvent(root_url, 'datachanged', '#chronotope-map')]


@tile('overlayeditform', interface=Location, permission="edit")
@plumbing(SubmitterAccessEditForm, OverlayEditForm)
class LocationOverlayEditForm(LocationEditing):

    def next(self, request):
        came_from_url = urllib2.unquote(request.get('authoring_came_from'))
        came_from_url += make_query(**{
            UX_IDENT: UX_FRONTEND,
            'submitter_came_from': submitter_came_from(self.request),
        })
        came_from_tile = request.get('came_from_tile')
        root_url = make_url(self.request, node=self.model.root)
        return [AjaxOverlay(action=came_from_tile, target=came_from_url),
                AjaxEvent(root_url, 'datachanged', '#chronotope-map')]
