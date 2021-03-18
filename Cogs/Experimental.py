import discord
from discord.ext import commands

from HousebotUtilities import BotMentionHandlers

class Experimental(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f"Greetings {member.mention}. Welcome to {member.guild.name}. I am the house bot, at your service. Please type `!help` to see what I can do for you.")


    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user in message.mentions:
            await self.handle_mention(message)


    async def handle_mention(self, message):
        """
        The given message has mentioned the bot. Analyze it further and perhaps respond.
        """
        mention_handlers = [
            BotMentionHandlers.identify_user
        ]

        # Every handler is expected to return True if it did something with the message.
        for handler in mention_handlers:
            if await handler(self.bot, message):
                return

        # If none of the listed handlers got a grasp of the message,
        # output a default acknowledgement of the situation.
        await message.channel.send(f"You mentioned me, {message.author.mention}.")