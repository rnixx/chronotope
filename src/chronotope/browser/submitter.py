from chronotope.model.attachment import Attachment
from chronotope.model.attachment import AttachmentRecord
from chronotope.model.facility import Facility
from chronotope.model.facility import FacilityRecord
from chronotope.model.location import Location
from chronotope.model.location import LocationRecord
from chronotope.model.occasion import Occasion
from chronotope.model.occasion import OccasionRecord
from chronotope.utils import UX_FRONTEND
from chronotope.utils import UX_IDENT
from chronotope.utils import authoring_came_from
from chronotope.utils import get_recaptcha_private_key
from chronotope.utils import get_recaptcha_public_key
from chronotope.utils import get_submitter
from chronotope.utils import submitter_came_from
from cone.app.browser.actions import ViewLink
from cone.app.browser.ajax import AjaxOverlay
from cone.app.browser.contents import ContentsTile
from cone.app.browser.utils import make_query
from cone.app.browser.utils import make_url
from cone.sql import get_session
from cone.tile import Tile
from cone.tile import tile
from node.utils import UNSET
from node.utils import instance_property
from plumber import Behavior
from plumber import default
from plumber import plumb
from pyramid.exceptions import Forbidden
from pyramid.i18n import TranslationStringFactory
from pyramid.security import authenticated_userid
from yafowil.base import ExtractionError
from yafowil.base import factory


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

    @property
    def creator(self):
        if not authenticated_userid(self.request):
            return None
        if self.model.attrs['submitter']:
            return self.model.attrs['submitter']
        return self.model.metadata.creator

    def __call__(self, model, request):
        check_submitter_access(model, request)
        return super(SubmitterAccessTile, self).__call__(model, request)


class SubmitterForm(Behavior):

    @default
    @property
    def authenticated(self):
        return bool(authenticated_userid(self.request))

    @default
    def accept_terms_of_use(self, widget, data):
        extracted = data.extracted
        if extracted is not UNSET and not extracted:
            raise ExtractionError(
                _('accept_terms_of_use_error',
                  default='You need to accept the terms of use in order to '
                          'contribute data')
            )
        return extracted

    @plumb
    def prepare(_next, self):
        _next(self)
        self.form['submitter_came_from'] = factory(
            'proxy',
            value=submitter_came_from(self.request),
        )
        self.form['authoring_came_from'] = factory(
            'proxy',
            value=authoring_came_from(self.request),
        )
        self.form['came_from_tile'] = factory(
            'proxy',
            value=self.request.params.get('came_from_tile'),
        )
        if self.authenticated:
            return
        save_widget = self.form['controls']
        accept_terms_of_use = factory(
            'field:label:div:*accept_terms_of_use:error:help:checkbox',
            name='accept_terms_of_use',
            props={
                'label': _('accept_terms_of_use', default='Accept'),
                'help': _('accept_terms_of_use_help',
                          default='I have read the Terms of Use and agree to'),
                'label.class_add': 'col-sm-2',
                'div.class_add': 'col-sm-10',
                'error.position': 'after',
                'checkbox.class_add': 'accept_terms_of_use',
            },
            custom={
                'accept_terms_of_use': {
                    'extractors': [self.accept_terms_of_use]
                },
            },
        )
        self.form.insertbefore(accept_terms_of_use, save_widget)
        captcha_widget = factory(
            'field:label:div:error:recaptcha',
            name='captcha',
            props={
                'label': _('verify', default='Verify'),
                'public_key': get_recaptcha_public_key(self.model),
                'private_key': get_recaptcha_private_key(self.model),
                'lang': 'de',
                'theme': 'clean',
                'label.class_add': 'col-sm-2',
                'div.class_add': 'col-sm-10',
                'error.position': 'after',
            },
        )
        self.form.insertbefore(captcha_widget, save_widget)

    @plumb
    def save(_next, self, widget, data):
        if not self.authenticated:
            submitter = get_submitter(self.request)
            self.model.attrs['submitter'] = submitter
        _next(self, widget, data)

    @default
    def next(self, request):
        came_from_url = authoring_came_from(self.request)
        came_from_url += make_query(**{
            UX_IDENT: UX_FRONTEND,
            'submitter_came_from': submitter_came_from(self.request),
        })
        came_from_tile = request.get('came_from_tile')
        return [AjaxOverlay(action=came_from_tile, target=came_from_url)]


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
        query = make_query(**{
            'sort': self.request.params.get('sort'),
            'term': self.request.params.get('term'),
            'order': self.request.params.get('order'),
            'b_page': self.request.params.get('b_page'),
            'size': self.request.params.get('size'),
        })
        came_from = make_url(self.request, node=self.model.root, query=query)
        query = make_query(**{
            UX_IDENT: UX_FRONTEND,
            'submitter_came_from': came_from
        })
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

    @property
    def icon(self):
        return self.model.nodeinfo.icon


@tile('submitter_contents',
      'cone.app.browser:templates/table.pt',
      permission='view')
class SubmitterContentsTile(ContentsTile):
    default_slicesize = 10
    table_id = 'submitter_contents'
    table_tile_name = 'submitter_contents'
    col_defs = [{
            'id': 'title',
            'title': _('title', default='Title'),
            'sort_key': 'title',
            'sort_title': _('sort_on_title', default='Sort on title'),
            'content': 'structure'
        }, {
            'id': 'created',
            'title': _('created', default='Created'),
            'sort_key': 'created',
            'sort_title': _('sort_on_created', default='Sort on created'),
            'content': 'datetime'
        }, {
            'id': 'modified',
            'title': _('modified', default='Modified'),
            'sort_key': 'modified',
            'sort_title': _('sort_on_modified', default='Sort on modified'),
            'content': 'datetime'
        }, {
            'id': 'state',
            'title': _('state', default='State'),
            'sort_key': 'state',
            'sort_title': _('sort_on_state', default='Sort on state'),
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
        row_data['state'] = _(node.attrs['state'])
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
        authenticated = authenticated_userid(self.request)
        submitter = get_submitter(self.request)
        if submitter and not authenticated:
            def query(cls):
                return session.query(cls.uid)\
                              .filter(cls.submitter == submitter).all()
        else:
            creator = authenticated

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
