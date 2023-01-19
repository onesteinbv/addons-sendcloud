/** @odoo-module */

import session from 'web.session';
import publicWidget from 'web.public.widget';
import core from 'web.core';
import { _t } from 'web.core';
import { loadJS } from "@web/core/assets";
import concurrency from 'web.concurrency';

const { onWillStart } = owl;
const Dialog = require('web.Dialog');
const QWeb = core.qweb;
const WebsiteSaleDeliverySendcloudWidget = publicWidget.registry.websiteSaleDelivery;

WebsiteSaleDeliverySendcloudWidget.include({
    events: _.extend({}, WebsiteSaleDeliverySendcloudWidget.prototype.events, {
            "click .o_website_sendcloud_btn": "_onClickSendcloudButton",
            "click .o_website_sendcloud_address": "_onClickSendcloudAddress"
    }),

    init(parent, params = {}) {
        this._super.apply(this, arguments);
        this.dp = new concurrency.DropPrevious();
        loadJS("/delivery_sendcloud_official/static/src/lib/sendcloud/api.min.js");
    },

    _handleCarrierUpdateResult: function (result) {
        const return_value = this._super(...arguments);

        // Update view
        var $allSendcloudBtns = this.$el.find(".o_website_sendcloud_btn");
        $allSendcloudBtns.addClass("d-none");
        var $allSendcloudAddr = this.$el.find(".o_website_sendcloud_address");
        $allSendcloudAddr.remove();

        // Show the selected carrier service point button
        var xpath_to_search = _.str.sprintf("input[name='delivery_type'][value='%s']", result.carrier_id);
        var $carrierSelect = this.$el.find(xpath_to_search).parent();
        var $sendcloudBtn = $carrierSelect.find("button[name='website_sendcloud_btn']");
        if (!$sendcloudBtn.length) {
            return;
        }
        $sendcloudBtn.removeClass("d-none");
        $sendcloudBtn.data("sendcloud_details", result.sendcloud_details);

        // Update sale order
        this.dp.add(this._rpc({
            route: "/shop/sendcloud_update_service_point_address",
            params: {
                order_id: result.sendcloud_details.order_id,
                sendcloud_service_point_address: false,
            }
        }));

        // Disable pay button
        var $payButton = this.$('button[name="o_payment_submit_button"]');
        $payButton.data('disabled_reasons', $payButton.data('disabled_reasons') || {});
        $payButton.data('disabled_reasons').carrier_selection = true;
        $payButton.attr('disabled', true);

        return return_value;
    },

    _onClickSendcloudButton: function(ev) {
        var $btn = $(ev.target);
        var sendcloudDetails = $btn.data("sendcloud_details");

        const availableLanguages = ["en-us", "de-de", "en-gb", "es-es", "fr-fr", "it-it", "nl-nl"];
        const lang = session.user_context.lang || session.get_cookie('frontend_lang') || "en-us";
        const langIndex = _.indexOf(availableLanguages, lang.replace('_', '-').toLowerCase());
        const selectedLanguage = availableLanguages[langIndex === -1 ? 0 : langIndex];
        const config = {
            apiKey: sendcloudDetails.key,
            country: sendcloudDetails.country_code,
            postalCode: sendcloudDetails.postcode,
            language: selectedLanguage,
            carriers: sendcloudDetails.carrier_name,
        };

        sendcloud.servicePoints.open(
            config,
            this._onServicePointSelected.bind(this, $btn, sendcloudDetails),
            this._onServicePointError.bind(this)
        );
    },

    _onServicePointSelected: function($btn, sendcloudDetails, servicePoint) {

        // Update view
        this.$('.o_website_sendcloud_address').remove();
        var address = QWeb.render("website_sendcloud_official.Address", {
            servicePoint: servicePoint
        });
        $btn.after(address);

        // Update sale order
        this.dp.add(this._rpc({
            route: "/shop/sendcloud_update_service_point_address",
            params: {
                order_id: sendcloudDetails.order_id,
                sendcloud_service_point_address: JSON.stringify(servicePoint),
            }
        }));

        // Enable pay button
        const $payButton = this.$('button[name="o_payment_submit_button"]');
        var disabledReasons = $payButton.data('disabled_reasons') || {};
        disabledReasons.carrier_selection = false;
        $payButton.data('disabled_reasons', disabledReasons);
        $payButton.attr('disabled', false);
    },

    _onServicePointError: function(errors) {
        const irrelevantErrors = ['Closed'];
        var relevantErrors = _.difference(errors, irrelevantErrors);

        if (relevantErrors.length) {
            return Dialog.alert(this, relevantErrors.join("\n"));
        }
    },

    _onClickSendcloudAddress: function(ev) {
        ev.stopPropagation();
    }
});
