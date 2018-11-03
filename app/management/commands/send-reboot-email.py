import smtplib

from django.core.management.base import BaseCommand, CommandError
from app.models import SystemSetting

from email.mime.text import MIMEText

class Command(BaseCommand):

    args = ''
    help = 'sends the reboot email with info'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', help='ip address or FQDN to the web interface')
    
    def handle(self, *args, **options):
        username = SystemSetting.objects.get(name='email-smtp-username').value
        password = SystemSetting.objects.get(name='email-smtp-password').value


        email_subject = 'Bahay Domotic System - The system was rebooted'
        email_from = SystemSetting.objects.get(name='email-sender').value
        email_to = ('elia.zanaboni@gmail.com')
        email_text = 'Bahay was rebooted, this is the received IP Address:\n {}'.format(options['ip_address'])

        msg = MIMEText(email_text)
        msg['Subject'] = email_subject
        msg['From'] = email_from
        msg['To'] = email_to

        s = None
        if SystemSetting.objects.get(name='email-smtp-type').value == 'SSL':
            s = smtplib.SMTP_SSL('{}:{}'.format(SystemSetting.objects.get(name='email-smtp-server').value, SystemSetting.objects.get(name='email-smtp-port').value))
        else:
            s = smtplib.SMTP('{}:{}'.format(SystemSetting.objects.get(name='email-smtp-server').value, SystemSetting.objects.get(name='email-smtp-port').value))

        s.set_debuglevel(0)
        s.login(username, password)
        s.sendmail(email_from, email_to, msg.as_string())
        s.quit()

