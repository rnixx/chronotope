from cone.tile import registerTile
from pyramid.static import static_view


static_resources = static_view('static', use_subpath=True)


registerTile('logo', 'templates/logo.pt', permission='login')
registerTile('footer', 'templates/footer.pt', permission='login')
