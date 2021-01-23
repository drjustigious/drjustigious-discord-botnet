import logging
import logging.handlers
import os

from discord.ext import commands

class Autodiagnostics(commands.Cog):

    def __init__(self, bot):
        self.LOGGING_FORMAT = '[%(asctime)s] %(levelname)s %(message)s'
        self.DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
        self.LOG_FILE = os.getenv('LOG_FILE')
        self.LOG_LEVEL = int(os.getenv('LOG_LEVEL'))

        self.bot = bot
        self.configure_logger()

    def configure_logger(self):

        rfh = logging.handlers.RotatingFileHandler(
            filename=self.LOG_FILE,
            mode='a',
            maxBytes=20*1024*1024,
            backupCount=2,
            encoding='utf-8',
            delay=0
        )

        logging.basicConfig(
            level=self.LOG_LEVEL,
            format=self.LOGGING_FORMAT,
            datefmt=self.DATE_FORMAT,
            handlers=[rfh]
        )

        logging.debug('This message should go to the log file')
        logging.info('So should this')
        logging.warning('And this, too')
        logging.error('And non-ASCII stuff, too, like Øresund and Malmö')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')
        logging.info(f'{self.bot.user.name} has connected to Discord!')