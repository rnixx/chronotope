from pyramid.i18n import TranslationStringFactory
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
)
from chronotope.browser import UXMixin
from chronotope.utils import (
    UX_IDENT,
    UX_FRONTEND,
)


_ = TranslationStringFactory('chronotope')


class OverlayActions(Tile, UXMixin):

    @property
    def actions(self):
        actions = list()
        if self.is_backend:
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
            'title': _('edit_location', default=u'Edit Location'),
        }

    @property
    def add_facility(self):
        query = make_query(**{
            UX_IDENT: UX_FRONTEND,
            'factory': 'facility',
        })
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
        query = make_query(**{
            UX_IDENT: UX_FRONTEND,
            'factory': 'occasion',
        })
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
        query = make_query(**{
            UX_IDENT: UX_FRONTEND,
            'factory': 'attachment',
        })
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
            'title': _('edit_location', default=u'Edit Location'),
        }


@tile('overlay_actions', 'templates/overlay_actions.pt', interface=Facility)
class FacilityOverlayActions(OverlayActions):
    pass


@tile('overlay_actions', 'templates/overlay_actions.pt', interface=Occasion)
class OccasionOverlayActions(OverlayActions):
    pass
