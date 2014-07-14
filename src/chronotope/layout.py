from zope.interface import implementer
from zope.component import adapter
from pyramid.security import authenticated_userid
from pyramid.threadlocal import get_current_request
from cone.app.interfaces import (
    IApplicationNode,
    ILayout,
)


@implementer(ILayout)
@adapter(IApplicationNode)
class ChronotopeLayout(object):
    mainmenu = True
    mainmenu_fluid = False
    livesearch = True
    personaltools = True
    columns_fluid = False
    pathbar = True
    sidebar_left = ['navtree']
    sidebar_left_grid_width = 3
    content_grid_width = 9

    def __init__(self, context):
        if authenticated_userid(get_current_request()):
            return
        self.mainmenu_fluid = True
        self.personaltools = False
        self.columns_fluid = True
        self.sidebar_left = []
        self.content_grid_width = 12
