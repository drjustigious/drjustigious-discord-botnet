import discord
from discord.ext import commands

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def weather(self, ctx, *, town: str = None):
        """Forecast weather for the given town in Finland."""

        await ctx.send(f"<@{ctx.author.id}>, you asked for the weather in {town} but won't get none because of reasons.")