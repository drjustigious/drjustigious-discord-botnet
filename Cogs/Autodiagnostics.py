import logging
import logging.handlers
import os
import sys

from discord.ext import commands


class Autodiagnostics(commands.Cog):
    """
    This cog sets up the bot's logging system and tracks its life cycle.
    """

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
        """
        This event occurs once when the bot starts and has successfully connected to Discord.
        """
        logging.info(f"Connected to Discord as user '{self.bot.user.name}'.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exception):
        """
        This event occurs in response to any error in a bot command.
        Other exceptions that arise during events will be handled
        by the bot client's 'on_error' handler defined in 'drjbot.py'.
        """
        # Looks like we need to re-raise the exception to get it through into the logs.
        try:
            raise exception

        except commands.errors.CommandNotFound:
            await ctx.send(f"Sorry {ctx.author.mention}, I did not recognize your command. Please type `!help` to see what I can do for you.")

        except commands.errors.BadArgument:
            await ctx.send(f"Sorry {ctx.author.mention}, something about the parameters of your command made no sense to me. Please type `!help` to see what I can do for you.")            

        except Exception as e:
            logging.exception(f"Error during command '{ctx.command}'.")