import re
import pyquery
import datetime
import logging

from django.utils.timezone import utc

from celery.schedules import crontab
from celery.task import task, periodic_task
from .models import Station, Status

STATION_LIST_URL = u'http://www.tel-o-fun.co.il/%D7%AA%D7%97%D7%A0%D7%95%D7%AA%D7%AA%D7%9C%D7%90%D7%95%D7%A4%D7%9F.aspx'
STATION_DATA_URL = u'http://www.tel-o-fun.co.il/DesktopModules/Locations/StationData.ashx?sid={0}'


def build_station_list():
    dom = pyquery.PyQuery(STATION_LIST_URL)
    raw_stations = dom('.bicycle_station')
    stations = {}
    for elem in raw_stations:
        id = elem.attrib['sid']
        stations[id] = {'name': unicode(elem.text),
                        'longitude': elem.attrib['x'],
                        'latitude': elem.attrib['y']}
    return stations


def get_station_metadata(id):
    """Gets the metadata for a given station

    Returns a two-element tuple consisting of available (bikes, docks)
    """
    dom = pyquery.PyQuery(STATION_DATA_URL.format(id))
    return tuple(re.findall('\d+', dom('div')[4].text_content()))


@periodic_task(ignore_result=True, run_every=crontab(minute="*/15"))
def scrape_station_list():
    timestamp = datetime.datetime.utcnow().replace(tzinfo=utc)
    logging.info("Fetching station list at {}".format(timestamp.isoformat()))
    stations = build_station_list()
    logging.info("Found {} stations".format(len(stations)))
    for id, defaults in stations.items():
        station, created = Station.objects.get_or_create(id=id, defaults=defaults)
        scrape_station_data.delay(id, timestamp)


@task(ignore_result=True)
def scrape_station_data(id, timestamp):
    actual_timestamp = datetime.datetime.utcnow().replace(tzinfo=utc)
    try:
        station = Station.objects.get(id=id)
    except Station.DoesNotExist:
        raise
    logging.info("Fetching Station {} at {}".format(id, actual_timestamp.isoformat()))
    bikes, docks = get_station_metadata(id)
    Status.objects.create(station=station, bikes=bikes, docks=docks,
                          timestamp=timestamp, actual_timestamp=actual_timestamp)
    logging.info("Station {} has {} bikes, {} docks".format(id, bikes, docks))
