from plumber import (
    Behavior,
    default,
)
from pyramid.security import authenticated_userid
from pyramid.static import static_view
from pyramid.view import view_config
from pyramid.response import Response
from cone.tile import (
    Tile,
    tile,
    registerTile,
    render_tile,
)
from cone.app.browser.utils import make_url
from cone.app.browser.ajax import AjaxAction
from chronotope.utils import (
    UX_IDENT,
    UX_FRONTEND,
)


static_resources = static_view('static', use_subpath=True)


registerTile('logo', 'templates/logo.pt', permission='login', strict=False)
registerTile('footer', 'templates/footer.pt', permission='login', strict=False)
registerTile('location_controls', 'templates/location_controls.pt',
             permission='login', strict=False)


@view_config('chronotope.location_controls')
def location_controls(model, request):
    return Response(render_tile(model, request, 'location_controls'))


class UXMixin(object):

    @property
    def is_frontent(self):
        return self.request.params.get(UX_IDENT) == UX_FRONTEND

    @property
    def is_backend(self):
        return self.request.params.get(UX_IDENT) != UX_FRONTEND


@tile('chronotope', 'templates/chronotope.pt',
      permission='login', strict=False)
class MapTile(Tile):

    @property
    def authenticated(self):
        return bool(authenticated_userid(self.request))
