import logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from django.core.management.base import BaseCommand, CommandError

from telegram.ext import Updater, RegexHandler

from app.models import SystemSetting


class Command(BaseCommand):

    args = ''
    help = 'starts the telegram bot'
    admin = SystemSetting.objects.get(name='telegram-admin').value

    def hello(self, bot, update, groupdict):
        if update.message.chat.id == self.admin:
            update.message.reply_text('Benvenuto/a signorino/a, a suo desiderio posso descriverle lo STATO delle tapparelle, ALZA ad esempio la tapparella della CUCINA, CHIUDI quella del BAGNO. Oppure potrei andare in vacanza a Dubai visto quanto vengo pagato per questo lavoro.')

    def openshutter(self, bot, update, groupdict):
        if update.message.chat.id == self.admin:
            #update.message.reply_text('La tapparella {} è alzata.'.format(groupdict))
            splitted = [shutter.strip().lower() for shutter in groupdict.what.split(' ')]
            update.message.reply_text('{}'.format(splitted))

    def handle(self, *args, **options):
        telegramkey = SystemSetting.objects.get(name='telegram-bot-api-key').value
        updater = Updater(telegramkey)
        updater.dispatcher.add_handler(RegexHandler('(?i).*(alza).*(tapparella)(?P<what>.*)', self.openshutter, pass_groupdict=True))
        updater.dispatcher.add_handler(RegexHandler('(?i)^(ciao)$|^(buongiorno)$|^(buonasera)$|^(addio)$', self.hello, pass_groupdict=True))
        updater.start_polling()
        updater.idle()


