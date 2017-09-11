import html2text
import os
import uuid
import urllib2


UX_IDENT = '__ux'
UX_FRONTEND = 'fe'


def ensure_uuid(val):
    if not isinstance(val, uuid.UUID):
        val = uuid.UUID(val)
    return val


def get_settings_path():
    return os.environ['chronotope.settings.path']


def html_2_text(value):
    if not isinstance(value, unicode):
        value = value.decode('utf-8')
    return html2text.html2text(value)


def html_index_transform(instance, value):
    return html_2_text(value)


def get_submitter(request):
    return request.cookies.get('chronotope.submitter')


def authoring_came_from(request):
    came_from = request.params.get('authoring_came_from')
    if came_from:
        return urllib2.unquote(came_from)


def submitter_came_from(request):
    came_from = request.params.get('submitter_came_from')
    if came_from:
        return urllib2.unquote(came_from)


def get_recaptcha_public_key(model):
    return model.root['settings']['chronotope'].attrs['recaptcha_public_key']


def get_recaptcha_private_key(model):
    return model.root['settings']['chronotope'].attrs['recaptcha_private_key']
