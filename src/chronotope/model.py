from node.utils import instance_property
from pyramid.i18n import TranslationStringFactory
from cone.app.model import (
    BaseNode,
    Properties,
    Metadata,
)


_ = TranslationStringFactory('chronotope')


class Chronotope(BaseNode):

    @instance_property
    def properties(self):
        props = Properties()
        props.in_navtree = True
        props.icon = 'chronotope-static/images/chronotope_16_16.png'
        return props

    @instance_property
    def metadata(self):
        metadata = Metadata()
        metadata.title = _('chronotope_node', default=u'Chronotope')
        metadata.description = _('chronotope_node_description',
                                 default=u'Chronotope - Time has come today')
        return metadata
