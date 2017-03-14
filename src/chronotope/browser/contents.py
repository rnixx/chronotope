from chronotope.model import Attachments
from chronotope.model import Facilities
from chronotope.model import Locations
from chronotope.model import Occasions
from cone.app.browser.contents import ContentsTile
from cone.tile import tile
from pyramid.i18n import TranslationStringFactory


_ = TranslationStringFactory('chronotope')
table_template = 'cone.app.browser:templates/table.pt'


@tile('contents', table_template, interface=Locations, permission='list')
@tile('contents', table_template, interface=Facilities, permission='list')
@tile('contents', table_template, interface=Occasions, permission='list')
@tile('contents', table_template, interface=Attachments, permission='list')
class ChronotopeContentsTile(ContentsTile):
    col_defs = ContentsTile.col_defs + [{
        'id': 'state',
        'title': _('state', default='State'),
        'sort_key': 'state',
        'sort_title': _('sort_on_state', default='Sort on state'),
        'content': 'string'
    }]
    sort_keys = ContentsTile.sort_keys.copy()
    sort_keys['creator'] = lambda x: x.attrs['submitter'] \
        and x.attrs['submitter'].lower() or x.metadata.creator.lower()
    sort_keys['state'] = lambda x: x.attrs['state']

    def row_data(self, node):
        row_data = super(ChronotopeContentsTile, self).row_data(node)
        row_data['creator'] = node.attrs['submitter'] \
            and node.attrs['submitter'] or node.metadata.creator
        row_data['state'] = _(node.attrs['state'])
        return row_data
