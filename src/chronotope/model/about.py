from odict import odict
from pyramid.i18n import TranslationStringFactory
from pyramid.security import authenticated_userid
from pyramid.threadlocal import get_current_request
from cone.app.model import (
    BaseNode,
    FactoryNode,
    Metadata,
    Properties,
    Layout,
)
from chronotope.security import chronotope_about_acl


_ = TranslationStringFactory('chronotope')


class AboutProject(BaseNode):
    __acl__ = chronotope_about_acl

    @property
    def properties(self):
        props = Properties()
        props.icon = 'glyphicon glyphicon-info-sign'
        return props

    @property
    def metadata(self):
        md = Metadata()
        md.title = _('about_project', default='About the Project')
        return md

    @property
    def layout(self):
        return self.parent.layout


class AboutMap(BaseNode):
    __acl__ = chronotope_about_acl

    @property
    def properties(self):
        props = Properties()
        props.icon = 'glyphicon glyphicon-info-sign'
        return props

    @property
    def metadata(self):
        md = Metadata()
        md.title = _('about_map', default='About the Map')
        return md

    @property
    def layout(self):
        return self.parent.layout


class AboutTermsOfUse(BaseNode):
    __acl__ = chronotope_about_acl

    @property
    def properties(self):
        props = Properties()
        props.icon = 'glyphicon glyphicon-info-sign'
        return props

    @property
    def metadata(self):
        md = Metadata()
        md.title = _('about_terms_of_use',
                     default='Terms of use')
        return md

    @property
    def layout(self):
        return self.parent.layout


class AboutPrivacyPolicy(BaseNode):
    __acl__ = chronotope_about_acl

    @property
    def properties(self):
        props = Properties()
        props.icon = 'glyphicon glyphicon-info-sign'
        return props

    @property
    def metadata(self):
        md = Metadata()
        md.title = _('about_privacy_policy',
                     default='Privacy policy')
        return md

    @property
    def layout(self):
        return self.parent.layout


class AboutImprint(BaseNode):
    __acl__ = chronotope_about_acl

    @property
    def properties(self):
        props = Properties()
        props.icon = 'glyphicon glyphicon-info-sign'
        return props

    @property
    def metadata(self):
        md = Metadata()
        md.title = _('about_imprint', default='Imprint/Contact')
        return md

    @property
    def layout(self):
        return self.parent.layout


class About(FactoryNode):
    factories = odict()
    factories['project'] = AboutProject
    factories['map'] = AboutMap
    factories['terms_of_use'] = AboutTermsOfUse
    factories['privacy_policy'] = AboutPrivacyPolicy
    factories['imprint'] = AboutImprint

    __acl__ = chronotope_about_acl

    @property
    def properties(self):
        props = Properties()
        props.icon = 'glyphicon glyphicon-info-sign'
        props.mainmenu_display_children = True
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
        if authenticated_userid(get_current_request()):
            layout.personaltools = True
        layout.columns_fluid = False
        layout.pathbar = False
        layout.sidebar_left = []
        layout.content_grid_width = 12
        return layout
