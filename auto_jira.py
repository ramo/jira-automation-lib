from jira import JIRA
import os


class WorkFlow:
    def __init__(self):
        """
            271 - Open
            151 - Issue is sprint ready
            161 - Assign to current sprint
            91 - Begin work
            191 - Ready for code review
            201 - Passed code review
            21 - Ready for testing
            121 - Closed
        """
        self.OPEN = 271
        self.SPRINT_READY = 151
        self.CURRENT_SPRINT = 161
        self.BEGIN_WORK = 91
        self.CODE_REVIEW = 191
        self.INTEGRATION = 201
        self.TEST = 21
        self.CLOSED = 121

        self.__wfo = [
            self.OPEN,
            self.SPRINT_READY,
            self.CURRENT_SPRINT,
            self.BEGIN_WORK,
            self.CODE_REVIEW,
            self.INTEGRATION,
            self.TEST,
            self.CLOSED
        ]

    def previous(self, n):
        return self.__wfo[self.__wfo.index(n) - 1]

    def next(self, n):
        return self.__wfo[self.__wfo.index(n) + 1]


class AutoJIRA:
    def __init__(self):
        self.__jc = JIRA(server=os.environ['JIRA_URL'],
                         basic_auth=(os.environ['JIRA_API_USER'], os.environ['JIRA_API_TOKEN']))
        self.__me = os.environ['JIRA_ME']
        self.__dt = os.environ['JIRA_DEFAULT_TESTER']
        self.__dtc = os.environ['JIRA_DEFAULT_COMMENT_TEST']
        self.__wf = WorkFlow()

    def close_my_verified_tickets(self):
        issues = self.__jc.search_issues(jql_str='assignee={} and status=verified'.format(self.__me))
        for issue in issues:
            print('Closing the ticket: ', issue.key)
            self.__move(issue, self.__wf.CLOSED)
        print('Done')

    def move_my_code_review_tickets_to_test(self):
        issues = self.__jc.search_issues(jql_str='assignee={} and status="code review"'.format(self.__me))
        for issue in issues:
            self.move_to_test_by_issue(issue)
        print('Done')

    def move_to_test_by_issue(self, issue):
        print("Moving ticket {} to test".format(issue.key))
        self.__move(issue, self.__wf.TEST)
        self.__jc.add_comment(issue, self.__dtc)
        self.__jc.assign_issue(issue, self.__dt)

    def __move(self, issue, n):
        if n not in list(map(lambda x: int(x['id']), self.__jc.transitions(issue))):
            self.__move(issue, self.__wf.previous(n))
        self.__jc.transition_issue(issue, n)

    def move_to_test_by_issue_key(self, issue_key):
        self.move_to_test_by_issue(self.__jc.issue(issue_key))


def main():
    aj = AutoJIRA()
    aj.close_my_verified_tickets()
    aj.move_my_code_review_tickets_to_test()


if __name__ == '__main__':
    main()
