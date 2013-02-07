import logging
from utils import authed_fetch


def get_repo_events(repos):
    for repository in repos:
        events = authed_fetch('https://api.github.com/repos/{}/events'.format(
            repository['full_name']))
        for event in events.json():
            yield event


def build_events(event_info):
    sentence_templates = {
        'PushEvent': 'Pushed to ',
        'CreateEvent': (
            'Created a new {ref_type}; '),
        'DeleteEvent': (
            'Deleted a {ref_type} on repository '),
        'PullRequestEvent': '{action} a pull request on '
    }
    if event_info['type'] not in sentence_templates:
        return

    event_info['invoker'] = event_info['actor']['login']
    event_info['repository'] = event_info['repo']['name']
    if 'ref_type' in event_info['payload']:
        event_info['ref_type'] = event_info['payload']['ref_type']

    if 'action' in event_info['payload']:
        event_info['action'] = event_info['payload']['action']

    string = sentence_templates[event_info['type']].format(**event_info).title()

    event_info['string'] = string

    return event_info

import datetime
import time


def get_events():
    end_events = []
    all_events = list(get_repo_events(repos.json()))
    for event in all_events:
        parsed_date = datetime.datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        unix_time = time.mktime(parsed_date.timetuple())
        event['created_at'] = unix_time

    all_events = sorted(all_events, key=lambda x: x['created_at'])[::-1]

    for event in all_events:
        event_dict = build_events(event)
        if event_dict:
            end_events.append(event_dict)
    return end_events


logging.info('Setting up github event stream...')

# with open('debug.json', 'r') as fh:
#     repo_events = json.load(fh)

# setup
repos = authed_fetch('https://api.github.com/orgs/galaxy-team/repos')

logging.info(', '.join([repo['full_name'] for repo in repos.json()]))

# repo_events = list(
#     get_repo_events(repos.json()))
# with open('debug.json', 'w') as fh:
#     json.dump(list(repo_events), fh)

logging.info('Setup finished')
