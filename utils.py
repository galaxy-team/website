import urllib
import logging
import json
import requests
import os

if 'HEROKU' not in os.environ:
    # authentication data
    with open('auth_data.json', 'r') as fh:
        auth_data = json.loads(fh.read())
        client_auth_data = auth_data["client_auth_data"]
else:
    client_auth_data = {}
    client_auth_data['client_id'] = os.environ['CLIENT_ID']
    client_auth_data['client_secret'] = os.environ['CLIENT_SECRET']


def authed_fetch(url, headers={}):
    headers.update({'X-Admin-Contact': 'me@mause.me'})
    url += '?' + urllib.parse.urlencode(client_auth_data)
    r = requests.get(url=url, headers=headers)
    if 'x-ratelimit-remaining' in r.headers.keys():
        logging.info('{} requests remaining for this hour.'.format(
            r.headers['x-ratelimit-remaining']))
    else:
        logging.info('Request remaing for hour could not determined')
        logging.info(r.content)
    return r
