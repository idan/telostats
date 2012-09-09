from django.core.management.base import NoArgsCommand
from telostats.stations.tasks import measure
import logging

logging.basicConfig(level=logging.DEBUG)

class Command(NoArgsCommand):
    help = 'Scrape station data from the Tel-o-fun website.'

    def handle_noargs(self, **options):
        measure()
