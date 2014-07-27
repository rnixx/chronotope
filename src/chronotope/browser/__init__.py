from plumber import (
    Behavior,
    plumb,
)
from pyramid.i18n import TranslationStringFactory
from pyramid.security import authenticated_userid
from pyramid.static import static_view
from pyramid.exceptions import Forbidden
from yafowil.base import factory
from cone.tile import (
    Tile,
    tile,
    registerTile,
)
from chronotope.utils import (
    UX_IDENT,
    UX_FRONTEND,
    get_submitter,
    get_recaptcha_public_key,
    get_recaptcha_private_key,
)


_ = TranslationStringFactory('chronotope')


static_resources = static_view('static', use_subpath=True)


registerTile('logo', 'templates/logo.pt', permission='login')
registerTile('footer', 'templates/footer.pt', permission='login')


@tile('chronotope', 'templates/chronotope.pt',
      permission='view', strict=False)
class MapTile(Tile):

    @property
    def authenticated(self):
        return bool(authenticated_userid(self.request))


def check_submitter_access(model, request):
    authenticated = authenticated_userid(request)
    if not authenticated:
        submitter = get_submitter(request)
        if model.attrs['state'] != 'published':
            if not submitter:
                raise Forbidden
            if model.attrs['submitter'] != submitter:
                raise Forbidden
            if model.attrs['state'] != 'draft':
                raise Forbidden


class SubmitterAccessTile(Tile):

    def __call__(self, model, request):
        check_submitter_access(model, request)
        return super(SubmitterAccessTile, self).__call__(model, request)


class SubmitterForm(Behavior):

    @plumb
    def prepare(_next, self):
        _next(self)
        if authenticated_userid(self.request):
            return
        captcha_widget = factory(
            'field:label:div:error:recaptcha',
            name='captcha',
            props={
                'label': _('verify_human', default='Verify'),
                'public_key': get_recaptcha_public_key(),
                'private_key': get_recaptcha_private_key(),
                'lang': 'de',
                'theme': 'clean',
                'label.class_add': 'col-sm-2',
                'div.class_add': 'col-sm-10',
                'error.position': 'after',
            },
        )
        save_widget = self.form['controls']
        self.form.insertbefore(captcha_widget, save_widget)

    @plumb
    def save(_next, self, widget, data):
        authenticated = authenticated_userid(self.request)
        if not authenticated:
            submitter = get_submitter(self.request)
            self.model.attrs['submitter'] = submitter
        _next(self, widget, data)


class SubmitterAccessAddForm(SubmitterForm):

    @plumb
    def prepare(_next, self):
        authenticated = authenticated_userid(self.request)
        submitter = get_submitter(self.request)
        if not authenticated:
            if not submitter:
                raise Forbidden
        _next(self)


class SubmitterAccessEditForm(SubmitterForm):

    @plumb
    def prepare(_next, self):
        authenticated = authenticated_userid(self.request)
        submitter = get_submitter(self.request)
        if not authenticated:
            if not submitter:
                raise Forbidden
            if submitter != self.model.attrs['submitter']:
                raise Forbidden
        _next(self)


class UXMixin(object):

    @property
    def is_frontent(self):
        return self.request.params.get(UX_IDENT) == UX_FRONTEND

    @property
    def is_backend(self):
        return self.request.params.get(UX_IDENT) != UX_FRONTEND


class UXMixinProxy(Behavior):

    @plumb
    def prepare(_next, self):
        _next(self)
        self.form[UX_IDENT] = factory(
            'proxy',
            value=self.request.params.get(UX_IDENT),
        )
