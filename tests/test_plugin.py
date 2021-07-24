from unittest import TestCase
from unittest.mock import patch, MagicMock

from nose2_rp_agent import ReportPortalPlugin


class ReportPortalPluginTest(TestCase):
    @patch("nose2_rp_agent.ReportPortalService")
    def test_init(self, mock_rp_service):

        instance = ReportPortalPlugin()

        mock_rp_service.assert_called_with(endpoint=None, project=None, token=None)
        self.assertEqual(instance.tests, {})

    @patch("nose2_rp_agent.ReportPortalService")
    @patch("nose2_rp_agent.timestamp")
    def test_start_test_run(self, mock_timestamp, mock_rp_service):
        mock_timestamp.return_value = "timestamp"

        mock_rp_instance = MagicMock(name="rp_instance")
        mock_rp_service.return_value = mock_rp_instance

        plugin = ReportPortalPlugin()
        plugin.config = MagicMock(name="config")
        plugin.config.as_str.return_value = " "

        plugin.startTestRun(None)

        mock_rp_instance.start_launch.assert_called_with(
            start_time="timestamp", name=" ", attributes=["", ""], description=" "
        )
        plugin.config.as_str.assert_any_call("launch_name")
        plugin.config.as_str.assert_any_call("launch_attributes")
        plugin.config.as_str.assert_any_call("launch_description")

    @patch("nose2_rp_agent.timestamp")
    def test_start_test(self, mock_timestamp):
        event = MagicMock(name="event")
        event.test._testMethodName = "method"

        mock_timestamp.return_value = "timestamp"

        plugin = ReportPortalPlugin()
        plugin.config = MagicMock(name="config")
        plugin.config.as_str.return_value = " "

        plugin.startTest(event)

        self.assertEqual(
            plugin.tests,
            {
                "unittest.mock.MagicMock": {
                    "_start_time": "timestamp",
                    "_status": "PASSED",
                    "method": {"_start_time": "timestamp"},
                }
            },
        )
