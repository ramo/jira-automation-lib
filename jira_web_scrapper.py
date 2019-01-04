import requests
from bs4 import BeautifulSoup
import os


def get_jira_url():
    return os.environ['JIRA_URL']


def get_page_soup(task_id):
    url = get_jira_url() + "/browse/" + task_id
    page = get(url)
    return BeautifulSoup(page.text, 'html.parser')


def get_task_description(task_id):
    soup = get_page_soup(task_id)
    return soup.find('h1', {'id': 'summary-val'}).text


def get(url, **kwargs):
    cookies = kwargs['cookies'] if 'cookies' in kwargs else {}
    cookies['cloud.session.token'] = os.environ['JIRA_TOKEN']
    return requests.get(url, kwargs, cookies=cookies)


def main():
    # print(get_task_description(sys.argv[1]))
    task_id = 'CPM-182'
    page = get_page_soup(task_id)
    print(page.text)


if __name__ == '__main__':
    main()
