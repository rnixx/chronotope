from cone.app.browser.layout import MainMenu
from cone.tile import registerTile
from pyramid.static import static_view


static_resources = static_view('static', use_subpath=True)


registerTile('logo', 'templates/logo.pt', permission='login')
registerTile('footer', 'templates/footer.pt', permission='login')
registerTile('intro', 'templates/intro.pt', permission='login')
registerTile('mainmenu', 'templates/mainmenu.pt',
             class_=MainMenu, permission='view',
             strict=False)
