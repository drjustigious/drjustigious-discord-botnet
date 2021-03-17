import random
import logging

from discord.ext import commands


class Games(commands.Cog):
    MAX_DICE = 50

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rolldice(self, ctx, *, num_dice: int = 1):
        """
        Roll the given number of 6-sided dice.

        Arguments
        ---------
        num_dice: int
            How many dice to roll. Must not exceed 50. Optional.

        Example
        -------
        !rolldice 2
        """
        if num_dice < 1:
            message = f"<@{ctx.author.id}> Please specify a positive number of dice to roll."
            await ctx.send(message)
            return

        if num_dice > self.MAX_DICE:
            message = f"Sorry <@{ctx.author.id}>, I only have {self.MAX_DICE} dice to roll. Please specify a smaller number of dice."
            await ctx.send(message)
            return

        die_faces = [
            "` ⚀ 1 `", "` ⚁ 2 `", "` ⚂ 3 `", "` ⚃ 4 `", "` ⚄ 5 `", "` ⚅ 6 `"
        ]

        roll_results = [
            random.choice(die_faces) for _ in range(num_dice)
        ]

        joined_results = "\n".join(roll_results)
        message = f"<@{ctx.author.id}> The dice say:\n{joined_results}"
        await ctx.send(message)


    @commands.command()
    async def drawcards(self, ctx, *, num_cards: int = 1):
        """
        Draw the specified number of cards from a full deck without Jokers.

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
            message = f"<@{ctx.author.id}> Please specify a positive number of cards to draw."
            await ctx.send(message)
            return        

        if num_cards > 52:
            message = f"Sorry <@{ctx.author.id}>, I only have one deck of 52 cards to draw from. Please specify a smaller number of cards."
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
        message = f"<@{ctx.author.id}> The cards say:\n{joined_results}"
        await ctx.send(message)