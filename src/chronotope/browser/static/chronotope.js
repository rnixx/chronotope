(function($) {

    $(document).ready(function() {

        // initial binding
        chronotope.binder(document);

        // add binders to bdajax binding callbacks
        $.extend(bdajax.binders, {
            chronotope_binder: chronotope.binder
        });
    });

    chronotope = {

        binder: function(context) {
            chronotope.chronotope_map(context);
            chronotope.attachment_form(context);
        },

        chronotope_map: function(context) {
            var map_elem = $('#chronotope-map', context);
            if (!map_elem.length) {
                return;
            }
            if (!map_elem.data('authenticated')) {
                map_elem.css('height', $(window).height() - 96);
                map_elem.css('margin-top', -20);
                map_elem.css('margin-left', -15);
                map_elem.css('margin-right', -15);
            } else {
                map_elem.css('height', $(window).height() - 195);
            }
            var map = new L.map('chronotope-map').setView([0, 0], 8);
            var osm = 'Map data © <a href="http://openstreetmap.org">OSM</a>';
            var tiles = new L.tileLayer(
                'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                {
                    attribution: osm,
                    minZoom: 2,
                    maxZoom: 18
                });
            tiles.addTo(map);
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
