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
            chronotope.attachment_form(context);
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
