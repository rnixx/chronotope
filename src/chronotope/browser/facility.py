from chronotope.browser.category import CategoriesTile
from chronotope.browser.references import CategoryReferencing
from chronotope.browser.references import LocationReferencing
from chronotope.browser.references import OccasionReferencing
from chronotope.browser.references import json_references
from chronotope.browser.submitter import SubmitterAccessAddForm
from chronotope.browser.submitter import SubmitterAccessEditForm
from chronotope.browser.submitter import SubmitterAccessTile
from chronotope.browser.ux import UXMixin
from chronotope.browser.ux import UXMixinProxy
from chronotope.model.facility import Facility
from chronotope.model.facility import search_facilities
from cone.app.browser.authoring import ContentAddForm
from cone.app.browser.authoring import ContentEditForm
from cone.app.browser.authoring import OverlayAddForm
from cone.app.browser.authoring import OverlayEditForm
from cone.app.browser.form import Form
from cone.app.browser.form import YAMLForm
from cone.app.browser.layout import ProtectedContentTile
from cone.app.utils import add_creation_metadata
from cone.app.utils import update_creation_metadata
from cone.tile import tile
from plumber import plumbing
from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config
import uuid


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
        return exists_from if exists_from else _('unknown', default='Unknown')

    @property
    def exists_to(self):
        exists_to = self.model.attrs['exists_to']
        return exists_to if exists_to else _('unknown', default='Unknown')


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
        attrs['exists_from'] = fetch('exists_from')
        attrs['exists_to'] = fetch('exists_to')


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
