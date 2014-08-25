import uuid
from plumber import plumbing
from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config
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
    ContentAddForm,
    ContentEditForm,
    OverlayAddForm,
    OverlayEditForm,
)
from cone.app.browser.utils import format_date
from chronotope.model.facility import (
    Facility,
    search_facilities,
)
from chronotope.browser.category import CategoriesTile
from chronotope.browser.references import (
    json_references,
    CategoryReferencing,
    LocationReferencing,
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


_ = TranslationStringFactory('chronotope')


FACILITY_LIMIT = 100


@view_config(name='chronotope.facility',
             accept='application/json',
             renderer='json')
def json_facility(model, request):
    return json_references(model, request, search_facilities, FACILITY_LIMIT)


@tile('content', 'templates/view.pt',
      interface=Facility, permission='view',
      strict=False)
class FacilityView(ProtectedContentTile):
    view_tile = 'facility'


@tile('facility', 'templates/facility.pt',
      interface=Facility, permission='login',
      strict=False)
class FacilityTile(SubmitterAccessTile, CategoriesTile):

    @property
    def exists_from(self):
        exists_from = self.model.attrs['exists_from']
        return format_date(exists_from, long=False)

    @property
    def exists_to(self):
        exists_to = self.model.attrs['exists_to']
        return format_date(exists_to, long=False)


@plumbing(
    YAMLForm,
    UXMixinProxy,
    CategoryReferencing,
    LocationReferencing,
    OccasionReferencing)
class FacilityForm(Form, UXMixin):
    form_name = 'facilityform'
    form_template = 'chronotope.browser:forms/facility.yaml'

    @property
    def message_factory(self):
        return _

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


class FacilityAdding(FacilityForm):

    def save(self, widget, data):
        attrs = self.model.attrs
        attrs['uid'] = uuid.uuid4()
        add_creation_metadata(self.request, attrs)
        super(FacilityAdding, self).save(widget, data)
        self.model.parent[str(attrs['uid'])] = self.model
        self.model()


class FacilityEditing(FacilityForm):

    def save(self, widget, data):
        attrs = self.model.attrs
        update_creation_metadata(self.request, attrs)
        super(FacilityEditing, self).save(widget, data)
        self.model()


@tile('addform', interface=Facility, permission="add")
@plumbing(ContentAddForm)
class FacilityAddForm(FacilityAdding):
    pass


@tile('editform', interface=Facility, permission="edit")
@plumbing(ContentEditForm)
class FacilityEditForm(FacilityEditing):
    pass


@tile('overlayaddform', interface=Facility, permission="add")
@plumbing(SubmitterAccessAddForm, OverlayAddForm)
class FacilityOverlayAddForm(FacilityAdding):
    pass


@tile('overlayeditform', interface=Facility, permission="edit")
@plumbing(SubmitterAccessEditForm, OverlayEditForm)
class FacilityOverlayEditForm(FacilityEditing):
    pass
