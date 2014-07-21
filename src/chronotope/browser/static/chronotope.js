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

    chronotope = {

        default_lon: 10.4144,
        default_lat: 53.2525,
        default_zoom: 10,
        min_zoom: 2,
        max_zoom: 18,
        map_attrib: 'Map data © <a href="http://openstreetmap.org">OSM</a>',
        map_tiles: '//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',

        binder: function(context) {
            chronotope.livesearch(context);
            chronotope.chronotope_map(context);
            chronotope.location_map(context);
            chronotope.attachment_form(context);
        },

        livesearch: function(context) {
            var input = $('input#search-text');
            var from_suggestion = false;
            input.on('typeahead:selected', function(evt, suggestion, dataset) {
                from_suggestion = true;
                console.log('display suggestion from livesearch');
                console.log(suggestion);
            });
            input.on('keydown', function(evt) {
                if (from_suggestion) {
                    from_suggestion = false;
                    return;
                }
                switch (evt.keyCode || evt.which) {
                    case 13:
                        console.log('display all results from livesearch');
                        input.typeahead('close');
                        evt.preventDefault();
                }
            });
        },

        create_map: function(el) {
            var lat = el.data('lat') ? el.data('lat') : this.default_lat;
            var lon = el.data('lon') ? el.data('lon') : this.default_lon;
            var zoom = el.data('zoom') ? el.data('zoom') : this.default_zoom;
            var map = new L.map(el.attr('id')).setView([lat, lon], zoom);
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

        chronotope_map: function(context) {
            var map_elem = $('#chronotope-map', context);
            if (!map_elem.length) {
                return;
            }
            this.resize_main_map(map_elem);
            var authenticated = map_elem.data('authenticated');
            var map = this.create_map(map_elem);
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

})(jQuery);
