from cone.tile import (
    tile,
    Tile,
)
from cone.app.browser.layout import ProtectedContentTile
from chronotope.model import Occasion


@tile('content', 'templates/view.pt',
      interface=Occasion, permission='view',
      strict=False)
class OccasionView(ProtectedContentTile):
    view_tile = 'occasion'


@tile('occasion', 'templates/occasion.pt',
      interface=Occasion, permission='login',
      strict=False)
class OccasionTile(Tile):
    pass
