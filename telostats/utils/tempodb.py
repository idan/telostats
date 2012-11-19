import requests
import json

from collections import defaultdict
from datetime import datetime, timedelta
from os import environ

API_HOST = 'api.tempo-db.com'
API_PORT = 443
API_VERSION = 'v1'

API_URL = 'https://{0}:{1}/{2}'.format(API_HOST, API_PORT, API_VERSION)

TEMPODB_KEY = environ['TEMPODB_KEY']
TEMPODB_SECRET = environ['TEMPODB_SECRET']


class TempoDbClient():
    def __init__(self, key=TEMPODB_KEY, secret=TEMPODB_SECRET):
        self.key = key
        self.secret = secret
        session_auth = requests.auth.HTTPBasicAuth(TEMPODB_KEY, TEMPODB_SECRET)
        self.session = requests.session(auth=session_auth)

    def get_data(self, station_id=None, start=None, end=None, interval='1hour',
            function='mean', tz='Asia/Jerusalem'):
        params = {
            'interval': interval,
            'function': function,
            'tz': tz
        }
        if start:
            params['start'] = start
        if end:
            params['end'] = end
        if station_id:
            params['attr[station]'] = station_id
        return self.session.get(API_URL + '/data/', params=params)

    def get_series(self, station_id=None, interval='1hour', start=timedelta(hours=24), **kwargs):
        start = (datetime.utcnow() - start).isoformat()
        data = self.get_data(station_id=station_id, start=start, interval=interval)
        content = data.content
        res = defaultdict(dict)

        d = json.loads(content)
        for series in d:
            station_id = series['series']['attributes']['station']
            data_type = series['series']['tags'][0]
            data_val = series['data']
            res[station_id][data_type] = data_val

        return dict(res)

    def get_latest_counts(self, station_id=None):
        '''This method is pending a proper get_latest API from tempo db'''
        start = datetime.utcnow() - timedelta(minutes=15)
        content = self.get_data(station_id=station_id, start=start).content
        res = defaultdict(dict)

        d = json.loads(content)
        for series in d:
            station_id = series['series']['attributes']['station']
            data_type = series['series']['tags'][0]
            data_val = series['data'][-1]['v']
            res[station_id][data_type] = data_val

        return dict(res)
