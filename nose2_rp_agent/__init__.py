from nose2.events import Plugin
from reportportal_client import ReportPortalService
from reportportal_client.helpers import timestamp


def _get_test_case_and_test_method(event):
    test_case = "{}.{}".format(
        event.test.__class__.__module__, event.test.__class__.__name__
    )
    test_method = event.test.__dict__["_testMethodName"]

    return (test_case, test_method)


RP_STATUS = {"passed": "PASSED", "error": "FAILED", "failed": "FAILED"}


class ReportPortalPlugin(Plugin):
    """
    Report Portal plugin for nose2
    """

    configSection = "reportportal"
    commandLineSwitch = (None, "rp", "Send report to Report Portal")

    def __init__(self, *args, **kwargs):
        super(ReportPortalPlugin, self).__init__(*args, **kwargs)

        self._rp = ReportPortalService(
            endpoint=self.config.as_str("endpoint"),
            project=self.config.as_str("project"),
            token=self.config.as_str("token"),
        )

        self.tests = {}

    def startTestRun(self, _event):
        self._rp.start_launch(
            start_time=timestamp(),
            name=self.config.as_str("launch_name"),
            attributes=self.config.as_str("launch_attributes").split(" "),
            description=self.config.as_str("launch_description"),
        )

    def afterSummaryReport(self, _event):
        # send tests
        for test_case in self.tests:

            item_id = self._rp.start_test_item(
                name=test_case,
                start_time=self.tests[test_case]["_start_time"],
                item_type="SUITE",
            )

            for test_method in self.tests[test_case]:
                if isinstance(self.tests[test_case][test_method], dict):
                    test_id = self._rp.start_test_item(
                        name="[{}]: {}".format(test_case, test_method),
                        start_time=self.tests[test_case][test_method]["_start_time"],
                        item_type="STEP",
                        parent_item_id=item_id,
                        description="",
                    )

                    self._rp.finish_test_item(
                        test_id,
                        self.tests[test_case][test_method]["_stop_time"],
                        self.tests[test_case][test_method]["_status"],
                    )

            self._rp.finish_test_item(
                item_id=item_id,
                end_time=self.tests[test_case]["_stop_time"],
                status=self.tests[test_case]["_status"],
            )

        # finish launch
        self._rp.finish_launch(end_time=timestamp())
        self._rp.terminate()

    def startTest(self, event):
        test_case, test_method = _get_test_case_and_test_method(event)

        if test_case not in self.tests:
            self.tests[test_case] = {"_start_time": timestamp(), "_status": "PASSED"}

        self.tests[test_case][test_method] = {"_start_time": timestamp()}

    def testOutcome(self, event):
        test_case, test_method = _get_test_case_and_test_method(event)
        self.tests[test_case][test_method]["_stop_time"] = timestamp()
        self.tests[test_case][test_method]["_status"] = RP_STATUS[event.outcome]

        self.tests[test_case]["_stop_time"] = timestamp()
        if event.outcome != "passed":
            self.tests[test_case]["_status"] = "FAILED"
