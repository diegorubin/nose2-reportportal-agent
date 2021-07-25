from unittest import TestCase
from unittest.mock import ANY, MagicMock, patch

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

    @patch("nose2_rp_agent.timestamp")
    def test_test_outcome(self, mock_timestamp):
        event = MagicMock(name="event")
        event.test._testMethodName = "method"
        event.outcome = "passed"

        mock_timestamp.return_value = "timestamp"

        plugin = ReportPortalPlugin()
        plugin.tests = {"unittest.mock.MagicMock": {"method": {}}}

        plugin.testOutcome(event)

        self.assertEqual(
            plugin.tests,
            {
                "unittest.mock.MagicMock": {
                    "_stop_time": "timestamp",
                    "method": {"_status": "PASSED", "_stop_time": "timestamp"},
                }
            },
        )

    @patch("nose2_rp_agent.timestamp")
    def test_test_outcome_failed(self, mock_timestamp):
        event = MagicMock(name="event")
        event.test._testMethodName = "method"
        event.outcome = "failed"

        mock_timestamp.return_value = "timestamp"

        plugin = ReportPortalPlugin()
        plugin.tests = {"unittest.mock.MagicMock": {"method": {}}}

        plugin.testOutcome(event)

        self.assertEqual(
            plugin.tests,
            {
                "unittest.mock.MagicMock": {
                    "_status": "FAILED",
                    "_stop_time": "timestamp",
                    "method": {"_status": "FAILED", "_stop_time": "timestamp"},
                }
            },
        )

    @patch("nose2_rp_agent.ReportPortalService")
    def test_after_summary_report(self, mock_rp_service):
        event = MagicMock(name="event")
        event.test._testMethodName = "method"

        mock_rp_instance = MagicMock(name="rp_instance")
        mock_rp_service.return_value = mock_rp_instance

        plugin = ReportPortalPlugin()
        plugin.tests = {
            "unittest.mock.MagicMock": {
                "_status": "FAILED",
                "_start_time": "timestamp",
                "_stop_time": "timestamp",
                "method": {
                    "_start_time": "timestamp",
                    "_status": "FAILED",
                    "_stop_time": "timestamp",
                },
            }
        }

        plugin.afterSummaryReport(None)

        mock_rp_instance.start_test_item.assert_any_call(
            name="unittest.mock.MagicMock", start_time="timestamp", item_type="SUITE"
        )
        mock_rp_instance.start_test_item.assert_any_call(
            name="[unittest.mock.MagicMock]: method",
            start_time="timestamp",
            item_type="STEP",
            parent_item_id=ANY,
            description="",
        )
        mock_rp_instance.finish_test_item.assert_any_call(ANY, "timestamp", "FAILED")
        mock_rp_instance.finish_test_item.assert_any_call(
            item_id=ANY, end_time="timestamp", status="FAILED"
        )

        mock_rp_instance.finish_launch.assert_called()
        mock_rp_instance.terminate.assert_called()
