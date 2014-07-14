from plumber import (
    Behavior,
    default,
)
from pyramid.security import authenticated_userid
from pyramid.static import static_view
from cone.tile import (
    Tile,
    tile,
    registerTile,
)
from cone.app.browser.utils import make_url
from cone.app.browser.ajax import AjaxAction


static_resources = static_view('static', use_subpath=True)


registerTile('logo', 'templates/logo.pt', permission='login', strict=False)
registerTile('footer', 'templates/footer.pt', permission='login', strict=False)


@tile('chronotope', 'templates/chronotope.pt',
      permission='login', strict=False)
class MapTile(Tile):

    @property
    def authenticated(self):
        return bool(authenticated_userid(self.request))
