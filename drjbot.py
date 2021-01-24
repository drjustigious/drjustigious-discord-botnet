import os
from discord.ext import commands
import dotenv
import logging

from Cogs import (
    Autodiagnostics,
    Weather
)

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_DEFAULT_GUILD')

bot = commands.Bot(command_prefix='!')
bot.add_cog(Autodiagnostics.Autodiagnostics(bot))
bot.add_cog(Weather.Weather(bot))

@bot.event
async def on_error(event, *args, **kwargs):
    logging.exception(f"Error during '{event}' event.")

bot.run(TOKEN)