from cone.tile import (
    tile,
    Tile,
)
from chronotope.model import About


@tile('content', 'templates/about.pt', interface=About, permission='view')
class About(Tile):

    @property
    def text(self):
        settings = self.model.root['settings']
        return settings['chronotope'].attrs['project_description']
