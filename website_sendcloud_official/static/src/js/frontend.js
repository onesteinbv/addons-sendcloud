/* Copyright 2021 Onestein (<https://www.onestein.nl>)
 * License OPL-1 (https://www.odoo.com/documentation/14.0/legal/licenses.html#odoo-apps). */

odoo.define("website_sendcloud_official.frontend", function(require) {
    "use strict";

    var core = require("web.core");
    var widget = require("web.public.widget");
    var concurrency = require("web.concurrency");
    var getUserSendcloudLanguage = require("sendcloud_delivery_official.common").getUserSendcloudLanguage;
    var Dialog = require('web.Dialog');
    var dp = new concurrency.DropPrevious();
    var _t = core._t;
    var qweb = core.qweb;

    widget.registry.websiteSaleDelivery.include({
        events: _.extend({}, widget.registry.websiteSaleDelivery.prototype.events, {
            "click #delivery_carrier .o_website_sendcloud_btn": "_onClickSendcloudButton",
            "click #delivery_carrier .o_website_sendcloud_address": "_onClickSendcloudAddress"
        }),

        xmlDependencies: ['/website_sendcloud_official/static/src/xml/frontend.xml'],

        _handleCarrierUpdateResult: function(result) {
            this._super.apply(this, arguments);

            if (!result.sendcloud_details) {
                return;
            }

            // Update view
            var $allSendcloudBtns = this.$el.find(".o_website_sendcloud_btn");
            $allSendcloudBtns.addClass("d-none");
            this.$el.find('#delivery_carrier .o_website_sendcloud_address').remove();

            // Show the selected carrier service point button
            var $carrierSelect = this.$el.find(
                _.str.sprintf("#delivery_carrier input[name='delivery_type'][value='%s']", result.carrier_id)
            ).parent();
            var $sendcloudBtn = $carrierSelect.find(".o_website_sendcloud_btn");
            if (!$sendcloudBtn.length) {
                return;
            }
            $sendcloudBtn.removeClass("d-none");
            $sendcloudBtn.data("sendcloud_details", result.sendcloud_details);

            // Update sale order
            dp.add(this._rpc({
                route: "/shop/sendcloud_update_service_point_address",
                params: {
                    order_id: result.sendcloud_details.order_id,
                    sendcloud_service_point_address: false
                }
            }));

            // Disable pay button
            var $payButton = this.$el.find("button[name='o_payment_submit_button']");
            $payButton.data('disabled_reasons', $payButton.data('disabled_reasons') || {});
            $payButton.data('disabled_reasons').carrier_selection = true;
            $payButton.prop('disabled', true);
        },

        _onClickSendcloudButton: function(ev) {
            var $btn = $(ev.target);
            var sendcloudDetails = $btn.data("sendcloud_details");

            var config = {
                apiKey: sendcloudDetails.key,
                country: sendcloudDetails.country_code,
                postalCode: sendcloudDetails.postcode,
                language: getUserSendcloudLanguage(),
                carriers: sendcloudDetails.carrier_name,
            };

            sendcloud.servicePoints.open(
                config,
                this._onServicePointSelected.bind(this, $btn),
                this._onServicePointError.bind(this)
            );
        },

        _onServicePointSelected: function($btn, servicePoint) {
            var sendcloudDetails = $btn.data("sendcloud_details");

            // Update view
            this.$el.find('#delivery_carrier .o_website_sendcloud_address').remove();
            var address = qweb.render("website_sendcloud_official.Address", {
                servicePoint: servicePoint
            });
            $btn.after(address);

            // Update sale order
            dp.add(this._rpc({
                route: "/shop/sendcloud_update_service_point_address",
                params: {
                    order_id: sendcloudDetails.order_id,
                    sendcloud_service_point_address: JSON.stringify(servicePoint),
                }
            }));

            // Enable pay button
            var $payButton = this.$el.find("button[name='o_payment_submit_button']");
            $payButton.data('disabled_reasons').carrier_selection = false;
            $payButton.prop('disabled', false);
        },

        _onServicePointError: function(errors) {
            var irrelevantErrors = ['Closed'];
            var relevantErrors = _.difference(errors, irrelevantErrors);

            if (relevantErrors.length) {
                return Dialog.alert(this, relevantErrors.join("\n"));
            }
        },

        _onClickSendcloudAddress: function(ev) {
            ev.stopPropagation();
        }
    });
});
