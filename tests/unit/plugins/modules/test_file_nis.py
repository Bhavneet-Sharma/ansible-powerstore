# Copyright: (c) 2024, Dell Technologies
# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)
"""Unit Tests for File NIS module for PowerStore"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import pytest
from mock.mock import MagicMock
# pylint: disable=unused-import

from ansible_collections.dellemc.powerstore.tests.unit.plugins.module_utils.libraries.initial_mock \
    import utils
from ansible_collections.dellemc.powerstore.plugins.modules.file_nis import \
    PowerStoreFileNIS
from ansible_collections.dellemc.powerstore.plugins.modules.file_nis import \
    FileNISHandler
from ansible_collections.dellemc.powerstore.plugins.modules.file_nis import \
    main

from ansible_collections.dellemc.powerstore.tests.unit.plugins.module_utils.mock_file_nis_api \
    import MockFileNISApi
from ansible_collections.dellemc.powerstore.tests.unit.plugins.module_utils.mock_api_exception import \
    MockApiException
from ansible_collections.dellemc.powerstore.tests.unit.plugins.module_utils.libraries.powerstore_unit_base \
    import PowerStoreUnitBase


class TestPowerStoreFileNIS(PowerStoreUnitBase):

    get_module_args = MockFileNISApi.FILE_NIS_COMMON_ARGS

    @pytest.fixture
    def module_object(self):
        return PowerStoreFileNIS

    def test_get_file_nis_response(self, powerstore_module_mock):
        self.set_module_params(
            powerstore_module_mock,
            self.get_module_args,
            {
                'file_nis_id': MockFileNISApi.FILE_NIS_DETAILS['id'],
                'state': "present"}
        )
        FileNISHandler().handle(powerstore_module_mock, powerstore_module_mock.module.params)
        powerstore_module_mock.file_nis.get_file_nis_details.assert_called()

    def test_get_file_nis_nas_response(self, powerstore_module_mock):
        self.set_module_params(
            powerstore_module_mock,
            self.get_module_args,
            {
                'nas_server': "nas_server_id",
                'state': "present"
            })
        FileNISHandler().handle(powerstore_module_mock, powerstore_module_mock.module.params)
        powerstore_module_mock.file_nis.get_file_nis_by_nas_server_id.assert_called()

    def test_get_file_nis_exception(self, powerstore_module_mock):
        MockApiException.HTTP_ERR = "1"
        MockApiException.err_code = "1"
        MockApiException.status_code = "404"
        self.set_module_params(
            powerstore_module_mock,
            self.get_module_args,
            {
                'file_nis_id': MockFileNISApi.FILE_NIS_DETAILS['id'],
                'state': "present"
            })
        powerstore_module_mock.file_nis.get_file_nis_details = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockFileNISApi.get_file_nis_exception_response(
                'get_file_nis_exception'), powerstore_module_mock, FileNISHandler)

    def test_create_file_nis_response(self, powerstore_module_mock):
        self.set_module_params(
            powerstore_module_mock,
            self.get_module_args,
            {
                'nas_server': "sample_nas_server",
                'domain': "domain1",
                'add_ip_addresses': ['10.10.10.10'],
                'remove_ip_addresses': ['10.10.10.11'],
                'state': "present"
            })
        powerstore_module_mock.module.params = self.get_module_args
        powerstore_module_mock.file_nis.get_file_nis_details_by_nas_server_id = MagicMock(
            return_value=None)
        FileNISHandler().handle(powerstore_module_mock, powerstore_module_mock.module.params)
        powerstore_module_mock.file_nis.create_file_nis.assert_called()

    def test_create_file_nis_exception(self, powerstore_module_mock):
        MockApiException.HTTP_ERR = "1"
        MockApiException.err_code = "1"
        MockApiException.status_code = "404"
        self.set_module_params(
            powerstore_module_mock,
            self.get_module_args,
            {
                'nas_server': "sample_nas_server",
                'domain': "domain1",
                'add_ip_addresses': ['10.10.10.10'],
                'remove_ip_addresses': ['10.10.10.11'],
                'state': "present"
            })
        powerstore_module_mock.module.params = self.get_module_args
        powerstore_module_mock.configuration.get_file_nis_details_by_nas_server_id = MagicMock(
            return_value=None)
        powerstore_module_mock.file_nis.create_file_nis = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockFileNISApi.get_file_nis_exception_response(
                'create_file_nis_exception'), powerstore_module_mock, FileNISHandler)

    def test_modify_file_nis(self, powerstore_module_mock):
        self.set_module_params(
            powerstore_module_mock,
            self.get_module_args,
            {
                'nas_server': "sample_nas_server",
                'add_ip_addresses': ['10.10.10.11'],
                'remove_ip_addresses': ['10.10.10.10'],
                'is_destination_override_enabled': True,
                'state': "present"
            })
        powerstore_module_mock.module.params = self.get_module_args
        powerstore_module_mock.file_nis.get_file_nis_details = MagicMock(
            return_value=MockFileNISApi.FILE_NIS_DETAILS)
        FileNISHandler().handle(powerstore_module_mock, powerstore_module_mock.module.params)
        powerstore_module_mock.file_nis.modify_file_nis.assert_called()

    def test_modify_file_nis_exception(self, powerstore_module_mock):
        MockApiException.HTTP_ERR = "1"
        MockApiException.err_code = "1"
        MockApiException.status_code = "404"
        self.set_module_params(
            powerstore_module_mock,
            self.get_module_args,
            {
                'nas_server': "sample_nas_server",
                'add_ip_addresses': ['10.10.10.11'],
                'remove_ip_addresses': ['10.10.10.10'],
                'is_destination_override_enabled': True,
                'state': "present"
            })
        powerstore_module_mock.module.params = self.get_module_args
        powerstore_module_mock.file_nis.get_file_nis_details = MagicMock(
            return_value=MockFileNISApi.FILE_NIS_DETAILS)
        powerstore_module_mock.file_nis.modify_file_nis = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockFileNISApi.get_file_nis_exception_response(
                'modify_file_nis_exception'), powerstore_module_mock, FileNISHandler)

    def test_delete_file_nis(self, powerstore_module_mock):
        self.set_module_params(
            powerstore_module_mock,
            self.get_module_args,
            {
                'file_nis_id': MockFileNISApi.FILE_NIS_DETAILS['id'],
                'state': "absent"
            })
        powerstore_module_mock.module.params = self.get_module_args
        powerstore_module_mock.file_nis.get_file_nis_details = MagicMock(
            return_value=MockFileNISApi.FILE_NIS_DETAILS)
        FileNISHandler().handle(powerstore_module_mock, powerstore_module_mock.module.params)
        powerstore_module_mock.file_nis.delete_file_nis.assert_called()

    def test_delete_file_nis_exception(self, powerstore_module_mock):
        MockApiException.HTTP_ERR = "1"
        MockApiException.err_code = "1"
        MockApiException.status_code = "404"
        self.set_module_params(
            powerstore_module_mock,
            self.get_module_args,
            {
                'file_nis_id': MockFileNISApi.FILE_NIS_DETAILS['id'],
                'state': "absent"
            })
        powerstore_module_mock.module.params = self.get_module_args
        powerstore_module_mock.file_nis.get_file_nis_details = MagicMock(
            return_value=MockFileNISApi.FILE_NIS_DETAILS)
        powerstore_module_mock.file_nis.delete_file_nis = MagicMock(
            side_effect=MockApiException)
        self.capture_fail_json_call(
            MockFileNISApi.get_file_nis_exception_response(
                'delete_file_nis_exception'), powerstore_module_mock, FileNISHandler)
