from gpiozero import LED
from time import sleep

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    args = ''
    help = 'test a relay'

    #def add_arguments(self, parser):
    #    parser.add_argument('ip_address', help='ip address or FQDN to the web interface')

    def handle(self, *args, **options):

        relay1 = LED(1)

        while True:
            print("Relay 1 On")
            relay1.on()
            sleep(2)
            print("Relay 1 Off")
            relay1.off()
            sleep(1)

