from plumber import (
    Behavior,
    default,
)
from pyramid.static import static_view
from cone.tile import registerTile
from cone.app.browser.utils import make_url
from cone.app.browser.ajax import AjaxAction


static_resources = static_view('static', use_subpath=True)

registerTile('logo', 'templates/logo.pt', permission='login', strict=False)
registerTile('footer', 'templates/footer.pt', permission='login', strict=False)
#registerTile('chronotope', 'templates/chronotope.pt', permission='login', strict=False)
