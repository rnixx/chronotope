import uuid
from plumber import plumber
from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config
from pyramid.security import authenticated_userid
from cone.tile import tile
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
from cone.app.browser.utils import format_date
from chronotope.model.facility import (
    Facility,
    search_facilities,
)
from chronotope.browser.category import CategoriesTile
from chronotope.browser.references import (
    LocationReferencing,
    CategoryReferencing,
)


_ = TranslationStringFactory('chronotope')


FACILITY_LIMIT = 100


@view_config(name='chronotope.facility',
             accept='application/json',
             renderer='json')
def json_facility(model, request):
    term = request.params['q']
    facilities = list()
    state = not authenticated_userid(request) and ['published'] or []
    for facility in search_facilities(request, term, state=state,
                                      limit=FACILITY_LIMIT):
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
class FacilityTile(CategoriesTile):

    @property
    def exists_from(self):
        exists_from = self.model.attrs['exists_from']
        return format_date(exists_from, long=False)

    @property
    def exists_to(self):
        exists_to = self.model.attrs['exists_to']
        return format_date(exists_to, long=False)


class FacilityForm(object):
    __metaclass__ = plumber
    __plumbing__ = (
        YAMLForm,
        CategoryReferencing,
        LocationReferencing,
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
