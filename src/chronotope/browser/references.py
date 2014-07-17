from cone.tile import (
    Tile,
    tile,
)
from cone.app.browser.utils import make_url
from chronotope.model.location import location_title


class References(Tile):

    @property
    def references(self):
        raise NotImplementedError(u'Abstract references tile does not '
                                  u'implement ``references``')

    def _make_reference(self, title, bind='click', target=None,
                        action=None, event=None, overlay=None, icon=''):
        return {
            'title': title,
            'bind': bind,
            'target': target,
            'action': action,
            'event': event,
            'overlay': overlay,
            'icon': icon,
        }


@tile('related_locations', 'templates/references.pt', permission='view')
class LocationReferences(References):

    @property
    def references(self):
        locations = self.model.attrs['location']
        ret = list()
        for loc in locations:
            title = location_title(loc.street, loc.zip, loc.city)
            target = make_url(self.request, path=['locations', str(loc.uid)])
            ref = self._make_reference(title,
                                       target=target,
                                       event='contextchanged:#layout',
                                       icon='glyphicon glyphicon-map-marker')
            ret.append(ref)
        return ret


@tile('related_facilities', 'templates/references.pt', permission='view')
class FacilityReferences(References):

    @property
    def references(self):
        facilities = self.model.attrs['facility']
        ret = list()
        for fac in facilities:
            target = make_url(self.request, path=['facilities', str(fac.uid)])
            ref = self._make_reference(fac.title,
                                       target=target,
                                       event='contextchanged:#layout',
                                       icon='glyphicon glyphicon-home')
            ret.append(ref)
        return ret


@tile('related_occasions', 'templates/references.pt', permission='view')
class OccasionReferences(References):

    @property
    def references(self):
        ossacions = self.model.attrs['occasion']
        ret = list()
        for occ in ossacions:
            target = make_url(self.request, path=['occasions', str(occ.uid)])
            ref = self._make_reference(occ.title,
                                       target=target,
                                       event='contextchanged:#layout',
                                       icon='glyphicon glyphicon-star-empty')
            ret.append(ref)
        return ret


@tile('related_attachments', 'templates/references.pt', permission='view')
class AttachmentReferences(References):

    @property
    def references(self):
        attachments = self.model.attrs['attachment']
        ret = list()
        for att in attachments:
            target = make_url(self.request, path=['attachments', str(att.uid)])
            ref = self._make_reference(att.title,
                                       target=target,
                                       event='contextchanged:#layout',
                                       icon='glyphicon glyphicon-file')
            ret.append(ref)
        return ret
