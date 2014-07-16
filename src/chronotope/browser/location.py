import uuid
from plumber import (
    plumber,
    plumb,
    default,
    Behavior,
)
from node.utils import UNSET
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
from chronotope.model.location import (
    Location,
    locations_by_uid,
    search_locations,
)


_ = TranslationStringFactory('chronotope')


LOCATION_LIMIT = 100


@view_config(name='chronotope.location',
             accept='application/json',
             renderer='json')
def json_location(model, request):
    term = request.params['q']
    locations = list()
    for location in search_locations(request, term, limit=LOCATION_LIMIT):
        name = u'{0} {1} {2}'.format(location.street,
                                    location.zip,
                                    location.city)
        locations.append({
            'id': str(location.uid),
            'text': name,
        })
    return locations


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


class LocationReferencingForm(Behavior):

    @default
    @property
    def location_value(self):
        value = list()
        for record in self.model.attrs['location']:
            value.append(str(record.uid))
        return value

    @default
    def location_vocab(self, widget, data):
        vocab = dict()
        value = self.request.params.get(widget.dottedpath)
        if value is not None:
            records = locations_by_uid(self.request, value.split(','))
        else:
            records = self.model.attrs['location']
        for record in records:
            name = u'{0} {1} {2}'.format(record.street,
                                         record.zip,
                                         record.city)
            vocab[str(record.uid)] = name
        return vocab

    @plumb
    def save(next_, self, widget, data):
        next_(self, widget, data)
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        # existing locations
        existing = self.location_value
        # expect a list of location uids
        locations = fetch('location')
        # remove locations
        remove_locations = list()
        for location in existing:
            if not location in locations:
                remove_locations.append(location)
        remove_locations = locations_by_uid(self.request, remove_locations)
        for location in remove_locations:
            self.model.attrs['location'].remove(location)
        # set remaining if necessary
        locations = locations_by_uid(self.request, locations)
        for location in locations:
            if not location in self.model.attrs['location']:
                self.model.attrs['location'].append(location)


class LocationForm(object):
    __metaclass__ = plumber
    __plumbing__ = YAMLForm

    form_name = 'locationform'
    form_template = 'chronotope.browser:forms/location.yaml'
    message_factory = _
    location_zoom = 15

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


@tile('addform', interface=Location, permission="add")
class LocationAddForm(LocationForm, Form):
    __metaclass__ = plumber
    __plumbing__ = AddBehavior

    def save(self, widget, data):
        attrs = self.model.attrs
        attrs['uid'] = uuid.uuid4()
        add_creation_metadata(self.request, attrs)
        super(LocationAddForm, self).save(widget, data)
        self.model.parent[str(attrs['uid'])] = self.model
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
