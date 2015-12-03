# Copyright 2015 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock

from cloudferrylib.utils import utils
from fabric.api import local
from tests import test


class forward_agentTestCase(test.TestCase):

    @mock.patch('cloudferrylib.utils.utils.local')
    def test_agent_is_already_run_w_keys(self, test_local):
        test_local.return_value = local(
            "echo test_session_num test_fingerprint test_key_1 test_type\n"
            "echo test_session_num test_fingerprint test_key_2 test_type\n",
            capture=True
        )
        fa = utils.forward_agent(['test_key_1', 'test_key_2'])

        self.assertTrue(fa._agent_already_running())

    @mock.patch('cloudferrylib.utils.utils.local')
    def test_agent_is_not_run(self, test_local):
        test_local.return_value = local(
            "echo The agent has no identities.",
            capture=True
        )
        fa = utils.forward_agent(['test_key_1', 'test_key_2'])

        self.assertFalse(fa._agent_already_running())

    @mock.patch('cloudferrylib.utils.utils.local')
    def test_agent_is_already_run_w_another_key(self, test_local):
        test_local.return_value = local(
            "echo test_session_num test_fingerprint test_key test_type\n",
            capture=True
        )
        fa = utils.forward_agent(['test_key_1', 'test_key_2'])

        self.assertFalse(fa._agent_already_running())