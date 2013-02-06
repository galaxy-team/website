import json
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
            'Created a new {ref_type} on repository '),
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

    end = {
        'string': string,
        'info': event_info
    }

    return end


def get_events():
    end_events = []
    for event in get_repo_events(repos.json()):
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
