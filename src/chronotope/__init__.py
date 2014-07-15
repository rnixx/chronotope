import os
import logging
import cone.app
from sqlalchemy import engine_from_config
from cone.app.model import AppRoot
from cone.app.security import acl_registry
from chronotope.layout import ChronotopeLayout
from chronotope.security import (
    chronotope_root_acl,
    chronotope_content_acl,
)
from chronotope.sql import initialize_sql
from chronotope import model


logger = logging.getLogger('chronotope')

# css resources
cone.app.cfg.css.public.append('chronotope-static/chronotope.css')

# js resources
cone.app.cfg.js.public.append('chronotope-static/chronotope.js')

# plugin entry nodes
cone.app.register_plugin('locations', model.Locations)
cone.app.register_plugin('facilities', model.Facilities)
cone.app.register_plugin('occasions', model.Occasions)
cone.app.register_plugin('attachments', model.Attachments)

# register ACL's for nodes
if not os.environ.get('TESTRUN_MARKER'):
    acl_registry.register(chronotope_root_acl, AppRoot)
acl_registry.register(chronotope_content_acl, model.Locations)
acl_registry.register(chronotope_content_acl, model.Location)
acl_registry.register(chronotope_content_acl, model.Facilities)
acl_registry.register(chronotope_content_acl, model.Facility)
acl_registry.register(chronotope_content_acl, model.Occasions)
acl_registry.register(chronotope_content_acl, model.Occasion)
acl_registry.register(chronotope_content_acl, model.Attachments)
acl_registry.register(chronotope_content_acl, model.Attachment)


# application startup initialization
def initialize_chronotope(config, global_config, local_config):
    # chronotope layout adapter
    if not os.environ.get('TESTRUN_MARKER'):
        config.registry.registerAdapter(ChronotopeLayout)

    # add translation
    config.add_translation_dirs('chronotope:locales/')

    # static resources
    config.add_view('chronotope.browser.static_resources',
                    name='chronotope-static')

    # scan browser package
    config.scan('chronotope.browser')

    # index directory
    os.environ['chronotope.index.dir'] = local_config['chronotope.index.dir']

    # database initialization
    prefix = 'chronotope.dbinit.'
    if local_config.get('%surl' % prefix, None) is None:
        return
    engine = engine_from_config(local_config, prefix)
    initialize_sql(engine)

cone.app.register_main_hook(initialize_chronotope)
