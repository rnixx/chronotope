import uuid
import datetime
from plumber import plumber
from webob.exc import HTTPFound
from pyramid.security import authenticated_userid
from pyramid.i18n import TranslationStringFactory
from cone.tile import tile
from cone.app.browser.ajax import (
    AjaxAction,
)
from cone.app.browser.form import (
    Form,
    YAMLForm,
)
from cone.app.browser.authoring import (
    AddBehavior,
    EditBehavior,
)
from cone.app.browser.utils import make_url
from chronotope.model import Facility


_ = TranslationStringFactory('chronotope')


class FacilityForm(object):
    __metaclass__ = plumber
    __plumbing__ = YAMLForm

    form_template = 'chronotope.browser:forms/facility.yaml'
    message_factory = _

    @property
    def category_value(self):
        return []

    @property
    def location_value(self):
        return []

    def save(self, widget, data):
        def fetch(name):
            return data.fetch('facilityform.%s' % name).extracted
        attrs = self.model.attrs
        attrs['title'] = fetch('title')
        attrs['description'] = fetch('description')
        attrs['exists_from'] = fetch('exists_from')
        attrs['exists_to'] = fetch('exists_to')
        #attrs['category'] = fetch('category')
        #attrs['location'] = fetch('location')

    def next(self, request):
        model = self.model
        tile = 'content'
        if self.request.params.get('action.facilityform.cancel'):
            model = model.parent
        url = make_url(request.request, node=model)
        if self.ajax_request:
            return [
                AjaxAction(url, tile, 'inner', '#content'),
            ]
        return HTTPFound(location=url)


@tile('addform', interface=Facility, permission="add")
class FacilityAddForm(FacilityForm, Form):
    __metaclass__ = plumber
    __plumbing__ = AddBehavior

    def save(self, widget, data):
        attrs = self.model.attrs
        attrs['creator'] = authenticated_userid(self.request)
        attrs['created'] = datetime.datetime.now()
        attrs['modified'] = attrs['created']
        super(FacilityAddForm, self).save(widget, data)
        self.model.parent[str(uuid.uuid4())] = self.model
        self.model()


@tile('editform', interface=Facility, permission="edit")
class FacilityEditForm(FacilityForm, Form):
    __metaclass__ = plumber
    __plumbing__ = EditBehavior

    def save(self, widget, data):
        attrs = self.model.attrs
        attrs['modified'] = datetime.datetime.now()
        super(FacilityEditForm, self).save(widget, data)
        self.model()
