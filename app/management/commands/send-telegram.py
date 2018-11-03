import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from django.core.management.base import BaseCommand, CommandError

from telegram.ext import Updater, RegexHandler

from app.models import SystemSetting


class Command(BaseCommand):

    args = ''
    help = 'starts the telegram bot'
    admin = SystemSetting.objects.get(name='email-smtp-password').value
    def add_arguments(self, parser):
        parser.add_argument('message', nargs=1, type=str)

    def handle(self, *args, **options):
        telegramkey = SystemSetting.objects.get(name='telegram-bot-api-key').value
        updater = Updater(telegramkey)
        dispatcher = updater.dispatcher
        dispatcher.bot.send_message(chat_id=self.admin, text=options['message'][0])



