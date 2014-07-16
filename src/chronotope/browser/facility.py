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
from chronotope.model.facility import (
    Facility,
    facilities_by_uid,
    search_facilities,
)
from chronotope.browser.category import CategoryReferencingForm
from chronotope.browser.location import LocationReferencingForm


_ = TranslationStringFactory('chronotope')


FACILITY_LIMIT = 100


@view_config(name='chronotope.facility',
             accept='application/json',
             renderer='json')
def json_facility(model, request):
    term = request.params['q']
    facilities = list()
    for facility in search_facilities(request, term, limit=FACILITY_LIMIT):
        facilities.append({
            'id': str(facility.uid),
            'text': facility.title,
        })
    return facilities


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


class FacilityReferencingForm(Behavior):

    @default
    @property
    def facility_value(self):
        value = list()
        for record in self.model.attrs['facility']:
            value.append(str(record.uid))
        return value

    @default
    def facility_vocab(self, widget, data):
        vocab = dict()
        value = self.request.params.get(widget.dottedpath)
        if value is not None:
            value = [it for it in value.split(',') if it]
            records = facilities_by_uid(self.request, value)
        else:
            records = self.model.attrs['facility']
        for record in records:
            vocab[str(record.uid)] = record.title
        return vocab

    @plumb
    def save(next_, self, widget, data):
        next_(self, widget, data)
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        # existing facilities
        existing = self.facility_value
        # expect a list of facility uids
        facilities = fetch('facility')
        # remove facilities
        remove_facilities = list()
        for facility in existing:
            if not facility in facilities:
                remove_facilities.append(facility)
        remove_facilities = facilities_by_uid(self.request, remove_facilities)
        for facility in remove_facilities:
            self.model.attrs['facility'].remove(facility)
        # set remaining if necessary
        facilities = facilities_by_uid(self.request, facilities)
        for facility in facilities:
            if not facility in self.model.attrs['facility']:
                self.model.attrs['facility'].append(facility)


class FacilityForm(object):
    __metaclass__ = plumber
    __plumbing__ = (
        YAMLForm,
        CategoryReferencingForm,
        LocationReferencingForm,
    )

    form_name = 'facilityform'
    form_template = 'chronotope.browser:forms/facility.yaml'
    message_factory = _

    def save(self, widget, data):
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        attrs = self.model.attrs
        attrs['title'] = fetch('title')
        attrs['description'] = fetch('description')
        exists_from = fetch('exists_from')
        if exists_from:
            attrs['exists_from'] = exists_from
        exists_to = fetch('exists_to')
        if exists_to:
            attrs['exists_to'] = exists_to


@tile('addform', interface=Facility, permission="add")
class FacilityAddForm(FacilityForm, Form):
    __metaclass__ = plumber
    __plumbing__ = AddBehavior

    def save(self, widget, data):
        attrs = self.model.attrs
        attrs['uid'] = uuid.uuid4()
        add_creation_metadata(self.request, attrs)
        super(FacilityAddForm, self).save(widget, data)
        self.model.parent[str(attrs['uid'])] = self.model
        self.model()


@tile('editform', interface=Facility, permission="edit")
class FacilityEditForm(FacilityForm, Form):
    __metaclass__ = plumber
    __plumbing__ = EditBehavior

    def save(self, widget, data):
        attrs = self.model.attrs
        update_creation_metadata(self.request, attrs)
        super(FacilityEditForm, self).save(widget, data)
        self.model()
