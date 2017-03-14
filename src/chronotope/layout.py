from cone.app.interfaces import IApplicationNode
from cone.app.interfaces import ILayout
from cone.app.model import AppRoot
from pyramid.security import authenticated_userid
from pyramid.threadlocal import get_current_request
from zope.component import adapter
from zope.interface import implementer


@implementer(ILayout)
@adapter(IApplicationNode)
class ChronotopeLayout(object):
    mainmenu = True
    mainmenu_fluid = False
    livesearch = True
    personaltools = True
    columns_fluid = False
    pathbar = True
    sidebar_left = []
    content_grid_width = 12

    def __init__(self, context):
        request = get_current_request()
        if not isinstance(context, AppRoot):
            self.livesearch = False
            if authenticated_userid(request):
                return
        if not authenticated_userid(request):
            self.personaltools = False
        self.columns_fluid = True
        self.pathbar = False
