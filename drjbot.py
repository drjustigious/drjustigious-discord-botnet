import os
from discord.ext import commands
import dotenv
import random

from Cogs import (
    ExperimentalCogs,
    DiagnosticCogs
)

dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_DEFAULT_GUILD')

bot = commands.Bot(command_prefix='!')
bot.add_cog(ExperimentalCogs.Greetings(bot))
bot.add_cog(DiagnosticCogs.Autodiagnostics(bot))

@bot.command(name='99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

bot.run(TOKEN)