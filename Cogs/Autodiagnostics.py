import logging
import logging.handlers
import os
import sys
import traceback

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

        rotating_file_handler = logging.handlers.RotatingFileHandler(
            filename=self.LOG_FILE,
            mode='a',
            maxBytes=20*1024*1024,
            backupCount=2,
            encoding='utf-8',
            delay=0
        )

        console_logging_handler = logging.StreamHandler(
            stream=sys.stdout
        )

        logging.basicConfig(
            level=self.LOG_LEVEL,
            format=self.LOGGING_FORMAT,
            datefmt=self.DATE_FORMAT,
            handlers=[
                rotating_file_handler,
                console_logging_handler
            ]
        )

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"Connected to Discord as user '{self.bot.user.name}'.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exception):
        try:
            raise exception
        except Exception as e:
            logging.exception(f"Error during command '{ctx.command}'.")