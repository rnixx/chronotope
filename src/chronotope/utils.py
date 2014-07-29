import os
import uuid
import html2text


UX_IDENT = '__ux'
UX_FRONTEND = 'fe'

# XXX: move to cone.app

def ensure_uuid(val):
    if not isinstance(val, uuid.UUID):
        val = uuid.UUID(val)
    return val


def save_encode(val):
    if isinstance(val, unicode):
        val = val.encode('utf-8')
    return val


def save_decode(val):
    if not isinstance(val, unicode):
        val = val.decode('utf-8')
    return val

# /XXX: end move

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


def submitter_came_from(request):
    return request.params.get('submitter_came_from')


def get_recaptcha_public_key(model):
    return model.root['settings'].attrs['recaptcha_public_key']


def get_recaptcha_private_key(model):
    return model.root['settings'].attrs['recaptcha_private_key']
