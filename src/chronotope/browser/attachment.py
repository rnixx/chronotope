import uuid
import pickle
from StringIO import StringIO
from plumber import plumber
from node.utils import UNSET
from yafowil.base import ExtractionError
from pyramid.i18n import TranslationStringFactory
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import authenticated_userid
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
from cone.app.browser.utils import (
    make_url,
    make_query,
)
from chronotope.model import Attachment
from chronotope.utils import html_2_text
from chronotope.browser.references import (
    LocationReferencing,
    FacilityReferencing,
    OccasionReferencing,
)


_ = TranslationStringFactory('chronotope')


@view_config('download', context=Attachment)
def download(model, request):
    # XXX: permission checks
    a_type = model.attrs['attachment_type']
    payload = model.attrs['payload']
    response = Response()
    if a_type == 'text':
        response.text = html_2_text(payload)
        response.headers['Content-Type'] = 'text/plain'
        response.headers['Content-Disposition'] = \
            'attachment;filename={0}.txt'.format(model.name)
    elif a_type == 'file':
        payload = pickle.loads(payload)
        file_data = payload['file']
        file_data.seek(0)
        response.body = file_data.read()
        response.headers['Content-Type'] = payload['mimetype']
        response.headers['Content-Disposition'] = \
            'attachment;filename={0}'.format(payload['filename'])
    elif a_type == 'image':
        payload = pickle.loads(payload)
        scale = request.params.get('scale')
        filename = payload['filename']
        if scale:
            image_data = payload['scales'][scale]
            filename = '{0}_{1}.{2}'.format(
                filename[:filename.rfind('.')], scale,
                filename[filename.rfind('.') + 1:])
        else:
            image_data = payload['image']
        image_data.seek(0)
        response.body = image_data.read()
        response.headers['Content-Type'] = payload['mimetype']
        response.headers['Content-Disposition'] = \
            'attachment;filename={0}'.format(filename)
    return response


@tile('content', 'templates/view.pt',
      interface=Attachment, permission='view',
      strict=False)
class AttachmentView(ProtectedContentTile):
    view_tile = 'attachment'


@tile('attachment', 'templates/attachment.pt',
      interface=Attachment, permission='login',
      strict=False)
class AttachmentTile(Tile):

    @property
    def authenticated(self):
        return bool(authenticated_userid(self.request))

    @property
    def title(self):
        return self.model.attrs['title']

    @property
    def type(self):
        return self.model.attrs['attachment_type']

    @property
    def text(self):
        return self.type == 'text' \
            and self.model.attrs['payload'].decode('utf-8') or u''

    @property
    def fileinfo(self):
        if self.type == 'text':
            return {}
        payload = pickle.loads(self.model.attrs['payload'])
        return {
            'filename': payload['filename'],
            'mimetype': payload['mimetype'],
        }

    @property
    def preview(self):
        query = make_query(scale='preview')
        return make_url(self.request,
                        node=self.model,
                        resource='download',
                        query=query)

    @property
    def download_url(self):
        return make_url(self.request, node=self.model, resource='download')


class AttachmentForm(object):
    __metaclass__ = plumber
    __plumbing__ = (
        YAMLForm,
        LocationReferencing,
        FacilityReferencing,
        OccasionReferencing,
    )

    form_name = 'attachmentform'
    form_template = 'chronotope.browser:forms/attachment.yaml'
    message_factory = _
    default_attachment_type = 'text'

    def _fetch_data(self, data, name):
        return data.fetch('{0}.{1}'.format(self.form_name, name))

    @property
    def file_action_vocabulary(self):
        return [
            ('keep', u'Keep Existing image'),
            ('replace', u'Replace existing image'),
        ]

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
            return self.model.attrs['payload'].decode('utf-8')
        return UNSET

    @property
    def file_value(self):
        a_type = self.model.attrs['attachment_type']
        if a_type == 'file':
            # XXX: replace with exists marker
            return {'file': True}
        return UNSET

    @property
    def image_value(self):
        a_type = self.model.attrs['attachment_type']
        if a_type == 'image':
            # XXX: replace with exists marker
            #      no useless data loading then any longer
            payload = pickle.loads(self.model.attrs['payload'])
            image_file = payload['image']
            image_file.seek(0)
            return {
                'file': image_file,
                'mimetype': payload['mimetype'],
            }
        return UNSET

    @property
    def image_maxsize(self):
        return (1600, 1600)

    @property
    def image_scales(self):
        return {
            'thumb': (120, 120),
            'mini': (200, 200),
            'preview': (400, 400),
            'large': (1000, 1000),
        }

    @property
    def image_src(self):
        a_type = self.model.attrs['attachment_type']
        if a_type == 'image':
            query = make_query(scale='mini')
            return make_url(self.request,
                            node=self.model,
                            resource='download',
                            query=query)

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

    def save(self, widget, data):
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        attrs = self.model.attrs
        attrs['title'] = fetch('title')
        attrs['attachment_type'] = a_type = fetch('type')
        if a_type == 'text':
            attrs['payload'] = fetch('text').encode('utf-8')
        elif a_type == 'file':
            a_file = fetch('file')
            if a_file['action'] in ['new', 'replace']:
                payload = dict()
                payload['mimetype'] = a_file['mimetype']
                payload['filename'] = a_file['filename']
                file_data = StringIO()
                file_data.write(a_file['file'].read())
                payload['file'] = file_data
                attrs['payload'] = pickle.dumps(payload)
        elif a_type == 'image':
            image = fetch('image')
            if image['action'] in ['new', 'replace']:
                payload = dict()
                payload['mimetype'] = 'image/jpeg'
                filename = image['original'].filename
                filename = '{0}.jpg'.format(filename[:filename.rfind('.')])
                payload['filename'] = filename
                image_data = StringIO()
                image['image'].save(image_data, 'jpeg')
                payload['image'] = image_data
                scales = dict()
                for scale_name in image['scales']:
                    scale_data = StringIO()
                    image['scales'][scale_name].save(scale_data, 'jpeg')
                    scales[scale_name] = scale_data
                payload['scales'] = scales
                attrs['payload'] = pickle.dumps(payload)


@tile('addform', interface=Attachment, permission="add")
class AttachmentAddForm(AttachmentForm, Form):
    __metaclass__ = plumber
    __plumbing__ = AddBehavior

    def save(self, widget, data):
        attrs = self.model.attrs
        attrs['uid'] = uuid.uuid4()
        add_creation_metadata(self.request, attrs)
        super(AttachmentAddForm, self).save(widget, data)
        self.model.parent[str(attrs['uid'])] = self.model
        self.model()


@tile('editform', interface=Attachment, permission="edit")
class AttachmentEditForm(AttachmentForm, Form):
    __metaclass__ = plumber
    __plumbing__ = EditBehavior

    def save(self, widget, data):
        attrs = self.model.attrs
        update_creation_metadata(self.request, attrs)
        super(AttachmentEditForm, self).save(widget, data)
        self.model()
