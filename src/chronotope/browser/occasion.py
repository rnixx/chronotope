import uuid
from plumber import plumber
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
from chronotope.model.occasion import (
    Occasion,
    search_occasions,
)
from chronotope.browser.references import (
    json_references,
    LocationReferencing,
    FacilityReferencing,
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


OCCASION_LIMIT = 100


@view_config(name='chronotope.occasion',
             accept='application/json',
             renderer='json')
def json_occasion(model, request):
    return json_references(model, request, search_occasions, OCCASION_LIMIT)


@tile('content', 'templates/view.pt',
      interface=Occasion, permission='view',
      strict=False)
class OccasionView(ProtectedContentTile):
    view_tile = 'occasion'


@tile('occasion', 'templates/occasion.pt',
      interface=Occasion, permission='login',
      strict=False)
class OccasionTile(SubmitterAccessTile):

    @property
    def duration_from(self):
        duration_from = self.model.attrs['duration_from']
        return format_date(duration_from, long=False)

    @property
    def duration_to(self):
        duration_to = self.model.attrs['duration_to']
        return format_date(duration_to, long=False)


class OccasionForm(Form, UXMixin):
    __metaclass__ = plumber
    __plumbing__ = (
        YAMLForm,
        UXMixinProxy,
        LocationReferencing,
        FacilityReferencing,
    )

    form_name = 'occasionform'
    form_template = 'chronotope.browser:forms/occasion.yaml'
    message_factory = _

    def save(self, widget, data):
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        attrs = self.model.attrs
        attrs['title'] = fetch('title')
        attrs['description'] = fetch('description')
        duration_from = fetch('duration_from')
        if duration_from:
            attrs['duration_from'] = duration_from
        duration_to = fetch('duration_to')
        if duration_to:
            attrs['duration_to'] = duration_to


class OccasionAdding(OccasionForm):

    def save(self, widget, data):
        attrs = self.model.attrs
        attrs['uid'] = uuid.uuid4()
        add_creation_metadata(self.request, attrs)
        super(OccasionAdding, self).save(widget, data)
        self.model.parent[str(attrs['uid'])] = self.model
        self.model()


class OccasionEditing(OccasionForm):

    def save(self, widget, data):
        attrs = self.model.attrs
        update_creation_metadata(self.request, attrs)
        super(OccasionEditing, self).save(widget, data)
        self.model()


@tile('addform', interface=Occasion, permission="add")
class OccasionAddForm(OccasionAdding):
    __metaclass__ = plumber
    __plumbing__ = ContentAddForm


@tile('editform', interface=Occasion, permission="edit")
class OccasionEditForm(OccasionEditing):
    __metaclass__ = plumber
    __plumbing__ = ContentEditForm


@tile('overlayaddform', interface=Occasion, permission="add")
class OccasionOverlayAddForm(OccasionAdding):
    __metaclass__ = plumber
    __plumbing__ = (
        SubmitterAccessAddForm,
        OverlayAddForm,
    )


@tile('overlayeditform', interface=Occasion, permission="edit")
class OccasionOverlayEditForm(OccasionEditing):
    __metaclass__ = plumber
    __plumbing__ = (
        SubmitterAccessEditForm,
        OverlayEditForm,
    )
