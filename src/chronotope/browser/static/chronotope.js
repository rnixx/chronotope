var chronotope;

(function($, bdajax, L) {
    "use strict";

    $(document).ready(function() {
        bdajax.register(chronotope.binder.bind(chronotope), true);

        $(window).on('resize', function() {
            var map_elem = $('#chronotope-map', document);
            if (!map_elem.length) {
                return;
            }
            chronotope.resize_main_map(map_elem);
        });

        var skip_intro = 'false';
        if (typeof(Storage) !== 'undefined') {
            skip_intro = sessionStorage.getItem('skip_intro');
        }

        var hash = window.location.hash;
        if (hash) {
            skip_intro = 'true';
        }

        if (skip_intro !== 'true') {
            bdajax.overlay({
                action: 'intro',
                target: window.location.href,
                css: 'intro-overlay',
                on_close: function() {
                    chronotope.handle_perma_link();
                }
            });
            sessionStorage.setItem('skip_intro', 'true');
            return;
        }

        chronotope.handle_perma_link();
    });

    var email_re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    L.Control.LocationControl = L.Control.extend({
        options: {
            position: 'topleft',
            submitter_cookie: 'chronotope.submitter'
        },

        initialize: function (options) {
            L.Util.extend(this.options, options);
        },

        pending_action: null,

        prevent_pending: function() {
            if (this.pending_action === null) {
                return;
            }
            this.map.off('click', this.pending_action);
            this.pending_action = null;
            $(this.map.getContainer()).css('cursor', '');
        },

        onAdd: function(map) {
            this.map = map;
            var controls = $('<div class="leaflet-control-location"></div>');
            this.controls = controls;
            var that = this;
            bdajax.request({
                success: function(data) {
                    that.controls.html(data);
                    that.bind_actions();
                    if ($('.authenticated', that.controls).length) {
                        that.enable_add_location();
                        that.enable_show_submitter_contents();
                        return;
                    }
                    that.bind_submitter();
                    var submitter = that.get_submitter();
                    if (submitter) {
                        $('#submitter_email', that.controls).val(submitter);
                        that.set_submitter_state('success');
                    } else {
                        that.set_submitter_state('empty');
                    }
                },
                url: 'chronotope.location_controls'
            });
            return controls.get(0);
        },

        add_location: function() {
            var that = this;
            var map = this.map;
            this.prevent_pending();
            map.once('click', function(evt) {
                var map_container = $(map.getContainer());
                map_container.css('cursor', 'crosshair');
                var handler = function(evt) {
                    map_container.css('cursor', '');
                    var latlng = evt.latlng;
                    var zoom = map.getZoom();
                    var target =
                        '/locations/?__ux=fe' +
                        '&factory=location' +
                        '&locationform.coordinates.lat=' + latlng.lat +
                        '&locationform.coordinates.lon=' + latlng.lng +
                        '&locationform.coordinates.zoom=' + zoom;
                    bdajax.path({
                        path: '/',
                        target: target,
                        overlay: 'overlayadd'
                    });
                    bdajax.overlay({
                        action: 'overlayadd',
                        target: target,
                        on_close: chronotope.set_root_path
                    });
                };
                that.pending_action = handler;
                map.once('click', handler);
            });
        },

        set_default_center: function() {
            var that = this;
            var map = this.map;
            this.prevent_pending();
            map.once('click', function(evt) {
                var map_container = $(map.getContainer());
                map_container.css('cursor', 'crosshair');
                var handler = function(evt) {
                    map_container.css('cursor', '');
                    var center = map.getCenter();
                    chronotope.set_default_center(center);
                    var messages = chronotope.get_messages();
                    bdajax.info(
                        messages.default_center_set +
                        '<br/>&nbsp;&nbsp;&nbsp;&nbsp;' +
                        messages.longitude + ': ' + center.lng +
                        '<br/>&nbsp;&nbsp;&nbsp;&nbsp;' +
                        messages.latitude + ': ' + center.lat
                    );
                };
                that.pending_action = handler;
                map.once('click', handler);
            });
        },

        set_default_zoom: function() {
            this.prevent_pending();
            var map = this.map;
            var zoom = map.getZoom();
            chronotope.set_default_zoom(zoom);
            var messages = chronotope.get_messages();
            bdajax.info(messages.default_zoom_set);
        },

        show_submitter_contents: function(elem) {
            this.prevent_pending();
            bdajax.overlay({
                action: 'submitter_contents',
                target: elem.data('target'),
                on_close: chronotope.set_root_path
            });
        },

        dispatch_action: function(elem) {
            if (elem.hasClass('add-location-action')
                    && !elem.hasClass('disabled')) {
                this.add_location();
                return;
            }
            if (elem.hasClass('set-default-center-action')) {
                this.set_default_center();
                return;
            }
            if (elem.hasClass('set-default-zoom-action')) {
                this.set_default_zoom();
                return;
            }
            if (elem.hasClass('show-submitter-contents-action')) {
                this.show_submitter_contents(elem);
                return;
            }
            return false;
        },

        bind_actions: function() {
            var that = this;
            $('#location-controls-dropdown', this.controls).on(
                    'click', function(evt) {
                var elem = $(this);
                elem.parents('.dropdown').toggleClass('open');
                evt.preventDefault();
                evt.stopPropagation();
            });
            $('#location-controls-dropdown', this.controls).on(
                    'dblclick mousemove', function(evt) {
                evt.preventDefault();
                evt.stopPropagation();
            });
            $('.dropdown-menu', this.controls).on(
                    'click dblclick mousemove', function(evt) {
                if ($(evt.target).hasClass('dropdown-menu')) {
                    evt.preventDefault();
                    evt.stopPropagation();
                }
            });
            $('.dropdown-menu li', this.controls).on(
                    'dblclick mousemove', function(evt) {
                evt.preventDefault();
                evt.stopPropagation();
            });
            $('.dropdown-menu li', this.controls).on('click', function(evt) {
                evt.preventDefault();
                return that.dispatch_action($(this));
            });
        },

        bind_submitter: function() {
            var controls = this.controls;
            var that = this;
            $('#submitter_email', controls).on('click', function(evt) {
                $(this).focus();
            });
            $('#submitter_email', controls).on('keyup blur', function(evt) {
                var input = $(evt.target);
                var value = input.val();
                if (!value) {
                    that.set_submitter('');
                    that.set_submitter_state('empty');
                } else if (!email_re.test(value)) {
                    that.set_submitter('');
                    that.set_submitter_state('error');
                } else {
                    that.set_submitter(value);
                    that.set_submitter_state('success');
                }
            });
        },

        set_submitter_state: function(state) {
            var controls = this.controls;
            var form_group = $('.form-group', controls);
            var help_empty = $('.submitter-empty', controls);
            var help_success = $('.submitter-success', controls);
            var help_error = $('.submitter-error', controls);
            if (state == 'empty') {
                this.disable_add_location();
                this.disable_show_submitter_contents();
                help_success.hide();
                help_error.hide();
                help_empty.show();
                form_group.removeClass('has-success').removeClass('has-error');
            } else if (state == 'error') {
                this.disable_add_location();
                this.disable_show_submitter_contents();
                help_empty.hide();
                help_success.hide();
                help_error.show();
                form_group.removeClass('has-success').addClass('has-error');
            } else if (state == 'success') {
                this.enable_add_location();
                this.enable_show_submitter_contents();
                help_empty.hide();
                help_error.hide();
                help_success.show();
                form_group.addClass('has-success').removeClass('has-error');
            }
        },

        set_submitter: function(email) {
            createCookie(this.options.submitter_cookie, email);
        },

        get_submitter: function() {
            return readCookie(this.options.submitter_cookie);
        },

        enable_add_location: function() {
            $('.add-location-action', this.controls).removeClass('disabled');
        },

        disable_add_location: function() {
            $('.add-location-action', this.controls).addClass('disabled');
        },

        enable_show_submitter_contents: function() {
            $('.show-submitter-contents-action', this.controls).show();
        },

        disable_show_submitter_contents: function() {
            $('.show-submitter-contents-action', this.controls).hide();
        }
    });

    chronotope = {

        default_lon: 9.6967,
        default_lat: 52.8675,
        default_zoom: 8,
        min_zoom: 2,
        max_zoom: 18,
        map: null,
        markers: null,
        location_control: null,
        default_layer_cookie: 'chronotope.default_layer',
        default_lon_cookie: 'chronotope.default_lon',
        default_lat_cookie: 'chronotope.default_lat',
        default_zoom_cookie: 'chronotope.default_zoom',
        lang: 'de',

        messages: {
            en: {
                default_center_set: 'Default center has been set to',
                latitude: 'Latitude',
                longitude: 'Longitude',
                default_zoom_set: 'Default zoom has been set',
                search_label: 'search for address ...',
                not_found_message: 'Sorry, that address could not be found'
            },
            de: {
                default_center_set: 'Standard Zentrum gesetzt',
                latitude: 'Breitengrad',
                longitude: 'Längengrad',
                default_zoom_set: 'Standard Ansicht gesetzt',
                search_label: 'Nach Adresse suchen ...',
                not_found_message: 'Diese Adresse konnte nicht gefunden werden'
            }
        },

        get_messages: function() {
            return this.messages[this.lang];
        },

        set_default_center: function(latlon) {
            createCookie(this.default_lat_cookie, latlon.lat);
            createCookie(this.default_lon_cookie, latlon.lng);
        },

        get_default_center: function() {
            var lat = readCookie(this.default_lat_cookie);
            var lon = readCookie(this.default_lon_cookie);
            if (lat !== null && lon !== null) {
                return {
                    lat: lat,
                    lon: lon
                };
            }
            return {
                lat: this.default_lat,
                lon: this.default_lon
            };
        },

        get_default_zoom: function() {
            var zoom = readCookie(this.default_zoom_cookie);
            if (zoom !== null) {
                return zoom;
            }
            return this.default_zoom;
        },

        set_default_zoom: function(zoom) {
            createCookie(this.default_zoom_cookie, zoom);
        },

        get_default_layer_index: function() {
            var index = parseInt(readCookie(this.default_layer_cookie));
            if (!isNaN(index)) {
                return parseInt(index);
            }
            return 0;
        },

        set_default_layer_index: function(index) {
            createCookie(this.default_layer_cookie, index);
        },

        set_root_path: function(replace) {
            bdajax.path({
                path: '/',
                event: 'contextchanged:#layout',
                overlay: 'CLOSE',
                replace: replace
            });
        },

        handle_perma_link: function() {
            var hash = window.location.hash;
            if (!hash) {
                this.set_root_path(true);
                return;
            }
            var action = hash.substring(1, hash.indexOf(':'));
            var path = hash.substring(hash.indexOf(':') + 1, hash.length);
            var target = {
                url: window.location.origin + path,
                path: path,
                params: {__ux: 'fe'}
            };
            bdajax.overlay({
                action: action,
                target: target,
                on_close: this.set_root_path
            });
            bdajax.path({
                path: hash,
                overlay: action,
                target: target,
                replace: true
            });
        },

        binder: function(context) {
            chronotope.livesearch(context);
            chronotope.chronotope_map(context);
            chronotope.location_map(context);
            chronotope.location_form(context);
            chronotope.attachment_form(context);
        },

        render_livesearch_suggestion: function (datum) {
            return '<span class="' + datum.icon + '"></span> ' + datum.value;
        },

        livesearch: function(context) {
            var input = $('input#search-text');
            var from_suggestion = false;

            input.off('blur.livesearch');
            input.on('blur.livesearch', function(evt) {
                if (!input.val()) {
                    chronotope.search_in_bounds();
                }
            });

            input.off('typeahead:selected');
            input.on('typeahead:selected', function(evt, suggestion, dataset) {
                from_suggestion = true;
                bdajax.request({
                    success: function(data) {
                        chronotope.set_markers(data);
                        if (data.length) {
                            chronotope.fit_bounds();
                        }
                    },
                    url: 'chronotope.related_locations',
                    params: {
                        uid: suggestion.uid,
                        action: suggestion.action
                    },
                    type: 'json'
                });
                var path = '#' + suggestion.action + ':' + bdajax.parsepath(
                    suggestion.target
                );
                bdajax.path({
                    path: path,
                    target: suggestion.target,
                    overlay: suggestion.action
                });
                bdajax.overlay({
                    action: suggestion.action,
                    target: suggestion.target,
                    on_close: chronotope.set_root_path
                });
            });

            input.off('keyup.livesearch');
            input.on('keyup.livesearch', function(evt) {
                if (from_suggestion) {
                    from_suggestion = false;
                    return;
                }
                var key_code = evt.keyCode || evt.which;
                if (key_code == 13) {
                    input.typeahead('close');
                    evt.preventDefault();
                    if (!input.val()) {
                        chronotope.search_in_bounds();
                        return;
                    }
                    bdajax.request({
                        success: function(data) {
                            chronotope.set_markers(data);
                            if (data.length) {
                                chronotope.fit_bounds();
                            }
                        },
                        url: 'chronotope.search_locations',
                        params: {term: input.val()},
                        type: 'json'
                    });
                }
            });
        },

        create_map: function(el, options) {
            var default_center = this.get_default_center();
            var default_zoom = this.get_default_zoom();
            var lat = el.data('lat') ? el.data('lat') : default_center.lat;
            var lon = el.data('lon') ? el.data('lon') : default_center.lon;
            var zoom = el.data('zoom') ? el.data('zoom') : default_zoom;
            var map = this.map = new L.map(el.attr('id'), options);
            map.setView([lat, lon], zoom);
            return map;
        },

        resize_main_map: function(el) {
            el.css('height', $(window).height() - 96)
              .css('margin-top', -20)
              .css('margin-left', -15)
              .css('margin-right', -15);
        },

        add_geosearch_control: function(map) {
            var messages = this.get_messages();
            var geosearch_control = new L.Control.GeoSearch({
                provider: new L.GeoSearch.Provider.OpenStreetMap(),
                position: 'topleft',
                showMarker: false,
                searchLabel: messages.search_label,
                notFoundMessage: messages.not_found_message
            });
            geosearch_control.addTo(map);
            return geosearch_control;
        },

        add_zoom_control: function(map) {
            var zoom_control = new L.control.zoom();
            zoom_control.addTo(map);
            return zoom_control;
        },

        add_location_control: function(map) {
            var location_control = new L.Control.LocationControl();
            location_control.addTo(map);
            return location_control;
        },

        add_layers_control: function(map) {
            var layers = this.create_layers();
            var default_layer_index = this.get_default_layer_index();
            if (default_layer_index >= layers.length) {
                default_layer_index = 0;
            }
            var default_layer = layers[default_layer_index].layer;
            default_layer.addTo(map);
            return default_layer;
            /* XXX: later - no layers wanted right now
            var layer_mapping = {};
            for (var idx in layers) {
                var layer_defs = layers[idx];
                layer_mapping[layer_defs.title] = layer_defs.layer;
            }
            var layer_controls = L.control.layers(layer_mapping);
            layer_controls.addTo(map);
            map.on('baselayerchange', function(evt) {
                var layer_name = evt.name;
                for (var idx in layers) {
                    if (layer_name == layers[idx].title) {
                        chronotope.set_default_layer_index(idx);
                        break;
                    }
                }
            });
            return layer_controls;
            */
        },

        available_layers: [
            {
                title: 'Openstreetmap',
                tiles: '//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                attrib: 'OSM map data © <a href="http://openstreetmap.org">OSM</a>'
            }, {
                title: 'Stamen toner',
                tiles: '//{s}.tile.stamen.com/toner/{z}/{x}/{y}.png',
                attrib: 'Stamen map data © <a href="http://stamen.com">Stamen Design</a>'
            }, {
                title: 'Stamen hybrid',
                tiles: '//{s}.tile.stamen.com/toner-hybrid/{z}/{x}/{y}.png',
                attrib: 'Stamen map data © <a href="http://stamen.com">Stamen Design</a>'
            }
        ],

        create_layers: function() {
            var layers = [];
            for (var idx in this.available_layers) {
                var layer_def = this.available_layers[idx];
                var layer = new L.tileLayer(layer_def.tiles, {
                    attribution: layer_def.attrib,
                    minZoom: this.min_zoom,
                    maxZoom: this.max_zoom
                });
                layers.push({
                    title: layer_def.title,
                    layer: layer
                });
            }
            return layers;
        },

        create_markers: function(map) {
            var markers = new L.MarkerClusterGroup();
            this.markers = markers;
            map.addLayer(markers);
            return markers;
        },

        icon_url: function(datum) {
            var images_base = 'chronotope-static/images/marker-icon-';
            return images_base + datum.state + '.png';
        },

        shadow_url: 'chronotope-static/Leaflet/images/marker-shadow.png',

        set_markers: function(data) {
            chronotope.map.removeLayer(chronotope.markers);
            var markers = chronotope.create_markers(chronotope.map);
            $(data).each(function() {
                var datum = this;
                var coords = [datum.lat, datum.lon];
                var marker = new L.marker(coords, {
                    icon: L.icon({
                        iconUrl: chronotope.icon_url(datum),
                        shadowUrl: chronotope.shadow_url,
                        iconSize: [25, 41],
                        iconAnchor: [12, 41],
                        popupAnchor: [1, -34],
                        shadowSize: [41, 41]
                    })
                });
                marker.bindPopup('');
                marker.on('mouseover', function(evt) {
                    var popup = this.getPopup();
                    if (popup._isOpen) {
                        return;
                    }
                    var target = bdajax.parsetarget(datum.target);
                    bdajax.request({
                        success: function(data) {
                            popup.setContent(data);
                        },
                        url: target.url + '/chronotope.location_tooltip'
                    });
                    this.openPopup();
                });
                marker.addTo(markers);
                marker.on('click', function(evt) {
                    chronotope.location_control.prevent_pending();
                    var path = '#location:' + bdajax.parsepath(datum.target);
                    bdajax.path({
                        path: path,
                        target: datum.target,
                        overlay: datum.action
                    });
                    bdajax.overlay({
                        action: datum.action,
                        target: datum.target,
                        on_close: chronotope.set_root_path
                    });
                });
            });
            return markers;
        },

        fit_bounds: function() {
            this.map.fitBounds(this.markers.getBounds());
        },

        search_in_bounds: function() {
            var bounds = this.map.getBounds();
            bdajax.request({
                success: function(data) {
                    chronotope.set_markers(data);
                },
                url: 'chronotope.locations_in_bounds',
                params: {
                    n: bounds.getNorth(),
                    s: bounds.getSouth(),
                    w: bounds.getWest(),
                    e: bounds.getEast()
                },
                type: 'json'
            });
        },

        chronotope_map: function(context) {
            var map_elem = $('#chronotope-map', context);
            if (!map_elem.length) {
                return;
            }
            this.resize_main_map(map_elem);
            var authenticated = map_elem.data('authenticated');
            var map = this.create_map(map_elem, {
                zoomControl: false
            });
            this.add_layers_control(map);
            this.create_markers(map);
            this.add_geosearch_control(map);
            this.add_zoom_control(map);
            this.location_control = this.add_location_control(map);
            map.on('moveend', function() {
                var input = $('input#search-text');
                if (input.val()) {
                    return;
                }
                chronotope.search_in_bounds();
            });
            map_elem.on('datachanged', function(evt) {
                var input = $('input#search-text');
                if (input.val()) {
                    input.val('');
                }
                chronotope.search_in_bounds();
            });
            this.search_in_bounds();
        },

        location_map: function(context) {
            var map_elems = $('.location-view-map', context);
            $(map_elems).each(function() {
                var map_elem = $(this);
                var map = chronotope.create_map(map_elem);
                chronotope.add_layers_control(map);
                var markers = new L.FeatureGroup();
                map.addLayer(markers);
                var marker = new L.marker(
                    [map_elem.data('lat'), map_elem.data('lon')]
                );
                marker.addTo(markers);
            });
        },

        location_form: function(context) {
            var that = this;
            var map = this.map;
            var form_sel = '#form-locationform';
            var trigger_sel = form_sel + ' a.change_coordinates';
            $(trigger_sel, context).bind('click', function(evt) {
                evt.preventDefault();
                var map_container = $(map.getContainer());
                var overly = $('#ajax-overlay');
                overly.fadeOut(300);
                map_container.css('cursor', 'crosshair');
                var handler = function(evt) {
                    map_container.css('cursor', '');
                    var latlng = evt.latlng;
                    var form = $(form_sel);
                    $('#display-locationform-coordinates-lat').html(latlng.lat);
                    $('#display-locationform-coordinates-lon').html(latlng.lng);
                    $('input[name="locationform.coordinates.lat"]').val(
                        latlng.lat);
                    $('input[name="locationform.coordinates.lon"]').val(
                        latlng.lng);
                    overly.fadeIn(300);
                };
                that.location_control.pending_action = handler;
                map.once('click', handler);
            });
        },

        attachment_form: function(context) {
            var type_sel = '#input-attachmentform-type';
            var sel = $(type_sel, context);
            sel.each(function() {
                var elem = $(this);
                var wrapper = elem.parent().parent();
                var type = elem.val();
                $('.' + type + '_payload', wrapper).show();
            });
            sel.on('change', function() {
                var elem = $(this);
                var wrapper = elem.parent().parent();
                var type = elem.val();
                $('.attachment_payload', wrapper).each(function() {
                    var payload = $(this);
                    if (payload.is(':visible')) {
                        payload.fadeOut(500, function() {
                            $('.' + type + '_payload', wrapper).fadeIn(500);
                        });
                    }
                });
            });
        }
    };

    // extend livesearch options
    livesearch_options.templates = {
        suggestion: chronotope.render_livesearch_suggestion
    };

})(jQuery, bdajax, L);
