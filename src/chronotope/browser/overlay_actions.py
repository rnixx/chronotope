from chronotope.browser.ux import UXMixin
from chronotope.model import Attachment
from chronotope.model import Facility
from chronotope.model import Location
from chronotope.model import Occasion
from chronotope.utils import UX_FRONTEND
from chronotope.utils import UX_IDENT
from chronotope.utils import get_submitter
from chronotope.utils import submitter_came_from
from cone.app.browser.utils import make_query
from cone.app.browser.utils import make_url
from cone.tile import Tile
from cone.tile import tile
from pyramid.i18n import TranslationStringFactory
from pyramid.security import authenticated_userid
import urllib2


_ = TranslationStringFactory('chronotope')


class OverlayActions(Tile, UXMixin):
    additional_adding_params = {}
    additional_editing_params = {}

    @property
    def actions(self):
        if self.is_backend:
            return False
        authenticated = bool(authenticated_userid(self.request))
        if not authenticated and not get_submitter(self.request):
            return False
        return True

    @property
    def context_actions(self):
        actions = [
            self.edit,
        ]
        actions = [action for action in actions if action]
        return actions

    @property
    def user_actions(self):
        actions = [
            self.contents,
        ]
        actions = [action for action in actions if action]
        return actions

    @property
    def authoring_actions(self):
        actions = [
            self.add_facility,
            self.add_occasion,
            self.add_attachment,
        ]
        actions = [action for action in actions if action]
        return actions

    @property
    def authoring_came_from(self):
        return urllib2.quote(make_url(self.request, node=self.model))

    @property
    def can_edit(self):
        authenticated = bool(authenticated_userid(self.request))
        if not authenticated:
            submitter = get_submitter(self.request)
            if not submitter:
                return False
            if self.model.attrs['submitter'] != submitter:
                return False
            if self.model.attrs['state'] != 'draft':
                return False
        return True

    @property
    def contents(self):
        url = submitter_came_from(self.request)
        if not url:
            query = make_query(**{UX_IDENT: UX_FRONTEND})
            url = make_url(self.request, node=self.model.root, query=query)
        else:
            url = urllib2.unquote(url)
        return {
            'btn': 'default',
            'target': url,
            'overlay': 'submitter_contents',
            'icon': 'glyphicon glyphicon-th-list',
            'title': _('my_items', default=u'My Items'),
        }

    @property
    def edit(self):
        if not self.can_edit:
            return None
        params = {
            UX_IDENT: UX_FRONTEND,
            'authoring_came_from': self.authoring_came_from,
            'submitter_came_from': submitter_came_from(self.request),
        }
        params.update(self.additional_editing_params)
        query = make_query(**params)
        url = make_url(self.request, node=self.model, query=query)
        return {
            'btn': 'default',
            'target': url,
            'overlay': 'overlayedit',
            'icon': 'glyphicon glyphicon-pencil',
            'title': _('edit', default=u'Edit'),
        }

    @property
    def add_facility(self):
        params = {
            UX_IDENT: UX_FRONTEND,
            'factory': 'facility',
            'authoring_came_from': self.authoring_came_from,
            'submitter_came_from': submitter_came_from(self.request),
        }
        params.update(self.additional_adding_params)
        query = make_query(**params)
        url = make_url(
            self.request,
            node=self.model.root['facilities'],
            query=query
        )
        return {
            'btn': 'default',
            'target': url,
            'overlay': 'overlayadd',
            'icon': 'glyphicon glyphicon-home',
            'title': _('add_facility', default=u'Add Facility'),
        }

    @property
    def add_occasion(self):
        params = {
            UX_IDENT: UX_FRONTEND,
            'factory': 'occasion',
            'authoring_came_from': self.authoring_came_from,
            'submitter_came_from': submitter_came_from(self.request),
        }
        params.update(self.additional_adding_params)
        query = make_query(**params)
        url = make_url(
            self.request,
            node=self.model.root['occasions'],
            query=query
        )
        return {
            'btn': 'default',
            'target': url,
            'overlay': 'overlayadd',
            'icon': 'glyphicon glyphicon-star-empty',
            'title': _('add_occasion', default=u'Add Occasion'),
        }

    @property
    def add_attachment(self):
        params = {
            UX_IDENT: UX_FRONTEND,
            'factory': 'attachment',
            'authoring_came_from': self.authoring_came_from,
            'submitter_came_from': submitter_came_from(self.request),
        }
        params.update(self.additional_adding_params)
        query = make_query(**params)
        url = make_url(
            self.request,
            node=self.model.root['attachments'],
            query=query
        )
        return {
            'btn': 'default',
            'target': url,
            'overlay': 'overlayadd',
            'icon': 'glyphicon glyphicon-file',
            'title': _('add_attachment', default=u'Add Attachment'),
        }


@tile('overlay_actions', 'templates/overlay_actions.pt', interface=Location)
class LocationOverlayActions(OverlayActions):

    @property
    def edit(self):
        if not self.can_edit:
            return None
        params = {
            UX_IDENT: UX_FRONTEND,
            'authoring_came_from': self.authoring_came_from,
            'submitter_came_from': submitter_came_from(self.request),
            'came_from_tile': 'location',
            'locationform.coordinates.lat': str(self.model.attrs['lat']),
            'locationform.coordinates.lon': str(self.model.attrs['lon']),
            'locationform.coordinates.zoom': str(15),
        }
        query = make_query(**params)
        url = make_url(self.request, node=self.model, query=query)
        return {
            'btn': 'default',
            'target': url,
            'overlay': 'overlayedit',
            'icon': 'glyphicon glyphicon-pencil',
            'title': _('edit', default=u'Edit'),
        }

    @property
    def additional_adding_params(self):
        return {
            'preset.location': str(self.model.attrs['uid']),
            'came_from_tile': 'location',
        }


@tile('overlay_actions', 'templates/overlay_actions.pt', interface=Facility)
class FacilityOverlayActions(OverlayActions):
    add_facility = None

    @property
    def additional_adding_params(self):
        return {
            'preset.facility': str(self.model.attrs['uid']),
            'came_from_tile': 'facility',
        }

    @property
    def additional_editing_params(self):
        return {'came_from_tile': 'facility'}


@tile('overlay_actions', 'templates/overlay_actions.pt', interface=Occasion)
class OccasionOverlayActions(OverlayActions):
    add_facility = None
    add_occasion = None

    @property
    def additional_adding_params(self):
        return {
            'preset.occasion': str(self.model.attrs['uid']),
            'came_from_tile': 'occasion',
        }

    @property
    def additional_editing_params(self):
        return {'came_from_tile': 'occasion'}


@tile('overlay_actions', 'templates/overlay_actions.pt', interface=Attachment)
class AttachmentOverlayActions(OverlayActions):
    add_facility = None
    add_occasion = None
    add_attachment = None

    @property
    def additional_adding_params(self):
        return {'came_from_tile': 'attachment'}

    @property
    def additional_editing_params(self):
        return {'came_from_tile': 'attachment'}
