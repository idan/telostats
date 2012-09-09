import re
from bs4 import BeautifulSoup
import requests
import datetime
import logging
import os
import json

from django.utils.timezone import utc
from pyparsing import commaSeparatedList
from .models import Station

STATION_LIST_URL = u'http://www.tel-o-fun.co.il/Default.aspx?TabID=64'

TEMPODB_KEY = os.environ['TEMPODB_KEY']
TEMPODB_SECRET = os.environ['TEMPODB_SECRET']
TEMPODB_BASEURL = 'https://api.tempo-db.com/v1'
TEMPO_JSONCT = {'content-type': 'application/json'}
tempo_auth = requests.auth.HTTPBasicAuth(TEMPODB_KEY, TEMPODB_SECRET)
tempo = requests.session(auth=tempo_auth)

FIELD_KEYS = ['longitude', 'latitude', 'id', 'name', 'address', 'poles', 'available']


def measure():
    logging.info("Measuring stations...")
    timestamp = datetime.datetime.utcnow().replace(tzinfo=utc)
    stations = parse_stations(scrape_stations())
    store_stations(stations)
    log_data(timestamp, stations)
    logging.info("Measured {} stations.".format(len(stations)))
    # TODO: periodically write more metadata about stations to the tempo series?


def scrape_stations():
    # timestamp = datetime.datetime.utcnow().replace(tzinfo=utc)
    logging.debug("Scraping site content...")
    r = requests.get(STATION_LIST_URL)
    logging.debug("Parsing DOM...")
    soup = BeautifulSoup(r.content)
    raw_stations = soup.find_all(lambda t:
        t.name == 'script' and
        hasattr(t, 'text') and
        t.decode_contents().startswith('function loadMarkers'))[0].decode_contents()
    return raw_stations


def parse_stations(raw_stations):
    logging.debug("Extracting raw stations...")
    filtered = re.findall(r'setMarker\((.+?)\);(?=setMarker|\})', raw_stations)
    logging.debug("Parsing stations...")
    parsed = []
    for station in filtered:
        stripped = [s.strip("' ") for s in commaSeparatedList.parseString(station)[:7]]
        d = dict(zip(FIELD_KEYS, stripped))
        for floatkey in ['longitude', 'latitude']:
            d[floatkey] = float(d[floatkey])
        for intkey in ['id', 'poles', 'available']:
            d[intkey] = int(d[intkey])
        parsed.append(d)
    logging.debug("Parsed {} stations".format(len(parsed)))
    return parsed


def store_stations(stations):
    logging.debug("Create/update station metadata in Django DB...")
    for station in stations:
        fields = ['longitude', 'latitude', 'name', 'address']
        metadata = dict((f, station[f]) for f in fields)
        obj, created = Station.objects.get_or_create(
            id=station['id'], defaults=metadata)
        obj.poles = station['poles']
        obj.available = station['available']
        obj.save()


def station_poles_key(station):
    return "station:{id}.poles.{id}".format(**station)


def station_available_key(station):
    return "station:{id}.available.{id}".format(**station)


def log_data(timestamp, stations):
    logging.debug("Logging measurements to TempoDB...")
    payload = {}
    payload['t'] = timestamp.isoformat()
    data = []
    for station in stations:
        poles_key = station_poles_key(station)
        available_key = station_available_key(station)
        data.append({'key': poles_key, 'v': station['poles']})
        data.append({'key': available_key, 'v': station['available']})
    payload['data'] = data
    tempo.post(TEMPODB_BASEURL + '/data/',
               headers=TEMPO_JSONCT,
               data=json.dumps(payload))
