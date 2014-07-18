import uuid
from plumber import (
    plumb,
    default,
    Behavior,
)
from cone.tile import (
    Tile,
    tile,
)
from cone.app.browser.utils import make_url
from chronotope.model.location import (
    locations_by_uid,
    location_title,
)
from chronotope.model.facility import facilities_by_uid
from chronotope.model.occasion import occasions_by_uid
from chronotope.model.category import (
    add_category,
    delete_category,
    category_by_name,
    category_by_uid,
    categories_by_uid,
)


###############################################################################
# general
###############################################################################

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


###############################################################################
# location references
###############################################################################

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


class LocationReferencing(Behavior):

    @default
    @property
    def location_value(self):
        value = list()
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


class FacilityReferencing(Behavior):

    @default
    @property
    def facility_value(self):
        value = list()
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


class OccasionReferencing(Behavior):

    @default
    @property
    def occasion_value(self):
        value = list()
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
