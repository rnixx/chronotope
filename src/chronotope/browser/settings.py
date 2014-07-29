from plumber import plumber
from pyramid.i18n import TranslationStringFactory
from cone.tile import (
    tile,
    registerTile,
)
from cone.app.browser.form import (
    Form,
    YAMLForm,
)
from cone.app.browser.settings import SettingsBehavior
from chronotope.model import Settings


_ = TranslationStringFactory('chronotope')


registerTile('content',
             'templates/settings.pt',
             interface=Settings,
             permission='manage')


@tile('editform', interface=Settings, permission='manage')
class SettingsForm(Form):
    __metaclass__ = plumber
    __plumbing__ = (
        YAMLForm,
        SettingsBehavior,
    )

    action_resource = 'edit'
    form_name = 'chronotopesettingsform'
    form_template = 'chronotope.browser:forms/settings.yaml'
    message_factory = _

    def save(self, widget, data):
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        attrs = self.model.attrs
        attrs['recaptcha_public_key'] = fetch('recaptcha_public_key')
        attrs['recaptcha_private_key'] = fetch('recaptcha_private_key')
        attrs['project_description'] = fetch('project_description')
        self.model()
