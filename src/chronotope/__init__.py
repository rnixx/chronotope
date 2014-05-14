import logging
import cone.app
from sqlalchemy import engine_from_config
from cone.app.security import acl_registry
from chronotope.security import chronotope_default_acl
from chronotope.sql import initialize_sql
from chronotope.model import Chronotope
from chronotope.browser import static_resources


logger = logging.getLogger('chronotope')

# css resources
cone.app.cfg.merged.css.public.append((static_resources, 'chronotope.css'))

# js resources
cone.app.cfg.js.public.append(
    'http://cdn.tortuga.squarewave.at/osm/latest/OpenLayers.js')
cone.app.cfg.merged.js.public.append((static_resources, 'chronotope.js'))

# hide livesearch
cone.app.cfg.layout.livesearch = False

# no settings node needed
del cone.app.root.factories['settings']

# plugin entry
cone.app.register_plugin('chronotope', Chronotope)

# register ACL's for nodes
acl_registry.register(chronotope_default_acl, Chronotope)


# application startup initialization
def initialize_chronotope(config, global_config, local_config):
    # add translation
    config.add_translation_dirs('chronotope:locales/')

    # static resources
    config.add_view('chronotope.browser.static_resources',
                    name='chronotope-static')

    # scan browser package
    config.scan('chronotope.browser')

    # database initialization
    prefix = 'chronotope.dbinit.'
    if local_config.get('%surl' % prefix, None) is None:
        return
    engine = engine_from_config(local_config, prefix)
    initialize_sql(engine)

cone.app.register_main_hook(initialize_chronotope)
