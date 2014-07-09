from cone.tile import (
    tile,
    Tile,
)
from cone.app.browser.layout import ProtectedContentTile
from chronotope.model import Attachment


@tile('content', 'templates/view.pt',
      interface=Attachment, permission='view',
      strict=False)
class AttachmentView(ProtectedContentTile):
    view_tile = 'attachment'


@tile('attachment', 'templates/attachment.pt',
      interface=Attachment, permission='login',
      strict=False)
class AttachmentTile(Tile):
    pass
