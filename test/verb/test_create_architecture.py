# Copyright 2021 Research Institute of Systems Planning, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from logging import ERROR, INFO

try:
    import os
    from caret_analyze import MAX_CALLBACK_CONSTRUCTION_ORDER_ON_PATH_SEARCHING
except ModuleNotFoundError as e:
    if 'GITHUB_ACTION' in os.environ:
        MAX_CALLBACK_CONSTRUCTION_ORDER_ON_PATH_SEARCHING = 10
    else:
        raise e
from ros2caret.verb.create_architecture import CreateArchitecture


class TestCreateArchitecture:

    def test_create_success_case(self, caplog, mocker):
        architecture_mock = mocker.Mock()
        mocker.patch.object(architecture_mock, 'export', return_value=None)
        create_arch = CreateArchitecture('',
                                         MAX_CALLBACK_CONSTRUCTION_ORDER_ON_PATH_SEARCHING,
                                         architecture_mock)

        create_arch.create('output_path', True)
        assert len(caplog.records) == 1
        record = caplog.records[0]
        assert record.levelno == INFO

    def test_create_fail_case(self, caplog, mocker):
        architecture_mock = mocker.Mock()
        mocker.patch.object(architecture_mock,
                            'export',
                            side_effect=OSError(''))
        create_arch = CreateArchitecture('',
                                         MAX_CALLBACK_CONSTRUCTION_ORDER_ON_PATH_SEARCHING,
                                         architecture_mock)

        create_arch.create('output_path', True)
        assert len(caplog.records) == 1
        record = caplog.records[0]
        assert record.levelno == ERROR
