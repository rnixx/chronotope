from pyramid.i18n import TranslationStringFactory
from pyramid.security import authenticated_userid
from cone.tile import (
    tile,
    Tile,
)
from cone.app.browser.utils import (
    make_url,
    make_query,
)
from chronotope.model import (
    Location,
    Facility,
    Occasion,
    Attachment,
)
from chronotope.browser.ux import UXMixin
from chronotope.utils import (
    UX_IDENT,
    UX_FRONTEND,
    get_submitter,
)


_ = TranslationStringFactory('chronotope')


class OverlayActions(Tile, UXMixin):
    additional_adding_params = {}

    @property
    def actions(self):
        actions = list()
        if self.is_backend:
            return actions
        authenticated = bool(authenticated_userid(self.request))
        if not authenticated and not get_submitter(self.request):
            return actions
        actions = [
            self.edit,
            self.add_facility,
            self.add_occasion,
            self.add_attachment,
        ]
        actions = [action for action in actions if action]
        return actions

    @property
    def edit(self):
        query = make_query(**{UX_IDENT: UX_FRONTEND})
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
        query = make_query(**{
            UX_IDENT: UX_FRONTEND,
            'locationform.coordinates.lat': str(self.model.attrs['lat']),
            'locationform.coordinates.lon': str(self.model.attrs['lon']),
            'locationform.coordinates.zoom': str(15),
        })
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
        return {'preset.location': str(self.model.attrs['uid'])}


@tile('overlay_actions', 'templates/overlay_actions.pt', interface=Facility)
class FacilityOverlayActions(OverlayActions):
    add_facility = None

    @property
    def additional_adding_params(self):
        return {'preset.facility': str(self.model.attrs['uid'])}


@tile('overlay_actions', 'templates/overlay_actions.pt', interface=Occasion)
class OccasionOverlayActions(OverlayActions):
    add_facility = None
    add_occasion = None

    @property
    def additional_adding_params(self):
        return {'preset.occasion': str(self.model.attrs['uid'])}


@tile('overlay_actions', 'templates/overlay_actions.pt', interface=Attachment)
class AttachmentOverlayActions(OverlayActions):
    add_facility = None
    add_occasion = None
    add_attachment = None
