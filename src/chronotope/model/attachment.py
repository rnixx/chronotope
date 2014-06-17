from sqlalchemy import (
    Table,
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from node.utils import instance_property
from pyramid.i18n import TranslationStringFactory
from cone.app.model import (
    BaseNode,
    Properties,
    Metadata,
    NodeInfo,
    registerNodeInfo,
)
from ..sql import (
    Base,
    SQLRowNodeAttributes,
    SQLRowNode,
)


_ = TranslationStringFactory('chronotope')


attachment_location_references = Table(
        'attachment_location_references', Base.metadata,
    Column('attachment_id', Integer, ForeignKey('attachment.id')),
    Column('location_id', Integer, ForeignKey('location.id'))
)


attachment_facility_references = Table(
        'attachment_facility_references', Base.metadata,
    Column('attachment_id', Integer, ForeignKey('attachment.id')),
    Column('facility_id', Integer, ForeignKey('facility.id'))
)


class AttachmentRecord(Base):
    __tablename__ = 'attachment'
    id = Column(Integer, primary_key=True)
    uid = Column(String)
    creator = Column(String)
    created = Column(DateTime)
    modified = Column(DateTime)
    title = Column(String)
    attachment_type = Column(String)
    #payload = Column()
    location = relationship(
        "Location",
        secondary=attachment_location_references,
        backref="parents")
    facility = relationship(
        "Facility",
        secondary=attachment_facility_references,
        backref="parents")


class AttachmentAttributes(SQLRowNodeAttributes):
    _keys = ['id', 'uid', 'creator', 'created', 'modified', 'title',
             'attachment_type', 'payload', 'location', 'facility']


class Attachment(SQLRowNode):
    node_info_name = 'attachment'

    def record_factory(self):
        return AttachmentRecord()

    def attributes_factory(self, name, parent):
        return AttachmentAttributes(name, parent, self.record)

    @instance_property
    def properties(self):
        props = Properties()
        props.action_up = True
        props.action_view = True
        props.action_delete = True
        return props

    @instance_property
    def metadata(self):
        md = Metadata()
        md.title = _('attachment_label', default='Attachment')
        md.description = _('attachment_description', default='An Attachment')
        return md


info = NodeInfo()
info.title = _('attachment_label', default='Attachment')
info.description = _('attachment_description', default='An attachment')
info.node = Attachment
info.addables = []
info.icon = 'icon-file'
registerNodeInfo('attachment', info)


class Attachments(BaseNode):
    node_info_name = 'attachments'

    @instance_property
    def properties(self):
        props = Properties()
        props.in_navtree = True
        props.action_up = True
        props.action_up_tile = 'content'
        props.action_add = True
        props.default_content_tile = 'listing'
        return props

    @instance_property
    def metadata(self):
        md = Metadata()
        md.title = _('attachments_label', default='Attachments')
        md.description = \
            _('attachments_description', default='Container for Attachments')
        return md

    def __getitem__(self, name):
        # traversal expects KeyError before looking up views.
        raise KeyError(name)

    def __delitem__(self, name):
        pass


info = NodeInfo()
info.title = _('attachments_label', default='Attachments')
info.description = \
    _('attachments_description', default='Container for Attachments')
info.node = Attachments
info.addables = ['attachment']
info.icon = 'icon-folder-open'
registerNodeInfo('attachments', info)