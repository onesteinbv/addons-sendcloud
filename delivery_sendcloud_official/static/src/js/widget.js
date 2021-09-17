/* Copyright 2021 Onestein (<https://www.onestein.nl>)
 * License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps). */

odoo.define("delivery_sendcloud_official.widget", function(require) {
    "use strict";

    var AbstractField = require("web.AbstractField");
    var core = require("web.core");
    var registry = require("web.field_registry");

    var _t = core._t;

    var SendCloudCustomPriceWidget = AbstractField.extend({
        events: _.extend({}, AbstractField.prototype.events, {
            click: "_onClick",
        }),
        noLabel: true,

        /**
         * @override
         */
        isSet: function() {
            return this.value !== "unavailable";
        },

        /**
         * @override
         * @private
         */
        _render: function() {
            var className = "";
            var style = "btn fa fa-arrow-circle-right o_price_check ";
            var title = "";
            if (this.recordData.price_check === "custom") {
                className = "o_is_custom";
                title = _t("Custom price");
            } else {
                title = _t("Standard price");
            }
            var $button = $("<button/>", {
                type: "button",
                title: title,
            }).addClass(style + className);
            this.$el.html($button);
        },

        /**
         * @private
         * @param {MouseEvent} event
         */
        _onClick: function(event) {
            event.stopPropagation();
            this.trigger_up("button_clicked", {
                attrs: {
                    name: "sendcloud_custom_price_details",
                    type: "object",
                },
                record: this.record,
            });
        },
    });

    registry.add("sendcloud_price_check_widget", SendCloudCustomPriceWidget);
});
