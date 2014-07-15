from sqlalchemy import (
    Table,
    Column,
    String,
    DateTime,
    LargeBinary,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from node.utils import instance_property
from pyramid.i18n import TranslationStringFactory
from cone.app.model import (
    Properties,
    Metadata,
    node_info,
)
from chronotope.sql import (
    Base,
    GUID,
    SQLTableNode,
    SQLRowNode,
)
from chronotope.model import (
    LocationRecord,
    FacilityRecord,
    OccasionRecord,
)


_ = TranslationStringFactory('chronotope')


attachment_location_references = Table(
        'attachment_location_references', Base.metadata,
    Column('attachment_uid', GUID, ForeignKey('attachment.uid')),
    Column('location_uid', GUID, ForeignKey('location.uid'))
)


attachment_facility_references = Table(
        'attachment_facility_references', Base.metadata,
    Column('attachment_uid', GUID, ForeignKey('attachment.uid')),
    Column('facility_uid', GUID, ForeignKey('facility.uid'))
)


attachment_occasion_references = Table(
        'attachment_occasion_references', Base.metadata,
    Column('attachment_uid', GUID, ForeignKey('attachment.uid')),
    Column('occasion_uid', GUID, ForeignKey('occasion.uid'))
)


class AttachmentRecord(Base):
    __tablename__ = 'attachment'
    __index_attrs__ = ['title']

    uid = Column(GUID, primary_key=True)
    creator = Column(String)
    created = Column(DateTime)
    modified = Column(DateTime)
    state = Column(String)
    title = Column(String)
    attachment_type = Column(String) # 'text', 'file' or 'image'
    payload = Column(LargeBinary)

    location = relationship(
        LocationRecord,
        secondary=attachment_location_references,
        backref='attachment')
    facility = relationship(
        FacilityRecord,
        secondary=attachment_facility_references,
        backref='attachment')
    occasion = relationship(
        OccasionRecord,
        secondary=attachment_occasion_references,
        backref='attachment')


@node_info(
    name='attachment',
    title=_('attachment_label', default='Attachment'),
    description=_('attachment_description', default='An attachment'),
    icon='glyphicon glyphicon-file')
class Attachment(SQLRowNode):
    record_factory = AttachmentRecord

    @instance_property
    def properties(self):
        props = super(Attachment, self).properties
        props.action_up = True
        props.action_up_tile = 'listing'
        props.action_view = True
        props.action_edit = True
        props.action_delete = True
        return props

    @instance_property
    def metadata(self):
        md = Metadata()
        md.title = self.attrs['title']
        md.creator = self.attrs['creator']
        md.created = self.attrs['created']
        md.modified = self.attrs['modified']
        return md


@node_info(
    name='attachments',
    title=_('attachments_label', default='Attachments'),
    description=_('attachments_description',
                  default='Container for Attachments'),
    icon='glyphicon glyphicon-folder-open',
    addables=['attachment'])
class Attachments(SQLTableNode):
    record_class = AttachmentRecord
    child_factory = Attachment

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
