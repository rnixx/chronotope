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
    AddForm,
    EditForm,
    OverlayAddForm,
    OverlayEditForm,
)
from cone.app.browser.ajax import AjaxOverlay
from cone.app.browser.utils import (
    make_url,
    make_query,
    format_date,
)
from chronotope.model.occasion import (
    Occasion,
    search_occasions,
)
from chronotope.browser.references import (
    LocationReferencing,
    FacilityReferencing,
)
from chronotope.browser import (
    UXMixin,
    UXMixinProxy,
    SubmitterAccessTile,
    SubmitterAccessAddForm,
    SubmitterAccessEditForm,
)
from chronotope.utils import (
    UX_IDENT,
    UX_FRONTEND,
    get_submitter,
)


_ = TranslationStringFactory('chronotope')


OCCASION_LIMIT = 100


@view_config(name='chronotope.occasion',
             accept='application/json',
             renderer='json')
def json_occasion(model, request):
    term = request.params['q']
    # authenticated gets all locations
    authenticated = bool(authenticated_userid(request))
    if authenticated:
        records = search_occasions(request, term, limit=OCCASION_LIMIT)
    # anonymous gets published locations
    else:
        records = search_occasions(request, term, state=['published'],
                                   limit=OCCASION_LIMIT)
        # additionally add records by submitter
        submitter = get_submitter(request)
        if submitter:
            records += search_occasions(request, term, state=['draft'],
                                        submitter=submitter,
                                        limit=OCCASION_LIMIT)
    # create and return result
    occasions = list()
    for occasion in records:
        occasions.append({
            'id': str(occasion.uid),
            'text': occasion.title,
        })
    return sorted(occasions, key=lambda x: x['text'])


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
    __plumbing__ = AddForm


@tile('editform', interface=Occasion, permission="edit")
class OccasionEditForm(OccasionEditing):
    __metaclass__ = plumber
    __plumbing__ = EditForm


@tile('overlayaddform', interface=Occasion, permission="add")
class OccasionOverlayAddForm(OccasionAdding):
    __metaclass__ = plumber
    __plumbing__ = (
        OverlayAddForm,
        SubmitterAccessAddForm,
    )

    def next(self, request):
        query = make_query(**{UX_IDENT: UX_FRONTEND})
        occasion_url = make_url(self.request, node=self.model, query=query)
        return [AjaxOverlay(action='occasion', target=occasion_url)]


@tile('overlayeditform', interface=Occasion, permission="edit")
class OccasionOverlayEditForm(OccasionEditing):
    __metaclass__ = plumber
    __plumbing__ = (
        OverlayEditForm,
        SubmitterAccessEditForm,
    )

    def next(self, request):
        query = make_query(**{UX_IDENT: UX_FRONTEND})
        occasion_url = make_url(self.request, node=self.model, query=query)
        return [AjaxOverlay(action='occasion', target=occasion_url)]
