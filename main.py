import os
from autojira import AutoJIRA
from autojira import WorkFlow

__me = os.environ['JIRA_ME']
__dt = os.environ['JIRA_DEFAULT_TESTER']
__dtc = os.environ['JIRA_DEFAULT_COMMENT_TEST']
aj = AutoJIRA()
wf = WorkFlow()


def close_my_verified_tickets():
    jql = 'assignee={} and status=verified'.format(__me)
    aj.move(wf.CLOSED, jql=jql)


def move_my_code_review_tickets_to_test():
    jql = 'assignee={} and status="code review"'.format(__me)
    aj.move(wf.TEST, jql=jql, comments=__dtc, assignee=__dt)


def begin_work_by_issue_key(issue_key):
    aj.move(wf.BEGIN_WORK, key=issue_key)


def move_to_integration_by_issue_key(issue_key):
    aj.move(wf.INTEGRATION, key=issue_key, assignee=__me)


def move_to_verify_by_file(issue_file, assignee=__me):
    comments = "Sample comment"
    aj.move(wf.VERIFY, file=issue_file, assignee=assignee, comments=comments)


def main():
    move_to_verify_by_file('/tmp/issue_file', 'test.user')


if __name__ == '__main__':
    main()


