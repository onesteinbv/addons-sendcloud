/* Copyright 2021 Onestein (<https://www.onestein.nl>)
 * License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps). */

odoo.define("sendcloud_delivery_official.ServicePointSelector", function(require) {
    "use strict";

    var AbstractField = require("web.AbstractField");
    var ServicesMixin = require("web.ServicesMixin");
    var Dialog = require('web.Dialog');
    var BasicModel = require('web.BasicModel');
    var core = require("web.core");
    var session = require('web.session');
    var field_registry = require("web.field_registry");
    var getUserSendcloudLanguage = require("sendcloud_delivery_official.common").getUserSendcloudLanguage;
    var qweb = core.qweb;
    var _t = core._t;

    BasicModel.include({
        _fetchSpecialSendcloudDetails: function(record, fieldName) {
            var context = record.getContext({
                fieldName: fieldName
            });

            if (typeof record.res_id === 'string') {
                return Promise.resolve();
            }

            return this._rpc({
                model: record.model,
                method: 'get_sendcloud_details',
                args: [record.res_id],
                context: context,
            });
        },
    });

    var ServicePointSelector = AbstractField.extend({

        events: {
            "click .o_delivery_sendcloud_select": "_onSelectClick",
            "click .o_delivery_sendcloud_clear": "_onClearClick",
        },

        specialData: '_fetchSpecialSendcloudDetails',

        supportedFieldTypes: ["text"],

        _getHumanReadableValue: function(value, formatted) {
            if (!value) {
                return "";
            }

            var parsedValue = JSON.parse(value);
            if (formatted) {
                return qweb.render("delivery_sendcloud_official.ServicePointAddress", {
                    servicePoint: parsedValue
                });
            }

            return [
                parsedValue.street,
                parsedValue.house_number,
                parsedValue.postal_code,
                parsedValue.city
            ].join(', ');
        },

        _renderEdit: function() {
            var renderValues = {
                widget: this,
                value: this._getHumanReadableValue(this.value, false)
            };

            if (!this.record.specialData[this.name]) {
                return this.$el.html(
                    _.str.sprintf("<i>%s</i>", _t("You've to save the record first to select a service point."))
                );
            }

            this.$el.html(
                qweb.render(
                    "delivery_sendcloud_official.ServicePointSelector",
                    renderValues
                )
            );
        },

        _renderReadonly: function() {
            this.$el.html(this._getHumanReadableValue(this.value, true));
        },

        _clearServicePoint: function() {
            return this._setValue("");
        },

        _onClearClick: function(event) {
            return this._clearServicePoint();
        },

        _selectServicePoint: function() {
            var sendcloudDetails = this.record.specialData[this.name];

            if (!sendcloudDetails) {
                return;
            }

            var config = {
                apiKey: sendcloudDetails.key,
                country: sendcloudDetails.country_code,
                postalCode: sendcloudDetails.postcode,
                language: getUserSendcloudLanguage(),
                carriers: sendcloudDetails.carrier_name,
            };

            sendcloud.servicePoints.open(
                config,
                this._onServicePointSelected.bind(this),
                this._onServicePointError.bind(this)
            );
        },

        _onServicePointError: function(errors) {
            var irrelevantErrors = ['Closed'];
            var relevantErrors = _.difference(errors, irrelevantErrors);

            if (relevantErrors.length) {
                return Dialog.alert(this, relevantErrors.join("\n"));
            }
        },

        _onServicePointSelected: function(servicePoint) {
            return this._setValue(JSON.stringify(servicePoint));
        },

        _onSelectClick: function(event) {
            return this._selectServicePoint();
        },
    });

    field_registry.add('sendcloud_service_point_selector', ServicePointSelector);

});
