from odict import odict
from node.utils import instance_property
from pyramid.i18n import TranslationStringFactory
from cone.app.model import (
    FactoryNode,
    Properties,
    Metadata,
)
from chronotope.model.location import (
    LocationRecord,
    Location,
    Locations,
)
from chronotope.model.facility import (
    FacilityRecord,
    Facility,
    Facilities,
)
from chronotope.model.occasion import (
    OccasionRecord,
    Occasion,
    Occasions,
)
from chronotope.model.attachment import (
    AttachmentRecord,
    Attachment,
    Attachments,
)


_ = TranslationStringFactory('chronotope')


child_factories = odict()
child_factories['locations'] = Locations
child_factories['facilities'] = Facilities
child_factories['occasions'] = Occasions
child_factories['attachments'] = Attachments


class Chronotope(FactoryNode):
    factories = child_factories

    @instance_property
    def properties(self):
        props = Properties()
        props.in_navtree = True
        props.icon = 'icon-globe'
        return props

    @instance_property
    def metadata(self):
        md = Metadata()
        md.title = _('chronotope_label', default=u'Chronotope')
        md.description = _('chronotope_description',
                           default=u'Chronotope - Time has come today')
        return md
