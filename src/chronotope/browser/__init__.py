from pyramid.security import authenticated_userid
from pyramid.static import static_view
from cone.tile import (
    Tile,
    tile,
    registerTile,
)
from chronotope.utils import (
    UX_IDENT,
    UX_FRONTEND,
)


static_resources = static_view('static', use_subpath=True)


registerTile('logo', 'templates/logo.pt', permission='login', strict=False)
registerTile('footer', 'templates/footer.pt', permission='login', strict=False)


@tile('chronotope', 'templates/chronotope.pt',
      permission='login', strict=False)
class MapTile(Tile):

    @property
    def authenticated(self):
        return bool(authenticated_userid(self.request))


class UXMixin(object):

    @property
    def is_frontent(self):
        return self.request.params.get(UX_IDENT) == UX_FRONTEND

    @property
    def is_backend(self):
        return self.request.params.get(UX_IDENT) != UX_FRONTEND
