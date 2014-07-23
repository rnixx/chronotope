(function($) {

    $(document).ready(function() {

        // initial binding
        chronotope.binder(document);

        // add binders to bdajax binding callbacks
        $.extend(bdajax.binders, {
            chronotope_binder: chronotope.binder
        });

        $(window).on('resize', function() {
            var map_elem = $('#chronotope-map', document);
            if (!map_elem.length) {
                return;
            }
            chronotope.resize_main_map(map_elem);
        });
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

        onAdd: function (map) {
            this.map = map;
            var controls = $('<div class="leaflet-control-location"></div>');
            this.controls = controls;
            var that = this;
            bdajax.request({
                success: function(data) {
                    that.controls.html(data);
                    that.bind_actions();
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

        bind_actions: function() {
            var that = this;
            $('.dropdown-menu li', this.controls).on('click', function(evt) {
                var elem = $(this);
                if (elem.hasClass('add-location-action')) {
                    var map = that.map;
                    map.once('click', function(evt) {
                        var map_container = $(map.getContainer());
                        map_container.css('cursor', 'crosshair');
                        map.once('click', function(evt) {
                            map_container.css('cursor', '');
                            console.log('trigger location form');
                        });
                    });
                    return;
                }
                return false;
            });
        },

        bind_submitter: function() {
            var controls = this.controls;
            var that = this;
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
                help_success.hide();
                help_error.hide();
                help_empty.show();
                form_group.removeClass('has-success').removeClass('has-error');
            } else if (state == 'error') {
                this.disable_add_location();
                help_empty.hide();
                help_success.hide();
                help_error.show();
                form_group.removeClass('has-success').addClass('has-error');
            } else if (state == 'success') {
                this.enable_add_location();
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
        }
    });

    chronotope = {

        default_lon: 10.4144,
        default_lat: 53.2525,
        default_zoom: 10,
        min_zoom: 2,
        max_zoom: 18,
        map_attrib: 'Map data © <a href="http://openstreetmap.org">OSM</a>',
        map_tiles: '//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        map: null,
        markers: null,

        binder: function(context) {
            chronotope.livesearch(context);
            chronotope.chronotope_map(context);
            chronotope.location_map(context);
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
                bdajax.overlay({
                    action: suggestion.action,
                    target: suggestion.target
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
            var lat = el.data('lat') ? el.data('lat') : this.default_lat;
            var lon = el.data('lon') ? el.data('lon') : this.default_lon;
            var zoom = el.data('zoom') ? el.data('zoom') : this.default_zoom;
            var map = new L.map(el.attr('id'), options);
            this.map = map;
            map.setView([lat, lon], zoom);
            var tiles = new L.tileLayer(this.map_tiles, {
                attribution: this.map_attrib,
                minZoom: this.min_zoom,
                maxZoom: this.max_zoom
            });
            tiles.addTo(map);
            return map;
        },

        resize_main_map: function(el) {
            el.css('height', $(window).height() - 96)
              .css('margin-top', -20)
              .css('margin-left', -15)
              .css('margin-right', -15);
        },

        add_geosearch_control: function(map) {
            var geosearch_control = new L.Control.GeoSearch({
                provider: new L.GeoSearch.Provider.OpenStreetMap(),
                position: 'topleft',
                showMarker: false
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

        create_markers: function(map) {
            var markers = new L.MarkerClusterGroup();
            this.markers = markers;
            map.addLayer(markers);
            return markers;
        },

        set_markers: function(data) {
            chronotope.map.removeLayer(chronotope.markers);
            var markers = chronotope.create_markers(chronotope.map);
            $(data).each(function() {
                var datum = this;
                var coords = [datum.lat, datum.lon];
                var marker = new L.marker(coords);
                marker.addTo(markers);
                marker.on('click', function(evt) {
                    bdajax.overlay({
                        action: datum.action,
                        target: datum.target
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
            this.create_markers(map);
            this.add_geosearch_control(map);
            this.add_zoom_control(map);
            this.add_location_control(map);
            map.on('moveend', function() {
                var input = $('input#search-text');
                if (input.val()) {
                    return;
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
                var markers = new L.FeatureGroup();
                map.addLayer(markers);
                var marker = new L.marker(
                    [map_elem.data('lat'), map_elem.data('lon')]
                );
                marker.addTo(markers);
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
    }

    // extend livesearch options
    livesearch_options.templates = {
        suggestion: chronotope.render_livesearch_suggestion
    };

})(jQuery);
