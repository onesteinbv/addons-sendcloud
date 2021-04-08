# Copyright 2020 Onestein (<https://www.onestein.eu>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import logging

from os.path import dirname, join

from vcr import VCR

from odoo.tests import TransactionCase

logging.getLogger("vcr").setLevel(logging.WARNING)

recorder = VCR(
    record_mode="once",
    cassette_library_dir=join(dirname(__file__), "vcr_cassettes"),
    path_transformer=VCR.ensure_suffix(".yaml"),
    filter_headers=["Authorization"],
)


class TestDeliverySendCloud(TransactionCase):
    def setUp(self):
        super().setUp()

    # def test_01_sender_address(self):
    #     with recorder.use_cassette('sender_address'):
    #         sender_address = self.env["sendcloud.request"].get_sender_address()
    #         self.assertTrue(sender_address)
    #     with recorder.use_cassette('sender_address'):
    #         self.env["sendcloud.sender.address"].sendcloud_update_sender_address()

    # def test_02_retrieve_shipping_methods(self):
    #     with recorder.use_cassette('shipping_methods'):
    #         self.env["delivery.carrier"]._sendcloud_create_update_shipping_methods(self.env.company.id)

    # def test_03_retrieve_integrations(self):
    #     with recorder.use_cassette('integrations'):
    #         self.env["sendcloud.integration"].sendcloud_update_integrations()
    #
    # def test_04_servicepoints(self):
    #     params = {
    #         "country": "NL",
    #     }
    #     with recorder.use_cassette('servicepoints'):
    #         self.env["sendcloud.request"].get_servicepoints(params)
    #
    # def test_05_retrieve_brands(self):
    #     with recorder.use_cassette('brands'):
    #         self.env["sendcloud.request"].get_brands()
