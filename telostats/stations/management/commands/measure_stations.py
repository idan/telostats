import logging

from django.core.management.base import BaseCommand
from optparse import make_option
from telostats.stations.tasks import measure

logging.basicConfig(level=logging.DEBUG)


class Command(BaseCommand):
    help = 'Scrape station data from the Tel-o-fun website.'
    option_list = BaseCommand.option_list + (
        make_option('-n', '--no-log',
            action='store_false',
            dest='log_tempodb',
            default=True,
            help='Do not log measurements to Tempo DB (use this in local env)'),
    )

    def handle(self, *args, **options):
        measure(log_tempodb=options['log_tempodb'])
