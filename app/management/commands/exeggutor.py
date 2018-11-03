import datetime, pytz, os
os.environ['GPIOZERO_PIN_FACTORY'] = os.environ.get('GPIOZERO_PIN_FACTORY', 'mock')
from time import sleep
from django.core.management.base import BaseCommand, CommandError

from app.models import SystemSetting, Job

import gpiozero
from gpiozero import OutputDevice

relays = {
    'sala': [
        OutputDevice(18, active_high=False, initial_value=True),
        OutputDevice(27, active_high=False, initial_value=True)
    ],
    'bagno': [
        OutputDevice(22, active_high=False, initial_value=True),
        OutputDevice(23, active_high=False, initial_value=True),
    ],

    'studio': [
        OutputDevice(24, active_high=False, initial_value=True),
        OutputDevice(25, active_high=False, initial_value=True),
    ],
    'camera': [
        OutputDevice(4, active_high=False, initial_value=True),
        OutputDevice(2, active_high=False, initial_value=True),
    ],
}

class Command(BaseCommand):

    args = ''
    help = 'monitors the job table for changes and execute the pin configurations'

    def handle(self, *args, **options):
        while True:
            sleep(1)
            now = datetime.datetime.now().utcnow().replace(tzinfo=pytz.UTC)
            jobs = Job.objects.all()
            for job in jobs:
                if job.timetoexecute > now:
                    print('found job {}, to be started on {}, starting now {}.'.format(job.name, job.timetoexecute, now))
                    job.delete()
                else:
                    print('found job {}, to be started on {}, not starting now {}.'.format(job.name, job.timetoexecute, now))


