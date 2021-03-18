import random
import logging

from discord.ext import commands


class Games(commands.Cog):
    MAX_DICE = 50

    def __init__(self, bot):
        self.bot = bot
        self.previous_choices = []

    @commands.command()
    async def rolldice(self, ctx, *, num_dice: int = 1):
        """
        Roll a given number of 6-sided dice.

        Arguments
        ---------
        num_dice: int
            How many dice to roll. Must not exceed 50. Optional.

        Examples
        -------
        !rolldice
        !rolldice 2
        """
        if num_dice < 1:
            message = f"{ctx.author.mention} Please specify a positive number of dice to roll."
            await ctx.send(message)
            return

        if num_dice > self.MAX_DICE:
            message = f"Sorry {ctx.author.mention}, I only have {self.MAX_DICE} dice to roll. Please specify a smaller number of dice."
            await ctx.send(message)
            return

        die_faces = [
            "` ⚀ 1 `", "` ⚁ 2 `", "` ⚂ 3 `", "` ⚃ 4 `", "` ⚄ 5 `", "` ⚅ 6 `"
        ]

        roll_results = [
            random.choice(die_faces) for _ in range(num_dice)
        ]

        joined_results = "\n".join(roll_results)
        message = f"{ctx.author.mention} The dice say:\n{joined_results}"
        await ctx.send(message)


    @commands.command()
    async def drawcards(self, ctx, *, num_cards: int = 1):
        """
        Draw a specified number of playing cards.

        The cards will be drawn from a standard 52-card deck (without Jokers).

        Arguments
        ---------
        num_cards: int
            How many cards to draw. Must not exceed 52. Optional.

        Example
        -------
        !drawcards 2
        """

        # Validate the input.
        if num_cards < 1:
            message = f"{ctx.author.mention} Please specify a positive number of cards to draw."
            await ctx.send(message)
            return        

        if num_cards > 52:
            message = f"Sorry {ctx.author.mention}, I only have one deck of 52 cards to draw from. Please specify a smaller number of cards."
            await ctx.send(message)
            return        

        suits = [
            "Clubs ♣",
            "Diamonds ♦",
            "Hearts ♥",
            "Spades ♠"
        ]

        ranks = [
            "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"
        ]

        # Construct a full deck of cards.
        deck_of_cards = []
        for suit in suits:
            for rank in ranks:
                deck_of_cards.append(f"` {rank} of {suit} `")

        # Draw the given number of cards and sort them back into standard deck order.
        drawn_card_indices = random.sample(range(52), num_cards)
        drawn_card_indices.sort()
        drawn_cards = [deck_of_cards[i] for i in drawn_card_indices]

        # Send the results as a Discord message.
        joined_results = "\n".join(drawn_cards)
        message = f"{ctx.author.mention} The cards say:\n{joined_results}"
        await ctx.send(message)


    @commands.command()
    async def choose(self, ctx, *, choices: str = ""):
        """
        Randomly choose one of the given strings.

        Arguments
        ---------
        choices: string
            A comma-separated list of items to choose from. Optional. Omit to choose again from the previous options.

        Examples
        -------
        !choose skeld, mirahq, polus
        !choose
        """

        # Parse the given choices assuming comma separation, but fall back to space separation
        # if there aren't any commas in the input string.
        list_choices = choices.split(",")
        if len(list_choices) == 1:
            list_choices = choices.split(" ")

        # Remove whitespace and only retain non-empty choices.
        list_choices = [item.strip() for item in list_choices if item.strip()]

        logging.debug(f"CHOICES: {list_choices}")

        # If no new set of choices was given, try to choose again from the previous ones.
        if not list_choices:
            if not self.previous_choices:
                message = f"{ctx.author.mention} Please give me a list of items to choose from. Type `!help` for details."
                await ctx.send(message)
                return

            choice = random.choice(self.previous_choices)
            options = ", ".join(self.previous_choices)
            message = f"{ctx.author.mention} I choose `{choice}`.\nThe options I remember were `{options}`."
            await ctx.send(message)
            return

        # Looks like we had a new set of choices. Remember those for later.
        self.previous_choices = list_choices

        choice = random.choice(list_choices)
        message = f"{ctx.author.mention} I choose `{choice}`."
        await ctx.send(message)