from plumber import (
    Behavior,
    plumb,
    default,
)
from node.utils import instance_property
from pyramid.i18n import TranslationStringFactory
from pyramid.security import authenticated_userid
from pyramid.exceptions import Forbidden
from yafowil.base import factory
from cone.tile import (
    Tile,
    tile,
)
from cone.app.browser.contents import ContentsTile
from cone.app.browser.actions import ViewLink
from cone.app.browser.utils import (
    make_query,
    make_url,
)
from chronotope.sql import get_session
from chronotope.model.attachment import (
    AttachmentRecord,
    Attachment,
)
from chronotope.model.facility import (
    FacilityRecord,
    Facility,
)
from chronotope.model.location import (
    LocationRecord,
    Location,
)
from chronotope.model.occasion import (
    OccasionRecord,
    Occasion,
)
from chronotope.utils import (
    UX_IDENT,
    UX_FRONTEND,
    get_submitter,
    get_recaptcha_public_key,
    get_recaptcha_private_key,
)


_ = TranslationStringFactory('chronotope')


def check_submitter_access(model, request):
    authenticated = authenticated_userid(request)
    if not authenticated:
        submitter = get_submitter(request)
        if model.attrs['state'] != 'published':
            if not submitter:
                raise Forbidden
            if model.attrs['submitter'] != submitter:
                raise Forbidden
            if model.attrs['state'] != 'draft':
                raise Forbidden


class SubmitterAccessTile(Tile):

    def __call__(self, model, request):
        check_submitter_access(model, request)
        return super(SubmitterAccessTile, self).__call__(model, request)


class SubmitterForm(Behavior):

    @default
    @property
    def authenticated(self):
        return bool(authenticated_userid(self.request))

    @plumb
    def prepare(_next, self):
        _next(self)
        if self.authenticated:
            return
        captcha_widget = factory(
            'field:label:div:error:recaptcha',
            name='captcha',
            props={
                'label': _('verify', default='Verify'),
                'public_key': get_recaptcha_public_key(),
                'private_key': get_recaptcha_private_key(),
                'lang': 'de',
                'theme': 'clean',
                'label.class_add': 'col-sm-2',
                'div.class_add': 'col-sm-10',
                'error.position': 'after',
            },
        )
        save_widget = self.form['controls']
        self.form.insertbefore(captcha_widget, save_widget)

    @plumb
    def save(_next, self, widget, data):
        if not self.authenticated:
            submitter = get_submitter(self.request)
            self.model.attrs['submitter'] = submitter
        _next(self, widget, data)


class SubmitterAccessAddForm(SubmitterForm):

    @plumb
    def prepare(_next, self):
        submitter = get_submitter(self.request)
        if not self.authenticated:
            if not submitter:
                raise Forbidden
        _next(self)


class SubmitterAccessEditForm(SubmitterForm):

    @plumb
    def prepare(_next, self):
        submitter = get_submitter(self.request)
        if not self.authenticated:
            if not submitter:
                raise Forbidden
            if submitter != self.model.attrs['submitter']:
                raise Forbidden
        _next(self)


class SubmitterViewLink(ViewLink):
    css = 'title'
    event = None
    action = None

    @property
    def target(self):
        query = make_query(**{UX_IDENT: UX_FRONTEND})
        return make_url(self.request, node=self.model, query=query)

    @property
    def overlay(self):
        if isinstance(self.model, Attachment):
            return 'attachment'
        if isinstance(self.model, Facility):
            return 'facility'
        if isinstance(self.model, Location):
            return 'location'
        if isinstance(self.model, Occasion):
            return 'occasion'


@tile('submitter_contents',
      'cone.app.browser:templates/table.pt',
      permission='view')
class SubmitterContentsTile(ContentsTile):
    table_id = 'submitter_contents'
    table_tile_name = 'submitter_contents'
    col_defs = [{
            'id': 'title',
            'title': _('title', 'Title'),
            'sort_key': 'title',
            'sort_title': _('sort_on_title', 'Sort on title'),
            'content': 'structure'
        }, {
            'id': 'created',
            'title': _('created', 'Created'),
            'sort_key': 'created',
            'sort_title': _('sort_on_created', 'Sort on created'),
            'content': 'datetime'
        }, {
            'id': 'modified',
            'title': _('modified', 'Modified'),
            'sort_key': 'modified',
            'sort_title': _('sort_on_modified', 'Sort on modified'),
            'content': 'datetime'
        }, {
            'id': 'state',
            'title': _('state', 'State'),
            'sort_key': 'state',
            'sort_title': _('sort_on_state', 'Sort on state'),
            'content': 'string'
        }
    ]
    sort_keys = ContentsTile.sort_keys.copy()
    sort_keys['state'] = lambda x: x.attrs['state']

    @instance_property
    def view_link(self):
        return SubmitterViewLink()

    def row_data(self, node):
        row_data = super(SubmitterContentsTile, self).row_data(node)
        row_data['state'] = node.attrs['state']
        return row_data

    def sorted_rows(self, start, end, sort, order):
        children = self.sorted_children(sort, order)
        rows = list()
        for child in children[start:end]:
            row_data = self.row_data(child)
            row_data.css += ' state-%s' % child.state
            rows.append(row_data)
        return rows

    @property
    def listable_children(self):
        submitter = get_submitter(self.request)
        if submitter:
            def query(cls):
                return session.query(cls.uid)\
                              .filter(cls.submitter == submitter).all()
        else:
            creator = authenticated_userid(self.request)
            def query(cls):
                return session.query(cls.uid)\
                              .filter(cls.creator == creator).all()
        root = self.model.root
        def fetch_node(container, uid):
            return container[str(uid)]
        nodes = list()
        session = get_session(self.request)
        attachments = root['attachments']
        for record in query(AttachmentRecord):
            nodes.append(fetch_node(attachments, record[0]))
        facilities = root['facilities']
        for record in query(FacilityRecord):
            nodes.append(fetch_node(facilities, record[0]))
        locations = root['locations']
        for record in query(LocationRecord):
            nodes.append(fetch_node(locations, record[0]))
        occasions = root['occasions']
        for record in query(OccasionRecord):
            nodes.append(fetch_node(occasions, record[0]))
        return nodes

    @property
    def table_title(self):
        authenticated = authenticated_userid(self.request)
        if authenticated:
            return authenticated
        return get_submitter(self.request)

    def __call__(self, model, request):
        if not authenticated_userid(request):
            if not get_submitter(request):
                raise Forbidden
        return super(SubmitterContentsTile, self).__call__(model, request)
