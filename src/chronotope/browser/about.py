from cone.tile import (
    tile,
    Tile,
)
from chronotope.model import (
    AboutProject,
    AboutMap,
    AboutImprint,
)


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
