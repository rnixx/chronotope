import uuid
from plumber import plumber
from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config
from cone.tile import (
    tile,
    Tile,
)
from cone.app.utils import (
    add_creation_metadata,
    update_creation_metadata,
)
from cone.app.browser.layout import ProtectedContentTile
from cone.app.browser.form import (
    Form,
    YAMLForm,
)
from cone.app.browser.authoring import (
    AddBehavior,
    EditBehavior,
)
from chronotope.model import Attachment
from chronotope.browser import AuthoringNext


_ = TranslationStringFactory('chronotope')


@tile('content', 'templates/view.pt',
      interface=Attachment, permission='view',
      strict=False)
class AttachmentView(ProtectedContentTile):
    view_tile = 'attachment'


@tile('attachment', 'templates/attachment.pt',
      interface=Attachment, permission='login',
      strict=False)
class AttachmentTile(Tile):
    pass


class AttachmentForm(object):
    __metaclass__ = plumber
    __plumbing__ = YAMLForm

    form_name = 'attachmentform'
    form_template = 'chronotope.browser:forms/attachment.yaml'
    message_factory = _

    @property
    def location_value(self):
        return ['a', 'b', 'c']

    @property
    def facility_value(self):
        return ['d', 'e', 'f']

    @property
    def occasion_value(self):
        return ['g', 'h', 'i']

    def save(self, widget, data):
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        attrs = self.model.attrs
        attrs['title'] = fetch('title')
        print fetch('location')
        print fetch('facility')
        print fetch('occasion')
        #attrs['location'] = fetch('location')
        #attrs['facility'] = fetch('facility')
        #attrs['occasion'] = fetch('occasion')


@tile('addform', interface=Attachment, permission="add")
class AttachmentAddForm(AttachmentForm, Form):
    __metaclass__ = plumber
    __plumbing__ = (
        AddBehavior,
        AuthoringNext,
    )

    def save(self, widget, data):
        attrs = self.model.attrs
        add_creation_metadata(self.request, attrs)
        super(AttachmentAddForm, self).save(widget, data)
        self.model.parent[str(uuid.uuid4())] = self.model
        self.model()


@tile('editform', interface=Attachment, permission="edit")
class AttachmentEditForm(AttachmentForm, Form):
    __metaclass__ = plumber
    __plumbing__ = (
        EditBehavior,
        AuthoringNext,
    )

    def save(self, widget, data):
        attrs = self.model.attrs
        update_creation_metadata(self.request, attrs)
        super(AttachmentEditForm, self).save(widget, data)
        self.model()
