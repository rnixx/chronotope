import uuid
from plumber import plumber
from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config
from pyramid.security import authenticated_userid
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
    AddForm,
    EditForm,
)
from cone.app.browser.utils import format_date
from chronotope.model.occasion import (
    Occasion,
    search_occasions,
)
from chronotope.browser.references import (
    LocationReferencing,
    FacilityReferencing,
)


_ = TranslationStringFactory('chronotope')


OCCASION_LIMIT = 100


@view_config(name='chronotope.occasion',
             accept='application/json',
             renderer='json')
def json_occasion(model, request):
    term = request.params['q']
    occasions = list()
    state = not authenticated_userid(request) and ['published'] or []
    for occasion in search_occasions(request, term, state=state,
                                     limit=OCCASION_LIMIT):
        occasions.append({
            'id': str(occasion.uid),
            'text': occasion.title,
        })
    return occasions


@tile('content', 'templates/view.pt',
      interface=Occasion, permission='view',
      strict=False)
class OccasionView(ProtectedContentTile):
    view_tile = 'occasion'


@tile('occasion', 'templates/occasion.pt',
      interface=Occasion, permission='login',
      strict=False)
class OccasionTile(Tile):

    @property
    def duration_from(self):
        duration_from = self.model.attrs['duration_from']
        return format_date(duration_from, long=False)

    @property
    def duration_to(self):
        duration_to = self.model.attrs['duration_to']
        return format_date(duration_to, long=False)


class OccasionForm(object):
    __metaclass__ = plumber
    __plumbing__ = (
        YAMLForm,
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


@tile('addform', interface=Occasion, permission="add")
class OccasionAddForm(OccasionForm, Form):
    __metaclass__ = plumber
    __plumbing__ = AddForm

    def save(self, widget, data):
        attrs = self.model.attrs
        attrs['uid'] = uuid.uuid4()
        add_creation_metadata(self.request, attrs)
        super(OccasionAddForm, self).save(widget, data)
        self.model.parent[str(attrs['uid'])] = self.model
        self.model()


@tile('editform', interface=Occasion, permission="edit")
class OccasionEditForm(OccasionForm, Form):
    __metaclass__ = plumber
    __plumbing__ = EditForm

    def save(self, widget, data):
        attrs = self.model.attrs
        update_creation_metadata(self.request, attrs)
        super(OccasionEditForm, self).save(widget, data)
        self.model()
