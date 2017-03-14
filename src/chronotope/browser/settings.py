from chronotope.model import Settings
from cone.app.browser.form import Form
from cone.app.browser.form import YAMLForm
from cone.app.browser.settings import SettingsBehavior
from cone.tile import registerTile
from cone.tile import tile
from plumber import plumbing
from pyramid.i18n import TranslationStringFactory


_ = TranslationStringFactory('chronotope')


registerTile('content',
             'templates/settings.pt',
             interface=Settings,
             permission='manage')


@tile('editform', interface=Settings, permission='manage')
@plumbing(YAMLForm, SettingsBehavior)
class SettingsForm(Form):
    action_resource = 'edit'
    form_name = 'chronotopesettingsform'
    form_template = 'chronotope.browser:forms/settings.yaml'

    @property
    def message_factory(self):
        return _

    def save(self, widget, data):
        def fetch(name):
            return data.fetch('{0}.{1}'.format(self.form_name, name)).extracted
        attrs = self.model.attrs
        attrs['recaptcha_public_key'] = fetch('recaptcha_public_key')
        attrs['recaptcha_private_key'] = fetch('recaptcha_private_key')
        attrs['project_description'] = fetch('project_description')
        attrs['map_description'] = fetch('map_description')
        attrs['imprint_contact'] = fetch('imprint_contact')
        attrs['terms_of_use'] = fetch('terms_of_use')
        attrs['privacy_policy'] = fetch('privacy_policy')
        self.model()
