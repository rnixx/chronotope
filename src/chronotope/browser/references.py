from chronotope.browser.ux import UXMixin
from chronotope.model.category import add_category
from chronotope.model.category import categories_by_uid
from chronotope.model.category import category_by_name
from chronotope.model.category import category_by_uid
from chronotope.model.category import delete_category
from chronotope.model.facility import facilities_by_uid
from chronotope.model.facility import facility_by_uid
from chronotope.model.location import location_by_uid
from chronotope.model.location import location_title
from chronotope.model.location import locations_by_uid
from chronotope.model.occasion import occasion_by_uid
from chronotope.model.occasion import occasions_by_uid
from chronotope.utils import UX_FRONTEND
from chronotope.utils import UX_IDENT
from chronotope.utils import get_submitter
from chronotope.utils import submitter_came_from
from cone.app.browser.batch import Batch
from cone.app.browser.utils import make_query
from cone.app.browser.utils import make_url
from cone.app.browser.utils import nodepath
from cone.tile import Tile
from cone.tile import tile
from plumber import Behavior
from plumber import default
from plumber import plumb
from pyramid.security import authenticated_userid
import uuid


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


class ReferencesSlice(object):

    def __init__(self, references_tile, model, request):
        self.references_tile = references_tile
        self.model = model
        self.request = request

    @property
    def slice(self):
        current = int(self.request.params.get('b_page', '0'))
        start = current * self.references_tile.slicesize
        end = start + self.references_tile.slicesize
        return start, end

    @property
    def references(self):
        start, end = self.slice
        return self.references_tile.references(start, end)


class ReferencesBatch(Batch):

    def __init__(self, references_tile):
        self.references_tile = references_tile
        self.name = references_tile.references_id + 'batch'

    @property
    def display(self):
        return len(self.vocab) > 1

    @property
    def vocab(self):
        ret = list()
        path = nodepath(self.model)
        count = self.references_tile.item_count
        slicesize = self.references_tile.slicesize
        pages = count / slicesize
        if count % slicesize != 0:
            pages += 1
        current = self.request.params.get('b_page', '0')
        params = {
            UX_IDENT: UX_FRONTEND,
            'submitter_came_from': submitter_came_from(self.request),
            'size': slicesize,
        }
        for i in range(pages):
            params['b_page'] = str(i)
            query = make_query(**params)
            url = make_url(self.request, path=path, query=query)
            ret.append({
                'page': '%i' % (i + 1),
                'current': current == str(i),
                'visible': True,
                'url': url,
            })
        return ret


class References(Tile, UXMixin):
    slicesize = 5
    references_id = None
    references_tile = None
    reference_tile = None
    icon = None

    @property
    def reference_records(self):
        raise NotImplementedError(u'Anstract ``References`` does not '
                                  u'implement ``reference_records``')

    @property
    def references_target(self):
        return make_url(self.request, node=self.model)

    @property
    def slice(self):
        return ReferencesSlice(self, self.model, self.request)

    @property
    def batch(self):
        return ReferencesBatch(self)(self.model, self.request)

    @property
    def item_count(self):
        return len(self.visible_references)

    @property
    def visible_references(self):
        records = list()
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
            records.append(record)
        return records

    def references(self, start, end):
        ret = list()
        for record in self.visible_references[start:end]:
            # ref title and path
            title = self.reference_title(record)
            path = self.reference_path(record)
            # case rendered in frontend
            if self.is_frontend:
                query = make_query(**{
                    UX_IDENT: UX_FRONTEND,
                    'submitter_came_from': submitter_came_from(self.request),
                })
                ref = self._make_reference(
                    title,
                    target=make_url(self.request, path=path, query=query),
                    overlay=self.reference_tile,
                    icon=self.icon,
                    path=self.reference_permalink(record)
                )
            # case rendered in backend
            else:
                ref = self._make_reference(
                    title,
                    target=make_url(self.request, path=path),
                    event='contextchanged:#layout',
                    icon=self.icon,
                    path='target'
                )
            ret.append(ref)
        return ret

    def reference_path(self, record):
        raise NotImplementedError(u'Anstract ``References`` does not '
                                  u'implement ``reference_path``')

    def reference_permalink(self, record):
        raise NotImplementedError(u'Anstract ``References`` does not '
                                  u'implement ``reference_permalink``')

    def reference_title(self, record):
        return record.title

    def _make_reference(self, title, bind='click', target=None,
                        action=None, event=None, overlay=None,
                        icon='', path=None):
        return {
            'title': title,
            'bind': bind,
            'target': target,
            'action': action,
            'event': event,
            'overlay': overlay,
            'icon': icon,
            'path': path
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
            if reference not in references:
                remove_references.append(reference)
        remove_references = references_by_uid(self.request, remove_references)
        for reference in remove_references:
            self.model.attrs[name].remove(reference)
        # set remaining if necessary
        references = references_by_uid(self.request, references)
        for reference in references:
            if reference not in self.model.attrs[name]:
                self.model.attrs[name].append(reference)


###############################################################################
# location references
###############################################################################

@tile('related_locations', 'templates/references.pt', permission='view')
class LocationReferences(References):
    references_id = 'relatedlocations'
    references_tile = 'related_locations'
    reference_tile = 'location'
    icon = 'glyphicon glyphicon-map-marker'

    @property
    def reference_records(self):
        return self.model.attrs['location']

    def reference_path(self, record):
        return ['locations', str(record.uid)]

    def reference_permalink(self, record):
        return '/#location:/{}'.format('/'.join(self.reference_path(record)))

    def reference_title(self, record):
        return location_title(
            self.request,
            record.street,
            record.zip,
            record.city,
            record.lat,
            record.lon)


class LocationReferencing(Referencing):

    @default
    @property
    def location_value(self):
        return self.references_value('location')

    @default
    def location_vocab(self, widget, data):
        def extract_title(record):
            return location_title(
                self.request,
                record.street,
                record.zip,
                record.city,
                record.lat,
                record.lon)
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
    references_id = 'relatedfacilities'
    references_tile = 'related_facilities'
    reference_tile = 'facility'
    icon = 'glyphicon glyphicon-home'

    @property
    def reference_records(self):
        return self.model.attrs['facility']

    def reference_path(self, record):
        return ['facilities', str(record.uid)]

    def reference_permalink(self, record):
        return '/#facility:/{}'.format('/'.join(self.reference_path(record)))


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
    references_id = 'relatedoccasions'
    references_tile = 'related_occasions'
    reference_tile = 'occasion'
    icon = 'glyphicon glyphicon-star-empty'

    @property
    def reference_records(self):
        return self.model.attrs['occasion']

    def reference_path(self, record):
        return ['occasions', str(record.uid)]

    def reference_permalink(self, record):
        return '/#occasion:/{}'.format('/'.join(self.reference_path(record)))


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
    references_id = 'relatedattachments'
    references_tile = 'related_attachments'
    reference_tile = 'attachment'
    icon = 'glyphicon glyphicon-file'

    @property
    def reference_records(self):
        return self.model.attrs['attachment']

    def reference_path(self, record):
        return ['attachments', str(record.uid)]

    def reference_permalink(self, record):
        return '/#attachment:/{}'.format('/'.join(self.reference_path(record)))


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
            if category not in reduced:
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
