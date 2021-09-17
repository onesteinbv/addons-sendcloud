/* Copyright 2021 Onestein (<https://www.onestein.nl>)
 * License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps). */

odoo.define("sendcloud_delivery_official.common", function(require) {
    var session = require('web.session');


    var availableLanguages = ["en-us", "de-de", "en-gb", "es-es", "fr-fr", "it-it", "nl-nl"];

    var getUserSendcloudLanguage = function() {
        var lang = session.user_context.lang || session.get_cookie('frontend_lang') || '';

        var langIndex = _.indexOf(
            availableLanguages,
            lang.replace('_', '-').toLowerCase()
        );

        return availableLanguages[langIndex === -1 ? 0 : langIndex];
    }

    return {
        availableLanguages: availableLanguages,
        getUserSendcloudLanguage: getUserSendcloudLanguage
    };
});
