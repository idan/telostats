import json
import logging

from django.core.management.base import NoArgsCommand
from telostats.stations.models import Station
from unipath import FSPath as Path


logging.basicConfig(level=logging.DEBUG)

class Command(NoArgsCommand):
    help = 'Import station polygon JSON data'

    def handle_noargs(self, **options):
        project_dir = Path(__file__).absolute().ancestor(4)
        data_file = project_dir.child('static', 'js', 'station_polys.json')
        with open(data_file, 'r') as f:
            data = json.loads(f.read())
            for station_id, coords in data.items():
                station = Station.objects.get(id=station_id)
                station.polygon = coords
                station.save()
