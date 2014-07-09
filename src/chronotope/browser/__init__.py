from pyramid.static import static_view
from cone.tile import registerTile

static_resources = static_view('static', use_subpath=True)

registerTile('logo', 'templates/logo.pt', permission='login', strict=False)
#registerTile('footer', 'templates/footer.pt', permission='login', strict=False)
