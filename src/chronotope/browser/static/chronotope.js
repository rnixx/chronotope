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
            position: 'topleft'
        },

        initialize: function (options) {
            L.Util.extend(this.options, options);
        },

        controls_tmpl: function() {
            return $(
            '<div class="leaflet-control-location">' +
                '<div class="dropdown">' +
                    '<button class="btn dropdown-toggle" ' +
                            'type="button" ' +
                            'id="location-controls-dropdown" ' +
                            'data-toggle="dropdown">' +
                        '<span class="glyphicon glyphicon-map-marker"></span>' +
                    '</button>' +
                    '<ul class="dropdown-menu">' +
                        '<li>' +
                            '<div class="form-group has-error submitter_email">' +
                                '<label for="submitter_email">' +
                                    'Submitter' +
                                '</label>' +
                                '<input type="email" ' +
                                       'class="form-control" ' +
                                       'id="submitter_email" ' +
                                       'placeholder="Enter email address" />' +
                                '<p class="help-block">' +
                                    'Needs to be filled in order to add ' +
                                    'contents.' +
                                '</p>' +
                            '</div>' +
                        '</li>' +
                        '<li class="divider"></li>' +
                        '<li class="disabled">' +
                        '<a href="#">Add new location</a>' +
                    '</li>' +
                    '</ul>' +
                '</div>' +
            '</div>');
        },

        onAdd: function (map) {
            var controls = this.controls_tmpl();
            $('.dropdown-menu li', controls).on('click', function(evt) {
                console.log('dropdown li clicked');
                return false;
            });
            $('#submitter_email', controls).on('keyup blur', function(evt) {
                var input = $(evt.target);
                var form_group = $('.form-group', input.parents());
                var value = input.val();
                if (!email_re.test(value)) {
                    form_group.addClass('has-error');
                    return;
                }
                form_group.removeClass('has-error');
            });
            this.map = map;
            this.controls = controls.get(0);
            return this.controls;
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
                    bdajax.request({
                        success: function(data) {
                            if (!data.length) {
                                return;
                            }
                            chronotope.set_markers(data);
                            chronotope.fit_bounds();
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
            var markers = new L.FeatureGroup();
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
