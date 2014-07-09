from pyramid.i18n import TranslationStringFactory


_ = TranslationStringFactory('chronotope')


PUBLICATION_TRANSITION_NAMES = {
    'draft_2_published': _('draft_2_published', default='Publish'),
    'draft_2_declined': _('draft_2_declined', default='Decline'),
    'published_2_draft': _('published_2_draft', default='Retract'),
    'published_2_declined': _('published_2_declined', default='Decline'),
    'declined_2_draft': _('declined_2_draft', default='Retract'),
    'declined_2_published': _('declined_2_published', default='Publish'),
}
