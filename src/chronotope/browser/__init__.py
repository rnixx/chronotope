from pyramid.static import static_view
from cone.tile import registerTile
from cone.app.browser.layout import ProtectedContentTile
from chronotope.model import Chronotope

static_resources = static_view('static', use_subpath=True)

registerTile('logo', 'templates/logo.pt', permission='login', strict=False)
registerTile('footer', 'templates/footer.pt', permission='login', strict=False)

registerTile('content',
             'chronotope:browser/templates/chronotope.pt',
             interface=Chronotope,
             class_=ProtectedContentTile,
             permission='login')
