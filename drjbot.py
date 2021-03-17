import os
from discord.ext import commands
import dotenv
import logging

from Cogs import (
    Autodiagnostics,
    Weather
)

# The bot code relies on several environment variables.
# The supported variables are listed in 'sample.env'.
# The actual environment variables can be passed in a file
# named '.env' placed next to 'drjbot.py'.
DOTENV_FILE = ".env"
dotenv.load_dotenv(DOTENV_FILE)

# The bot's command prefix defaults to '!' but can be overridden by an env var.
bot = commands.Bot(command_prefix=os.getenv('BOT_COMMAND_PREFIX', '!'))

# Set up logging and global error handling.
bot.add_cog(Autodiagnostics.Autodiagnostics(bot))

@bot.event
async def on_error(event, *args, **kwargs):
    logging.exception(f"Error during '{event}' event.")

# Attach the remaining cogs.
INSTALLED_COGS = [
    Weather.Weather
]

for cog in INSTALLED_COGS:
    bot.add_cog(cog(bot))

# Start the bot client and connect to Discord.
bot.run(os.getenv('DISCORD_API_TOKEN'))