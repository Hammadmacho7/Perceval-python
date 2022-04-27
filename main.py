# This is a sample Python script.
from perceval.backends.core.git import Git
from perceval.backends.core.github import GitHub
from collections import Counter
import datetime
import dateutil.parser


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.


def extract_github_identities():
    counterClosed = 0
    counterOpen = 0
    closedIssueWithNoAssignee = 0
    averageTimeTakenToCloseAll = 0
    closedIssueWithAssignee = 0
    averageTimeTakenToCloseAllWithAssigne = 0
    first_issue_created_date = None
    last_issue_created_date = None
    first_issue_flag = False

    today_date = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    today_date = dateutil.parser.isoparse(today_date)
    print("Today's date is " + str(today_date))

    pull_request_users = []
    issue_users = []

    repo = GitHub("Azure", "MachineLearningNotebooks", api_token=["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"],
                  sleep_for_rate=True)
    for issue in repo.fetch():
        #print("Today's date is " + str(today_date))
        login = issue['data']['user_data']['login']
        # email = issue['data']['user_data']['login']

        # if not login:
        # login = ""

        # print(issue['data']['state'])
        if "pull_request" in issue['data']:
            pass
        else:
            if issue['data']['state'] == 'closed':
                counterClosed = counterClosed + 1
                if issue['data']['assignee'] is None:
                    closedIssueWithNoAssignee = closedIssueWithNoAssignee + 1
                    o_time = dateutil.parser.parse(issue['data']['created_at'])
                    c_time = dateutil.parser.parse(issue['data']['closed_at'])
                    d_time = (c_time - o_time).days
                    averageTimeTakenToCloseAll = int(d_time) + averageTimeTakenToCloseAll
                else:
                    closedIssueWithAssignee = closedIssueWithAssignee + 1
                    o_time = dateutil.parser.parse(issue['data']['created_at'])
                    c_time = dateutil.parser.parse(issue['data']['closed_at'])
                    d_time = (c_time - o_time).days
                    averageTimeTakenToCloseAllWithAssigne = int(d_time) + averageTimeTakenToCloseAllWithAssigne
            else:
                counterOpen = counterOpen + 1

       # print('date ' + str(issue["data"]["created_at"]))
        if first_issue_flag is False:
            first_issue_created_date = last_issue_created_date = dateutil.parser.parse(issue["data"]["created_at"])
            first_issue_flag = True


        created_date = dateutil.parser.parse(issue["data"]["created_at"])
        first_issue_created_date = min(created_date, first_issue_created_date)
        last_issue_created_date = max(created_date, last_issue_created_date)

        if "pull_request" in issue['data']:
            pass
        else:
            issue_users.append(login)

       # print(issue['data']['state'])
       # print(issue['data']['assignee'])


        # if issue['data']['state'] == 'closed' and issue['data']['assignee'] is None:
        # closedIssueWithNoAssignee = closedIssueWithNoAssignee + 1
        #  o_time = dateutil.parser.parse(issue['data']['created_at'])
        #  c_time = dateutil.parser.parse(issue['data']['closed_at'])
        # averageTimeTakenToCloseAll = o_time - c_time
        # averageTimeTakenToCloseAll = averageTimeTakenToCloseAll + d_time

    print("--------PART 2----------")
    print("First Opened Issue Date:")
    print(first_issue_created_date)
    print("Last Opened Issue Date:")
    print(last_issue_created_date)
    ageOfRepo = (last_issue_created_date-first_issue_created_date).days
    print("Age of repository in days: " + str(ageOfRepo))
    print("")
    print("--------PART 3----------")
    print("the number of closed issues:")
    print(counterClosed)
    print("the number of open issues:")
    print(counterOpen)
    print("")
    # [print("issues:" + str(Counter(issue_users).get(u)) + "\t user: " + u) for u in Counter(issue_users).keys()]
    print("--------PART 4----------")
    c = Counter(issue_users)
    print("Top 5 users:")
    print(c.most_common(5))
    print("")
    print("--------PART 5----------")
    if (closedIssueWithNoAssignee == 0 or averageTimeTakenToCloseAll == 0):
        print("Number of closed issues with no assignee = " + "0")
        print("Average number of days to close issues with no assignee = " + "0")
    else:
        print("Number of closed issues with at least no assignee:")
        print(round(closedIssueWithNoAssignee))

        print("Average number of days to close issues with at least no assignee:")
        print(round(averageTimeTakenToCloseAll / closedIssueWithNoAssignee))
    print("")
    print("--------PART 6----------")
    if (closedIssueWithAssignee == 0 or averageTimeTakenToCloseAllWithAssigne == 0):
        print("Number of closed issues with at least one assignee = " + "0")
        print("Average number of days to close issues with at least one assignee = " + "0")
    else:
        print("Number of closed issues with at least one assignee:")
        print(round(closedIssueWithAssignee))
        print("Average number of days to close issues with at least one assignee:")
        print(round(averageTimeTakenToCloseAllWithAssigne / closedIssueWithAssignee))
    print("")


# print(averageTimeTakenToCloseAll / closedIssueWithNoAssignee)

# [print("pr:" + str(Counter(pull_request_users).get(u)) + "\t user: " + u) for u in Counter(pull_request_users).keys()]


def extract_git_identities():
    users = []
    issue_users = []

    # URL for the git repo to analyze
    repo_url = 'http://github.com/grimoirelab/perceval.git'
    # directory for letting perceval clone the git repo
    repo_dir = '/tmp/perceval.git'
    # fetch all commits and store the author
    repo = Git(uri=repo_url, gitpath=repo_dir)
    for commit in repo.fetch():
        users.append(commit['data']['Author'])

        # count commits per user
        [print("commits:" + str(Counter(users).get(u)) + "\t user: " + u) for u in Counter(users).keys()]


def main():
    # extract_git_identities()
    print("---------------------")
    extract_github_identities()


if __name__ == '__main__':
    main()
