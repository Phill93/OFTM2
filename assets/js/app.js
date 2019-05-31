import 'material-design-lite';
import 'getmdl-select/src/js/getmdl-select';
import 'expose-loader?$!jquery';
import 'expose-loader?jQuery!jquery';

jQuery(document).ready(function($) {
    $('.clickable-row').click(function() {
        window.location = $(this).data('href');
    });
});