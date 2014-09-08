import os
from pyramid.i18n import TranslationStringFactory
from cone.app.model import (
    BaseNode,
    XMLProperties,
    Metadata,
)
from cone.app.security import DEFAULT_SETTINGS_ACL
from chronotope.utils import get_settings_path


_ = TranslationStringFactory('chronotope')


SETTINGS_TMPL = """\
<properties>
  <recaptcha_public_key></recaptcha_public_key>
  <recaptcha_private_key></recaptcha_private_key>
  <project_description></project_description>
</properties>
"""


class Settings(BaseNode):
    __acl__ = DEFAULT_SETTINGS_ACL

    @property
    def attrs(self):
        settings_path = get_settings_path()
        if not os.path.exists(settings_path):
            with open(settings_path, 'w') as settings:
                settings.write(SETTINGS_TMPL)
        if not hasattr(self, '_settings') or self._settings is None:
            self._settings = XMLProperties(settings_path)
        return self._settings

    @property
    def metadata(self):
        metadata = Metadata()
        metadata.title = _('poptraces_settings',
                           default='Poptraces Settings')
        return metadata

    def __call__(self):
        self.attrs()
