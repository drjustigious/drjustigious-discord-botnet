import random
from discord.ext import commands


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rolldice(self, ctx, *, num_dice: int = 1):
        """
        Roll the given number of 6-sided dice.

        Arguments
        ---------
        num_dice: int
            How many dice to roll. Optional.

        Example
        -------
        !rolldice 2
        """
        die_faces = [
            "` ⚀ 1 `", "` ⚁ 2 `", "` ⚂ 3 `", "` ⚃ 4 `", "` ⚄ 5 `", "` ⚅ 6 `"
        ]

        roll_results = [
            random.choice(die_faces) for _ in range(num_dice)
        ]

        joined_results = "   ".join(roll_results)

        message = f"<@{ctx.author.id}> The dice say:\n{joined_results}"

        await ctx.send(message)