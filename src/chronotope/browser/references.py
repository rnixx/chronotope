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
from chronotope.browser.ux import UXMixin
from chronotope.utils import (
    UX_IDENT,
    UX_FRONTEND,
    get_submitter,
)


###############################################################################
# general
###############################################################################

def json_references(model, request, search_references, limit,
                    extract_title=None):
    term = request.params['q']
    # authenticated gets all
    authenticated = bool(authenticated_userid(request))
    if authenticated:
        records = search_references(request, term, limit=limit)
    # anonymous gets published
    else:
        records = search_references(
            request, term, state=['published'], limit=limit)
        # additionally add by submitter
        submitter = get_submitter(request)
        if submitter:
            records += search_references(
                request, term, state=['draft'],
                submitter=submitter, limit=limit)
    # create and return result
    result = list()
    for record in records:
        if extract_title is not None:
            name = extract_title(record)
        else:
            name = record.title
        result.append({
            'id': str(record.uid),
            'text': name,
        })
    return sorted(result, key=lambda x: x['text'])


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
        submitter = get_submitter(self.request)
        for record in self.reference_records:
            # check ignoring not authenticated
            if not authenticated and record.state != 'published':
                # no submitter, continue
                if not submitter:
                    continue
                # wrong submitter, continue
                if record.submitter != submitter:
                    continue
                # wrong state, continue
                if record.state != 'draft':
                    continue
            # ref title and path
            title = self.reference_title(record)
            path = self.reference_path(record)
            # case rendered in frontend
            if self.is_frontent:
                query = make_query(**{UX_IDENT: UX_FRONTEND})
                ref = self._make_reference(
                    title,
                    target=make_url(self.request, path=path, query=query),
                    overlay=self.reference_tile,
                    icon=self.icon,
                )
            # case rendered in backend
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


class Referencing(Behavior):

    @default
    def references_value(self, name):
        value = list()
        preset = self.request.params.get('preset.{0}'.format(name))
        if preset:
            value.append(preset)
        for record in self.model.attrs[name]:
            value.append(str(record.uid))
        return value

    @default
    def references_vocab(self, widget, data, name,
                         references_by_uid, reference_by_uid,
                         extract_title=None):
        vocab = dict()
        value = self.request.params.get(widget.dottedpath)
        if value is not None:
            value = [it for it in value.split(',') if it]
            records = references_by_uid(self.request, value)
        else:
            records = self.model.attrs[name]
        for record in records:
            if extract_title is not None:
                vocab[str(record.uid)] = extract_title(record)
            else:
                vocab[str(record.uid)] = record.title
        preset = self.request.params.get('preset.{0}'.format(name))
        if preset:
            record = reference_by_uid(self.request, preset)
            if extract_title is not None:
                vocab[preset] = extract_title(record)
            else:
                vocab[preset] = record.title
        return vocab

    @default
    def references_save(self, widget, data, name, references_by_uid):
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        # existing references
        existing = self.references_value(name)
        # expect a list of reference uids
        references = fetch(name)
        # remove references
        remove_references = list()
        for reference in existing:
            if not reference in references:
                remove_references.append(reference)
        remove_references = references_by_uid(self.request, remove_references)
        for reference in remove_references:
            self.model.attrs[name].remove(reference)
        # set remaining if necessary
        references = references_by_uid(self.request, references)
        for reference in references:
            if not reference in self.model.attrs[name]:
                self.model.attrs[name].append(reference)


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


class LocationReferencing(Referencing):

    @default
    @property
    def location_value(self):
        return self.references_value('location')

    @default
    def location_vocab(self, widget, data):
        def extract_title(record):
            return location_title(record.street, record.zip, record.city)
        return self.references_vocab(
            widget, data, 'location', locations_by_uid, location_by_uid,
            extract_title=extract_title)

    @plumb
    def save(next_, self, widget, data):
        next_(self, widget, data)
        self.references_save(widget, data, 'location', locations_by_uid)


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


class FacilityReferencing(Referencing):

    @default
    @property
    def facility_value(self):
        return self.references_value('facility')

    @default
    def facility_vocab(self, widget, data):
        return self.references_vocab(
            widget, data, 'facility', facilities_by_uid, facility_by_uid)

    @plumb
    def save(next_, self, widget, data):
        next_(self, widget, data)
        self.references_save(widget, data, 'facility', facilities_by_uid)


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


class OccasionReferencing(Referencing):

    @default
    @property
    def occasion_value(self):
        return self.references_value('occasion')

    @default
    def occasion_vocab(self, widget, data):
        return self.references_vocab(
            widget, data, 'occasion', occasions_by_uid, occasion_by_uid)

    @plumb
    def save(next_, self, widget, data):
        next_(self, widget, data)
        self.references_save(widget, data, 'occasion', occasions_by_uid)


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
