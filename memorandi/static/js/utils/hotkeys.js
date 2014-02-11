/**
 * utils/hotkeys.js
 * Keyboard hotkeys for the Memorandi App
 *
 * Copyright (C) 2014 Benjamin Bengfort
 * For license information, see LICENSE.txt
 *
 * Author:  Benjamin Bengfort <benjamin@bengfort.com>
 * Created: Tue Feb 11 11:17:49 2014 -0500
 *
 * ID: hotkeys.js [] benjamin@bengfort.com $
 */

(function($) {
    $(document).ready(function() {

        $(document).keyup(function(e) {

            if (e.keyCode == 27) {
                e.preventDefault();
                window.location = "/admin/";
            }

        });

    });
})(jQuery);
