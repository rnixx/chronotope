import uuid
from plumber import plumber
from node.utils import UNSET
from yafowil.base import ExtractionError
from pyramid.i18n import TranslationStringFactory
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
    default_attachment_type = 'text'

    def _fetch_data(self, data, name):
        return data.fetch('{0}.{1}'.format(self.form_name, name))

    @property
    def type_value(self):
        a_type = self.model.attrs['attachment_type']
        return a_type and a_type or self.default_attachment_type

    @property
    def type_vocab(self):
        return [
            ('text', _('attachment_type_text', default=u'Text')),
            ('file', _('attachment_type_file', default=u'File')),
            ('image', _('attachment_type_image', default=u'Image')),
        ]

    @property
    def text_value(self):
        a_type = self.model.attrs['attachment_type']
        if a_type == 'text':
            return self.model.attrs['payload']
        return UNSET

    @property
    def file_value(self):
        return UNSET

    @property
    def image_value(self):
        return UNSET

    def attachment_field_class(self, widget, data):
        if 'type' in data:
            a_type = self._fetch_data(data, 'type')
            if self._fetch_data(data, a_type.extracted).errors:
                return 'form-group has-error'
        return 'form-group'

    def type_required(self, widget, data):
        a_type = self._fetch_data(data, 'type')
        if not a_type.extracted:
            return data.extracted
        if a_type.extracted == widget.name and not data.extracted:
            raise ExtractionError(widget.attrs['type_required'])
        return data.extracted

    @property
    def location_value(self):
        return ['a', 'b', 'c']

    @property
    def location_vocab(self):
        return {
            'a': 'Label a',
            'b': 'Label a',
            'c': 'Label a',
        }

    @property
    def facility_value(self):
        return ['d', 'e', 'f']

    @property
    def facility_vocab(self):
        return {
            'd': 'Label d',
            'e': 'Label e',
            'f': 'Label f',
        }

    @property
    def occasion_value(self):
        return ['g', 'h', 'i']

    @property
    def occasion_vocab(self):
        return {
            'g': 'Label g',
            'h': 'Label h',
            'i': 'Label i',
        }

    def save(self, widget, data):
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        attrs = self.model.attrs
        attrs['title'] = fetch('title')
        attrs['attachment_type'] = a_type = fetch('type')
        if a_type == 'text':
            attrs['payload'] = fetch('text')
        elif a_type == 'file':
            print fetch('file')
        elif a_type == 'image':
            print fetch('image')
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
