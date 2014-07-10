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
            console.log('chronotope.binder');
        }
    }

})(jQuery);
