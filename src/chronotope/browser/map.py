from pyramid.security import authenticated_userid
from cone.tile import Tile
from cone.tile import tile


@tile('chronotope', 'templates/chronotope.pt',
      permission='view', strict=False)
class MapTile(Tile):

    @property
    def authenticated(self):
        return bool(authenticated_userid(self.request))
