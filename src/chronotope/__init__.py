import os
import logging
import cone.app
from sqlalchemy import engine_from_config
from cone.app.model import AppRoot
from cone.app.security import acl_registry
from chronotope.layout import ChronotopeLayout
from chronotope.security import (
    chronotope_root_acl,
    chronotope_container_acl,
)
from chronotope.sql import initialize_sql
from chronotope import model


logger = logging.getLogger('chronotope')

# cone.app global config
cfg = cone.app.cfg

# css resources
cfg.css.public.append('chronotope-static/Leaflet/leaflet.css')
cfg.css.public.append('chronotope-static/L.GeoSearch/l.geosearch.css')
cfg.css.public.append('chronotope-static/L.mc/MarkerCluster.css')
cfg.css.public.append('chronotope-static/L.mc/MarkerCluster.Default.css')
cfg.css.public.append('chronotope-static/chronotope.css')

# js resources
cfg.js.public.append('chronotope-static/Leaflet/leaflet-src.js')
cfg.js.public.append('chronotope-static/L.GeoSearch/l.control.geosearch.js')
cfg.js.public.append('chronotope-static/L.GeoSearch/l.geosearch.provider.openstreetmap.js')
cfg.js.public.append('chronotope-static/L.mc/leaflet.markercluster-src.js')
cfg.js.public.append('chronotope-static/chronotope.js')

# ignore yafowil.widget.location dependencies
cfg.yafowil.js_skip.add('yafowil.widget.location.dependencies')
cfg.yafowil.css_skip.add('yafowil.widget.location.dependencies')

# plugin entry nodes
cone.app.register_plugin('locations', model.Locations)
cone.app.register_plugin('facilities', model.Facilities)
cone.app.register_plugin('occasions', model.Occasions)
cone.app.register_plugin('attachments', model.Attachments)

# plugin settings
cone.app.register_plugin_config('chronotope', model.Settings)

# register ACL's for nodes
if not os.environ.get('TESTRUN_MARKER'):
    acl_registry.register(chronotope_root_acl, AppRoot)
acl_registry.register(chronotope_container_acl, model.Locations, 'locations')
acl_registry.register(chronotope_container_acl, model.Facilities, 'facilities')
acl_registry.register(chronotope_container_acl, model.Occasions, 'occasions')
acl_registry.register(chronotope_container_acl, model.Attachments, 'attachments')


# application startup initialization
def initialize_chronotope(config, global_config, local_config):
    # chronotope layout adapter
    config.registry.registerAdapter(ChronotopeLayout)

    # add translation
    config.add_translation_dirs('chronotope:locales/')

    # static resources
    config.add_view('chronotope.browser.static_resources',
                    name='chronotope-static')

    # scan browser package
    config.scan('chronotope.browser')

    # chronotope livesearch adapter
    from chronotope.browser.search import LiveSearch
    config.registry.registerAdapter(LiveSearch)

    # index directory
    os.environ['chronotope.index.dir'] = local_config['chronotope.index.dir']

    # settings path
    os.environ['chronotope.settings.path'] = \
        local_config['chronotope.settings.path']

    # database initialization
    prefix = 'chronotope.dbinit.'
    if local_config.get('%surl' % prefix, None) is None:
        return
    engine = engine_from_config(local_config, prefix)
    initialize_sql(engine)

cone.app.register_main_hook(initialize_chronotope)
