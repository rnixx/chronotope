import uuid
from plumber import (
    plumb,
    default,
    Behavior,
)
from pyramid.security import authenticated_userid
from cone.tile import (
    Tile,
    tile,
)
from cone.app.browser.utils import (
    make_url,
    make_query,
)
from chronotope.model.location import (
    location_by_uid,
    locations_by_uid,
    location_title,
)
from chronotope.model.facility import (
    facility_by_uid,
    facilities_by_uid,
)
from chronotope.model.occasion import (
    occasion_by_uid,
    occasions_by_uid,
)
from chronotope.model.category import (
    add_category,
    delete_category,
    category_by_name,
    category_by_uid,
    categories_by_uid,
)
from chronotope.browser import UXMixin
from chronotope.utils import (
    UX_IDENT,
    UX_FRONTEND,
)


###############################################################################
# general
###############################################################################

class References(Tile, UXMixin):
    icon = None
    reference_tile = None

    @property
    def reference_records(self):
        raise NotImplementedError(u'Anstract ``References`` does not '
                                  u'implement ``reference_records``')

    @property
    def references(self):
        ret = list()
        authenticated = bool(authenticated_userid(self.request))
        for record in self.reference_records:
            if not authenticated and record.state != 'published':
                continue
            title = self.reference_title(record)
            path = self.reference_path(record)
            if self.is_frontent:
                query = make_query(**{UX_IDENT: UX_FRONTEND})
                ref = self._make_reference(
                    title,
                    target=make_url(self.request, path=path, query=query),
                    overlay=self.reference_tile,
                    icon=self.icon,
                )
            else:
                ref = self._make_reference(
                    title,
                    target=make_url(self.request, path=path),
                    event='contextchanged:#layout',
                    icon=self.icon,
                )
            ret.append(ref)
        return ret

    def reference_path(self, record):
        raise NotImplementedError(u'Anstract ``References`` does not '
                                  u'implement ``reference_path``')

    def reference_title(self, record):
        return record.title

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


###############################################################################
# location references
###############################################################################

@tile('related_locations', 'templates/references.pt', permission='view')
class LocationReferences(References):
    icon = 'glyphicon glyphicon-map-marker'
    reference_tile = 'location'

    @property
    def reference_records(self):
        return self.model.attrs['location']

    def reference_path(self, record):
        return ['locations', str(record.uid)]

    def reference_title(self, record):
        return location_title(record.street, record.zip, record.city)


class LocationReferencing(Behavior):

    @default
    @property
    def location_value(self):
        value = list()
        preset = self.request.params.get('preset.location')
        if preset:
            value.append(preset)
        for record in self.model.attrs['location']:
            value.append(str(record.uid))
        return value

    @default
    def location_vocab(self, widget, data):
        vocab = dict()
        value = self.request.params.get(widget.dottedpath)
        if value is not None:
            value = [it for it in value.split(',') if it]
            records = locations_by_uid(self.request, value)
        else:
            records = self.model.attrs['location']
        for record in records:
            name = location_title(record.street, record.zip, record.city)
            vocab[str(record.uid)] = name
        preset = self.request.params.get('preset.location')
        if preset:
            record = location_by_uid(self.request, preset)
            name = location_title(record.street, record.zip, record.city)
            vocab[preset] = name
        return vocab

    @plumb
    def save(next_, self, widget, data):
        next_(self, widget, data)
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        # existing locations
        existing = self.location_value
        # expect a list of location uids
        locations = fetch('location')
        # remove locations
        remove_locations = list()
        for location in existing:
            if not location in locations:
                remove_locations.append(location)
        remove_locations = locations_by_uid(self.request, remove_locations)
        for location in remove_locations:
            self.model.attrs['location'].remove(location)
        # set remaining if necessary
        locations = locations_by_uid(self.request, locations)
        for location in locations:
            if not location in self.model.attrs['location']:
                self.model.attrs['location'].append(location)


###############################################################################
# facility references
###############################################################################

@tile('related_facilities', 'templates/references.pt', permission='view')
class FacilityReferences(References):
    icon = 'glyphicon glyphicon-home'
    reference_tile = 'facility'

    @property
    def reference_records(self):
        return self.model.attrs['facility']

    def reference_path(self, record):
        return ['facilities', str(record.uid)]


class FacilityReferencing(Behavior):

    @default
    @property
    def facility_value(self):
        value = list()
        preset = self.request.params.get('preset.facility')
        if preset:
            value.append(preset)
        for record in self.model.attrs['facility']:
            value.append(str(record.uid))
        return value

    @default
    def facility_vocab(self, widget, data):
        vocab = dict()
        value = self.request.params.get(widget.dottedpath)
        if value is not None:
            value = [it for it in value.split(',') if it]
            records = facilities_by_uid(self.request, value)
        else:
            records = self.model.attrs['facility']
        for record in records:
            vocab[str(record.uid)] = record.title
        preset = self.request.params.get('preset.facility')
        if preset:
            record = facility_by_uid(self.request, preset)
            vocab[preset] = record.title
        return vocab

    @plumb
    def save(next_, self, widget, data):
        next_(self, widget, data)
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        # existing facilities
        existing = self.facility_value
        # expect a list of facility uids
        facilities = fetch('facility')
        # remove facilities
        remove_facilities = list()
        for facility in existing:
            if not facility in facilities:
                remove_facilities.append(facility)
        remove_facilities = facilities_by_uid(self.request, remove_facilities)
        for facility in remove_facilities:
            self.model.attrs['facility'].remove(facility)
        # set remaining if necessary
        facilities = facilities_by_uid(self.request, facilities)
        for facility in facilities:
            if not facility in self.model.attrs['facility']:
                self.model.attrs['facility'].append(facility)


###############################################################################
# occasion references
###############################################################################

@tile('related_occasions', 'templates/references.pt', permission='view')
class OccasionReferences(References):
    icon = 'glyphicon glyphicon-star-empty'
    reference_tile = 'occasion'

    @property
    def reference_records(self):
        return self.model.attrs['occasion']

    def reference_path(self, record):
        return ['occasions', str(record.uid)]


class OccasionReferencing(Behavior):

    @default
    @property
    def occasion_value(self):
        value = list()
        preset = self.request.params.get('preset.occasion')
        if preset:
            value.append(preset)
        for record in self.model.attrs['occasion']:
            value.append(str(record.uid))
        return value

    @default
    def occasion_vocab(self, widget, data):
        vocab = dict()
        value = self.request.params.get(widget.dottedpath)
        if value is not None:
            value = [it for it in value.split(',') if it]
            records = occasions_by_uid(self.request, value)
        else:
            records = self.model.attrs['occasion']
        for record in records:
            vocab[str(record.uid)] = record.title
        preset = self.request.params.get('preset.occasion')
        if preset:
            record = occasion_by_uid(self.request, preset)
            vocab[preset] = record.title
        return vocab

    @plumb
    def save(next_, self, widget, data):
        next_(self, widget, data)
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        # existing occasion
        existing = self.occasion_value
        # expect a list of occasion uids
        occasions = fetch('occasion')
        # remove occasions
        remove_occasions = list()
        for occasion in existing:
            if not occasion in occasions:
                remove_occasions.append(occasion)
        remove_occasions = occasions_by_uid(self.request, remove_occasions)
        for occasion in remove_occasions:
            self.model.attrs['occasion'].remove(occasion)
        # set remaining if necessary
        occasions = occasions_by_uid(self.request, occasions)
        for occasion in occasions:
            if not occasion in self.model.attrs['occasion']:
                self.model.attrs['occasion'].append(occasion)


###############################################################################
# attachment references
###############################################################################

@tile('related_attachments', 'templates/references.pt', permission='view')
class AttachmentReferences(References):
    icon = 'glyphicon glyphicon-file'
    reference_tile = 'attachment'

    @property
    def reference_records(self):
        return self.model.attrs['attachment']

    def reference_path(self, record):
        return ['attachments', str(record.uid)]


###############################################################################
# category references (tagging behavior)
###############################################################################

class CategoryReferencing(Behavior):

    @default
    @property
    def category_value(self):
        value = list()
        for record in self.model.attrs['category']:
            value.append(str(record.uid))
        return value

    @default
    def category_vocab(self, widget, data):
        vocab = dict()
        value = self.request.params.get(widget.dottedpath)
        if value is not None:
            value = [it for it in value.split(',') if it]
            for category in value:
                try:
                    uid = uuid.UUID(category)
                    category = category_by_uid(self.request, uid)
                    if category:
                        vocab[str(uid)] = category.name
                except ValueError:
                    vocab[category] = category
        else:
            for record in self.model.attrs['category']:
                vocab[str(record.uid)] = record.name
        return vocab

    @plumb
    def save(next_, self, widget, data):
        next_(self, widget, data)
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        # existing categories
        existing = self.category_value
        # expect a list of category uids, newly added categories consists of
        # ``CATEGORY_NEW_MARKER`` prefix followed by the value.
        categories = fetch('category')
        # new categories
        new_categories = list()
        for category in categories:
            try:
                uuid.UUID(category)
            except ValueError:
                # try to get by name, possibly added by others in meantime
                cat = category_by_name(self.request, category)
                if not cat:
                    cat = add_category(self.request, category)
                new_categories.append(cat)
        for category in new_categories:
            self.model.attrs['category'].append(category)
        # reduce categories
        reduced = list()
        for cat in categories:
            try:
                uuid.UUID(cat)
                reduced.append(cat)
            except ValueError:
                pass
        # remove categories
        remove_categories = list()
        for category in existing:
            if not category in reduced:
                remove_categories.append(category)
        remove_categories = categories_by_uid(self.request, remove_categories)
        for category in remove_categories:
            self.model.attrs['category'].remove(category)
            # remove category entirely if not used any longer
            # XXX: need to adopt once other than facilities are categorized
            if not category.facility:
                delete_category(self.request, category)
        # set categories
        categories = categories_by_uid(self.request, reduced)
        for category in categories:
            if not category in self.model.attrs['category']:
                self.model.attrs['category'].append(category)
