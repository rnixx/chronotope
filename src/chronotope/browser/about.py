from chronotope.model import AboutImprint
from chronotope.model import AboutMap
from chronotope.model import AboutPrivacyPolicy
from chronotope.model import AboutProject
from chronotope.model import AboutTermsOfUse
from cone.tile import Tile
from cone.tile import tile


@tile('content', 'templates/about.pt',
      interface=AboutProject, permission='view')
class AboutProjectContent(Tile):

    @property
    def text(self):
        settings = self.model.root['settings']
        return settings['chronotope'].attrs['project_description']


@tile('content', 'templates/about.pt', interface=AboutMap, permission='view')
class AboutMapContent(Tile):

    @property
    def text(self):
        settings = self.model.root['settings']
        return settings['chronotope'].attrs['map_description']


@tile('content', 'templates/about.pt',
      interface=AboutImprint, permission='view')
class AboutImprintContent(Tile):

    @property
    def text(self):
        settings = self.model.root['settings']
        return settings['chronotope'].attrs['imprint_contact']


@tile('content', 'templates/about.pt',
      interface=AboutTermsOfUse, permission='view')
class AboutTermsOfUseContent(Tile):

    @property
    def text(self):
        settings = self.model.root['settings']
        return settings['chronotope'].attrs['terms_of_use']


@tile('content', 'templates/about.pt',
      interface=AboutPrivacyPolicy, permission='view')
class AboutPrivacyPolicyContent(Tile):

    @property
    def text(self):
        settings = self.model.root['settings']
        return settings['chronotope'].attrs['privacy_policy']
