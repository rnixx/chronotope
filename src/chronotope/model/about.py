from pyramid.i18n import TranslationStringFactory
from cone.app.model import (
    BaseNode,
    Metadata,
    Properties,
    Layout,
)
from chronotope.security import chronotope_about_acl


_ = TranslationStringFactory('chronotope')


class About(BaseNode):
    __acl__ = chronotope_about_acl

    @property
    def properties(self):
        props = Properties()
        props.icon = 'glyphicon glyphicon-info-sign'
        return props

    @property
    def metadata(self):
        md = Metadata()
        md.title = _('about', default='About')
        return md

    @property
    def layout(self):
        layout = Layout()
        layout.mainmenu = True
        layout.mainmenu_fluid = False
        layout.livesearch = False
        layout.personaltools = False
        layout.columns_fluid = False
        layout.pathbar = False
        layout.sidebar_left = []
        layout.content_grid_width = 12
        return layout
